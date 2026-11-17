# GE-SpMM Retuned: project talk

Slides for our CSC 548 (Parallel Systems, NC State, Fall 2026) final-project talk.
Pradyumna Chacham and Dilip Kumar.

The talk is 4 minutes plus 30 seconds of questions, so it covers the setup, two findings and the
results. Everything else is in the final report and the explainer page.

## View the slides

- **Online:** https://pradyumna-chacham.github.io/gespmm-talk/
- **PDF:** [`slides.pdf`](slides.pdf) (same slides, one page each)
- **Locally:** `python3 -m http.server 8000` in this folder, then open http://localhost:8000

Keys while presenting: `→` / `←` move, `F` full screen, `S` opens the speaker view
(notes and a timer), `Esc` shows all slides.

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The slides (reveal.js), with speaker notes on each slide |
| `SCRIPT.md` | The speaker notes as one script, with timings |
| `slides.pdf` | PDF export of the slides (made with `decktape reveal --size 1280x720`) |
| `assets/theme.css` | The look: red NC State bar, Inter font, red-underlined titles, as in the CSC 548 lectures |
| `assets/img/` | Two figures from our analysis: warp timelines on wiki-Talk, and the roofline |
| `vendor/reveal/` | reveal.js 5.1.0 (MIT licence), kept here so the slides work offline |

## Where the numbers come from

Every number on the slides comes from our measurement runs on NCSU ARC
(RTX 5060 Ti GPU, AMD EPYC 9115 CPU). The November 2026 run covers 118 matrices; two numbers on the
"Finding 1" slide come from the October run, and the slide says so. The project code and the full
analysis are in the `gespmm-retuned` repository (`results/analysis_nov2026/SUMMARY.md`).

## Slide outline

1. Title
2. The problem from first principles: sparse matrices, CSR, SpMV vs SpMM, why GNNs need SpMM
3. Four lessons carried over from HW1–HW3 and the midterm
4. The paper (GE-SpMM, SC 2020), its two tricks, and our setup
5. Finding 1: the paper's fixed settings no longer win on a 2025 GPU
6. Finding 2: uneven graphs need work split by nonzeros (merge path), as in HW2
7. Results
8. Roofline: why SpMM is still limited by memory
9. Takeaways, and what the talk leaves out
10. Backup: the hypotheses we tested
11. Backup: terms used in the talk
