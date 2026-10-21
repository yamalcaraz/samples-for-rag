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

It is a **closed-box table**, i.e. every cell outlined, which is what a real printed form looks
like — and precisely the layout that breaks default OCR. Measured on this file with Tesseract 5.5:

| segmentation | words recovered | zipcodes (of 12 rows) |
|---|---|---|
| `--psm 3` (auto) | 18 | 0 |
| `--psm 4` (single column) | 66 | 9 |

Auto page segmentation reads the boxed cells as graphics. `psm 4` recovers the rows. Any pipeline
that hard-codes `psm 3` will report an empty document here and blame the scan.

Preprocessing helps as well: 2× LANCZOS upscale plus autocontrast before OCR.

## Provenance

* `report.pdf` is a public KU Leuven document, included unchanged for demonstration.
* `customer_table.jpg` was generated for this repo. Every name, address and zipcode is fictional;
  the page was drawn, skewed by 0.4°, given sensor noise and saved as a JPEG, so there is no text
  layer to cheat with.
