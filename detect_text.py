#!/usr/bin/env python3
"""
Simple script to detect (and optionally visualise) text inside an image using
Tesseract OCR via the pytesseract wrapper.

Usage:
    python detect_text.py --image /path/to/image.png [--visualise]

Dependencies (add these to requirements.txt):
    opencv-python
    pytesseract
    pillow

System requirement:
    Tesseract-OCR engine must be installed and in PATH.
    On Debian/Ubuntu:  sudo apt-get install tesseract-ocr
"""

import argparse
from pathlib import Path

import cv2  # type: ignore
import pytesseract
from pytesseract import Output

BOLD = "\033[1m"
RESET = "\033[0m"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Detect text in an image using Tesseract OCR")
    parser.add_argument("--image", "-i", required=True, type=Path, help="Path to the input image")
    parser.add_argument(
        "--visualise",
        "-v",
        action="store_true",
        help="If set, display the image with detected text bounding boxes",
    )
    parser.add_argument(
        "--min_confidence",
        "-c",
        type=int,
        default=60,
        help="Minimum confidence (0-100) to consider a detection valid",
    )
    return parser.parse_args()


def load_image(image_path: Path):
    """Load image from disk and return as BGR numpy array."""
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return image


def preprocess(image):
    """Pre-process image for better OCR results (grayscale + denoise + threshold)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Denoise
    gray = cv2.medianBlur(gray, 3)
    # Adaptive threshold for binarisation
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        15,
        9,
    )
    return thresh


def perform_ocr(image, min_confidence: int):
    """Run Tesseract OCR and return recognised text and bounding boxes."""
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(data["level"])
    results = []
    for i in range(n_boxes):
        conf = int(data["conf"][i])
        text = data["text"][i].strip()
        if conf >= min_confidence and text:
            x, y, w, h = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )
            results.append({"text": text, "conf": conf, "bbox": (x, y, w, h)})
    return results


def draw_boxes(image, results):
    """Draw bounding boxes and text labels on the image."""
    for r in results:
        x, y, w, h = r["bbox"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            r["text"],
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )
    return image


def main() -> None:
    args = parse_args()
    image = load_image(args.image)
    preprocessed = preprocess(image)

    results = perform_ocr(preprocessed, args.min_confidence)

    # Print recognised text lines
    if results:
        print(f"{BOLD}Detected text (confidence >= {args.min_confidence}):{RESET}")
        for r in results:
            print(f" - {BOLD}{r['text']}{RESET} (conf={r['conf']})")
    else:
        print(f"{BOLD}No text detected with the given confidence threshold.{RESET}")

    if args.visualise:
        image_with_boxes = draw_boxes(image.copy(), results)
        cv2.imshow("OCR Results", image_with_boxes)
        print("Press any key in the image window to exit …")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()