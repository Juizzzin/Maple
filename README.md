<p align="center">
  <img src="assets/Maple400x400.png" width="120"/>
</p>

# Maple

**Maple** is a CLI tool to snapshot and restore your installed software using your system’s native package manager.

It generates a small, portable blueprint string that can be used to replicate your environment on another machine.

> **Status:** Early-stage project. Currently most reliable on Windows using winget.  
> macOS (Homebrew) and Linux (apt) support are experimental.


## Features

- Scan installed packages
- Generate a compact, shareable blueprint string
- Restore packages using native package managers
- Lightweight and fast


## Quick Start

### Windows

1. Download `Maple-windows.exe` from the [latest release](https://github.com/Juizzzin/Maple/releases)
2. Run it via double-click or in PowerShell/CMD


### macOS & Linux (Setup Required)

macOS and Linux require manual permission to execute the binary.

1. Download the appropriate binary (`Maple-macos` or `Maple-linux`)
2. Open Terminal and navigate to your download folder
3. Grant execute permission and run:
```bash
chmod +x Maple-linux  # or Maple-macos
./Maple-linux  # or Maple-macos
```


## Build from Source

If you prefer to run it with Python:

```bash
git clone https://github.com/Juizzzin/Maple.git
cd Maple
python3 maple.py
```


## How It Works

1. **Scan**  
   Maple identifies user-installed packages from your system’s package manager.
2. **Generate Blueprint**  
   The package list is compressed and encoded into a compact string.
3. **Restore**  
   Paste the blueprint on another machine to reinstall your packages.


## Current Support

- **Windows (winget)** — primary and most tested  
- **macOS (Homebrew)** — experimental  
- **Linux (apt)** — experimental  


## Future Goals

- Better compression
- Cross-platform restore support  
- Improved package detection and filtering  
- Version-aware restores  
- More package manager integrations  


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
