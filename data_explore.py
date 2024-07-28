import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sksurv.nonparametric import kaplan_meier_estimator

csv_files = ["array_TF_success_time.csv", "array_TF_fail_time.csv"]
for csv in range(len(csv_files)):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_files[csv])

    # Convert the DataFrame to a structured NumPy array with the specified dtype
    dtype = [('Status', '?'), ('Survival_in_Seconds', '<f8')]
    array_TF_success_time = np.array(list(df.itertuples(index=False, name=None)), dtype=dtype)

    # Extract the status and survival times
    status = array_TF_success_time['Status']
    survival_times = array_TF_success_time['Survival_in_Seconds']
    print("status:", status)
    print("survival_times:", survival_times)
    # find index of negative survival times
    index = np.where(survival_times < 0)[0]
    print("index:", index)
    print("survival_times[index]:", survival_times[index])
    print("status[index]:", status[index])
    # remove negative survival times and corresponding status
    survival_times = np.delete(survival_times, index)
    status = np.delete(status, index)

    # Compute the Kaplan-Meier estimator
    time, survival_prob, conf_int = kaplan_meier_estimator(
        status, survival_times, conf_type="log-log"
    )
    #print("time:", time)
    #print("survival_prob:", survival_prob)

    half_survival_time = np.interp(0.5, survival_prob[::-1], time[::-1]) #linearly extrapolate to find the time at which the estimated probability of survival is 0.5
    #if there is a lot of censored data points, the estimated probability of survival may not reach 0.5

    # Plot the Kaplan-Meier estimator
    plt.step(time, survival_prob, where="post")
    plt.fill_between(time, conf_int[0], conf_int[1], alpha=0.25, step="post")
    plt.axhline(y=0.5, color='r', linestyle='--')
    plt.axvline(x=half_survival_time, color='r', linestyle='--')
    plt.annotate(f'({half_survival_time:.2f}, 0.5)', xy=(half_survival_time, 0.5), xytext=(half_survival_time, 0.6),
                arrowprops=dict(facecolor='black', shrink=0.05))
    plt.ylim(0, 1)
    plt.ylabel(r"est. probability of survival $\hat{S}(t)$")
    plt.xlabel("time $t$")
    plt.show()

    print("half_survival_time:", half_survival_time)
    #322.5 ends up being when we estimate that we should score a goal by

    probability_score_in_given_second = 1/half_survival_time
    print("probability_score_in_given_second:", probability_score_in_given_second)


