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

# -----------------------------
# Country-level classification
# -----------------------------
#  - 한국식 : 포함된 한글 음절 여부로 판별
#  - 일본식 : 히라가나(ぁ-ん)·가타카나(ァ-ン) 포함 여부로 판별
#  - 미국식 : ASCII 영문·숫자·공백·하이픈만 존재(최대 8~9자)로 간략 판별

KOREAN_CHAR_REGEX = re.compile(r"[가-힣]")
JAPANESE_CHAR_REGEX = re.compile(r"[ぁ-んァ-ン]")
US_PLATE_REGEX = re.compile(r"^[A-Z0-9\-\s]{2,9}$", re.I)


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


def classify_country(plate: str) -> str:
    """Return plate country style: 한국식, 일본식, 미국식, or Unknown."""
    s = plate.strip()

    if KOREAN_CHAR_REGEX.search(s):
        return "한국식"

    if JAPANESE_CHAR_REGEX.search(s):
        return "일본식"

    # If only ASCII letters/digits/hyphens/spaces, treat as US style
    if US_PLATE_REGEX.fullmatch(s):
        return "미국식"

    return "Unknown"


def _extract_digits(plate: str) -> str:
    """Helper to extract all digits from the plate string."""
    return "".join(re.findall(r"\d", plate))


def main():
    print("다국적 차량 번호판 분류기 (한국·일본·미국) + 세부 판별 및 숫자 추출")
    print("종료하려면 빈 줄을 입력하세요.\n")

    while True:
        raw = input("번호판 입력 > ").strip()
        if not raw:
            break

        country = classify_country(raw)

        if country == "한국식":
            subtype, numbers = classify_plate(raw)
            subtype_info = f" (세부: {subtype})" if subtype != "Unknown" else ""
        else:
            subtype_info = ""
            numbers = _extract_digits(raw)

        print(f"  국가/형식 : {country}{subtype_info}")
        print(f"  숫자만 추출 : {numbers}\n")


if __name__ == "__main__":
    main()