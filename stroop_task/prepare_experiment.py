import random

from psychopy import logging, visual


def prepare_stimuli(win, config):
    stimuli = dict()
    stimuli["red_czerwony"] = visual.TextStim(
        win=win,
        text="CZERWONY",
        color="red",
        height=config["Target_size"],
        name="red_czerwony",
    )
    stimuli["green_zielony"] = visual.TextStim(
        win=win,
        text="ZIELONY",
        color="green",
        height=config["Target_size"],
        name="green_zielony",
    )
    stimuli["red_zielony"] = visual.TextStim(
        win=win,
        text="ZIELONY",
        color="red",
        height=config["Target_size"],
        name="red_zielony",
    )
    stimuli["green_czerwony"] = visual.TextStim(
        win=win,
        text="CZERWONY",
        color="green",
        height=config["Target_size"],
        name="green_czerwony",
    )
    stimuli["red_niebieski"] = visual.TextStim(
        win=win,
        text="NIEBIESKI",
        color="red",
        height=config["Target_size"],
        name="red_niebieski",
    )
    stimuli["green_niebieski"] = visual.TextStim(
        win=win,
        text="NIEBIESKI",
        color="green",
        height=config["Target_size"],
        name="green_niebieski",
    )
    # stimuli["blue_niebieski"] = visual.TextStim(
    #     win=win,
    #     text="NIEBIESKI",
    #     color="blue",
    #     height=config["Target_size"],
    #     name="blue_niebieski",
    # )
    # stimuli["blue_czerwony"] = visual.TextStim(
    #     win=win,
    #     text="CZERWONY",
    #     color="blue",
    #     height=config["Target_size"],
    #     name="blue_czerwony",
    # )
    # stimuli["blue_zielony"] = visual.TextStim(
    #     win=win,
    #     text="ZIELONY",
    #     color="blue",
    #     height=config["Target_size"],
    #     name="blue_zielony",
    # )
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
