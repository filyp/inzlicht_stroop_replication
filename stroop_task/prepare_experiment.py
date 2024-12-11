import random

from psychopy import logging, visual


def prepare_stimuli(win, config):
    stimuli = dict()
    for text in ["CZERWONY", "ZIELONY", "NIEBIESKI", "ŻÓŁTY"]:
        for color in ["red", "green", "blue", "yellow"]:
            name = f"{color}_{text.lower()}"
            stimuli[name] = visual.TextStim(
                win=win,
                text=text,
                color=color,
                height=config["Target_size"],
                name=name,
            )
    return stimuli


def prepare_trials(block, stimuli, config):
    all_trials = []

    number_of_trials = block.get(
        "number_of_trials", 0
    )  # if not given, assume it's a break block
    assert number_of_trials % 6 == 0  # it must be multiple of 6

    for _ in range(int(number_of_trials // 6)):
        all_trials.append(
            dict(
                target=stimuli["red_czerwony"],
                target_name="red_czerwony",
                type="congruent",
                font_color="red",
                text="czerwony",
                correct_side=config["Response_key"]["red"],
            )
        )
        all_trials.append(
            dict(
                target=stimuli["green_zielony"],
                target_name="green_zielony",
                type="congruent",
                font_color="green",
                text="zielony",
                correct_side=config["Response_key"]["green"],
            )
        )
        all_trials.append(
            dict(
                target=stimuli["red_zielony"],
                target_name="red_zielony",
                type="incongruent",
                font_color="red",
                text="zielony",
                correct_side=config["Response_key"]["red"],
            )
        )
        all_trials.append(
            dict(
                target=stimuli["green_czerwony"],
                target_name="green_czerwony",
                type="incongruent",
                font_color="green",
                text="czerwony",
                correct_side=config["Response_key"]["green"],
            )
        )
        all_trials.append(
            dict(
                target=stimuli["red_niebieski"],
                target_name="red_niebieski",
                type="neutral",
                font_color="red",
                text="niebieski",
                correct_side=config["Response_key"]["red"],
            )
        )
        all_trials.append(
            dict(
                target=stimuli["green_niebieski"],
                target_name="green_niebieski",
                type="neutral",
                font_color="green",
                text="niebieski",
                correct_side=config["Response_key"]["green"],
            )
        )

    random.shuffle(all_trials)
    return all_trials


# def prepare_trials_inzlicht(block, stimuli, config):
#     all_trials = []

#     # we want 24 congruent trials + 12 incongruent trials

#     # congruent
#     for _ in range(8):
#         all_trials.append(
#             dict(
#                 target=stimuli["red_czerwony"],
#                 target_name="red_czerwony",
#                 type="congruent",
#                 font_color="red",
#                 text="czerwony",
#                 correct_side=config["Response_key"]["red"],
#             )
#         )
#         all_trials.append(
#             dict(
#                 target=stimuli["green_zielony"],
#                 target_name="green_zielony",
#                 type="congruent",
#                 font_color="green",
#                 text="zielony",
#                 correct_side=config["Response_key"]["green"],
#             )
#         )
#         all_trials.append(
#             dict(
#                 target=stimuli["blue_niebieski"],
#                 target_name="blue_niebieski",
#                 type="congruent",
#                 font_color="blue",
#                 text="niebieski",
#                 correct_side=config["Response_key"]["blue"],
#             )
#         )
