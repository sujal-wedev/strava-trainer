#!/usr/bin/env python3
"""Local development server runner for LiftMate.

Starts the LiftMate WSGI app using Python's standard library wsgiref server.
Auto-detects and uses the project's .venv interpreter even if not explicitly activated.
"""
import os
import sys
import subprocess

# Auto-detect and switch to .venv interpreter if running with a system Python
project_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = (
    os.path.join(project_dir, ".venv", "Scripts", "python.exe")
    if sys.platform == "win32"
    else os.path.join(project_dir, ".venv", "bin", "python")
)

if os.path.exists(venv_python):
    current_exe = os.path.normcase(os.path.abspath(sys.executable))
    target_exe = os.path.normcase(os.path.abspath(venv_python))
    if current_exe != target_exe:
        sys.exit(subprocess.call([venv_python] + sys.argv))

# Ensure project root is in sys.path
sys.path.insert(0, project_dir)

from wsgiref.simple_server import make_server
from api.index import app
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    port = int(os.environ.get("PORT", 3000))
    host = os.environ.get("HOST", "0.0.0.0")

    print("=" * 60)
    print("  [LiftMate] Local Development Server")
    print(f"  Listening on: http://localhost:{port}")
    print(f"  Health check: http://localhost:{port}/health")
    print(f"  Configured App URL: {settings.app_url}")
    print(f"  Athlete Goal: {settings.training_goal}")
    print("=" * 60)
    print("  Available endpoints:")
    print("    - GET  /health")
    print("    - GET  /api/webhook/strava (Subscription verify)")
    print("    - POST /api/webhook/strava (Activity event)")
    print("    - POST /api/webhook/telegram (Bot message)")
    print("    - GET  /api/oauth/strava/callback (OAuth exchange)")
    print("    - POST /api/worker (QStash asynchronous worker)")
    print("    - GET  /api/cron/weekly_digest (Cron)")
    print("    - GET  /api/cron/purge_cache (Cron)")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.\n")

    try:
        with make_server(host, port, app) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nLiftMate server stopped.")
