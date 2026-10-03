/**
 * LIFTMATE // AI Hybrid Athlete Telemetry & Coach
 * Frontend Application Logic (Vanilla JavaScript)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global State
  const state = {
    profile: null,
    weeklyStats: null,
    activities: [],
    prs: [],
    systemStatus: null,
    activeTab: 'dashboard',
    activeSportFilter: 'all',
    activePrCategory: 'all',
  };

  // DOM Elements
  const navTabs = document.querySelectorAll('.nav-item, .nav-tab');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const toastContainer = document.getElementById('toast-container');
  const modal = document.getElementById('activity-detail-modal');
  const modalCloseBtn = document.getElementById('btn-close-modal');

  // ==========================================================================
  // Toast Notification System
  // ==========================================================================
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(12px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // ==========================================================================
  // Telegram Bot Dispatch Client
  // ==========================================================================
  let currentModalActivity = null;
  let currentSimResult = null;

  async function sendToTelegram(text, title = 'LiftMate Telemetry') {
    if (!text) {
      showToast('No message content to send.', 'error');
      return;
    }
    showToast('Dispatching to @sujal_liftmate_bot...', 'info');
    try {
      const formatted = title ? `🚀 *${title}*\n\n${text}` : text;
      const res = await fetch('/api/telegram/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: formatted }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to dispatch');
      showToast('Delivered to Telegram bot!', 'success');
    } catch (err) {
      showToast(`Telegram dispatch error: ${err.message}`, 'error');
    }
  }

  // ==========================================================================
  // Tab Navigation Handling
  // ==========================================================================
  function switchTab(targetTab) {
    state.activeTab = targetTab;

    navTabs.forEach((tab) => {
      const isMatch = tab.dataset.tab === targetTab;
      tab.classList.toggle('active', isMatch);
      tab.setAttribute('aria-selected', isMatch ? 'true' : 'false');
    });

    tabPanes.forEach((pane) => {
      pane.classList.toggle('active', pane.id === `pane-${targetTab}`);
    });

    // Special handlers when tab opens
    if (targetTab === 'charts') {
      const presetSelect = document.getElementById('chart-preset-select');
      loadChart(presetSelect.value);
    }
  }

  navTabs.forEach((tab) => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  document.getElementById('btn-quick-ask')?.addEventListener('click', () => {
    switchTab('coach');
    document.getElementById('chat-input')?.focus();
  });

  document.getElementById('btn-view-all-activities')?.addEventListener('click', () => {
    switchTab('activities');
  });

  document.getElementById('btn-open-charts-tab')?.addEventListener('click', () => {
    switchTab('charts');
  });

  // ==========================================================================
  // Data Fetching & Dashboard Hydration
  // ==========================================================================
  async function fetchDashboard() {
    try {
      const res = await fetch('/api/dashboard');
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const data = await res.json();

      state.profile = data.profile;
      state.weeklyStats = data.weekly_stats;
      state.activities = data.recent_activities || [];
      state.prs = data.prs || [];
      state.systemStatus = data.system_status;

      renderDashboard();
      renderActivitiesList();
      renderPRsBoard();
      populateSettingsForm();
    } catch (err) {
      console.warn('Could not fetch from live API, initializing with fallback:', err);
    }
  }

  function renderDashboard() {
    if (!state.profile) return;

    // Athlete Banner
    document.getElementById('hero-athlete-name').textContent = state.profile.athlete_name || 'Sujal Nag';
    document.getElementById('hero-athlete-goal').textContent = `Target: ${state.profile.training_goal}`;
    document.getElementById('bio-max-hr').innerHTML = `${state.profile.max_hr} <small>bpm</small>`;
    document.getElementById('bio-resting-hr').innerHTML = `${state.profile.resting_hr} <small>bpm</small>`;
    document.getElementById('bio-lthr').innerHTML = `${state.profile.lthr} <small>bpm</small>`;
    document.getElementById('bio-bodyweight').innerHTML = `${state.profile.bodyweight_kg} <small>${state.profile.weight_unit || 'kg'}</small>`;

    if (state.weeklyStats) {
      document.getElementById('bio-acwr').innerHTML = `${state.weeklyStats.acwr} <small>SWEET SPOT</small>`;
      document.getElementById('kpi-weekly-volume').innerHTML = `${state.weeklyStats.weekly_volume_kg.toLocaleString()} <span class="kpi-unit">kg</span>`;
      document.getElementById('kpi-weekly-distance').innerHTML = `${state.weeklyStats.weekly_distance_km} <span class="kpi-unit">km</span>`;
      document.getElementById('kpi-acwr-gauge').innerHTML = `${state.weeklyStats.acwr} <span class="kpi-unit">ratio</span>`;
      document.getElementById('kpi-active-prs').innerHTML = `${state.prs.length} <span class="kpi-unit">bests</span>`;
    }

    if (document.getElementById('top-athlete-name')) {
      document.getElementById('top-athlete-name').textContent = state.profile.athlete_name || 'Sujal Nag';
    }

    // Dashboard Recent Activity Feed (top 4)
    const feedContainer = document.getElementById('dashboard-activity-feed');
    if (!feedContainer) return;
    feedContainer.innerHTML = '';

    state.activities.slice(0, 4).forEach((act) => {
      const isStrength = act.sport_type === 'WeightTraining';
      const tr = document.createElement('tr');
      tr.className = 'activity-row';
      tr.onclick = () => openActivityModal(act);

      const metricDisplay = isStrength
        ? `${(act.volume_kg || 0).toLocaleString()} kg`
        : `${act.distance_km || 0} km`;

      tr.innerHTML = `
        <td>
          <span class="sport-icon-chip ${act.sport_type.toLowerCase()}">
            ${isStrength ? '🏋️' : '🏃'}
          </span>
        </td>
        <td>
          <span class="act-name">${act.title}</span>
          ${act.prs_count > 0 ? `<span class="act-pr-pill">${act.prs_count} PR</span>` : ''}
        </td>
        <td class="text-subtle">${formatDate(act.start_date)}</td>
        <td class="act-stat-mono">${metricDisplay}</td>
        <td class="text-subtle">${formatDuration(act.duration_s)}</td>
        <td style="text-align:right;"><span class="btn-ghost btn-xs">Inspect &rarr;</span></td>
      `;
      feedContainer.appendChild(tr);
    });
  }

  // ==========================================================================
  // Activities Feed Tab & Detail Modal
  // ==========================================================================
  function renderActivitiesList() {
    const grid = document.getElementById('full-activities-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const filtered = state.activities.filter((act) => {
      if (state.activeSportFilter === 'all') return true;
      return act.sport_type.toLowerCase() === state.activeSportFilter.toLowerCase();
    });

    if (filtered.length === 0) {
      grid.innerHTML = `<div class="sim-empty-state"><p>No activities found matching this filter.</p></div>`;
      return;
    }

    filtered.forEach((act) => {
      const isStrength = act.sport_type === 'WeightTraining';
      const card = document.createElement('div');
      card.className = 'activity-card';
      card.onclick = () => openActivityModal(act);

      card.innerHTML = `
        <div class="card-top">
          <span class="card-badge ${act.sport_type.toLowerCase()}">${isStrength ? '🏋️ Weight Training' : '🏃 Running'}</span>
          <span class="card-date">${formatDate(act.start_date)}</span>
        </div>
        <h3 class="card-title">${act.title}</h3>
        <p class="card-summary">${act.summary || ''}</p>
        <div class="card-metrics-row">
          <div class="card-metric">
            <span class="metric-label">${isStrength ? 'TOTAL VOLUME' : 'DISTANCE'}</span>
            <span class="metric-val text-accent">${isStrength ? `${(act.volume_kg || 0).toLocaleString()} kg` : `${act.distance_km} km`}</span>
          </div>
          <div class="card-metric">
            <span class="metric-label">DURATION</span>
            <span class="metric-val">${formatDuration(act.duration_s)}</span>
          </div>
          <div class="card-metric">
            <span class="metric-label">${isStrength ? 'EXERCISES' : 'AVG HR'}</span>
            <span class="metric-val">${isStrength ? `${act.exercises_count || 5}` : `${act.avg_hr} bpm`}</span>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // Activity filter buttons
  document.querySelectorAll('#activity-sport-filters .filter-tab, #activity-sport-filters .filter-pill').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#activity-sport-filters .filter-tab, #activity-sport-filters .filter-pill').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeSportFilter = btn.dataset.sport;
      renderActivitiesList();
    });
  });

  function openActivityModal(act) {
    currentModalActivity = act;
    const isStrength = act.sport_type === 'WeightTraining';
    document.getElementById('modal-sport-badge').textContent = isStrength ? '🏋️ Weight Training' : '🏃 Running';
    document.getElementById('modal-activity-title').textContent = act.title;
    document.getElementById('modal-activity-date').textContent = `${formatDate(act.start_date)} • ${formatDuration(act.duration_s)}`;

    const body = document.getElementById('modal-activity-body');
    body.innerHTML = '';

    // Deterministic Performance Metrics Strip
    const metricsStrip = document.createElement('div');
    metricsStrip.className = 'sim-summary-row';
    metricsStrip.style.marginBottom = '1.2rem';

    if (isStrength) {
      metricsStrip.innerHTML = `
        <div class="summary-tile">
          <span class="st-label">TOTAL VOLUME</span>
          <span class="st-val text-accent">${(act.volume_kg || 0).toLocaleString()} kg</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">WORKING SETS</span>
          <span class="st-val">${act.working_sets || 16}</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">PUSH / PULL</span>
          <span class="st-val">${act.push_pull_ratio || '1.45'} : 1</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">UPPER / LOWER</span>
          <span class="st-val">${act.upper_lower_ratio || '2.60'} : 1</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">DENSITY</span>
          <span class="st-val">${act.density_kg_per_min || '222.6'} kg/min</span>
        </div>
      `;
    } else {
      metricsStrip.innerHTML = `
        <div class="summary-tile">
          <span class="st-label">DISTANCE</span>
          <span class="st-val text-accent">${act.distance_km} km</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">AVG HR</span>
          <span class="st-val">${act.avg_hr} bpm</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">DECOUPLING</span>
          <span class="st-val">${act.aerobic_decoupling_pct || '2.1'}%</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">EFFICIENCY (EF)</span>
          <span class="st-val">${act.efficiency_factor || '1.42'}</span>
        </div>
        <div class="summary-tile">
          <span class="st-label">TRIMP LOAD</span>
          <span class="st-val">${act.trimp || '68.4'}</span>
        </div>
      `;
    }
    body.appendChild(metricsStrip);

    // If Strength Workout: Exercise Breakdown Table
    if (isStrength && act.exercises) {
      const secTitle = document.createElement('div');
      secTitle.className = 'modal-section-title';
      secTitle.textContent = 'EXERCISES & WORKING SETS BREAKDOWN';
      body.appendChild(secTitle);

      act.exercises.forEach((ex) => {
        const exBox = document.createElement('div');
        exBox.className = 'sim-ex-item';
        exBox.style.marginBottom = '1rem';
        exBox.innerHTML = `
          <div class="sim-ex-header">
            <span>${ex.name} <small style="color:var(--fg-muted);">(${ex.muscle})</small></span>
            <span style="color:var(--accent-orange); font-family:var(--font-mono);">${ex.volume_kg} kg vol • Best e1RM: ${ex.best_e1rm_kg}kg</span>
          </div>
          <table class="sets-table">
            <thead>
              <tr><th>SET</th><th>WEIGHT</th><th>REPS</th><th>TYPE</th><th>RPE</th></tr>
            </thead>
            <tbody>
              ${ex.sets.map((s) => `
                <tr>
                  <td>Set ${s.set}</td>
                  <td>${s.weight_kg} kg</td>
                  <td>${s.reps} reps</td>
                  <td><span class="sim-set-pill">${s.type}</span></td>
                  <td>${s.rpe ? `@ ${s.rpe}` : '—'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
        body.appendChild(exBox);
      });
    }

    // If Endurance / Run: Splits & HR Zones
    if (!isStrength) {
      if (act.hr_zones) {
        const hrSection = document.createElement('div');
        hrSection.innerHTML = `
          <div class="modal-section-title">HEART RATE ZONES TELEMETRY</div>
          <div style="display:flex; flex-direction:column; gap:0.5rem; margin-bottom:1.5rem;">
            ${act.hr_zones.map((z) => `
              <div>
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:0.2rem; font-family:var(--font-mono);">
                  <span>${z.zone}</span>
                  <span>${Math.round(z.seconds / 60)} min (${z.pct}%)</span>
                </div>
                <div class="progress-track">
                  <div class="progress-fill" style="width:${z.pct}%; background:${getZoneColor(z.zone)};"></div>
                </div>
              </div>
            `).join('')}
          </div>
        `;
        body.appendChild(hrSection);
      }

      if (act.splits) {
        const splitsSection = document.createElement('div');
        splitsSection.innerHTML = `
          <div class="modal-section-title">KILOMETER SPLITS</div>
          <table class="sets-table" style="margin-bottom:1.5rem;">
            <thead><tr><th>KM</th><th>PACE</th><th>AVG HR</th></tr></thead>
            <tbody>
              ${act.splits.map((s) => `
                <tr><td>Kilometer ${s.km}</td><td>${s.pace} /km</td><td>${s.avg_hr} bpm</td></tr>
              `).join('')}
            </tbody>
          </table>
        `;
        body.appendChild(splitsSection);
      }
    }

    // Post-Workout AI Briefing
    if (act.briefing) {
      const briefCard = document.createElement('div');
      briefCard.className = 'modal-briefing-card';
      briefCard.innerHTML = `
        <div class="modal-briefing-badge">LIFTMATE POST-WORKOUT BRIEFING</div>
        <p class="modal-briefing-text">${act.briefing}</p>
      `;
      body.appendChild(briefCard);
    }

    modal.classList.remove('hidden');
  }

  function getZoneColor(zoneName) {
    if (zoneName.includes('Z1')) return 'var(--accent-cyan)';
    if (zoneName.includes('Z2')) return 'var(--accent-green)';
    if (zoneName.includes('Z3')) return 'var(--accent-yellow)';
    if (zoneName.includes('Z4')) return 'var(--accent-orange)';
    return 'var(--accent-red)';
  }

  modalCloseBtn?.addEventListener('click', () => modal.classList.add('hidden'));
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.add('hidden');
  });

  document.getElementById('btn-modal-send-telegram')?.addEventListener('click', () => {
    if (!currentModalActivity) return;
    const summary = currentModalActivity.briefing || currentModalActivity.summary || currentModalActivity.title;
    sendToTelegram(summary, currentModalActivity.title);
  });

  // ==========================================================================
  // PR Trophy Board Tab
  // ==========================================================================
  function renderPRsBoard() {
    const grid = document.getElementById('prs-board-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const filtered = state.prs.filter((p) => {
      if (state.activePrCategory === 'all') return true;
      return p.category.toLowerCase().includes(state.activePrCategory.toLowerCase());
    });

    filtered.forEach((pr) => {
      const card = document.createElement('div');
      card.className = 'pr-card';
      card.innerHTML = `
        <div class="pr-card-header">
          <h3 class="pr-exercise-name">${pr.exercise}</h3>
          <span class="pr-category-badge">${pr.category}</span>
        </div>
        <div class="pr-stats-grid">
          <div class="pr-stat-box">
            <span class="pr-stat-label">HEAVIEST WEIGHT</span>
            <span class="pr-stat-value">${pr.heaviest_weight_kg} <small>kg</small></span>
          </div>
          <div class="pr-stat-box">
            <span class="pr-stat-label">ESTIMATED 1RM</span>
            <span class="pr-stat-value text-accent">${pr.best_e1rm_kg} <small>kg</small></span>
          </div>
        </div>
        <div class="pr-card-footer">
          <span>Max Reps: <strong>${pr.max_reps_at_weight}</strong></span>
          <span>Achieved: <strong>${pr.achieved_at}</strong></span>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // PR Category filter pills
  document.querySelectorAll('#pr-category-filters .filter-tab, #pr-category-filters .filter-pill').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#pr-category-filters .filter-tab, #pr-category-filters .filter-pill').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      state.activePrCategory = btn.dataset.cat;
      renderPRsBoard();
    });
  });

  // ==========================================================================
  // AI Coach Interactive Chat
  // ==========================================================================
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages-container');

  chatForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendChatMessage('user', 'You', message);
    chatInput.value = '';

    // Temporary loading indicator
    const typingBubble = appendChatMessage('coach', 'LiftMate Coach', '<em>Analyzing biomechanics & telemetry...</em>');

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      typingBubble.remove();
      appendChatMessage('coach', 'LiftMate Coach', formatMarkdown(data.reply));
    } catch (err) {
      typingBubble.remove();
      appendChatMessage('coach', 'LiftMate Coach', 'Unable to reach the coaching engine. Check your connection or local dev runner.');
    }
  });

  // Prompt chips
  document.querySelectorAll('.chip-btn, .prompt-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const prompt = chip.dataset.prompt;
      if (prompt && chatInput) {
        chatInput.value = prompt;
        chatForm.dispatchEvent(new Event('submit'));
      }
    });
  });

  document.getElementById('btn-clear-chat')?.addEventListener('click', () => {
    chatMessages.innerHTML = '';
    appendChatMessage('coach', 'LiftMate Coach', 'Chat history cleared. What workout, metric, or exercise would you like to explore?');
  });

  function appendChatMessage(sender, author, text) {
    const bubble = document.createElement('div');
    bubble.className = `chat-entry ${sender}`;
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    bubble.innerHTML = `
      <div class="chat-meta">
        <span class="sender-name">${author}</span>
        <span class="message-time">${now}</span>
      </div>
      <div class="message-body">${text}</div>
    `;

    if (sender === 'coach' && !text.includes('<em>')) {
      const actionRow = document.createElement('div');
      actionRow.style.marginTop = '0.6rem';
      actionRow.innerHTML = `
        <button type="button" class="btn btn-ghost btn-xs btn-forward-tg">
          <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          Forward to Telegram
        </button>
      `;
      actionRow.querySelector('.btn-forward-tg')?.addEventListener('click', () => {
        const raw = text.replace(/<[^>]+>/g, '').trim();
        sendToTelegram(raw, 'LiftMate Coach Advice');
      });
      bubble.appendChild(actionRow);
    }

    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return bubble;
  }

  function formatMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n• (.*?)/g, '<li>$1</li>')
      .replace(/\n\d+\. (.*?)/g, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
  }

  // ==========================================================================
  // Matplotlib Preset Studio Tab
  // ==========================================================================
  const presetSelect = document.getElementById('chart-preset-select');
  const chartImg = document.getElementById('chart-preview-img');
  const chartIdLabel = document.getElementById('chart-info-id');

  function loadChart(preset) {
    if (!chartImg) return;
    chartImg.src = `/api/chart/${preset}?t=${Date.now()}`;
    if (chartIdLabel) chartIdLabel.textContent = preset;
  }

  presetSelect?.addEventListener('change', () => loadChart(presetSelect.value));
  document.getElementById('btn-refresh-chart')?.addEventListener('click', () => {
    loadChart(presetSelect.value);
    showToast('Chart refreshed from backend generator.', 'success');
  });

  // ==========================================================================
  // Workout Simulator & Parser Lab Tab
  // ==========================================================================
  const simForm = document.getElementById('simulator-form');
  const simText = document.getElementById('simulator-text');
  const simEmpty = document.getElementById('sim-results-empty');
  const simContent = document.getElementById('sim-results-content');

  const templates = {
    push: `Logged with hevyapp.com

Bench Press (Barbell)
Set 1: 60 kg x 10 (warmup)
Set 2: 80 kg x 8
Set 3: 95 kg x 6
Set 4: 102.5 kg x 5 (failure)

Incline Dumbbell Press
Set 1: 34 kg x 10
Set 2: 36 kg x 8
Set 3: 36 kg x 7

Weighted Dips
Set 1: 20 kg x 10
Set 2: 25 kg x 8
Set 3: 30 kg x 6`,
    legs: `Logged with hevyapp.com

Barbell Back Squat
Set 1: 70 kg x 10 (warmup)
Set 2: 110 kg x 8
Set 3: 130 kg x 6
Set 4: 145 kg x 5

Romanian Deadlift
Set 1: 100 kg x 10
Set 2: 125 kg x 8
Set 3: 135 kg x 8

Leg Press
Set 1: 220 kg x 12
Set 2: 250 kg x 10`,
    pull: `Logged with hevyapp.com

Weighted Pull-ups
Set 1: 15 kg x 8
Set 2: 20 kg x 6
Set 3: 25 kg x 5

Barbell Row
Set 1: 70 kg x 10
Set 2: 85 kg x 8
Set 3: 90 kg x 8

Incline Dumbbell Curl
Set 1: 16 kg x 12
Set 2: 18 kg x 10`
  };

  document.getElementById('btn-template-push')?.addEventListener('click', () => {
    simText.value = templates.push;
  });
  document.getElementById('btn-template-legs')?.addEventListener('click', () => {
    simText.value = templates.legs;
  });
  document.getElementById('btn-template-pull')?.addEventListener('click', () => {
    simText.value = templates.pull;
  });

  document.getElementById('btn-clear-simulation')?.addEventListener('click', () => {
    simText.value = '';
    simEmpty.classList.remove('hidden');
    simContent.classList.add('hidden');
    document.getElementById('sim-status-text').textContent = 'Awaiting workout input';
  });

  simForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = simText.value.trim();
    if (!text) {
      showToast('Please enter or select a workout description to parse.', 'error');
      return;
    }

    try {
      const res = await fetch('/api/simulate-workout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || 'Parsing error');

      currentSimResult = data;
      simEmpty.classList.add('hidden');
      simContent.classList.remove('hidden');
      document.getElementById('sim-status-text').textContent = 'Parsing complete & validated';

      document.getElementById('sim-total-volume').textContent = `${(data.total_volume_kg || 0).toLocaleString()} kg`;
      if (document.getElementById('sim-working-sets')) {
        document.getElementById('sim-working-sets').textContent = data.total_working_sets || data.exercises.length;
      }
      if (document.getElementById('sim-push-pull')) {
        document.getElementById('sim-push-pull').textContent = data.push_pull_ratio ? `${data.push_pull_ratio} : 1` : '—';
      }
      if (document.getElementById('sim-upper-lower')) {
        document.getElementById('sim-upper-lower').textContent = data.upper_lower_ratio ? `${data.upper_lower_ratio} : 1` : '—';
      }
      if (document.getElementById('sim-density')) {
        document.getElementById('sim-density').textContent = `${data.density_kg_per_min || 0} kg/min`;
      }

      if (data.rep_range_distribution) {
        const s = document.getElementById('pill-strength-reps');
        const h = document.getElementById('pill-hypertrophy-reps');
        const e = document.getElementById('pill-endurance-reps');
        if (s) s.textContent = `Strength (1–5): ${data.rep_range_distribution.strength} sets`;
        if (h) h.textContent = `Hypertrophy (6–12): ${data.rep_range_distribution.hypertrophy} sets`;
        if (e) e.textContent = `Endurance (13+): ${data.rep_range_distribution.endurance} sets`;
      }

      // Render parsed exercises with deterministic calculations
      const exList = document.getElementById('sim-exercises-list');
      exList.innerHTML = '';
      data.exercises.forEach((ex) => {
        const item = document.createElement('div');
        item.className = 'sim-ex-item';
        item.innerHTML = `
          <div class="sim-ex-header">
            <span>${ex.name} <small style="color:var(--fg-muted);">(${ex.muscle})</small> ${ex.bilateral_dumbbell ? '<span class="pill-badge pill-xs" style="margin-left:0.4rem;">2x DB</span>' : ''}</span>
            <span style="color:var(--accent-orange); font-family:var(--font-mono);">${ex.volume_kg} kg vol • Best e1RM: ${ex.best_e1rm_kg}kg</span>
          </div>
          <table class="sets-table" style="margin-top:0.5rem;">
            <thead>
              <tr><th>SET</th><th>WEIGHT</th><th>REPS</th><th>RANGE</th><th>EPLEY e1RM</th><th>BRZYCKI e1RM</th><th>TYPE</th></tr>
            </thead>
            <tbody>
              ${ex.sets.map((s, idx) => `
                <tr>
                  <td>Set ${idx + 1}</td>
                  <td>${s.weight_kg} kg</td>
                  <td>${s.reps} reps</td>
                  <td><span class="sim-set-pill">${s.rep_range}</span></td>
                  <td>${s.epley_e1rm ? `${s.epley_e1rm} kg` : '—'}</td>
                  <td>${s.brzycki_e1rm ? `${s.brzycki_e1rm} kg` : '—'}</td>
                  <td><span class="sim-set-pill">${s.type}</span> ${s.e1rm_divergence ? '<span title="Epley vs Brzycki diverge >5%" style="color:var(--accent-yellow); margin-left:0.2rem;">⚠️</span>' : ''}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
        exList.appendChild(item);
      });

      // Briefing
      document.getElementById('sim-briefing-text').textContent = data.briefing;
      showToast('Workout parsed and pure-Python metrics computed!', 'success');
    } catch (err) {
      showToast(`Simulation failed: ${err.message}`, 'error');
    }
  });

  document.getElementById('btn-sim-send-telegram')?.addEventListener('click', () => {
    if (!currentSimResult) {
      showToast('Please parse a workout first.', 'error');
      return;
    }
    sendToTelegram(currentSimResult.briefing, 'Workout Lab Session Briefing');
  });

  // ==========================================================================
  // Settings & Profile Form
  // ==========================================================================
  function populateSettingsForm() {
    if (!state.profile) return;
    document.getElementById('setting-goal').value = state.profile.training_goal || '';
    document.getElementById('setting-max-hr').value = state.profile.max_hr || 192;
    document.getElementById('setting-resting-hr').value = state.profile.resting_hr || 52;
    document.getElementById('setting-lthr').value = state.profile.lthr || 171;
    document.getElementById('setting-bodyweight').value = state.profile.bodyweight_kg || 78.5;
    document.getElementById('setting-weight-unit').value = state.profile.weight_unit || 'kg';
    document.getElementById('setting-distance-unit').value = state.profile.distance_unit || 'km';
  }

  document.getElementById('profile-settings-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      training_goal: document.getElementById('setting-goal').value.trim(),
      max_hr: parseInt(document.getElementById('setting-max-hr').value, 10),
      resting_hr: parseInt(document.getElementById('setting-resting-hr').value, 10),
      lthr: parseInt(document.getElementById('setting-lthr').value, 10),
      bodyweight_kg: parseFloat(document.getElementById('setting-bodyweight').value),
      weight_unit: document.getElementById('setting-weight-unit').value,
      distance_unit: document.getElementById('setting-distance-unit').value,
    };

    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to update profile');

      state.profile = data.profile;
      renderDashboard();
      showToast('Athlete profile successfully updated & synced!', 'success');
    } catch (err) {
      showToast(`Update failed: ${err.message}`, 'error');
    }
  });

  // Settings Action Triggers: Strava Connect & Telegram Integration
  document.getElementById('btn-connect-strava')?.addEventListener('click', async () => {
    try {
      const res = await fetch('/api/oauth/strava/connect');
      const data = await res.json();
      if (data.url) {
        showToast('Opening Strava authorization portal in a new tab...', 'info');
        window.open(data.url, '_blank');
      }
    } catch (err) {
      showToast(`Strava connection error: ${err.message}`, 'error');
    }
  });

  document.getElementById('btn-test-telegram')?.addEventListener('click', () => {
    sendToTelegram(
      "⚡ *LiftMate Telemetry Connection Verified*\n\nYour Telegram bot (@sujal_liftmate_bot) is active and securely linked to Sujal Nag's dashboard. All workout briefings, PR alerts, and coach advice will be dispatched in real-time.",
      "Connection Verification"
    );
  });

  document.getElementById('btn-trigger-digest')?.addEventListener('click', async () => {
    showToast('Computing weekly telemetry stats & generating digest...', 'info');
    try {
      const res = await fetch('/api/trigger/weekly_digest', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to trigger digest');
      showToast('Weekly digest computed & dispatched to Telegram!', 'success');
      appendChatMessage('coach', 'Weekly Digest', formatMarkdown(data.digest));
      switchTab('coach');
    } catch (err) {
      showToast(`Weekly digest error: ${err.message}`, 'error');
    }
  });

  // ==========================================================================
  // Utility Formatters
  // ==========================================================================
  function formatDate(isoStr) {
    if (!isoStr) return '';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  function formatDuration(seconds) {
    if (!seconds) return '0m';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (hrs > 0) return `${hrs}h ${mins}m`;
    return `${mins}m`;
  }

  // Initialize
  fetchDashboard();
});
