<p align="center">
  <img src="assets/Maple400x400.png" width="120"/>
</p>

# Maple
**Maple** is a cross-platform utility to snapshot and restore your installed software. It generates a tiny, portable blueprint string that you can use to replicate your environment on any other machine - currently only on the same OS.

## Quick Start

### Windows
1. Download `Maple.exe` from the [latest release](https://github.com/Juizzzin/Maple/releases).
2. Double-click to run (or run via PowerShell/CMD).

### macOS & Linux (Setup Required)
Unlike Windows, macOS and Linux require you to manually grant "Execute" permissions after downloading the binary.

1. **Download** the `Maple-macos` or `Maple-linux` binary.
2. **Open your Terminal** and navigate to your Downloads folder.
3. **Grant permission** by running:
   ```bash
   chmod +x Maple-linux  # or Maple-macos
   ```
4. **Run it:**
   ```bash
   ./Maple-linux # or Maple-macos
   ```

## Build from source
If you prefer to run with Python or build the binary yourself:
**Clone & Run**
   ```bash
   git clone https://github.com/Juizzzin/Maple.git
   cd Maple
   python3 maple.py
   ```

## How it works
1. **Scan:** Maple identefies all user-installed packages while filtering out system noise.
2. **Compress:** The list is compressed and encoded into a blueprint string
3. **Restore:** Paste the string on a new machine, and Maple will automatically trigger the native package manager to install everything.

## Licesne
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
