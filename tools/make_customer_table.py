"""Generate data/customer_table.jpg for the samples repo.

Legibility matters more than realism here: this image is the input to an OCR demo, so the type is
sized to be comfortably readable (11.5 pt at 200 dpi) while the page still carries the scan
artefacts that make OCR non-trivial - skew, sensor noise, soft focus, closed cell boxes.

Run: python3 tools/make_customer_table.py   (writes data/customer_table.jpg)
"""
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CUSTOMERS = [
    ("Delphine Maes", "Naamsestraat 45", "3000 Leuven"),
    ("Bram Claes", "Turnhoutsebaan 12", "2300 Turnhout"),
    ("Sofie Van den Broeck", "Veldstraat 88", "9000 Gent"),
    ("Pieter Janssens", "Meir 21", "2000 Antwerpen"),
    ("Amelie Dubois", "Rue de la Loi 33", "1000 Brussel"),
    ("Tom Verhoeven", "Grote Markt 7", "2800 Mechelen"),
    ("Els Peeters", "Stationsstraat 154", "3010 Kessel-Lo"),
    ("Karel De Smet", "Kerkstraat 9", "9300 Aalst"),
    ("Nadia Benali", "Bondgenotenlaan 101", "3000 Leuven"),
    ("Joris Willems", "Havenlaan 62", "8500 Kortrijk"),
    ("Lotte Hermans", "Dorpsstraat 3", "3001 Heverlee"),
    ("Ruben Aerts", "Leopoldlaan 44", "3700 Tongeren"),
]

DPI = 200
W, H = int(8.27 * DPI), int(11.69 * DPI)
# matplotlib's font manager is the easy route but it is absent from a bare runtime, and Pillow's
# default bitmap font is 11 px - it renders unreadable text at 26 "pt" and silently makes the
# whole OCR demo look broken. Try real TrueType files first, in the order they usually exist.
FONT_CANDIDATES = [
    "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def font(size, bold=False):
    for path in FONT_CANDIDATES:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size)
    try:
        from matplotlib import font_manager
        return ImageFont.truetype(font_manager.findfont("DejaVu Sans"), size)
    except Exception:
        return ImageFont.load_default(size=size)      # Pillow >= 10.1 honours the size


COLS = [(110, 90), (200, 520), (720, 560), (1280, 264)]
HEADERS = ["#", "CUSTOMER NAME", "ADDRESS", "ZIPCODE"]
BODY_SIZE = 32


def build():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    d.text((110, 110), "NORTHWIND TRADE SERVICES BV", font=font(46, True), fill="black")
    d.text((110, 190), "CUSTOMER MASTER LIST - extract", font=font(34), fill="black")
    d.text((110, 240), "ref CMS-2026-04   issued 14 March 2026   confidential",
           font=font(28), fill="black")
    d.line([(110, 300), (W - 110, 300)], fill="black", width=4)

    y = 350
    for (x, w), label in zip(COLS, HEADERS):
        d.rectangle([(x, y), (x + w, y + 80)], outline="black", width=2)
        d.text((x + 12, y + 20), label, font=font(30, True), fill="black")
    y += 80

    for number, (name, addr, zipc) in enumerate(CUSTOMERS, start=1):
        for (x, w), value in zip(COLS, (str(number), name, addr, zipc)):
            d.rectangle([(x, y), (x + w, y + 100)], outline=(150, 150, 150), width=2)
            d.text((x + 12, y + 30), value, font=font(BODY_SIZE), fill="black")
        y += 100

    d.text((110, H - 110), "Northwind Trade Services BV - KBC 012-3456789-01 - VAT BE0123.456.789",
           font=font(24), fill="black")
    d.text((W - 300, H - 110), "page 1 of 2", font=font(24), fill="black")

    # 0.1 degrees, and the exact value matters: at 0.00 the box rules line up perfectly with the
    # pixel rows, Tesseract folds them into the text lines and recovers 1 of 12 rows; at 0.10 it
    # recovers 12 of 12; at 0.25 it drops back to 10 of 12. Measure, do not pick a "realistic" number.
    img = img.rotate(0.10, resample=Image.BICUBIC, expand=False, fillcolor="white")
    base = np.asarray(img).astype(np.int16)
    noise = np.random.default_rng(7).normal(0, 2, base.shape).astype(np.int16)
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.15))


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parents[1] / "data" / "customer_table.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    build().save(out, format="JPEG", quality=90, optimize=True)
    print("wrote %s (%d KB, %dx%d)" % (out, out.stat().st_size // 1024, *Image.open(out).size))
