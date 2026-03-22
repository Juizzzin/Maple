import platform, subprocess, json, tempfile, os, gzip, base64, sys

RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

class Lazure:
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
        raw_data = "|".join(self.pkgs).encode("utf-8")
        compressed = gzip.compress(raw_data)
        return base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")
    
    def decompress(self, blueprint_str):
        missing_padding = len(blueprint_str) % 4
        if missing_padding:
            blueprint_str += "=" * (4 - missing_padding)
        data = base64.urlsafe_b64decode(blueprint_str)
        decompressed = gzip.decompress(data).decode("utf-8")
        parts = [p.strip() for p in decompressed.split("|") if p.strip()]
        parts.sort()
        return parts
    
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
                subprocess.run(["winget", "install", "--id", id, "--silent", "--accept-source-agreements", "--accept-package-agreements"], check=False)
        if self.manager == "brew":
            subprocess.run(["brew", "install"] + pkgs)
        if self.manager == "apt":
            print(f"{RED}[!] {RESET}Root privileges required.")
            subprocess.run(["sudo", "apt", "install", "-y"] + pkgs)

def main():
    app = Lazure()

    print(f"{RED}MAPLE{GRAY} | {platform.system().upper()}{RESET}")
    print(f"{RED}{"─" * 48}{RESET}")

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