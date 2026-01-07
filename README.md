# 🎨 Clone Hero Custom Name Generator

Create unique and visually stunning custom player names for Clone Hero with gradient colors, individual letter styling, and direct export to your profile.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Gradient Name Generation** - Create smooth color gradients across your player name with multiple color stops
- **Individual Letter Coloring** - Assign unique colors and styling to each letter independently
- **Advanced Text Styling** - Bold, italic, underline, and strikethrough options for maximum customization
- **Global Font Controls** - Adjust font size and character spacing for perfect visual balance
- **Live Preview** - Real-time visual feedback as you design your name
- **Direct Export** - One-click export to `profiles.ini` ready for Clone Hero
- **Intuitive Interface** - Modern, user-friendly GUI built with Tkinter

## 🚀 Quick Start

### Installation (Windows Executable)

1. **Download** the latest `.exe` from the [Releases](https://github.com/iamjrmh/CloneHeroColorGen/releases) page
2. **Extract** the zip file to your preferred location (e.g., `C:\Program Files\CloneHeroNameGen`)
3. **Run** `jrmh.rh Name Gen.exe`

No Python installation required!

## 🎨 Creating Your Custom Name

### Gradient Mode

Perfect for smooth, flowing color transitions across your entire name.

1. **Switch to "Gradient" tab** (may be labeled "Home")
2. **Enter your name** in the "Name:" field
3. **Choose colors**:
   - Select **Start Color** and **End Color**
   - Optionally add up to 3 intermediate colors for complex gradients
4. **Apply styling** (optional):
   - ✓ Bold
   - ✓ Italic
   - ✓ Underline
   - ✓ Strikethrough
5. **Adjust spacing** (optional):
   - Font Size
   - Character Spacing
6. **Click "Generate"**
7. **Preview** your name in real-time

### Individual Letter Mode

Perfect for rainbow effects or unique per-character styling.

1. **Switch to "Single Letter Coloring" tab**
2. **Enter your name** in the "Name:" field
3. **Click "Update Letters"** to generate controls for each character
4. **Customize each letter**:
   - Select individual color using picker or hex code
   - Apply per-letter styling (Bold, Italic, Underline, Strikethrough)
5. **Set global controls** (optional):
   - Font Size
   - Character Spacing
6. **Click "Generate"**
7. **Preview** your creation

## 📁 File Locations

| File | Location |
|------|----------|
| Clone Hero Profiles | `Documents\Clone Hero\profiles.ini` |

## 🎨 Color Format

Colors use standard hex format: `#RRGGBB`

**Examples:**
- `#FF0000` - Red
- `#00FF00` - Green
- `#0000FF` - Blue
- `#FF00FF` - Magenta
- `#FFFF00` - Yellow

**Tips:**
- Use [coolors.co](https://coolors.co) to find color schemes
- High contrast colors make names more readable
- Test in-game to ensure visibility against backgrounds

## 🐛 Troubleshooting

### Export button doesn't work
- **Cause**: `profiles.ini` is in use or read-only
- **Solution**: Close Clone Hero and ensure the file isn't read-only

### Preview looks different than in-game
- **Cause**: Preview is approximate; actual rendering depends on Clone Hero
- **Solution**: Test in-game for final appearance

### "Permission denied" error
- **Cause**: Application can't write to Documents folder
- **Solution**: Run as administrator or check folder permissions

## 💡 Pro Tips

- **Gradient Tips**:
  - Use 2-3 colors for smooth gradients
  - Avoid too many color stops (can look choppy)
  - Similar hues create subtle effects, contrasting hues create bold effects

- **Individual Letter Tips**:
  - Rainbow effects: Red → Orange → Yellow → Green → Blue → Purple
  - Alternating colors create a "vibrating" effect
  - Use spacing to separate letters with busy colors

- **Styling Tips**:
  - Bold makes names more visible on busy backgrounds
  - Avoid multiple effects (e.g., bold + italic + underline) - can be unreadable
  - Test readability at different screen distances

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## ⚠️ Disclaimer

Use at your own risk. The developer is not responsible for profile data loss.

Also ngl i lowkey kinda lost the original python file i was working on it with so this is highkey gonna be the last update until i remake it LMAOOO my fault guys

## 🎮 Related Projects

- [Clone Hero](https://clonehero.net/) - The rhythm game this tool supports
- [Clone Hero Bad Songs Cleaner](https://github.com/iamjrmh/CloneHeroBadSongsCleaner) - Clean up problematic songs from your library
- [Chorus](https://chorus.fightthe.pw/) - Song database and downloader

---

Made with 🎸 for the Clone Hero community
