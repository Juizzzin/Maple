# Use this if you want to see what your blueprint string actually contains

import gzip
import base64

def decompress(blueprint_str):
    missing_padding = len(blueprint_str) % 4
    if missing_padding:
        blueprint_str += "=" * (4 - missing_padding)
    data = base64.urlsafe_b64decode(blueprint_str)
    decompressed = gzip.decompress(data).decode("utf-8")
    parts = [p.strip() for p in decompressed.split("|") if p.strip()]
    parts.sort()
    return parts

def main():
    blueprint = input("Paste the blueprint string: ").strip()
    
    if not blueprint:
        print("No input detected.")
        return

    pkgs = decompress(blueprint)
    
    if pkgs:
        print(f"Decompressed {len(pkgs)} packages:")
        print("-" * 30)
        for i, pkg in enumerate(pkgs, 1):
            print(f"{i:3}. {pkg}")
        print("-" * 30)

if __name__ == "__main__":
    main()