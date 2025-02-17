# %%
import csv
from copy import deepcopy
from pathlib import Path

import pandas as pd

# # %%
# xlsx_file = "Triggers/Stroop_Task_Marker_Recoding MS.xlsx"
# xlsx_data = pd.read_excel(xlsx_file)
# s_name_to_our_trig_names = {}
# for i, row in xlsx_data.iterrows():
#     if not str(row[0]).startswith("S "):
#         continue
#     s_name = row[0]
#     our_trig_names = row[4:].dropna().tolist()
#     s_name_to_our_trig_names[s_name] = our_trig_names

# # %%
# # tests for xlsx file
# xlsx_file = "Triggers/Stroop_Task_Marker_Recoding MS.xlsx"
# xlsx_data = pd.read_excel(xlsx_file)
# s_name_to_our_trig_names = {}
# for i, row in xlsx_data.iterrows():
#     if not str(row.iloc[0]).startswith("S "):
#         continue

#     if i < 24:
#         s_name = row.iloc[0]
#         response = row.iloc[1]
#         trial_type = row.iloc[2]
#         response_type = row.iloc[3]

#         our_trig_names = row[4:].dropna().tolist()
#         for our_trig_name in our_trig_names:
#             fields = our_trig_name.split("*")
#             assert len(fields) == 5
#             assert fields[0] == "REACTION", fields
#             assert fields[1] == "exp"
#             if trial_type == "Congruent":
#                 assert fields[2] in ["red_czerwony", "green_zielony", "blue_niebieski", "yellow_zolty"]
#             elif trial_type == "Incongruent":
#                 assert fields[2] not in ["red_czerwony", "green_zielony", "blue_niebieski", "yellow_zolty"]
#             else:
#                 raise ValueError(f"Unknown trial type: {trial_type}")
            
#             if response_type == "Correct":
#                 assert fields[3] == fields[4]
#             elif response_type == "Incorrect":
#                 assert fields[3] != fields[4]
#             else:
#                 raise ValueError(f"Unknown response type: {response_type}")

#     else:
#         s_name = row.iloc[0]
#         stimuli_type = row.iloc[1]
#         font_color = row.iloc[2]
#         word_displayed = row.iloc[3]

#         our_trig_names = row[4:].dropna().tolist()
#         for our_trig_name in our_trig_names:
#             fields = our_trig_name.split("*")
#             assert len(fields) == 5
#             assert fields[0] == "TARGET_S", fields
#             assert fields[1] == "exp", fields
#             if stimuli_type == "Congruent":
#                 assert fields[2] in ["red_czerwony", "green_zielony", "blue_niebieski", "yellow_zolty"]
#             elif stimuli_type == "Incongruent":
#                 assert fields[2] not in ["red_czerwony", "green_zielony", "blue_niebieski", "yellow_zolty"], row
#             else:
#                 raise ValueError(f"Unknown stimuli type: {stimuli_type}")
#             color, word = fields[2].split("_")
            
#             assert color == font_color.lower()
#             if word_displayed == "Red":
#                 assert word == "czerwony"
#             elif word_displayed == "Green":
#                 assert word == "zielony"
#             elif word_displayed == "Blue":
#                 assert word == "niebieski"
#             elif word_displayed == "Yellow":
#                 assert word == "zolty"
#             else:
#                 raise ValueError(f"Unknown word displayed: {word_displayed}")
        

# %%

# fmt: off
s_name_to_our_trig_names = {'S  0': [],
 'S  1': ['REACTION*exp*red_czerwony*z*x', 'REACTION*exp*red_czerwony*z*n', 'REACTION*exp*red_czerwony*z*m'],
 'S  2': ['REACTION*exp*green_zielony*x*z', 'REACTION*exp*green_zielony*x*n', 'REACTION*exp*green_zielony*x*m'],
 'S  3': ['REACTION*exp*blue_niebieski*n*z', 'REACTION*exp*blue_niebieski*n*x', 'REACTION*exp*blue_niebieski*n*m'],
 'S  4': ['REACTION*exp*yellow_zolty*m*z', 'REACTION*exp*yellow_zolty*m*x', 'REACTION*exp*yellow_zolty*m*n'],
 'S  9': [],
 'S  5': ['REACTION*exp*red_czerwony*z*z'],
 'S  6': ['REACTION*exp*green_zielony*x*x'],
 'S  7': ['REACTION*exp*blue_niebieski*n*n'],
 'S  8': ['REACTION*exp*yellow_zolty*m*m'],
 'S 10': [],
 'S 15': ['REACTION*exp*red_zielony*z*x', 'REACTION*exp*red_zielony*z*n', 'REACTION*exp*red_zielony*z*m', 'REACTION*exp*red_niebieski*z*x', 'REACTION*exp*red_niebieski*z*n', 'REACTION*exp*red_niebieski*z*m', 'REACTION*exp*red_zolty*z*x', 'REACTION*exp*red_zolty*z*n', 'REACTION*exp*red_zolty*z*m'],
 'S 25': ['REACTION*exp*green_czerwony*x*z', 'REACTION*exp*green_czerwony*x*n', 'REACTION*exp*green_czerwony*x*m', 'REACTION*exp*green_niebieski*x*z', 'REACTION*exp*green_niebieski*x*n', 'REACTION*exp*green_niebieski*x*m', 'REACTION*exp*green_zolty*x*z', 'REACTION*exp*green_zolty*x*n', 'REACTION*exp*green_zolty*x*m'],
 'S 35': ['REACTION*exp*blue_czerwony*n*z', 'REACTION*exp*blue_czerwony*n*x', 'REACTION*exp*blue_czerwony*n*m', 'REACTION*exp*blue_zielony*n*z', 'REACTION*exp*blue_zielony*n*x', 'REACTION*exp*blue_zielony*n*m', 'REACTION*exp*blue_zolty*n*z', 'REACTION*exp*blue_zolty*n*x', 'REACTION*exp*blue_zolty*n*m'],
 'S 45': ['REACTION*exp*yellow_czerwony*m*z', 'REACTION*exp*yellow_czerwony*m*x', 'REACTION*exp*yellow_czerwony*m*n', 'REACTION*exp*yellow_niebieski*m*z', 'REACTION*exp*yellow_niebieski*m*x', 'REACTION*exp*yellow_niebieski*m*n', 'REACTION*exp*yellow_zielony*m*z', 'REACTION*exp*yellow_zielony*m*x', 'REACTION*exp*yellow_zielony*m*n'],
 'S 95': [],
 'S 55': ['REACTION*exp*red_zielony*z*z', 'REACTION*exp*red_niebieski*z*z', 'REACTION*exp*red_zolty*z*z'],
 'S 65': ['REACTION*exp*green_czerwony*x*x', 'REACTION*exp*green_niebieski*x*x', 'REACTION*exp*green_zolty*x*x'],
 'S 75': ['REACTION*exp*blue_czerwony*n*n', 'REACTION*exp*blue_zielony*n*n', 'REACTION*exp*blue_zolty*n*n'],
 'S 85': ['REACTION*exp*yellow_czerwony*m*m', 'REACTION*exp*yellow_niebieski*m*m', 'REACTION*exp*yellow_zielony*m*m'],
 'S 11': ['TARGET_S*exp*red_czerwony*z*z', 'TARGET_S*exp*red_czerwony*z*x', 'TARGET_S*exp*red_czerwony*z*n', 'TARGET_S*exp*red_czerwony*z*m'],
 'S 22': ['TARGET_S*exp*green_zielony*x*x', 'TARGET_S*exp*green_zielony*x*z', 'TARGET_S*exp*green_zielony*x*n', 'TARGET_S*exp*green_zielony*x*m'],
 'S 33': ['TARGET_S*exp*blue_niebieski*n*n', 'TARGET_S*exp*blue_niebieski*n*z', 'TARGET_S*exp*blue_niebieski*n*x', 'TARGET_S*exp*blue_niebieski*n*m'],
 'S 44': ['TARGET_S*exp*yellow_zolty*m*m', 'TARGET_S*exp*yellow_zolty*m*z', 'TARGET_S*exp*yellow_zolty*m*x', 'TARGET_S*exp*yellow_zolty*m*n'],
 'S 13': ['TARGET_S*exp*red_niebieski*z*x', 'TARGET_S*exp*red_niebieski*z*n', 'TARGET_S*exp*red_niebieski*z*m', 'TARGET_S*exp*red_niebieski*z*z'],
 'S 12': ['TARGET_S*exp*red_zielony*z*x', 'TARGET_S*exp*red_zielony*z*n', 'TARGET_S*exp*red_zielony*z*m', 'TARGET_S*exp*red_zielony*z*z'],
 'S 14': ['TARGET_S*exp*red_zolty*z*x', 'TARGET_S*exp*red_zolty*z*n', 'TARGET_S*exp*red_zolty*z*m', 'TARGET_S*exp*red_zolty*z*z'],
 'S 21': ['TARGET_S*exp*green_czerwony*x*z', 'TARGET_S*exp*green_czerwony*x*n', 'TARGET_S*exp*green_czerwony*x*m', 'TARGET_S*exp*green_czerwony*x*x'],
 'S 23': ['TARGET_S*exp*green_niebieski*x*z', 'TARGET_S*exp*green_niebieski*x*n', 'TARGET_S*exp*green_niebieski*x*m', 'TARGET_S*exp*green_niebieski*x*x'],
 'S 24': ['TARGET_S*exp*green_zolty*x*z', 'TARGET_S*exp*green_zolty*x*n', 'TARGET_S*exp*green_zolty*x*m', 'TARGET_S*exp*green_zolty*x*x'],
 'S 31': ['TARGET_S*exp*blue_czerwony*n*z', 'TARGET_S*exp*blue_czerwony*n*x', 'TARGET_S*exp*blue_czerwony*n*m', 'TARGET_S*exp*blue_czerwony*n*n'],
 'S 32': ['TARGET_S*exp*blue_zielony*n*z', 'TARGET_S*exp*blue_zielony*n*x', 'TARGET_S*exp*blue_zielony*n*m', 'TARGET_S*exp*blue_zielony*n*n'],
 'S 34': ['TARGET_S*exp*blue_zolty*n*z', 'TARGET_S*exp*blue_zolty*n*x', 'TARGET_S*exp*blue_zolty*n*m', 'TARGET_S*exp*blue_zolty*n*n'],
 'S 41': ['TARGET_S*exp*yellow_czerwony*m*z', 'TARGET_S*exp*yellow_czerwony*m*x', 'TARGET_S*exp*yellow_czerwony*m*n', 'TARGET_S*exp*yellow_czerwony*m*m'],
 'S 42': ['TARGET_S*exp*yellow_zielony*m*z', 'TARGET_S*exp*yellow_zielony*m*x', 'TARGET_S*exp*yellow_zielony*m*n', 'TARGET_S*exp*yellow_zielony*m*m'],
 'S 43': ['TARGET_S*exp*yellow_niebieski*m*z', 'TARGET_S*exp*yellow_niebieski*m*x', 'TARGET_S*exp*yellow_niebieski*m*n', 'TARGET_S*exp*yellow_niebieski*m*m']}
# fmt: on

exclusions = [
    "BLOCK_START*msg*-*-*",
    "*1tr*",
    "*2tr*",
    "*3tr*",
    "*4tr*",
    "BLOCK_START*exp*-*-*",
    "FIXATION*",
    "TARGET_E*",
    "BLOCK_START*bre*-*-*",
]

our_trig_names_to_s_name = {}
for s_name, our_trig_names in s_name_to_our_trig_names.items():
    for our_trig_name in our_trig_names:
        assert our_trig_name not in our_trig_names_to_s_name
        our_trig_names_to_s_name[our_trig_name] = s_name

# %%
# this will process all files in Triggers folder
# and will skip files that already have Stimulus, S in them

dir_ = Path("Triggers")
for in_path in dir_.glob("*.Markers"):
    text = in_path.read_text()
    if "Stimulus, S " in text:
        print(f"Skipping {in_path} - already processed")
        continue
    print(f"Processing {in_path}")

    new_lines = []
    for line in text.splitlines():
        if not line.startswith("Stimulus, "):
            new_lines.append(line)
            continue

        our_trig_name = line.split(", ")[1]
        if any(exclusion in our_trig_name for exclusion in exclusions):
            new_lines.append(line)
            continue

        # also ignore TARGET_S if no response
        if our_trig_name.startswith("TARGET_S") and our_trig_name.endswith("*-"):
            new_lines.append(line)
            continue

        # print(our_trig_name)
        s_name = our_trig_names_to_s_name[our_trig_name]
        new_line = line.split(", ")
        new_line[1] = s_name
        new_line = ", ".join(new_line)
        new_lines.append(new_line)

    in_path.write_text("\n".join(new_lines))