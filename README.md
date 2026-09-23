# TimerGo

TimerGo is a free, installable **multi-phase focus timer** — Pomodoro and beyond. Build your own sequence of timed phases (Work → Short Break → Work → Long Break, or anything else), and TimerGo cycles through them automatically with a smooth circular countdown, chimes, and desktop notifications.

It's a single self-contained web app: no build step, no backend, no account, no tracking. Every setting — your profiles, theme, wallpaper, quotes, window position, and even the **timer currently running** — is saved to your browser's `localStorage` and restored exactly as you left it, including after a refresh or relaunch.

## Features

- **Multi-phase sequences** — not just 25/5/15. Build any number of phases, each with its own name, duration, and accent color, looped or one-shot.
- **Custom profile builder** — create, switch between, and delete unlimited saved sequences from the Settings drawer.
- **Circular progress ring** with a phase-dot sequence strip that shows where you are in the cycle and lets you jump to any phase.
- **Auto-advance & looping** — chimes (Web Audio API, no sound files) and moves to the next phase automatically, or stops at the end if looping is off.
- **Day / Night themes** — one click, persisted.
- **Custom wallpapers** — curated gradient presets, a pasted image URL, or a local image upload (stored on-device as a data URL).
- **Motivational quotes** — built-in defaults or your own, editable in Settings, rotating automatically on each phase change.
- **Draggable, zoomable card** — drag the header to reposition the timer anywhere on screen, double-click to re-center, zoom 50–200% with the on-screen pill, keyboard, or Ctrl/Cmd + mouse wheel.
- **Desktop notifications** when a phase completes (if permission is granted).
- **Fullscreen mode** for distraction-free sessions.
- **Import / export backup** — one JSON file with everything: profiles, active profile, theme, wallpaper, quotes, zoom, and window position.
- **Installable PWA** — works fully offline once installed; see below.
- **Zero external dependencies** beyond a Google Fonts stylesheet — no frameworks, no analytics, no cookies.

## Install as a local app

TimerGo is a Progressive Web App, so it installs like a native app and runs offline. The one catch: **the offline service worker only registers over `http://` or `https://`, not `file://`**, so you need to serve the folder rather than double-clicking `index.html` if you want the full installable/offline experience (double-clicking still works fine for just using the timer in a browser tab — you only lose install + offline caching).

1. From this folder, start any static file server, for example:
   ```bash
   python3 -m http.server 8000
   ```
   or
   ```bash
   npx serve .
   ```
2. Open `http://localhost:8000` in Chrome, Edge, or another Chromium-based browser (or visit the app's hosted GitHub Pages URL, which works the same way).
3. Click the **install icon in the address bar** (or the browser's "Install App" / "Add to Home Screen" menu item).
4. TimerGo now runs as a standalone desktop/mobile app, works offline, and keeps all your data on-device.

No server on hand? Any static host works the same way — GitHub Pages, Netlify, Vercel, or similar.

## Your data (100% local, nothing ever leaves your device)

TimerGo stores everything in your browser's `localStorage`. There is no server and nothing is ever transmitted anywhere:

| Key | Stores |
|---|---|
| `timergo-profiles-v2` | All your saved timer profiles and their phases |
| `timergo-current-profile-v2` | Which profile is currently selected |
| `timergo-runtime-v1` | The live timer snapshot (current phase, time remaining, running/paused) — restored on refresh or relaunch |
| `timergo-theme` | Day/night theme choice |
| `timergo-zoom` | Card zoom level |
| `timergo-card-pos` | Card position on screen |
| `timergo-wallpaper` | Selected wallpaper (preset, URL, or uploaded image data) |
| `timergo-quotes` | Your custom motivational quotes |
| `timergo-quotes-enabled` | Whether the quote bar is shown |

Use **Settings → Data → Export** to save all of this to a single `timergo_backup.json` file, and **Import** to restore it (e.g. on a new device or browser).

## Keyboard shortcuts

| Key | Action |
|---|---|
| `Space` | Start / Pause |
| `R` | Reset current phase |
| `S` or `→` | Skip to next phase |
| `+` / `-` | Zoom in / out |
| `0` | Reset zoom |
| `Ctrl/Cmd` + mouse wheel | Fluid zoom |
| `Esc` | Close the Settings drawer or legal sheet |

Click the timer digits directly to type in a custom duration for the current phase.

## Getting started (quick look, no install)

1. Open `index.html` directly in any modern browser — no server required for basic use.
2. Pick or build a profile from the gear icon.
3. Click **Start**.

## Privacy & legal

Full disclaimer, privacy policy, and MIT license text are available in-app via the shield icon in the header (or see [LICENSE](LICENSE)). Short version: no accounts, no cookies, no analytics, no tracking — everything stays in your browser's local storage.

## Project structure

Everything ships as static files — no build step:

- `index.html` — the entire app: markup, styles, and logic.
- `sw.js` — service worker for offline caching.
- `manifest.json` — PWA manifest (name, icons, theme colors).
- `icon.svg`, `icon-192.png`, `icon-512.png` — app icons.
- `og-preview.jpg` — social share preview image.

## License

MIT — see [LICENSE](LICENSE).
