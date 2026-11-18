# GE-SpMM Retuned: project talk

Slides for our CSC 548 (Parallel Systems, NC State, Fall 2026) final-project talk.
Narasimhareddy Dilip Kumar Irala and Pradyumna Chacham.

14 slides: the problem (2–3), the paper and its two tricks (4–6), our work (7–8), results (9–10),
takeaways (11), future work (12), hypotheses (13), thank you and questions (14).

## View the slides

- **NC State design:** https://pradyumna-chacham.github.io/gespmm-talk/
- **Alternative design (same content):** https://pradyumna-chacham.github.io/gespmm-talk/alt/
- **Downloads** in [`downloads/`](downloads/): PDF and PPTX of each design. The PPTX files carry the full speaker notes;
  each slide is a full-resolution image of the web slide, so edit the web version for content changes.
- **Locally:** `python3 -m http.server 8000` in this folder, then open http://localhost:8000 (or `/alt/`).

Keys while presenting: `→` / `←` move, `F` full screen, `S` opens the speaker view (notes and a timer), `Esc` shows all slides.

## What is in this folder

| Path | What it is |
|---|---|
| `index.html`, `assets/theme.css`, `assets/final.css` | NC State deck (reveal.js), speaker notes on every slide |
| `alt/index.html`, `alt/alt.css` | Alternative-design deck, same content and notes |
| `SCRIPT.md` | All speaker notes as one script |
| `downloads/` | PDF (`decktape reveal --size 1280x720`) and PPTX exports of both decks |
| `analysis/` | `gen_compare.py` and its saved output (RTX 2080 SUPER vs RTX 5060 Ti comparison) |
| `vendor/reveal/` | reveal.js 5.1.0 (MIT licence), so the slides work offline |

## Where the numbers come from

Every number on the slides comes from our measurement runs on NCSU ARC (RTX 5060 Ti GPU, AMD EPYC 9115 CPU).
The "Nov run" (118 matrices, final kernels) is the main data set; the "Oct run" is used where a slide says so.
The full analysis is in the `gespmm-retuned` repository (`results/analysis_nov2026/SUMMARY.md`).
