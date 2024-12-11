# %% load data
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = "Cechy afektywne a kontrola poznawcza_ Podejście neurofizjologiczne (Responses).xlsx"
df = pd.read_excel(filename)

# %% find rows where "Email Address" is duplicated
df = df[~df["Email Address"].duplicated(keep="last")]

# assert that all "Email Address" are unique
assert len(df["Email Address"].unique()) == len(df)

# %% delete the duplicated person (K.C. @gmail)
to_delete = Path("to_delete.txt").read_text().strip()
df = df[df["Email Address"] != to_delete]

# %% recreate the index
df = df.reset_index(drop=True)
df

# %% slice into questionnaires
first_pswq_column = 4
first_spq_column = first_pswq_column + 16
first_snaq_column = first_spq_column + 31
first_meta_column = first_snaq_column + 2

pswq = df.iloc[:, first_pswq_column:first_spq_column]
spq = df.iloc[:, first_spq_column:first_snaq_column]
snaq = df.iloc[:, first_snaq_column:first_meta_column]
assert all("PSWQ" in column for column in pswq.columns)
assert all("SPQ" in column for column in spq.columns)
assert all("SNAQ" in column for column in snaq.columns)

# %% values to numbers and bools
pswq_answer_dict = {
    "Całkowicie nietypowe dla mnie": 1,
    "Raczej nietypowe dla mnie": 2,
    "Umiarkowanie typowe dla mnie": 3,
    "Raczej typowe dla mnie": 4,
    "Bardzo typowe dla mnie": 5,
}
bool_answer_dict = {
    "Prawda": True,
    "Fałsz": False,
}

pswq = pswq.applymap(lambda x: pswq_answer_dict[x])
spq = spq.applymap(lambda x: bool_answer_dict[x])
snaq = snaq.applymap(lambda x: bool_answer_dict[x])

# %% reverse some codes
pswq_rev_code = ["PSWQ-1", "PSWQ-3", "PSWQ-8", "PSWQ-10", "PSWQ-11"]
spq_rev_code = ["SPQ-6", "SPQ-12", "SPQ-14", "SPQ-16", "SPQ-17", "SPQ-20", "SPQ-25", "SPQ-27", "SPQ-28"]  # fmt: skip
snaq_rev_code = ["SNAQ-6", "SNAQ-12", "SNAQ-14", "SNAQ-16", "SNAQ-17", "SNAQ-20", "SNAQ-25", "SNAQ-27", "SNAQ-28"]  # fmt: skip
# note: compared to the german version, we don't reverse question 22

# original_pswq = pswq.copy()
# original_spq = spq.copy()
# original_snaq = snaq.copy()

# PSWQ
for i, column in enumerate(pswq.columns):
    column_code = re.match(r"PSWQ-\d+", column)[0]
    assert i + 1 == int(column_code.split("-")[1])
    if column_code in pswq_rev_code:
        pswq[column] = 6 - pswq[column]

# SPQ
for i, column in enumerate(spq.columns):
    column_code = re.match(r"SPQ-\d+", column)[0]
    assert i + 1 == int(column_code.split("-")[1])
    if column_code in spq_rev_code:
        spq[column] = ~spq[column]

# SNAQ
for i, column in enumerate(snaq.columns):
    column_code = re.match(r"SNAQ-\d+", column)[0]
    assert i + 1 == int(column_code.split("-")[1])
    if column_code in snaq_rev_code:
        snaq[column] = ~snaq[column]

# %% test by inverting again
# reinvert_pswq = pswq.copy()
# reinvert_spq = spq.copy()
# reinvert_snaq = snaq.copy()

# # PSWQ
# for i, column in enumerate(pswq.columns):
#     column_code = re.match(r"PSWQ-\d+", column)[0]
#     assert i + 1 == int(column_code.split("-")[1])
#     if column_code in pswq_rev_code:
#         reinvert_pswq[column] = 6 - reinvert_pswq[column]

# # SPQ
# for i, column in enumerate(spq.columns):
#     column_code = re.match(r"SPQ-\d+", column)[0]
#     assert i + 1 == int(column_code.split("-")[1])
#     if column_code in spq_rev_code:
#         reinvert_spq[column] = ~reinvert_spq[column]

# # SNAQ
# for i, column in enumerate(snaq.columns):
#     column_code = re.match(r"SNAQ-\d+", column)[0]
#     assert i + 1 == int(column_code.split("-")[1])
#     if column_code in snaq_rev_code:
#         reinvert_snaq[column] = ~reinvert_snaq[column]

# assert all(reinvert_pswq == original_pswq)
# assert all(reinvert_spq == original_spq)
# assert all(reinvert_snaq == original_snaq)

# %% sum scores
df["PSWQ total score"] = pswq.sum(axis=1)
df["SPQ total score"] = spq.sum(axis=1)
df["SNAQ total score"] = snaq.sum(axis=1)
df["SPQ+SNAQ total score"] = df["SPQ total score"] + df["SNAQ total score"]

# plt.hist(df["SNAQ total score"], bins=range(0, 32, 1))
# plt.title("Histogram of SNAQ scores")

# %% compute ranks
n = len(df)
for questionnaire in ["PSWQ", "SPQ", "SNAQ", "SPQ+SNAQ"]:
    enumerated = list(enumerate(df[f"{questionnaire} total score"]))
    _sorted_by_score = sorted(enumerated, key=lambda x: x[1])
    people_sorted_by_score = [index for index, score in _sorted_by_score]
    df[f"{questionnaire} rank"] = [
        people_sorted_by_score.index(pi) / n for pi in range(n)
    ]
# %% analyses
# np.corrcoef([df["PSWQ rank"], df["SPQ rank"], df["SNAQ rank"], df["SPQ+SNAQ rank"]])

# ax = df.plot.scatter(x="PSWQ rank", y="SPQ+SNAQ rank")
# pad = 0.05
# ax.set_xlim(0 - pad, 1 + pad)
# ax.set_ylim(0 - pad, 1 + pad)
# ax.set_aspect("equal")

# %% divide into groups
group_size = int(n / 5 / 3)
print(group_size)
df["Group"] = None

# control group
ind_to_rank = list(enumerate(df["PSWQ rank"] + df["SPQ+SNAQ rank"]))
_control_indexes_and_ranks = sorted(ind_to_rank, key=lambda x: x[1])[:group_size]
control_indexes = [ind for ind, rank in _control_indexes_and_ranks]
df.loc[control_indexes, "Group"] = "control"

# worry group
ind_to_rank = list(enumerate(df["PSWQ rank"] - df["SPQ+SNAQ rank"] / 3))
_worry_indexes_and_ranks = sorted(ind_to_rank, key=lambda x: x[1])[-group_size:]
worry_indexes = [ind for ind, rank in _worry_indexes_and_ranks]
df.loc[worry_indexes, "Group"] = "worry"

# phobia group
ind_to_rank = list(enumerate(df["SPQ+SNAQ rank"] - df["PSWQ rank"] / 3))
_phobia_indexes_and_ranks = sorted(ind_to_rank, key=lambda x: x[1])[-group_size:]
phobia_indexes = [ind for ind, rank in _phobia_indexes_and_ranks]
df.loc[phobia_indexes, "Group"] = "phobia"

assert set(control_indexes).isdisjoint(set(worry_indexes))
assert set(control_indexes).isdisjoint(set(phobia_indexes))
assert set(worry_indexes).isdisjoint(set(phobia_indexes))

# %% plots
color_map = {"control": "green", "worry": "yellow", "phobia": "red", None: "grey"}
colors = df["Group"].apply(lambda x: color_map[x])

ax = df.plot.scatter(x="PSWQ total score", y="SPQ+SNAQ total score", c=colors)
# pad = 0.05
# ax.set_xlim(0 - pad, 1 + pad)
# ax.set_ylim(0 - pad, 1 + pad)
# ax.set_aspect("equal")

# %% save
out_filename = "processed responses.xlsx"
df.to_excel(out_filename, index=False)

# %%
