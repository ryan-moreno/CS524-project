#!/usr/bin/env python
# coding: utf-8

# To run via slurm, first output the ipynb notebook to python using `jupyter nbconvert --to script brute_force_model.ipynb`

# In[27]:


import time
import pandas as pd
import matplotlib.pyplot as plt


# ## Load precomputed combinations to save computation time

# In[32]:


comb_df = pd.read_pickle("../precompute_combinations/precomputed_combinations_df.pkl")


def choose(n, k):
    index = n * 1201 + k
    return comb_df.at[index, "n_choose_k"]


# ## Probabilities based on our data analysis

# In[29]:


# Approximate probability of a goal in a given second
seconds_in_game = 20 * 60 * 3

# Probability of a goal in a given second during 5v5
p_a1 = 5.18 * 10**-4
p_b1 = p_a1

# Probability of the other team scoring during 6v5 increases
p_b2 = 7.85 * 10**-4

# Probability of our team scoring during 6v5 also increases, though not as much
p_a2 = 7.22 * 10**-4


# ## Inputs to model

# In[30]:


# Let's say the current score is 1 - 3
a_0 = 1
b_0 = 3

# 5 minutes left in the game
T = 5 * 60


# ## Brute force every choice of $s$
#
# Launching via slurm on SSCC clusters to speed up

# In[ ]:


decisions_df = pd.DataFrame(columns=["pull_time", "prob_success", "compute_time"])

results = []

#  Try out each possible time to pull the goalie
for s in range(1, T):

    # Timing for performance metrics
    start_time = time.time()

    prob_success = 0

    # Tracking num_arrangements for complexity considerations
    num_arrangements = 0

    # Number of goals scored by other team before pulling the goalie
    for g_b1 in range(0, s):
        prob_gb1 = choose(s, g_b1) * (p_b1**g_b1) * ((1 - p_b1) ** (s - g_b1))

        # Number of goals scored by our team before pulling the goalie
        for g_a1 in range(0, s):
            prob_ga1 = choose(s, g_a1) * (p_a1**g_a1) * ((1 - p_a1) ** (s - g_a1))

            # Number of goals scored by other team after pulling the goalie
            for g_b2 in range(0, T - s):
                prob_gb2 = (
                    choose(T - s, g_b2) * (p_b2**g_b2) * ((1 - p_b2) ** (T - s - g_b2))
                )

                # Number of goals scored by our team after pulling the goalie
                for g_a2 in range(0, T - s):
                    num_arrangements += 1
                    prob_ga2 = (
                        choose(T - s, g_a2)
                        * (p_a2**g_a2)
                        * ((1 - p_a2) ** (T - s - g_a2))
                    )

                    # Probability of this event
                    prob = prob_gb1 * prob_ga1 * prob_gb2 * prob_ga2

                    # Update the score
                    a = a_0 + g_a1 + g_a2
                    b = b_0 + g_b1 + g_b2

                    # Success if we win or tie
                    success = a >= b

                    prob_success = prob_success + prob * success

    prob_success = round(prob_success * 100, 4)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time = round(elapsed_time, 2)

    print(
        f"Pull time: {s}, num_arrangements: {num_arrangements} Probability of success: {prob_success}, Compute time: {elapsed_time}",
        flush=True,
    )

    results.append(
        {"pull_time": s, "prob_success": prob_success, "compute_time": elapsed_time}
    )

decisions_df = pd.DataFrame(results)

print(decisions_df, flush=True)


# ## Select the optimal choice

# In[ ]:


optimal_index = decisions_df["prob_success"].idxmax()
optimal_time = decisions_df.loc[optimal_index, "pull_time"]
optimal_prob = decisions_df.loc[optimal_index, "prob_success"]

print(
    f"Optimal time to pull the goalie: {optimal_time} seconds, resulting in a probability of {optimal_prob} of winning or tying the game.",
    flush=True,
)

# Plot pull time vs probability of success
plt.plot(decisions_df["pull_time"], decisions_df["prob_success"])
