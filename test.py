# Use this if you want to see what your blueprint string actually contains

import zlib, base64

def decompress(blueprint_str):
    try:
        data = base64.b64decode(blueprint_str.encode("utf-8"))
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
