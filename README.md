# samples-for-rag

Two sample documents for retrieval-augmented generation demos, one easy and one deliberately hard.

| file | what it is | why it is here |
|---|---|---|
| [`data/report.pdf`](data/report.pdf) | KU Leuven DigiSoc annual report 2023-2024 — 36 pages, 1.4 MB, real text layer | the easy path: PDF text extraction |
| [`data/customer_table.jpg`](data/customer_table.jpg) | customer register, 24 rows of name / address / zipcode — 1654 × 2339, 169 KB, **no text layer** | the hard path: OCR must read pixels |

Raw URLs:

```
https://raw.githubusercontent.com/yamalcaraz/samples-for-rag/main/data/report.pdf
https://raw.githubusercontent.com/yamalcaraz/samples-for-rag/main/data/customer_table.jpg
```

## Why the image looks like that

It is a **closed-box table** — every cell outlined, which is what a real printed form looks like.
The layout is the point: it is where OCR defaults stop working, and where "just look at the file"
is not enough. Everything below was measured on this file with Tesseract 5.5, counting rows that
came back exactly (name **and** address **and** zipcode correct).

| input | words | rows exact |
|---|---|---|
| native 200 dpi, `--psm 3` (auto) | 113 | **12 / 12** |
| native 200 dpi, `--psm 4` (single column) | 113 | **12 / 12** |
| 2× LANCZOS upscale, either mode | 34 | 0 / 12 |

Two things worth knowing before you reuse this file:

* **Upscaling can hurt.** The folklore "always 2× before OCR" is wrong here: native resolution
  reads every row, the upscale reads none. Try both and keep the better one.
* **The skew is chosen, not decorative.** At exactly 0.00° the cell rules align with the pixel
  rows, Tesseract folds them into the text lines and recovers **1 of 12** rows. At 0.10° it
  recovers **12 of 12**; at 0.25° it falls back to 10 of 12. The page is rotated by 0.10°.

A production pipeline would still de-line the image (morphological line removal) or use a
table-structure model such as PP-Structure, because columns here arrive as one text line, not as
fields.

## Provenance

* `report.pdf` is a public KU Leuven document, included unchanged for demonstration.
* `customer_table.jpg` was generated for this repo. Every name, address and zipcode is fictional;
  the page was drawn, skewed by 0.10°, given sensor noise and saved as a JPEG, so there is no
  text layer to cheat with. `tools/make_customer_table.py` regenerates it.
