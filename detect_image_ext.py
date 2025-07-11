# NOTE: imghdr was removed in Python 3.13. We replicate essential behaviour
# via simple signature checks and (optionally) Pillow.

from pathlib import Path

SIGNATURES: dict[bytes, str] = {
    b"\xFF\xD8\xFF": ".jpg",  # JPEG/JFIF
    b"\x89PNG": ".png",        # PNG
    b"GIF87a": ".gif",          # GIF87a
    b"GIF89a": ".gif",          # GIF89a
    b"BM": ".bmp",              # BMP
    b"II*\x00": ".tif",        # TIFF little-endian
    b"MM\x00*": ".tif",        # TIFF big-endian
    b"RIFF": ".webp",           # WEBP starts with RIFF....WEBP
}

try:
    from PIL import Image  # Optional; improves detection for more formats
except ImportError:
    Image = None


def get_image_extension(path: str | Path):
    """Return the actual image extension for the given file path.

    If the format cannot be determined, returns None.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)

    # First attempt: quick signature sniffing
    try:
        with path.open("rb") as fp:
            head = fp.read(12)
        for sig, ext in SIGNATURES.items():
            if head.startswith(sig):
                # Special case: WEBP requires 'WEBP' at offset 8
                if ext == ".webp" and b"WEBP" not in head[8:12]:
                    continue
                return ext
    except Exception:
        pass

    # Second attempt: Pillow (if available)
    if Image is not None:
        try:
            with Image.open(path) as img:
                fmt = img.format  # e.g., 'JPEG', 'PNG', ...
                if fmt:
                    # Pillow returns 'JPEG' for JPEG files, map to .jpg for convenience
                    return f".{fmt.lower() if fmt != 'JPEG' else 'jpg'}"
        except Exception:
            pass

    return None  # Could not determine


if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="Detect image file extension.")
    parser.add_argument("files", nargs="+", help="Image file paths to analyse")
    args = parser.parse_args()

    for file_path in args.files:
        try:
            ext = get_image_extension(file_path)
            print(f"{file_path}: {ext or 'unknown'}")
        except FileNotFoundError as e:
            print(e)