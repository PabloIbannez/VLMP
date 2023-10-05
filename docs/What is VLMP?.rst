What is VLMP?
=============

VLMP, or *Virtual Laboratory Massively Parallelized*, is designed to simplify the process of setting
up and running parallel simulations. Distributed as a Python library, VLMP provides a 
comprehensive toolkit that spans a range of models, with a particular focus on molecular 
dynamics and including continuous models like fluids.

The core advantage of VLMP lies in its multi-level parallelization. At the first level, individual
simulations are parallelized. At the second, multiple simulations can run concurrently on a single
GPU. The framework also allows for easy distribution of simulations across multiple GPUs. This
massive parallelization is made possible through VLMP's backend technology, UAMMD-structured, a
GPU-centric code.

While both UAMMD-structured and VLMP are general-purpose, VLMP has been particularly optimized for
coarse-grained models. These models often underutilize a GPU's computational power due to their
small size. However, UAMMD-structured solves this inefficiency by employing a batching technique,
enabling multiple small-scale simulations to run effectively on a single GPU.

VLMP is not just powerful but also adaptable. You can think of each simulation as a puzzle to which
you can add or remove pieces with minimal effort. Whether you're studying interactions between
proteins and DNA, or any other scientific phenomena, you can easily select, adapt, and combine
various models and components. This adaptability extends to the ease of sharing new scientific
models with the community, as researchers can distribute their models as VLMP modules.

Imagine running multiple simulations with differing particle counts, all batched together to fully
utilize the computational capabilities of one or more GPUs. VLMP can manage this complexity,
distributing simulations as needed and storing results separately for each run.
