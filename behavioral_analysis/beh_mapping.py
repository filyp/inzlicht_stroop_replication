# %%
import csv
import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


# path = sys.argv[1]
# path = "../results/stroop_red_right_full_procedure_test"
# path = "results/short_notrig_29f8e7"
path = "../results/short_notrig_29f8e7"

behavioral_data_glob = os.path.join(path, "behavioral_data", "*.csv")
files = glob.glob(behavioral_data_glob)
files.sort(key=os.path.getctime)
most_recent_file = files[-1]
print(f"Using file {most_recent_file}")


# %%

with open(most_recent_file, "r") as file:
    reader = csv.DictReader(file)
    rows = [row for row in reader]

# %%

# %%

experiment_rows = [row for row in rows if row["block_type"] == "experiment"]

# %%

congruent_correct_rts = []
incongruent_correct_rts = []
congruent_error_rts = []
incongruent_error_rts = []

num_no_reaction = 0
for row in experiment_rows:
    rt = row["rt"]
    if rt == "-":
        # no reaction was given
        num_no_reaction += 1
        continue
    rt = float(rt)

    if row["trial_type"] == "congruent":
        if row["reaction"] == "correct":
            congruent_correct_rts.append(rt)
        elif row["reaction"] == "incorrect":
            congruent_error_rts.append(rt)
        else:
            raise Exception()
    elif row["trial_type"] == "incongruent":
        if row["reaction"] == "correct":
            incongruent_correct_rts.append(rt)
        elif row["reaction"] == "incorrect":
            incongruent_error_rts.append(rt)
        else:
            raise Exception()
    else:
        print(row)
        raise Exception()

# %%


def stats(data):
    if len(data) < 2:
        return "      -      "
    mean = np.mean(data)
    # use ddof=1 to calculate sample std, not population std
    standard_error = np.std(data, ddof=1) / np.sqrt(len(data))
    return f"{mean:.3f} ± {standard_error:.3f}"


def print_len(data):
    return f"{len(data):8d}     "


print(
    f"""
REACTION TIMES:
             |     CORRECT     |      ERROR      |       ALL       |
CONGRUENT    |  {stats(congruent_correct_rts)}  |  {stats(congruent_error_rts)}  |  {stats(congruent_correct_rts + congruent_error_rts)}  |
INCONGRUENT  |  {stats(incongruent_correct_rts)}  |  {stats(incongruent_error_rts)}  |  {stats(incongruent_correct_rts + incongruent_error_rts)}  |
ALL          |  {stats(congruent_correct_rts + incongruent_correct_rts)}  |  {stats(congruent_error_rts + incongruent_error_rts)}  |  {stats(congruent_correct_rts + congruent_error_rts + incongruent_correct_rts + incongruent_error_rts)}  |


NUMBER OF TRIALS:
             |     CORRECT     |      ERROR      |       ALL       |
CONGRUENT    |  {print_len(congruent_correct_rts)}  |  {print_len(congruent_error_rts)}  |  {print_len(congruent_correct_rts + congruent_error_rts)}  |
INCONGRUENT  |  {print_len(incongruent_correct_rts)}  |  {print_len(incongruent_error_rts)}  |  {print_len(incongruent_correct_rts + incongruent_error_rts)}  |
ALL          |  {print_len(congruent_correct_rts + incongruent_correct_rts)}  |  {print_len(congruent_error_rts + incongruent_error_rts)}  |  {print_len(congruent_correct_rts + congruent_error_rts + incongruent_correct_rts + incongruent_error_rts)}  |
"""
)

print(f"Number of trials with no reaction: {num_no_reaction}")


# from collections import Counter

# c = Counter()

# for trial in experiment_rows:
# %%

rts = [float(row["rt"]) for row in experiment_rows if row["rt"] != "-"]
# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.hist(rts, bins=20)
ax1.set_title("Reaction times histogram")

ax2.plot(rts)
ax2.set_title("Reaction times sequence")

plt.tight_layout()
plt.show()