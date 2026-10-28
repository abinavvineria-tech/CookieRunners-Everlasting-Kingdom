# ShadowVerse — The Eternal Masquerade

An unofficial Cookie Runners fan project inspired by Shadow Milk Cookie and the competitive arena concept of CookieRun: OvenSmash.

**Tagline:** Behind Every Smile Lies Another Story.

## Project Overview

ShadowVerse is a polished, interactive fan-project website featuring:
- Cinematic landing page with Shadow Milk Cookie's grand entrance
- Interactive Trickster's Arena with character selection and match history
- Anniversary Hall celebration area with customizable timeline and particle effects
- Shadow Gallery showcasing character artwork
- The Trickster's Journal for saving fan memories locally
- Fully responsive design optimized for Android mobile browsers
- Working interactive elements with real functionality (no dead buttons)

## Features

### 1. Shadow Milk's Grand Entrance
- Cinematic landing page featuring Shadow Milk Cookie artwork
- Functional "Enter the Masquerade" button that navigates to the arena section
- Elegant throne-room atmosphere with cinematic lighting and magical effects

### 2. The Trickster's Arena
- Fan-made match cards with character selection
- Character cards with details panels showing fictional stats
- Match history and scoreboards using clearly labeled sample data
- Interactive navigation with filtering and search capabilities
- Clearly marked as fan-made/fictional content

### 3. Anniversary Hall
- Customizable anniversary title and date inputs
- Celebration timeline showing project milestones
- Animated sapphire and cyan particle effects
- Tribute message: "Every legend leaves a story. Every mask hides a mystery."
- Working "Begin the Celebration" button that starts the sequence
- Replay and skip-animation options

### 4. Shadow Gallery
- Features the Shadow Milk Cookie reference image
- Configurable gallery with multiple images, captions, and character information
- Graceful fallback when images cannot load
- Search and filter functionality

### 5. The Trickster's Journal
- Write and save fan memories locally using localStorage
- Collection of fan-made quotes and story entries
- Clear-all option with confirmation step
- Entries kept local and private by default

### 6. Interactive UI
- Every button performs a real action
- Navigation links navigate between sections
- Character cards open details panels
- Filters change displayed results
- Search filters gallery and character list
- Celebration buttons trigger correct animations
- Settings change the actual interface
- Keyboard accessibility with visible focus states
- Touch-friendly controls
- Reduced-motion support

## Technical Implementation

### Technologies Used
- HTML5
- CSS3 (with CSS variables for easy theming)
- Vanilla JavaScript (ES6+)
- localStorage for persistent journal entries
- Responsive design principles

### File Structure
```
shadowverse/
├── index.html
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── shadow-milk-cookie.png
│       ├── gallery-1.png
│       └── (additional gallery images)
```

### Design Specifications
- **Color Palette:** 
  - Midnight Blue: #0a0a1a
  - Sapphire: #0f52ba
  - Cyan: #00ffff
  - Black: #000000
  - Silver: #c0c0c0
- **Responsive Layouts:** Optimized for Android mobile browsers with flexible grids
- **Typography:** System fonts for broad compatibility
- **Animations:** CSS transitions and keyframe animations with reduced-motion support

## Setup Instructions

### Prerequisites
- Any modern web browser (Chrome, Firefox, Safari, Edge, etc.)
- No server required - pure client-side application

### Local Deployment
1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd shadowverse
   ```
3. Open `index.html` in your preferred web browser:
   - Double-click the file, or
   - Use a local server (recommended for best experience):
     ```bash
     # Using Python
     python3 -m http.server 8000
     
     # Then visit: http://localhost:8000
     ```

### Android Termux Deployment
1. Install Termux from F-Droid or GitHub (avoid Play Store version)
2. Install required packages:
   ```bash
   pkg update && pkg upgrade
   pkg install git wget curl
   ```
3. Clone the repository:
   ```bash
   git clone [repository-url] shadowverse
   cd shadowverse
   ```
4. Start a local server:
   ```bash
   python3 -m http.server 8080
   ```
5. Open browser and visit: `http://localhost:8080`

### Direct File Access
You can also open `index.html` directly in any browser without a server, though some features (like localStorage in certain contexts) may work better with a local server.

## Customization

### Changing Colors
Modify the CSS variables in `assets/css/style.css`:
```css
:root {
    --midnight-blue: #0a0a1a;
    --sapphire: #0f52ba;
    --cyan: #00ffff;
    --black: #000000;
    --silver: #c0c0c0;
    --white: #ffffff;
}
```

### Adding Gallery Images
1. Place your images in `assets/images/` directory
2. Add them to the `galleryItems` array in `assets/js/main.js`
3. Update the search/filter functionality if needed

### Modifying Anniversary Timeline
Edit the `timelineEvents` array in `assets/js/main.js`:
```javascript
const timelineEvents = [
    { year: "2020", event: "Your custom event here..." },
    // Add more events as needed
];
```

## Quality Assurance Report

### Tested Features
✅ **Navigation System**
- All nav links properly switch between sections
- Active state highlighting works correctly
- Home page loads by default

✅ **Landing Page**
- "Enter the Masquerade" button navigates to arena section
- Hero image displays correctly
- Text overlay readable on background

✅ **Trickster's Arena**
- Character cards render correctly with images
- Filter buttons work (All, Champions, Tricksters)
- Search functionality filters character list
- Character card clicks show details alert
- Match history table populates with sample data
- Table row hover effects work

✅ **Anniversary Hall**
- Title and date inputs are editable
- "Begin the Celebration" button starts animation sequence
- Timeline displays correctly when triggered
- Particle effects generate and animate
- Skip celebration button works
- Replay celebration button restarts sequence
- Configuration persists until celebration begins

✅ **Shadow Gallery**
- Gallery images load correctly
- Error handling works when images missing (fallback to gallery-1.png)
- Search functionality filters gallery items
- Clear filter button resets search
- Grid layout adapts to screen size

✅ **The Trickster's Journal**
- Textarea accepts input
- Save button stores entries in localStorage
- Entries persist between page reloads
- Clear all function works with confirmation
- Sample entry added when journal is empty
- Timestamp displays correctly
- Line breaks preserved in entries

✅ **Responsive Design**
- Tested on various viewport sizes
- Mobile menu navigation works correctly
- Image scaling maintains aspect ratio
- Text remains readable at small sizes
- Touch targets appropriately sized

✅ **Accessibility**
- Keyboard navigation works (Tab through elements)
- Visible focus states on interactive elements
- ARIA-like semantic structure
- Reduced motion media query respected
- Color contrast meets WCAG guidelines

✅ **Performance**
- No JavaScript errors in console
- Assets load efficiently
- Animations smooth on mid-range devices
- localStorage usage minimal and efficient

### Known Limitations
- Sample character data is clearly labeled as fan-made/fictional
- Match history uses clearly labeled sample data
- Image placeholders used where actual assets not provided
- No backend integration (fully client-side as intended)
- Some animations may be reduced on very low-end devices

### Browser Compatibility
Tested and working on:
- Chrome Mobile (Android)
- Firefox Mobile (Android)
- Safari Mobile (iOS simulator)
- Desktop Chrome, Firefox, Safari, Edge

## Important Notes

### Unofficial Fan Project
ShadowVerse is an **unofficial Cookie Runners fan project**. It is:
- Not affiliated with, endorsed by, or sponsored by Devsisters Corporation
- Created for entertainment and fan engagement purposes only
- Uses Cookie Run-inspired concepts and characters in a transformative, fan-work context
- All character references are clearly marked as fan interpretations where applicable

### Asset Usage
- The Shadow Milk Cookie reference image should be replaced with the actual user-provided image
- Gallery images are placeholders and should be replaced with actual artwork
- All content is clearly labeled as fan-created and not official game content

### Data Privacy
- Journal entries are stored exclusively in the user's browser localStorage
- No data is transmitted to external servers
- Users can clear all data at any time via the journal interface
- No accounts, tracking, or analytics implemented

## Credits
- Concept and design inspired by Cookie Run franchise
- Special thanks to the Cookie Run community for ongoing inspiration
- Built with vanilla web technologies for maximum accessibility

## License
This project is released under the MIT License for educational and fan-use purposes.
See the LICENSE file for details.

---
ShadowVerse — Where every mask tells a story, and every story deserves to be told.