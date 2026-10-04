"""Single Vercel Python entrypoint, exposed as a WSGI `app`. This runtime
requires exactly one ASGI/WSGI entrypoint (declared via [tool.vercel] in
pyproject.toml) — it neither auto-discovers one function per api/*.py file,
nor accepts a BaseHTTPRequestHandler class, despite both being shown in the
public docs (verified 2026-07-26 via failing `vercel build`/`vercel dev`
runs; see DECISIONS.md). All real logic still lives in app/web/*.py.
"""
from __future__ import annotations

from app.clients.telegram import TelegramClient
from app.config import get_settings
from app.platform.bootstrap import build_worker_deps
from app.platform.http_adapter import read_body, read_headers, read_query, wsgi_response
from app.security.auth import constant_time_eq
from app.security.crypto import TokenCipher
from app.storage.db import Database
from app.storage.event_log import EventLog
from app.storage.oauth_state import consume_oauth_state
from app.storage.oauth_tokens import PostgresTokenStore
from app.storage.queue import QStashQueue
from app.storage.redis import UpstashRedis
from app.web import cron, frontend, oauth_callback, strava_webhook, telegram_webhook
from app.web import worker as worker_module
from app.web.types import WebResponse

settings = get_settings()  # fail fast at cold start

_db = Database(settings.database_url)
_redis = UpstashRedis(settings.upstash_redis_rest_url, settings.upstash_redis_rest_token)
_event_log = EventLog(_db)
_queue = QStashQueue(settings.qstash_token)
_worker_url = f"{settings.app_url}/api/worker"
_token_store = PostgresTokenStore(_db, TokenCipher(settings.encryption_key))
_telegram = TelegramClient(settings.telegram_bot_token)
_worker_deps = build_worker_deps(settings)


def _check_cron_auth(headers: dict) -> bool:
    return constant_time_eq(headers.get("Authorization", ""), f"Bearer {settings.internal_api_secret}")


def _route_get(path: str, environ: dict) -> WebResponse:
    if path == "/api/webhook/strava":
        return strava_webhook.handle_get(read_query(environ), verify_token=settings.strava_verify_token)

    if path == "/api/oauth/strava/callback":
        return oauth_callback.handle_get(
            read_query(environ),
            consume_state=lambda state: consume_oauth_state(_redis, state),
            client_id=settings.strava_client_id,
            client_secret=settings.strava_client_secret,
            token_store=_token_store,
        )

    if path == "/api/oauth/strava/connect":
        return frontend.handle_strava_connect(settings)

    if path == "/api/cron/purge_cache":
        if not _check_cron_auth(read_headers(environ)):
            return WebResponse.json(401, {"error": "unauthorized"})
        return WebResponse.json(200, {"purged_rows": cron.purge_expired_activities(_db)})

    if path == "/api/cron/weekly_digest":
        if not _check_cron_auth(read_headers(environ)):
            return WebResponse.json(401, {"error": "unauthorized"})
        stats = cron.compute_weekly_stats(_db)
        _telegram.send_markdown(settings.telegram_owner_chat_id, cron.weekly_digest_text(**stats))
        return WebResponse.json(200, stats)

    if not path.startswith("/api/") and path != "/health":
        return frontend.handle_static(path)

    if path == "/api/dashboard":
        return frontend.handle_dashboard(_db, settings)

    if path == "/api/activities":
        return frontend.handle_activities(_db, read_query(environ))

    if path.startswith("/api/activity/"):
        try:
            act_id = int(path.split("/")[-1])
            return frontend.handle_activity_detail(_db, act_id)
        except ValueError:
            return WebResponse.json(400, {"error": "invalid activity id"})

    if path == "/api/prs":
        return frontend.handle_prs(_db)

    if path.startswith("/api/chart/"):
        chart_id = path.split("/")[-1]
        return frontend.handle_chart(chart_id, _db)

    if path == "/health":
        return WebResponse.json(200, {
            "status": "healthy",
            "app": "LiftMate",
            "version": "1.0.0",
            "endpoints": [
                "/",
                "/api/dashboard",
                "/api/activities",
                "/api/prs",
                "/api/chat",
                "/api/profile",
                "/api/simulate-workout",
                "/api/chart/{chart_id}",
                "/api/webhook/strava",
                "/api/webhook/telegram",
                "/api/oauth/strava/callback",
                "/api/worker",
                "/api/cron/weekly_digest",
                "/api/cron/purge_cache",
            ],
        })

    return WebResponse.json(404, {"error": "not found"})


def _route_post(path: str, environ: dict) -> WebResponse:
    if path == "/api/chat":
        return frontend.handle_chat(read_body(environ), _worker_deps, settings)

    if path == "/api/profile":
        return frontend.handle_update_profile(_db, read_body(environ))

    if path == "/api/simulate-workout":
        return frontend.handle_simulate_workout(read_body(environ))

    if path == "/api/telegram/dispatch":
        return frontend.handle_telegram_dispatch(read_body(environ), settings)

    if path == "/api/trigger/weekly_digest":
        return frontend.handle_trigger_weekly_digest(_db, settings)
    if path == "/api/webhook/strava":
        return strava_webhook.handle_post(
            read_body(environ),
            expected_subscription_id=settings.strava_subscription_id or -1,
            expected_athlete_id=settings.strava_athlete_id,
            event_log=_event_log,
            queue=_queue,
            worker_url=_worker_url,
        )

    if path == "/api/webhook/telegram":
        return telegram_webhook.handle_post(
            read_headers(environ), read_body(environ),
            webhook_secret=settings.telegram_webhook_secret,
            owner_chat_id=settings.telegram_owner_chat_id,
            queue=_queue,
            worker_url=_worker_url,
        )

    if path == "/api/worker":
        return worker_module.handle_post(
            read_headers(environ), read_body(environ),
            endpoint_url=_worker_url,
            current_signing_key=settings.qstash_current_signing_key,
            next_signing_key=settings.qstash_next_signing_key,
            deps=_worker_deps,
        )

    return WebResponse.json(404, {"error": "not found"})


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "")

    if method == "GET":
        response = _route_get(path, environ)
    elif method == "POST":
        response = _route_post(path, environ)
    else:
        response = WebResponse.json(405, {"error": "method not allowed"})

    return wsgi_response(response, start_response)
 
 
if __name__ == "__main__":
    import os
    from wsgiref.simple_server import make_server
 
    port = int(os.environ.get("PORT", 3000))
    print(f">> LiftMate WSGI server running at http://localhost:{port} (press Ctrl+C to stop)")
    with make_server("0.0.0.0", port, app) as httpd:
        httpd.serve_forever()

