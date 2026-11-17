# Speaker script (about 3:50)

Read at a calm pace; timestamps are cumulative. The script covers plan slides 2, 4, 7, 8, 9, 10, 13, 15, 16, 19 and 23 and clicks past the rest, which stay in the deck and the PDF as reference. Slides that were split into two or three parts share one script block: speak it over the first part and click through the others.
Every sentence is built only from the content of its slide. The same text is in each slide's speaker notes (press S).

- Slide 1 (plan slide 1): GE-SpMM Retuned: click past (reference)

## Slide 2–3 (plan slide 2): The problem: multiply a sparse matrix by a dense matrix (SpMM)

[0:00–0:20] SpMM multiplies a sparse matrix, which is mostly zeros, by a dense matrix with N columns. We store only the nonzeros, in the Compressed Sparse Row format from our homeworks. It matters because one layer of a graph neural network is exactly this: each node sums its neighbours' feature vectors.

- Slide 4 (plan slide 3): What makes it hard: irregular reads and uneven rows: click past (reference)

## Slide 5–6 (plan slide 4): Roofline: why SpMM is limited by memory, not arithmetic

[0:20–0:42] Each nonzero and each output column costs two flops and one 4-byte float of B, so 0.5 flops per byte; we measured a median of 1.22. The GPU needs about 54 flops per byte before arithmetic is the limit, so SpMM is memory-bound, and our best run reaches 94 percent of peak bandwidth. So every optimization here moves fewer bytes, or keeps more of the GPU busy.

- Slide 7 (plan slide 5): The paper's starting kernel: one warp per row: click past (reference)

- Slide 8–9 (plan slide 6): The paper's two tricks, and its claim: click past (reference)

## Slide 10–11 (plan slide 7): Our project: two tracks (from the proposal), one shared sweep

[0:42–1:02] The project has two tracks from the proposal. On the GPU I reproduce GE-SpMM, compare against every algorithm in the current cuSPARSE, and tune per matrix. On the CPU, Dilip wrote an OpenMP version with the same ideas, benchmarked against Intel MKL. Both share one matrix generator and 118 matrices, and every run is checked, with zero wrong results.

## Slide 12 (plan slide 8): Reproduction: the paper's published kernel no longer wins on a 2025 GPU

[1:02–1:20] First, reproduction. The authors' code, unchanged, is 0.95 times as fast as the best cuSPARSE at N = 512 on our 5060 Ti; the paper reported 1.37 to 1.43. On four older GPUs the same binary still wins, from 1.09 to 1.26. The puzzle: our own implementation of the same algorithm is up to 2 times faster, but only on the 5060 Ti.

## Slide 13–14 (plan slide 9): Why the paper's kernel lost on Blackwell: the compiler, not the hardware

[1:20–1:50] The counters show the same memory traffic, hit rates and occupancy, but each instruction waits 22 to 26 cycles for a memory load instead of 11 to 15. The cause is in the machine code. For older GPUs the compiler unrolls the authors' loop; for Blackwell it leaves it rolled, so each warp has one load in flight and every nonzero pays a full memory latency. Ours is unrolled, with 8 loads in flight. Skewed graphs suffer most: at N = 16, wiki-Talk and com-Youtube are 4.2 times slower.

## Slide 15–16 (plan slide 10): Three source lines account for the whole gap

[1:50–2:15] Three source lines account for the whole gap: a loop with two exit conditions, a last-block test, and a branch around every nonzero. Fixing the loop alone takes CF 1 to 0.95 at N = 512, and the paper's CF 2 in our code reaches 1.14 times over cuSPARSE. On the 4060 Ti the same fix changes nothing, which shows it is the compiler. Check the machine code before blaming the hardware.

- Slide 17–18 (plan slide 11): What the new hardware did change: CRC helps less, and coarsening hits the L2: click past (reference)

- Slide 19 (plan slide 12): Our method 1: re-implement, then tune per matrix: click past (reference)

## Slide 20–22 (plan slide 13): Our method 2: the longest-row problem, from CSR to COO to merge path

[2:15–2:40] The same problem keeps coming back: CSR makes a row the unit of work, so whoever gets the long row finishes last. It was in HW1, in HW2 and on the GPU, where wiki-Talk spends 85 percent of 14.8 milliseconds in a tail. COO cuts nonzeros evenly but stores a row index for each. Merge path makes that cut on CSR's own storage and is bit-identical every run: wiki-Talk drops to 8.5 milliseconds, and uneven matrices gain 1.72 times at N = 16.

- Slide 23 (plan slide 14): Our method 3: pick the settings for a new graph automatically: click past (reference)

## Slide 24 (plan slide 15): GPU results: faster than NVIDIA's library at every width

[2:40–3:00] Result: tuned, we beat the best cuSPARSE at every width, from 1.51 times at N = 16 to 1.58 at N = 512, and at 512 we are faster on 110 of 115 matrices. Row split alone gives 1.13 at 16 and 1.53 at 512. So load balancing carries the small-N gain, and tuning carries the large-N gain.

## Slide 25–26 (plan slide 16): Same code, newer GPU: 1.66× faster. What caused it?

[3:00–3:25] The same code is 1.66 times faster on the 5060 Ti than on the 2080 SUPER, although the 5060 Ti has 10 percent less DRAM bandwidth. The main cause is the 8 times larger L2 cache: when B fits in 32 megabytes but not in 4, the speedup is 2.26 times. cuSPARSE shows the same pattern, so it comes from the hardware. For a memory-bound kernel, a bigger cache can beat more bandwidth.

- Slide 27–28 (plan slide 17): Did the newer hardware give us our gain over cuSPARSE and the paper?: click past (reference)

- Slide 29–30 (plan slide 18): CPU track: the OpenMP design and what each piece bought: click past (reference)

## Slide 31 (plan slide 19): CPU results: scaling, vs MKL, and vs the GPU

[3:25–3:40] On the CPU, 16 threads give 6.7 times geomean. At N = 512, MKL reaches 0.77 of our speed, though at N = 16 MKL is still 1.10 times faster. The GPU is 1.9 times faster than our best CPU code at N = 16, rising to 4.8 times at N = 512, so the CPU is closest at small N, as H4 predicted.

- Slide 32 (plan slide 20): Skew: does it hurt the GPU more than the CPU? (H3): click past (reference)

- Slide 33 (plan slide 21): End to end in PyTorch: click past (reference)

- Slide 34 (plan slide 22): What our hypotheses said: click past (reference)

## Slide 35 (plan slide 23): Before December 7 (proposed: you decide which stay)

[3:40–3:50] Before December 7: a CPU roofline, re-running the skipped experiments with the final kernels, finishing the code-generation study, closing the gap to MKL at N = 16, one large real graph end to end, and the final report and code release.

- Slide 36 (plan slide 24): Takeaways: click past (reference)

- Slide 37 (backup B1): Terms (every short form): click past (reference)

- Slide 38 (backup B2): Paper vs ours: same algorithm, every fixed choice turned into a measured one: click past (reference)

Total spoken time: 3:50.
