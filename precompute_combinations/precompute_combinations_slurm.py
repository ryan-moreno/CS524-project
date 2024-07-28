import math
import time
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Retrieving range for n (inclusive).")
parser.add_argument("n_start", type=int, help="n_start")
parser.add_argument("n_end", type=int, help="n_end")

args = parser.parse_args()

comb_df = pd.DataFrame(columns=["n", "k", "n_choose_k"])

for seconds_remaining in range(args.n_start, args.n_end + 1):
    if (seconds_remaining % 60) == 0:
        print(f"... {seconds_remaining}/{args.n_end}")
    for goals_scored in range(0, seconds_remaining + 1):
        # If we have already computed this value using (n choose k) = (n choose (n-k)) trick then skip
        if not comb_df.loc[
            (comb_df["n"] == seconds_remaining) & (comb_df["k"] == goals_scored)
        ].empty:
            continue

        # Compute n choose k
        n_choose_k = math.comb(seconds_remaining, goals_scored)
        comb_df = pd.concat(
            [
                comb_df,
                pd.DataFrame(
                    {
                        "n": seconds_remaining,
                        "k": goals_scored,
                        "n_choose_k": n_choose_k,
                    },
                    index=[0],
                ),
            ],
            ignore_index=True,
        )

        # (n choose k) = (n choose (n-k)) so we can skip half the computations
        goals_unscored = (
            seconds_remaining - goals_scored
        )  # Number of seconds for which a goal was not scored
        comb_df = pd.concat(
            [
                comb_df,
                pd.DataFrame(
                    {
                        "n": seconds_remaining,
                        "k": goals_unscored,
                        "n_choose_k": n_choose_k,
                    },
                    index=[0],
                ),
            ],
            ignore_index=True,
        )

# Save the precomputed combinations df
comb_path = f"partial_dfs/df_{args.n_start}-{args.n_end}.pkl"
comb_df.to_pickle(comb_path)
