import json

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TimerGo</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="icon.svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        :root {
            --bg-color: #f43f5e;
            --primary-color: #f43f5e;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            transition: background-color 0.5s ease;
        }

        .container {
            max-width: 500px;
            width: 90%;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            text-align: center;
        }

        h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; letter-spacing: 0.05em; }

        select#profile-select {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 2rem 0.5rem 1rem;
            border-radius: 9999px;
            font-family: inherit;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            appearance: none;
            outline: none;
            text-align: center;
        }
        
        .select-wrapper { position: relative; display: inline-block; margin-bottom: 1.5rem; }
        .select-wrapper::after {
            content: '▼';
            font-size: 0.6rem;
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
        }

        .modes {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 2rem;
            background: rgba(0, 0, 0, 0.1);
            padding: 0.5rem;
            border-radius: 1.5rem;
        }

        .mode-btn {
            background: transparent;
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }

        .mode-btn:hover { background: rgba(255, 255, 255, 0.1); }
        .mode-btn.active { background: rgba(0, 0, 0, 0.15); font-weight: 700; box-shadow: 0 0 0 2px rgba(255,255,255,0.4); }

        .timer-display {
            font-size: 5.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.05em;
            line-height: 1;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .timer-display:hover { opacity: 0.8; }

        .controls { display: flex; justify-content: center; align-items: center; gap: 1rem; }

        .start-btn {
            background-color: white;
            color: var(--primary-color);
            border: none;
            padding: 1rem 2.5rem;
            border-radius: 9999px;
            font-size: 1.125rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transition: transform 0.1s ease, background-color 0.2s ease, color 0.5s ease;
            display: flex; align-items: center; gap: 0.5rem; font-family: inherit;
        }
        .start-btn:hover { background-color: #f3f4f6; transform: scale(1.05); }
        .start-btn:active { transform: scale(0.95); }

        .reset-btn {
            background: transparent; border: 2px solid rgba(255, 255, 255, 0.5);
            color: white; padding: 0.75rem; border-radius: 9999px; cursor: pointer;
            transition: all 0.2s ease; display: flex; align-items: center; justify-content: center;
        }
        .reset-btn:hover { background: rgba(255, 255, 255, 0.2); border-color: white; transform: scale(1.05); }
        .reset-btn:active { transform: scale(0.95); }
        svg { width: 1.25rem; height: 1.25rem; }
        .reset-btn svg { width: 1.5rem; height: 1.5rem; }
        .hidden { display: none !important; }

        /* Toolbar */
        .toolbar { position: absolute; top: 1rem; right: 1rem; display: flex; gap: 0.5rem; }
        .icon-btn {
            background: rgba(255, 255, 255, 0.2); border: none; color: white;
            padding: 0.6rem; border-radius: 50%; cursor: pointer;
            display: flex; align-items: center; justify-content: center; transition: background 0.2s;
        }
        .icon-btn:hover { background: rgba(255, 255, 255, 0.3); }

        /* Modal */
        .modal-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none; transition: opacity 0.3s; z-index: 100;
        }
        .modal-overlay.active { opacity: 1; pointer-events: auto; }
        .modal {
            background: white; color: #1f2937; padding: 2rem; border-radius: 1rem;
            width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; text-align: left;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        }
        .modal h2 { font-size: 1.5rem; margin-bottom: 1.5rem; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }
        .close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #9ca3af; }
        .close-btn:hover { color: #4b5563; }
        
        .modal-section { margin-bottom: 1.5rem; }
        .modal-section h3 { font-size: 1rem; margin-bottom: 0.75rem; font-weight: 600; color: #4b5563; }
        
        .profile-list { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
        .profile-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: #f9fafb; border-radius: 0.5rem; border: 1px solid #e5e7eb; }
        .profile-info { display: flex; flex-direction: column; gap: 0.25rem; font-weight: 600; font-size: 0.9rem; }
        .profile-info-subtitle { font-size: 0.75rem; color: #6b7280; font-weight: 400; }
        .profile-delete { color: #ef4444; cursor: pointer; border: none; background: none; padding: 0.25rem; border-radius: 0.25rem; }
        .profile-delete:hover { background: #fee2e2; }

        .form-group { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 1rem; }
        .form-group label { font-size: 0.875rem; font-weight: 600; color: #374151; }
        .form-group input[type="text"], .form-group input[type="number"] { padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-family: inherit; font-size: 1rem; }
        .checkbox-group { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.875rem; font-weight: 600; color: #374151; }
        .checkbox-group input[type="checkbox"] { width: 1.25rem; height: 1.25rem; }
        
        .color-presets { display: flex; gap: 0.5rem; align-items: center; }
        .color-preset { width: 2rem; height: 2rem; border-radius: 50%; cursor: pointer; border: 2px solid transparent; transition: transform 0.1s; }
        .color-preset:hover { transform: scale(1.1); }
        .color-preset.selected { border-color: #1f2937; }
        #custom-color { width: 2.2rem; height: 2.2rem; padding: 0; border: none; background: none; cursor: pointer; border-radius: 50%; }

        .btn { padding: 0.6rem 1rem; border-radius: 0.5rem; font-weight: 600; font-size: 0.875rem; cursor: pointer; border: none; font-family: inherit; transition: background 0.2s; }
        .btn-primary { background: #3b82f6; color: white; }
        .btn-primary:hover { background: #2563eb; }
        .btn-secondary { background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; }
        .btn-secondary:hover { background: #e5e7eb; }
        
        .flex-row { display: flex; gap: 0.5rem; }
        .mt-1 { margin-top: 1rem; }
        .w-full { width: 100%; }
        
        hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }

        /* Builder Styles */
        .builder-box { background: #f9fafb; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-bottom: 1rem; }
        .phase-list { margin-bottom: 1rem; }
        .phase-item { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background: white; border: 1px solid #d1d5db; border-radius: 0.375rem; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; }
        .phase-item-info { display: flex; align-items: center; gap: 0.5rem; }
        .phase-color-dot { width: 0.75rem; height: 0.75rem; border-radius: 50%; }
    </style>
</head>
<body>
    <div class="toolbar">
        <button class="icon-btn" onclick="toggleFullscreen()" title="Toggle Fullscreen">
            <svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/></svg>
        </button>
        <button class="icon-btn" onclick="openSettings()" title="Settings">
            <svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </button>
    </div>

    <div class="container">
        <h1>TimerGo</h1>

        <div class="select-wrapper">
            <select id="profile-select"></select>
        </div>

        <div class="modes" id="phases-container">
            <!-- Phase buttons rendered here -->
        </div>

        <div class="timer-display" id="timer-display" onclick="editTimer()" title="Click to edit timer">
            00:00
        </div>

        <div class="controls">
            <button id="start-btn" class="start-btn" onclick="toggleTimer()">
                <svg id="play-icon" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"/></svg>
                <svg id="pause-icon" class="hidden" fill="currentColor" viewBox="0 0 20 20"><path d="M5 4h3v12H5V4zm7 0h3v12h-3V4z"/></svg>
                <span id="start-text">Start</span>
            </button>
            <button class="reset-btn" onclick="resetTimer()" title="Reset Phase">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </button>
        </div>
    </div>

    <!-- Settings Modal -->
    <div class="modal-overlay" id="settings-modal">
        <div class="modal">
            <h2>Settings <button class="close-btn" onclick="closeSettings()">&times;</button></h2>
            
            <div class="modal-section">
                <h3>Your Profiles</h3>
                <div class="profile-list" id="profile-list">
                    <!-- Profile items rendered here -->
                </div>
            </div>

            <div class="modal-section builder-box">
                <h3>Build New Profile</h3>
                
                <div class="form-group">
                    <label>Profile Name</label>
                    <input type="text" id="new-profile-name" placeholder="e.g. Pomodoro Flow">
                </div>

                <div class="checkbox-group">
                    <input type="checkbox" id="new-profile-autostart" checked>
                    <label for="new-profile-autostart" style="margin:0;cursor:pointer;">Auto-start next phase</label>
                </div>

                <div class="checkbox-group">
                    <input type="checkbox" id="new-profile-loop" checked>
                    <label for="new-profile-loop" style="margin:0;cursor:pointer;">Loop sequence</label>
                </div>

                <hr style="margin: 1rem 0;">

                <div class="phase-list" id="new-phase-list">
                    <!-- Draft phases -->
                </div>

                <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px dashed #d1d5db; margin-bottom: 1rem;">
                    <div class="form-group" style="margin-bottom: 0.5rem;">
                        <input type="text" id="new-phase-name" placeholder="Phase Name (e.g. Work)">
                    </div>
                    <div class="form-group" style="margin-bottom: 0.5rem;">
                        <input type="number" id="new-phase-time" placeholder="Duration (mins)" min="0.1" step="0.1">
                    </div>
                    <div class="form-group" style="margin-bottom: 0.75rem;">
                        <div class="color-presets">
                            <div class="color-preset selected" style="background: #f43f5e" onclick="selectColor(this, '#f43f5e')"></div>
                            <div class="color-preset" style="background: #14b8a6" onclick="selectColor(this, '#14b8a6')"></div>
                            <div class="color-preset" style="background: #3b82f6" onclick="selectColor(this, '#3b82f6')"></div>
                            <div class="color-preset" style="background: #f59e0b" onclick="selectColor(this, '#f59e0b')"></div>
                            <div class="color-preset" style="background: #8b5cf6" onclick="selectColor(this, '#8b5cf6')"></div>
                            <input type="color" id="custom-color" value="#f43f5e" onchange="selectColor(null, this.value)" title="Custom Color">
                        </div>
                    </div>
                    <button class="btn btn-secondary w-full" onclick="addDraftPhase()">+ Add Phase</button>
                </div>

                <button class="btn btn-primary w-full" onclick="saveNewProfile()">Save Profile</button>
            </div>

            <hr>
            
            <div class="modal-section">
                <h3>Data Management</h3>
                <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.75rem;">Backup or restore your custom profiles.</p>
                <div class="flex-row">
                    <button class="btn btn-secondary w-full" onclick="exportData()">Export JSON</button>
                    <button class="btn btn-secondary w-full" onclick="document.getElementById('import-file').click()">Import JSON</button>
                    <input type="file" id="import-file" accept=".json" class="hidden" onchange="importData(event)">
                </div>
            </div>
        </div>
    </div>

    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('sw.js').catch(err => console.log('SW registration failed:', err));
            });
        }

        // --- Data & State Migration ---
        const defaultProfiles = {
            'pomodoro': {
                name: 'Classic Pomodoro',
                autoStart: true,
                loop: true,
                sequence: [
                    { name: 'Work', time: 25 * 60, color: '#f43f5e' },
                    { name: 'Short Break', time: 5 * 60, color: '#14b8a6' },
                    { name: 'Work', time: 25 * 60, color: '#f43f5e' },
                    { name: 'Short Break', time: 5 * 60, color: '#14b8a6' },
                    { name: 'Work', time: 25 * 60, color: '#f43f5e' },
                    { name: 'Long Break', time: 15 * 60, color: '#3b82f6' }
                ]
            }
        };

        let profiles = null;
        try {
            const raw = localStorage.getItem('timergo-profiles-v2');
            if (raw) profiles = JSON.parse(raw);
        } catch(e) {}

        if (!profiles) {
            profiles = defaultProfiles;
        }

        let currentProfileId = localStorage.getItem('timergo-current-profile-v2') || 'pomodoro';
        if (!profiles[currentProfileId]) currentProfileId = Object.keys(profiles)[0] || 'pomodoro';
        
        let currentPhaseIndex = 0;
        let timeLeft = 0;

        let timerId = null;
        let isRunning = false;
        let endTime = null;
        let audioCtx = null;
        
        let draftPhases = [];
        let selectedNewColor = '#f43f5e';

        const display = document.getElementById('timer-display');
        const startBtnText = document.getElementById('start-text');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');
        const root = document.documentElement;
        const profileSelect = document.getElementById('profile-select');

        // --- Core Timer Logic ---
        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            requestNotificationPermission();
        }

        function getActivePhase() {
            const p = profiles[currentProfileId];
            if (!p || !p.sequence || p.sequence.length === 0) return null;
            return p.sequence[currentPhaseIndex];
        }

        function updateDisplay() {
            const t = Math.max(0, timeLeft);
            const minutes = Math.floor(t / 60);
            const seconds = t % 60;
            const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            display.textContent = timeString;
            
            const phase = getActivePhase();
            const phaseName = phase ? phase.name : 'Timer';
            document.title = `${timeString} - ${phaseName} | TimerGo`;
        }

        function playChime() {
            try {
                if (!audioCtx) initAudio();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 1);
                gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 1);
            } catch (e) {}
        }

        function advancePhase() {
            const p = profiles[currentProfileId];
            if (!p) return;
            
            currentPhaseIndex++;
            if (currentPhaseIndex >= p.sequence.length) {
                if (p.loop) {
                    currentPhaseIndex = 0;
                } else {
                    currentPhaseIndex = p.sequence.length - 1; // Stay on last phase
                    resetTimer();
                    return;
                }
            }
            
            applyPhase(currentPhaseIndex, p.autoStart);
        }

        function toggleTimer() {
            initAudio();
            const phase = getActivePhase();
            if (!phase) return;

            if (isRunning) {
                clearInterval(timerId);
                isRunning = false;
                timeLeft = Math.round((endTime - Date.now()) / 1000);
                if (timeLeft < 0) timeLeft = 0;
                setStartBtnState(false);
                updateDisplay();
            } else {
                if (timeLeft <= 0) timeLeft = phase.time;
                isRunning = true;
                endTime = Date.now() + (timeLeft * 1000);
                setStartBtnState(true);
                updateDisplay();
                
                timerId = setInterval(() => {
                    const now = Date.now();
                    timeLeft = Math.round((endTime - now) / 1000);
                    if (timeLeft <= 0) {
                        timeLeft = 0;
                        updateDisplay();
                        clearInterval(timerId);
                        isRunning = false;
                        playChime();
                        sendNotification();
                        setStartBtnState(false);
                        
                        setTimeout(() => {
                            if (!isRunning && timeLeft <= 0) {
                                advancePhase();
                            }
                        }, 2000);
                    } else {
                        updateDisplay();
                    }
                }, 100);
            }
        }

        function setStartBtnState(running) {
            if (running) {
                startBtnText.textContent = 'Pause';
                playIcon.classList.add('hidden');
                pauseIcon.classList.remove('hidden');
            } else {
                startBtnText.textContent = 'Start';
                playIcon.classList.remove('hidden');
                pauseIcon.classList.add('hidden');
            }
        }

        function resetTimer() {
            clearInterval(timerId);
            isRunning = false;
            const phase = getActivePhase();
            timeLeft = phase ? phase.time : 25 * 60;
            setStartBtnState(false);
            updateDisplay();
        }

        function editTimer() {
            if (isRunning) toggleTimer();
            const currentMins = Math.ceil(timeLeft / 60);
            const input = prompt("Enter new time in minutes:", currentMins);
            if (input !== null) {
                const mins = parseFloat(input);
                if (!isNaN(mins) && mins > 0) {
                    timeLeft = Math.round(mins * 60);
                    updateDisplay();
                }
            }
        }

        // --- Profile & Phase Management ---
        function initProfileSelect() {
            profileSelect.innerHTML = '';
            Object.keys(profiles).forEach(key => {
                const opt = document.createElement('option');
                opt.value = key;
                opt.textContent = profiles[key].name;
                profileSelect.appendChild(opt);
            });
            profileSelect.value = currentProfileId;
        }

        profileSelect.addEventListener('change', (e) => {
            setProfile(e.target.value);
        });

        function setProfile(profileKey) {
            if (!profiles[profileKey]) return;
            currentProfileId = profileKey;
            currentPhaseIndex = 0;
            localStorage.setItem('timergo-current-profile-v2', currentProfileId);
            applyPhase(0, false);
        }

        function applyPhase(index, autoStart = false) {
            const profile = profiles[currentProfileId];
            if (!profile || !profile.sequence || profile.sequence.length === 0) return;
            
            currentPhaseIndex = index;
            const phase = profile.sequence[index];
            
            root.style.setProperty('--bg-color', phase.color);
            root.style.setProperty('--primary-color', phase.color);

            renderPhases();
            resetTimer();
            
            if (autoStart) {
                toggleTimer();
            }
        }

        function renderPhases() {
            const container = document.getElementById('phases-container');
            container.innerHTML = '';
            const profile = profiles[currentProfileId];
            if (!profile) return;
            
            profile.sequence.forEach((phase, index) => {
                const btn = document.createElement('button');
                btn.className = `mode-btn ${currentPhaseIndex === index ? 'active' : ''}`;
                btn.textContent = phase.name;
                btn.onclick = () => {
                    if(isRunning) toggleTimer();
                    applyPhase(index, false);
                };
                container.appendChild(btn);
            });
        }

        function saveProfiles() {
            localStorage.setItem('timergo-profiles-v2', JSON.stringify(profiles));
            initProfileSelect();
            renderPhases();
        }

        // --- Settings UI ---
        function openSettings() {
            document.getElementById('settings-modal').classList.add('active');
            renderProfileList();
            
            // Reset builder
            document.getElementById('new-profile-name').value = '';
            draftPhases = [];
            renderDraftPhases();
        }

        function closeSettings() {
            document.getElementById('settings-modal').classList.remove('active');
        }

        function renderProfileList() {
            const list = document.getElementById('profile-list');
            list.innerHTML = '';
            Object.keys(profiles).forEach(key => {
                const p = profiles[key];
                const totalSec = p.sequence.reduce((acc, curr) => acc + curr.time, 0);
                const subtitle = `${p.sequence.length} phases • ${Math.round(totalSec / 60)}m total`;
                
                list.innerHTML += `
                    <div class="profile-item">
                        <div class="profile-info">
                            <div>${p.name}</div>
                            <div class="profile-info-subtitle">${subtitle}</div>
                        </div>
                        <button class="profile-delete" onclick="deleteProfile('${key}')" title="Delete">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                        </button>
                    </div>
                `;
            });
        }

        function selectColor(element, color) {
            selectedNewColor = color;
            document.querySelectorAll('.color-preset').forEach(el => el.classList.remove('selected'));
            if (element) {
                element.classList.add('selected');
            } else {
                document.getElementById('custom-color').value = color;
            }
        }

        function addDraftPhase() {
            const nameInput = document.getElementById('new-phase-name');
            const timeInput = document.getElementById('new-phase-time');
            const name = nameInput.value.trim();
            const mins = parseFloat(timeInput.value);
            
            if (name && !isNaN(mins) && mins > 0) {
                draftPhases.push({ name: name, time: Math.round(mins * 60), color: selectedNewColor });
                renderDraftPhases();
                nameInput.value = '';
                timeInput.value = '';
            } else {
                alert("Please enter a valid phase name and duration.");
            }
        }

        function renderDraftPhases() {
            const list = document.getElementById('new-phase-list');
            list.innerHTML = '';
            draftPhases.forEach((phase, idx) => {
                list.innerHTML += `
                    <div class="phase-item">
                        <div class="phase-item-info">
                            <div class="phase-color-dot" style="background: ${phase.color}"></div>
                            ${phase.name} (${Math.round(phase.time / 60)}m)
                        </div>
                        <button class="phase-delete" onclick="removeDraftPhase(${idx})">✖</button>
                    </div>
                `;
            });
        }

        function removeDraftPhase(idx) {
            draftPhases.splice(idx, 1);
            renderDraftPhases();
        }

        function saveNewProfile() {
            const name = document.getElementById('new-profile-name').value.trim();
            const autoStart = document.getElementById('new-profile-autostart').checked;
            const loop = document.getElementById('new-profile-loop').checked;

            if (!name) return alert("Please enter a profile name.");
            if (draftPhases.length === 0) return alert("Please add at least one phase.");

            const key = 'custom_' + Date.now();
            profiles[key] = {
                name: name,
                autoStart: autoStart,
                loop: loop,
                sequence: [...draftPhases]
            };
            
            saveProfiles();
            renderProfileList();
            
            // Switch to it immediately
            setProfile(key);
            closeSettings();
        }

        function deleteProfile(key) {
            if (Object.keys(profiles).length <= 1) {
                alert("You must have at least one profile.");
                return;
            }
            if (confirm(`Delete profile "${profiles[key].name}"?`)) {
                delete profiles[key];
                if (currentProfileId === key) {
                    currentProfileId = Object.keys(profiles)[0];
                    localStorage.setItem('timergo-current-profile-v2', currentProfileId);
                    applyPhase(0, false);
                }
                saveProfiles();
                renderProfileList();
            }
        }

        // --- Import/Export ---
        function exportData() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(profiles));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "timergo_profiles_v2.json");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }

        function importData(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const parsed = JSON.parse(e.target.result);
                    if (typeof parsed === 'object' && Object.keys(parsed).length > 0) {
                        profiles = parsed;
                        currentProfileId = Object.keys(profiles)[0];
                        localStorage.setItem('timergo-current-profile-v2', currentProfileId);
                        saveProfiles();
                        renderProfileList();
                        applyPhase(0, false);
                        alert("Profiles imported successfully!");
                    }
                } catch (err) {
                    alert("Invalid JSON file.");
                }
            };
            reader.readAsText(file);
            event.target.value = '';
        }

        // --- Notifications & Fullscreen ---
        function requestNotificationPermission() {
            if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
                Notification.requestPermission();
            }
        }

        function sendNotification() {
            if ("Notification" in window && Notification.permission === "granted") {
                new Notification("TimerGo", {
                    body: "Time's up! Moving to next phase...",
                    icon: "icon.svg"
                });
            }
        }

        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.log(`Fullscreen error: ${err.message}`);
                });
            } else {
                document.exitFullscreen();
            }
        }

        // --- Initialization ---
        initProfileSelect();
        applyPhase(0, false);
    </script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)
