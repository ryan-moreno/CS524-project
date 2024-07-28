# CS524-project

Overleaf links:

- [Project proposal](https://www.overleaf.com/project/668f10d26a7e45ffca7ef942)
- [Progress report](https://www.overleaf.com/project/669e7eccbb1e44065a578440)

## Computing goal scoring probabilities

To compute the probability that the opponent scores during a given second in 5v5 play $p_{b1}$ and $p_{a1}$ we utilized datasets within our `data_condensed` folder, specifically subfolders `goals_against_by_strength` and `goals_for_by_strength`. We had also explored generating probabilities with period specific data but then did not have censored time ranges which led to higher probabilities than would be appropriate, that data is in the `goals_by_period` subfolder.

Results were printed in the `data_exploration.ipynb` notebook

To compute $p_{b2}$: probability that the opponent scores during a given second in 6v5 play, and $p_{a2}$ : probability that we score during a given second in 6v5 play, we first parsed through the csvs in our `data_condensed/csv` in the `data_exploration.ipynb` notebook in order to save off precomputed counts of seconds (and true/false) info needed for the Kaplan-Meier estimator for survival. This data was saved to `precomputed_data_for_survival_model` and then processed in `data_explore.py` which is a script that generated plots and printed the probabilities for $p_{a2}$ & $p_{b2}$

## Precomputing combinations

To speed up our model, we have precomputed all combinations `n choose k` for $n \in [0, \ldots 1200]$ and $k \leq n$. This was launched on the SSCC servers via slurm.

See `precompute_combinations/` folder for details.

## Optimization

We implemented the model by using brute force to check the probability of success for all possible values of $s$. This can be launched on the SSCC servers via slurm.

See `optimization/` folder for details.
