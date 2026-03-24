import platform, subprocess, json, tempfile, os, zlib, base64, sys

RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

class Maple:
    def __init__(self):
        self.system = platform.system().lower()
        self.manager = self._get_manager()
        self.pkgs = []

    def _get_manager(self) -> str:
        if self.system == "windows": return "winget"
        if self.system == "darwin": return "brew"
        if self.system == "linux": return "apt"
        raise OSError("Unsupported Operating System")
    
    def is_system_package(self, pkg_id: str) -> bool:
        pkg_id = pkg_id.lower()
        # List provided by AI. The filter is not verified and definetly not practical
        prefixes = [
            "microsoft.", "msix\\microsoft", "visual", "com.apple.",
            "libc", "libgcc", "libstdc++", "linux-", 
            "base-", "debian-", "ubuntu-", "ca-certificates"
        ]
        contains = [
            "bash", "dash", "grep", "gzip", "login", "hostname", 
            "ncurses", "util-linux", "init", "grub", "shim", "findutils"
        ]

        if any(pkg_id.startswith(p) for p in prefixes): return True
        if any(c in pkg_id for c in contains): return True
        return False
    
    def compress(self):
        self.pkgs.sort()
        normalized = []
        for pkg in self.pkgs:
            if pkg.startswith("."): # If a package starts with .
                pkg = "\\" + pkg
            parts = pkg.split(".")
            if len(parts) >= 2 and parts[0].lower() == parts[1].lower(): # Turns Brave.Brave into .Brave
                pkg = "." + parts[1]
            normalized.append(pkg)

        raw = "\x1f".join(normalized).encode("utf-8")
        compressed = zlib.compress(raw, level=9)
        # b85 is shorter but adds charcters that my cause conflicts in terminals
        # b64 is more terminal friendly but adds slightly more characters
        # Maybe add this later to argparse functionallity
        return base64.b64encode(compressed).decode("utf-8")
    
    def decompress(self, blueprint_str):
        try:
            data = base64.b64decode(blueprint_str.encode("utf-8")) # See compression
            decompressed = zlib.decompress(data).decode("utf-8")
        except Exception as e:
            raise ValueError("Invalid blueprint") from e
        parts = [p for p in decompressed.split("\x1f") if p]

        restored = []
        for pkg in parts:
            if pkg.startswith("\\."):
                pkg = pkg[1:]
            if pkg.startswith("."):
                name = pkg[1:]
                pkg = f"{name}.{name}"
            restored.append(pkg)
        return sorted(restored)
    
    def scanSystem(self):
        if self.manager == "winget":
            with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp: tmp_path = tmp.name
            try:
                subprocess.run(["winget", "export", "-o", tmp_path, "--accept-source-agreements"],
                               capture_output=True, text=True, check=True)
                with open(tmp_path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                for source in data.get("Sources", []):
                    for pkg in source.get("Packages", []):
                        pkg_id = pkg.get("PackageIdentifier")
                        if pkg_id and not self.is_system_package(pkg_id):
                            self.pkgs.append(pkg_id)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        if self.manager == "brew":
            res = subprocess.run(["brew", "leaves"], capture_output=True, text=True)
            self.pkgs = [line.strip() for line in res.stdout.splitlines() if line.strip() and not self.is_system_package(line)]
        
        if self.manager == "apt":
            res = subprocess.run(["apt-mark", "showmanual"], capture_output=True, text=True)
            self.pkgs = [line.strip() for line in res.stdout.splitlines() if line.strip() and not self.is_system_package(line)]

    def installPackages(self, pkgs):
        if not pkgs: return
        if self.manager == "winget":
            for id in pkgs:
                print(f"{RED}[~]{RESET} Installing {id}...")
                subprocess.run(["winget", "install", "--id", id, "--silent", "--accept-source-agreements", "--accept-package-agreements"], check=False) # Kepp check on False else the install will break
        if self.manager == "brew":
            subprocess.run(["brew", "install"] + pkgs)
        if self.manager == "apt":
            print(f"{RED}[!] {RESET}Root privileges required.")
            subprocess.run(["sudo", "apt", "install", "-y"] + pkgs)

def main():
    app = Maple()

    print(f"{RED}MAPLE{GRAY} | {platform.system().upper()}{RESET}")
    print(f"{RED}{"-" * 47}{RESET}") # For some reason pyinstaller doesent want me to use '─' and '\u2500'

    try:
        blueprint_input = input(f"{RED}[?]{RESET} Paste blueprint or press ENTER to generate: ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    except Exception as e:
        print(f"{RED}[!] Error:{RESET} {e}")

    if blueprint_input:
        print(f"\n{RED}[~]{RESET} Decoding blueprint...")
        try:
            pkgs = app.decompress(blueprint_input)
            print(f"{RED}[+]{RESET} Loaded {RED}{len(pkgs)}{RESET} packages:")
            for p in pkgs: print(f" - {p}")
            print(f"\n{RED}[~]{RESET} Starting installation...")
            app.installPackages(pkgs)
            print(f"\n{RED}[✓]{RESET} Installation complete.")
        except Exception as e:
            print(f"{RED}[!] Error:{RESET} {e}")
        return
    
    try:
        print(f"{RED}[~]{RESET} Analyzing installed packages...")
        app.scanSystem()
        if not app.pkgs:
            print(f"{RED}[!] No non-system packages found via {app.manager}.{RESET}")
            return
        print(f"{RED}[+]{RESET} Found {RED}{len(app.pkgs)}{RESET} packages")
        blueprint = app.compress()
        print(f"\n{GRAY}PORTABLE BLUEPRINT:{RESET}")
        print(f"{RED}{blueprint}{RESET}\n")
        print(f"{RED}[✓]{RESET} Copy your blueprint.")
        input()
    except Exception as e:
        print(f"{RED}[!] Scan Error:{RESET} {e}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
