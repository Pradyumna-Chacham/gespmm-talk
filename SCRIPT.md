# Speaker script (3:54)

Speaking rate about 150 words per minute. 586 words in total, about 3:54. Timestamps are cumulative. The same lines are in each slide's speaker notes (press S). Caveats are spoken before the numbers they qualify.

## Slide 1: Title: GE-SpMM Retuned

[0:00–0:06] (15 words) We re-tested a 2020 GPU kernel on a 2025 GPU and built its CPU twin.

## Slide 2: SpMM in one picture

[0:06–0:17] (28 words) A is the graph, mostly zeros. B is dense, N features per node. Each node sums its neighbours' feature rows: the core of a graph neural network layer.

## Slide 3: Roofline: why it's limited by memory

[0:17–0:30] (31 words) The CPU ceilings are our own measurement. Both chips wait on memory: the GPU uses under 3% of its math, the CPU under 10%. Speedups mean fewer bytes or busier workers.

## Slide 4: The two ways time gets wasted

[0:30–0:38] (21 words) Two ways time is wasted: redundant reads, and uneven rows that leave workers idle. Homeworks one and two showed the second.

## Slide 5: GE-SpMM (SC 2020), the paper we re-tested

[0:38–0:48] (26 words) GE-SpMM, SC 2020, claimed to beat cuSPARSE. Two tricks: share 32 nonzeros through on-chip memory, and give each thread two columns so sparse values are reused.

## Slide 6: Our project: two tracks

[0:48–0:58] (23 words) Two tracks. GPU: re-test the paper on an RTX 5060 Ti, then improve it. CPU: an OpenMP version as baseline. Same 118 matrices.

## Slide 7: Re-testing the paper: its code lost, and the compiler was the reason

[0:58–1:16] (45 words) Caveat: older GPUs compile this fine, and we haven't traced why this compiler differs. On the new GPU the published kernel is 0.94 times cuSPARSE: the loop wasn't unrolled, so loads wait. Three source lines fix it, same answers; same settings, our code: 1.14 times.

## Slide 8: Fixed settings stop being best, so tune per graph

[1:16–1:26] (25 words) Fixed settings stop being best, so we tune per graph. Trying every setting beats the paper's by 1.81 times. Row caching helps less; cause unknown.

## Slide 9: Uneven rows: merge path

[1:26–1:44] (46 words) Caveat: splitting costs speed on even graphs and fades at large widths, so we use it only on uneven ones. Give each warp equal nonzeros, not equal rows; answers stay bit-identical. wiki-Talk at width 128: 14.8 down to 8.5 milliseconds. As in homeworks one and two.

## Slide 10: The heuristic: choosing settings for unseen graphs

[1:44–2:02] (44 words) A decision tree memorized its training graphs and lost to the paper's setting. kNN copies similar graphs: fine for fine settings, but can't choose merge path. Our rule: rows uneven past a fitted threshold means merge path. Auto uses kNN for the fine settings.

## Slide 11: Did it generalize? 27 graphs it never saw

[2:02–2:11] (24 words) Caveat: scores are fractions of the best setting per graph, on 27 unseen graphs; 1% is noise. Auto 0.873, rulebook 0.849, best cuSPARSE 0.768.

## Slide 12: GPU results: two honest numbers

[2:11–2:28] (43 words) It depends on whether we may try every setting per graph. If so, 1.3 to 1.6 times the best cuSPARSE depending on width, an upper bound. Choosing automatically on unseen graphs, 1.14 times. Kernel time, one GPU; cuSPARSE still wins some small-width graphs.

## Slide 13: Newer GPU: what made the same code 1.66x faster?

[2:28–2:43] (36 words) Caveat: its clock is 1.44 times higher; we couldn't separate clock from cache. 1.66 times faster; biggest jump, 2.26 times, where data fits only the new cache. cuSPARSE sped up equally, so our lead isn't hardware.

## Slide 14: How a CPU runs SpMM, next to the GPU

[2:43–2:54] (28 words) On the CPU, a core replaces a warp, with 16-float vector instructions. Each core owns whole output rows, so no locks. OpenMP picks the schedule at run time.

## Slide 15: The CPU design: the same two problems, CPU-style fixes

[2:54–3:06] (31 words) Uneven rows: dynamic schedule, so idle cores grab the next rows. Latency: four accumulators overlap adds. Packing short rows gains 12 to 16 percent; cache blocking lost. AVX2 equals AVX-512: memory-bound.

## Slide 16: CPU roofline

[3:06–3:20] (35 words) Caveat: ceilings are our own measurement, and the extra traffic is inferred from timings, as cache-miss counters weren't available. Past width 64, big graphs stall: rows of B are re-read, about four times the minimum.

## Slide 17: CPU results

[3:20–3:35] (36 words) 16 cores give 6.7 times; one core already uses 38% of bandwidth. Our best variant beats MKL from width 32; MKL wins at 16. The GPU is 1.9 to 4.8 times faster, on a different chip.

## Slide 18: Takeaways

[3:35–3:51] (41 words) An old paper's rerun tests the compiler; we haven't traced why it chose differently. Fixed settings don't carry across hardware. Uneven rows hit us three times; one rule decides when to split. Both machines are limited by data movement, not math.

## Slide 19: Next, what we skipped, questions

[3:51–3:54] (8 words) Next, finish the experiments, close MKL's lead. Questions?

## Backup B1: Terms

Not spoken.
