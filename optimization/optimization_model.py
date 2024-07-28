#!/usr/bin/env python
# coding: utf-8

# To run via slurm, first output the ipynb notebook to python using `jupyter nbconvert --to script optimization_model.ipynb`

# In[1]:


import time
import pandas as pd


# ## Load precomputed combinations to save computation time

# In[8]:


comb_df = pd.read_pickle("precompute_combinations/precomputed_combinations_df.pkl")
# Set indices for faster accession
comb_df.set_index(["n", "k"], inplace=True)
comb_df.sort_index(inplace=True)

def choose(n, k):
    return comb_df.loc[(n, k), "n_choose_k"]


# ## Load probabilities
# 
# TODO: right now this just hard codes some values

# In[3]:


# Approximate probability of a goal in a given second
seconds_in_game = 20 * 60 * 3
p_a1 = 3.12 / seconds_in_game
p_b1 = p_a1

# Probability of the other team scoring during 6v5 increases
p_b2 = 1.5 * p_b1

# Probability of our team scoring during 6v5 also increases, though not as much
p_a1 = 1.25 * p_a1


# ## Inputs to model

# In[4]:


# Let's say the current score is 1 - 3
a_0 = 1
b_0 = 3

# 5 minutes left in the game
T = 5 * 60


# ## Brute force every choice of $s$

# In[9]:


decisions_df = pd.DataFrame(columns = [
    'pull_time',
    'prob_success',
    'compute_time'])

#  Try out each possible time to pull the goalie
for i in range(0, T):
    s = i
    if s % 30 == 0:
        display(f"...computing for s={s} seconds")
    start_time = time.time()

    prob_success = 0

    # Number of goals scored by other team before pulling the goalie
    for g_b1 in range(0, s):
        prob_gb1 = choose(s, g_b1) * (p_b1 ** g_b1) * ((1 - p_b1) ** (s - g_b1))

        # Number of goals scored by our team before pulling the goalie
        for g_a1 in range(0, s):
            prob_ga1 = choose(s, g_a1) * (p_a1 ** g_a1) * ((1 - p_a1) ** (s - g_a1))

            # Number of goals scored by other team after pulling the goalie
            for g_b2 in range(0, T - s):
                prob_gb2 = choose(T - s, g_b2) * (p_b2 ** g_b2) * ((1 - p_b2) ** (T - s - g_b2))

                # Number of goals scored by our team after pulling the goalie
                for g_a2 in range(0, T - s):
                    prob_ga2 = choose(T - s, g_a2) * (p_a1 ** g_a2) * ((1 - p_a1) ** (T - s - g_a2))

                    # Probability of this event
                    prob = prob_gb1 * prob_ga1 * prob_gb2 * prob_ga2

                    # Update the score
                    a = a_0 + g_a1 + g_a2
                    b = b_0 + g_b1 + g_b2

                    # Success if we win or tie
                    success = (a >= b)

                    prob_success = prob_success + prob * success
    end_time = time.time()
    elapsed_time = end_time - start_time

    decisions_df = pd.concat(
        [
            decisions_df,
            pd.DataFrame({
                "pull_time": s,
                "prob_success": prob_success,
                "compute_time": elapsed_time
            }, index=[0]),
        ], ignore_index=True
    )

display(decisions_df)


# ## Select the optimal choice

# In[ ]:


optimal_index = decisions_df["prob_success"].idxmax()
optimal_time = decisions_df.loc[optimal_index, "pull_time"]
optimal_prob = decisions_df.loc[optimal_index, "prob_success"]

print(f"Optimal time to pull the goalie: {optimal_time} seconds, resulting in a probability of {optimal_prob} of winning or tying the game.")

