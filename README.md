# Clone Hero Custom Name Generator

A desktop application to create unique and visually appealing custom player names for Clone Hero, featuring gradient and individual letter coloring, and direct export to `profiles.ini`.

## ✨ Features

* **Gradient Name Generation:** Create smooth color gradients across your player name using multiple color stops.
* **Individual Letter Coloring:** Assign unique colors and styling (bold, italic, underline, strikethrough) to each letter of your name.
* **Global Font Styling:** Apply global font size and character spacing to both gradient and individual letter modes.
* **Live Preview:** See a real-time visual preview of your generated name.
* **Direct Export:** Easily export your custom name directly into a `profiles.ini` file, ready for use in Clone Hero.
* **User-Friendly Interface:** An intuitive graphical user interface built with Tkinter.

## 🚀 How to Use

### Installation (Windows Executable)

1.  Download the latest compiled `.exe` version from the [Releases](https://github.com/iamjrmh/CloneHeroColorGen/releases) section of this repository.
2.  Unzip the downloaded file to a location on your computer (e.g., `C:\Program Files\CloneHeroNameGen`).
3.  Run `newgui.exe` (or `CloneHeroColorGen.exe` if renamed).

### Generating a Gradient Name

1.  Switch to the **"Gradient"** tab (this might be labeled "Home" initially, depending on your app version).
2.  Enter your desired player name in the "Name:" field.
3.  Select your desired **Start Color** and **End Color** using the provided color pickers or by typing hex codes (e.g., `#RRGGBB`).
4.  Optionally, add up to three intermediate colors for more complex gradients.
5.  Choose styling options: **Bold**, **Italic**, **Underline**, **Strikethrough**.
6.  Set a **Font Size** and **Spacing** if desired (optional).
7.  Click the **"Generate"** button.
8.  The generated tagged name will appear in the "Output:" box, and a visual "Preview:" will show below.

### Generating an Individual Letter Name

1.  Switch to the **"Single Letter Coloring"** tab (this might be labeled "Discovery" initially).
2.  Enter your desired player name in the "Name:" field.
3.  Click **"Update Letters"** to generate individual controls for each character.
4.  For each letter, choose its **Color** using the picker or hex code, and apply individual **Bold**, **Italic**, **Underline**, or **Strikethrough** styles.
5.  Set global **Font Size** and **Spacing** if desired (optional).
6.  Click the **"Generate"** button.
7.  The generated tagged name will appear in the "Output:" box, and a visual "Preview:" will show below.

### Exporting to `profiles.ini`

1.  After generating your desired name in either mode, click the **"Export to profiles.ini"** button.
2.  A folder selection dialog will appear. Navigate to your Clone Hero installation's `data` folder (or any other folder where you keep your `profiles.ini`) and select it.
3.  The application will add a new profile entry to your `profiles.ini` file. A confirmation message will appear upon successful export.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new features, improvements, or bug fixes, please open an issue or submit a pull request on the GitHub repository.

## 📄 License

This project is open-source. (Consider adding a specific license here, e.g., MIT, Apache 2.0).

---

