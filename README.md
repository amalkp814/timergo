# TimerGo

TimerGo is a simple, sleek, and highly precise Pomodoro timer built with pure HTML, CSS, and vanilla JavaScript. 
It features a modern UI with smooth transitions and is designed to run accurately even in background tabs, avoiding common JavaScript `setInterval` throttling issues.

## Features

- **Accurate Timing:** Uses system timestamps to ensure precise countdowns, regardless of browser background throttling.
- **Three Modes:**
  - Pomodoro (25 minutes)
  - Short Break (5 minutes)
  - Long Break (15 minutes)
- **Fluid UI & Animations:** Beautifully styled with CSS custom properties and transitions. Features a modern glassmorphism effect.
- **Audio Chime:** A soft, native Web Audio API chime plays when the timer concludes (fully compliant with modern browser autoplay policies).
- **Zero Dependencies:** No external libraries, frameworks, or assets required. 

## Getting Started

1. Clone or download this repository.
2. Open `index.html` in any modern web browser (no web server required).
3. Select your desired mode (Pomodoro, Short Break, or Long Break).
4. Click **Start** to begin the timer.

## Code Structure

The entire application is self-contained within `index.html`:
- **HTML structure:** A semantic, accessible layout for the timer and controls.
- **CSS styles:** Inline stylesheet managing colors, typography (via Google Fonts), responsiveness, and transitions.
- **JavaScript logic:** Handles precise timing using `Date.now()` differences, tab title updates, play/pause states, DOM manipulation, and Web Audio API interactions.

## Open Source

This project is open-source and free to use. Contributions, forks, and modifications are highly encouraged.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
