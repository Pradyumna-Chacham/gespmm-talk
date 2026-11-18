# GE-SpMM Retuned: project talk

Slides for our CSC 548 (Parallel Systems, NC State, Fall 2026) final-project talk.
Dilip Kumar (GPU track) and Pradyumna Chacham (CPU track).

The talk is 4 minutes plus 30 seconds of questions. The current deck (v6) has 13 slides plus 1 backup slide (Terms)
(PDF: 14 pages). The script in `SCRIPT.md` is about 3:50 at 150 words per minute. Flow: the problem (slides 2-4), the paper
(5-7), our work (8-9), results (10), insights (11), hypotheses and future work (12), thanks (13). Every number on a slide comes
from a claim table checked against the data, and each caveat sits in an amber "Read this first" box above its number.

## View the slides

- **Online (current, v6, 13 slides):** https://pradyumna-chacham.github.io/gespmm-talk/
- **Earlier version, v5 (20 pages):** https://pradyumna-chacham.github.io/gespmm-talk/v5/ (PDF: `v5/slides.pdf`)
- **Earlier version, v4 (38 slides):** https://pradyumna-chacham.github.io/gespmm-talk/v4/ (PDF: `v4/slides.pdf`)
- **PDF:** [`slides.pdf`](slides.pdf) (current deck, one page per slide)
- **Locally:** `python3 -m http.server 8000` in this folder, then open http://localhost:8000

Keys while presenting: `→` / `←` move, `F` full screen, `S` opens the speaker view
(notes and a timer), `Esc` shows all slides.

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The slides (reveal.js), with speaker notes on each slide |
| `SCRIPT.md` | The speaker notes as one script, with cumulative timings |
| `slides.pdf` | PDF export of the slides (made with `decktape reveal --size 1280x720`) |
| `assets/theme.css` | The look: red NC State bar, Inter font, red-underlined titles, as in the CSC 548 lectures; also the styles for the reused explainer diagrams (`svg.d`) |
| `assets/img/` | Figures from our analysis (roofline, wiki-Talk warp timelines, code-generation, CPU scaling, GPU vs CPU, skew study); the v6 deck uses `f24b_wikitalk.png`, the others are kept for the earlier versions |
| `analysis/gen_compare.py` | Script that computes the RTX 2080 SUPER vs RTX 5060 Ti comparison; its saved output is `analysis/gen_compare_output.txt` |
| `v4/`, `v5/` | Frozen copies of the earlier 38-slide and 20-page decks (each with its own script, assets and PDF) |
| `vendor/reveal/` | reveal.js 5.1.0 (MIT licence), kept here so the slides work offline |

## Where the numbers come from

Every number on the slides comes from our measurement runs on NCSU ARC (RTX 5060 Ti GPU, AMD EPYC 9115 CPU).
The "Nov run" (118 matrices, final kernels) is the main data set; the "Oct run" (106 matrices, before load
balancing) is used where a slide says so. The full analysis is in the `gespmm-retuned` repository
(`results/analysis_nov2026/SUMMARY.md`). Table and figure numbers on the slides (T1, F11, ...) refer to it;
D-xxx numbers refer to our decision log. The RTX 2080 SUPER comparison is computed by
`analysis/gen_compare.py` from the raw runs listed in its header.


## Where the numbers come from

Every number on the slides comes from our measurement runs on NCSU ARC (RTX 5060 Ti GPU, AMD EPYC 9115 CPU).
The "Nov run" (118 matrices, final kernels) is the main data set; the "Oct run" (106 matrices, before load
balancing) is used where a slide says so. The full analysis is in the `gespmm-retuned` repository
(`results/analysis_nov2026/SUMMARY.md`). Table and figure numbers on the slides (T1, F11, ...) refer to it;
D-xxx numbers refer to our decision log. The RTX 2080 SUPER comparison is computed by
`analysis/gen_compare.py` from the raw runs listed in its header.

## Slide outline (v6)

1. Title
2. Problem and objectives: SpMM is a core step of graph learning and leaves the hardware mostly idle
3. SpMM and CSR: N SpMVs that share the same sparse matrix
4. Applications and impact (with an Amdahl illustration)
5. The paper: GE-SpMM (SC 2020), its aim, claim and two tricks
6. CRC: read the sparse row once, share it through shared memory
7. CWM: one warp does more columns, so each nonzero is reused
8. Our work (1/2): reproduce, fix, extend to CPU; merge path for uneven rows
9. Our work (2/2): rule plus kNN picks the strategy for unseen graphs, held-out scores
10. Results: new hardware and compiler, and what our optimizations added
11. Insights: four explanations, each tested (experiment, meaning, result, verdict)
12. Hypotheses and future work
13. Thank you and questions

**Backup (unnumbered)**

- Terms used in the talk
