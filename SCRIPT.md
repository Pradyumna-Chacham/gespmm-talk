# Speaker script (about 3:50)
Read at a calm pace; the timings in brackets are cumulative. Slides 10–11 are backup for questions.

## 1. GE-SpMM Retuned

[0:00 to 0:10] Hi, we are Pradyumna and Dilip. We took a GPU kernel from a 2020 paper, rebuilt it, tested it on a 2025 GPU, and then made it faster. The project is much bigger than four minutes, so I will show the setup, two findings and the results. The rest is in the report.

## 2. Multiply a sparse matrix by a dense matrix

[0:10 to 0:35] All semester we did SpMV: a sparse matrix times one vector. SpMM is the same, but the vector becomes a dense matrix B with N columns. This is the main step of a graph neural network: every node adds up its neighbours' feature vectors. A is the graph, B holds the features. The hard part is that which rows of B we read depends on the graph, so memory access is irregular.

## 3. Four lessons from the homeworks, used again here

[0:35 to 1:00] Four things from the homeworks carry straight over. From HW3, one warp per row: a warp is 32 GPU threads that move together, and that is exactly how the paper's kernel starts. From HW2, balancing nonzeros instead of rows, which becomes our merge-path kernel. From the roofline in HW1 to HW3: SpMV is limited by memory, and so is SpMM. And from the midterm, tiling: keep reused data in fast memory, which is the paper's first trick.

## 4. GE-SpMM (Huang et al., SC 2020): two tricks on top of CSR

[1:00 to 1:25] The paper adds two tricks to the one-warp-per-row kernel. Trick one, row caching: instead of 32 threads reading the same nonzero, the warp reads 32 of them in one combined read and shares them. Trick two, warp merging: one warp does two groups of columns, so the sparse row is read once and used twice. We rebuilt both on a 2025 GPU and tested 118 matrices at six widths, about 78 thousand checked runs. The question: the new GPU has about ten times the cache. Do the tricks still help?

## 5. On a 2025 GPU, the paper’s fixed settings no longer win

[1:25 to 1:55] First finding: the paper's kernel with its fixed settings is now slightly slower than NVIDIA's library, 0.95 times, where the paper reported about 1.4 times faster. Profiling shows why: row caching cuts bytes read by a quarter but adds 62 percent more instructions, and the large cache already does that job. The best coarsening factor is usually 1, not the paper's 2. So we tune the settings for each matrix, which gives 1.8 times over the fixed settings.

## 6. Uneven graphs need work split by nonzeros, not by rows

[1:55 to 2:30] Second finding, and this one comes straight from HW2. Real graphs have a few giant rows. With one warp per row, everyone waits for the warp that got the giant row. On the left, one row of 100 thousand nonzeros keeps the kernel running to 14.8 milliseconds while most of the GPU is idle. Merge path cuts the work into equal pieces of rows plus nonzeros, like the nonzero split in HW2. On the right everything finishes together at 8.5 milliseconds, and we add the split rows in a fixed order so the answer is the same every run.

## 7. Faster than NVIDIA’s library on almost every matrix

[2:30 to 3:05] Results over 118 matrices. Against the best cuSPARSE method we are 1.58 times faster at width 512 and win on 110 of 115 matrices; 1.5 times at width 16. A simple, explainable rule picks the settings for a new graph and still beats cuSPARSE on matrices it never saw. The GPU is 4.8 times faster than our best CPU code, and that CPU code itself beats Intel MKL. Inside PyTorch, training a small graph network is about two times faster.

## 8. Why the gains are modest: SpMM is still limited by memory

[3:05 to 3:30] Why not ten times faster? The roofline. Arithmetic intensity is math per byte read. SpMV was 0.17; SpMM is about 1.2. The GPU needs about 50 operations per byte before math becomes the limit, so we are firmly limited by memory, and our best runs reach 94 percent of peak memory speed. Same lesson as the homeworks: all our gains came from moving fewer bytes or keeping the GPU busy.

## 9. Three takeaways

[3:30 to 3:50] Three takeaways. Re-running a paper is not reproducing it: the 2020 settings lose on new hardware, and tuning brings back the lead. Load balance matters on the GPU just as it did in HW2. And SpMM is limited by memory, so the work is about bytes, not math. Much more is in the report and the explainer page. Thank you.

## 10. The hypotheses we tested

Backup for Q and A. We wrote eight hypotheses before the big runs. Four were not supported, which is a result in itself: for example, the best coarsening factor does not depend on skew, it is simply 1 at most widths.

## 11. Terms used in this talk

Backup: definitions of every short form used in the talk.
