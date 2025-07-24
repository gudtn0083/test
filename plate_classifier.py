import re
from typing import Tuple

# Regular expression patterns for license plates
#  - New style (신형): 3 digits + Hangul + 4 digits (e.g., "123가4567")
#  - Old style (구형): 2 digits + Hangul + 4 digits (e.g., "12가3456")
# Both patterns may include optional spaces or hyphens.
NEW_PLATE_REGEX = re.compile(r"""
    ^\s*                 # optional leading whitespace
    (\d{3})              # 3 region digits (capture group 1)
    [\s-]*               # optional separator
    ([가-힣])             # Korean class character (capture group 2)
    [\s-]*               # optional separator
    (\d{4})              # 4 serial digits (capture group 3)
    \s*$                 # optional trailing whitespace
""", re.VERBOSE)

OLD_PLATE_REGEX = re.compile(r"""
    ^\s*                 # optional leading whitespace
    (\d{2})              # 2 region digits (capture group 1)
    [\s-]*               # optional separator
    ([가-힣])             # Korean class character (capture group 2)
    [\s-]*               # optional separator
    (\d{4})              # 4 serial digits (capture group 3)
    \s*$                 # optional trailing whitespace
""", re.VERBOSE)


def classify_plate(plate: str) -> Tuple[str, str]:
    """Classify a Korean license plate as 신형(new) or 구형(old).

    Parameters
    ----------
    plate : str
        The raw license plate string (e.g., "123가4567", "12가3456").

    Returns
    -------
    Tuple[str, str]
        ("신형" or "구형" or "Unknown", digits_only)
    """
    # Remove surrounding whitespace for robustness
    plate_stripped = plate.strip()

    # Attempt to match new style first
    if NEW_PLATE_REGEX.match(plate_stripped):
        return "신형", _extract_digits(plate_stripped)

    # Attempt to match old style next
    if OLD_PLATE_REGEX.match(plate_stripped):
        return "구형", _extract_digits(plate_stripped)

    # If neither pattern matches, return Unknown
    return "Unknown", _extract_digits(plate_stripped)


def _extract_digits(plate: str) -> str:
    """Helper to extract all digits from the plate string."""
    return "".join(re.findall(r"\d", plate))


def main():
    print("한국 차량 번호판 분류기 (신형/구형) 및 숫자 추출")
    print("종료하려면 빈 줄을 입력하세요.\n")

    while True:
        raw = input("번호판 입력 > ").strip()
        if not raw:
            break

        plate_type, numbers = classify_plate(raw)
        print(f"  판별 결과 : {plate_type}")
        print(f"  숫자만 추출 : {numbers}\n")


if __name__ == "__main__":
    main()