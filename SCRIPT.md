# Script (v6, 13 slides, 4:00)

[0:00–0:08] We re-tested a 2020 GPU kernel on today's GPUs, and built its CPU twin. Dilip Kumar covers the GPU track, Pradyumna Chacham the CPU track.

[0:08–0:25] SpMM multiplies a sparse matrix by a dense one. It is 30 to 40 percent of graph network training time, per the paper and our proposal, and it is memory-bound: under 3 percent of GPU arithmetic gets used. Our goals: reproduce the paper, find what newer GPUs change, and tune it, on GPU and CPU.

[0:25–0:45] From the homeworks: CSR format, and y equals A times x. SpMM is N SpMVs that share the same A. In a graph neural network layer, each node aggregates its neighbours' feature vectors; that is an SpMM.

[0:45–1:00] The same kernel appears in recommendation, sparse solvers, and pruned networks. As an illustration: if SpMM is 35 percent of a training step, doubling its speed makes the step about 1.2 times faster.

[1:00–1:15] GE-SpMM, Huang and colleagues, Supercomputing 2020, works on CSR directly. On a GTX 1080 Ti and an RTX 2080 it beat cuSPARSE's older csrmm2 routine by 1.37 to 1.43 times, using two tricks.

[1:15–1:30] CRC: a warp loads a chunk of the sparse row once, in one coalesced read, and all its threads share it. That is tiling, from the midterm.

[1:30–1:45] CWM: one warp computes several column groups, so each loaded nonzero is used several times. That is register blocking. The paper fixes the coarsening factor at 2.

[1:45–2:10] We reproduced the kernel, fixed a compiler problem, tested five GPU generations, and built the same algorithm on a 16-core CPU. Tuning per graph beats the paper's fixed settings by 1.81 times. Our main addition is merge path: one huge row keeps a warp busy while the GPU waits. It loses on even graphs, so we use it only on uneven rows, where it gains 1.72 times at N = 16.

[2:10–2:35] At run time we must choose from the graph alone. A decision tree overfit. kNN handles fine settings but cannot choose merge path. So a fitted skew rule picks the strategy, and kNN the fine settings. Scores are fractions of the best setting, on 27 unseen graphs; about 1 percent is noise. Auto scores 0.873, best cuSPARSE 0.768.

[2:35–3:05] On Blackwell, the published kernel reached 0.94 times cuSPARSE; our 3-line fix, same settings, 1.14 times. The same code ran 1.66 times faster than on the 2080 SUPER, but cuSPARSE sped up 1.61 times, so our lead is not from the hardware. The 1.3 to 1.6 times headline is an upper bound with every setting tried; automatic choice gives 1.14 times. A GCN epoch is 2.06 times faster than torch.sparse.

[3:05–3:40] We tested each explanation. Did the bigger L2 shrink CRC's benefit? The 4060 Ti has the same L2 and CRC still gains 22 percent, against 8 on the 5060 Ti: L2 size alone does not explain it. Did CRC's overhead win? No, it was the compiler: 8 loads against 68. Does coarsening cost cache? DRAM traffic rises from 158 to 847 megabytes. Does skew hurt GPUs more? Yes: 31 percent kept, against 82 on the CPU.

[3:40–3:55] Still hypotheses: the generation gain is mostly cache, and coarsening would pay again if B's slice stayed in L2. Next: lock both GPUs to one clock, try larger coarsening with an L2-sized tile, close the MKL gap at N = 16, and release code by December 7.

[3:55–4:00] Thank you. Questions?

