# CS524-project

Overleaf links:

- [Project proposal](https://www.overleaf.com/project/668f10d26a7e45ffca7ef942)
- [Progress report](https://www.overleaf.com/project/669e7eccbb1e44065a578440)

## Computing goal scoring probabilities

TODO: Laura can link files here

## Precomputing combinations

To speed up our model, we have precomputed all combinations `n choose k` for $n \in [0, \ldots 1200]$ and $k \leq n$. This was launched on the SSCC servers via slurm.

See `precompute_combinations/` folder for details.

## Optimization

We implemented the model by using brute force to check the probability of success for all possible values of $s$. This can be launched on the SSCC servers via slurm.

See `optimization/` folder for details.
