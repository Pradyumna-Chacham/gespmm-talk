# GE-SpMM Retuned: project talk

Slides for our CSC 548 (Parallel Systems, NC State, Fall 2026) final-project talk.
Dilip Kumar (GPU track) and Pradyumna Chacham (CPU track).

The talk is 4 minutes plus 30 seconds of questions. The deck has 19 slides plus 1 backup slide (Terms), one picture per slide
(PDF: 20 pages). The script in `SCRIPT.md` is about 3:54 at 150 words per minute. Structure: A the problem (slides 1-4),
B the paper and our project (5-6), C GPU track (7-13), D CPU track (14-17), E close (18-19). Every number on a slide comes
from a claim table checked against the data, and each caveat sits in an amber "Read this first" box above its number.

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
| `SCRIPT.md` | The speaker notes as one script, with cumulative timings |
| `slides.pdf` | PDF export of the slides (made with `decktape reveal --size 1280x720`) |
| `assets/theme.css` | The look: red NC State bar, Inter font, red-underlined titles, as in the CSC 548 lectures; also the styles for the reused explainer diagrams (`svg.d`) |
| `assets/img/` | Figures from our analysis: roofline, wiki-Talk warp timelines, the code-generation figures (`codegen_*.png`), CPU scaling (F9), GPU vs CPU (F8) and the skew study (F33) |
| `analysis/gen_compare.py` | Script that computes the RTX 2080 SUPER vs RTX 5060 Ti comparison ; its saved output is `analysis/gen_compare_output.txt` |
| `vendor/reveal/` | reveal.js 5.1.0 (MIT licence), kept here so the slides work offline |

## Where the numbers come from

Every number on the slides comes from our measurement runs on NCSU ARC (RTX 5060 Ti GPU, AMD EPYC 9115 CPU).
The "Nov run" (118 matrices, final kernels) is the main data set; the "Oct run" (106 matrices, before load
balancing) is used where a slide says so. The full analysis is in the `gespmm-retuned` repository
(`results/analysis_nov2026/SUMMARY.md`). Table and figure numbers on the slides (T1, F11, ...) refer to it;
D-xxx numbers refer to our decision log. The RTX 2080 SUPER comparison is computed by
`analysis/gen_compare.py` from the raw runs listed in its header.

## Slide outline

**Part A: The problem**
1. Title (slide 1)
2. The problem: multiply a sparse matrix by a dense matrix (SpMM) (slides 2–3)
3. What makes it hard: irregular reads and uneven rows (slide 4)
4. Roofline: why SpMM is limited by memory, not arithmetic (slides 5–6)

**Part B: The existing method (GE-SpMM, SC 2020)**

5. The paper's starting kernel: one warp per row (slide 7)
6. The paper's two tricks, and its claim (slides 8–9)

**Part C: Our project and setup**

7. Our project: two tracks, one shared sweep (slides 10–11)

**Part D: GPU track**

8. Reproduction: the published kernel no longer wins on a 2025 GPU (slide 12)
9. Why it lost on Blackwell: the compiler, not the hardware (slides 13–14)
10. Three source lines account for the whole gap (slides 15–16)
11. What the new hardware did change: CRC helps less, coarsening hits the L2 (slides 17–18)
12. Our method 1: re-implement, then tune per matrix (slide 19)
13. Our method 2: the longest-row problem, from CSR to COO to merge path (slides 20–22)
14. Our method 3: pick the settings for a new graph automatically (slide 23)
15. GPU results: faster than NVIDIA's library at every width (slide 24)
16. Same code, newer GPU: 1.66× faster. What caused it? 
17. Did the newer hardware give us our gain? (slides 27–28)

**Part E: CPU track**

18. The OpenMP design and what each piece bought (slides 29–30)
19. CPU results: scaling, vs MKL, and vs the GPU (slide 31)

**Part F: Both tracks together**

20. Skew: does it hurt the GPU more than the CPU? (H3) (slide 32)
21. End to end in PyTorch (slide 33)
22. What our hypotheses said (slide 34)

**Part G: Next**

23. Before December 7 (slide 35)
24. Takeaways (slide 36)

**Backup**

- B1. Terms (every short form) (slide 37)
- B2. Paper vs ours, full table (slide 38)
