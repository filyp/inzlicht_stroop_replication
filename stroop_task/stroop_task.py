import pathlib
import random
from collections import OrderedDict
from copy import copy
from textwrap import dedent

import numpy as np
from psychopy import core, event, logging, visual
from unidecode import unidecode

from psychopy_experiment_helpers.show_info import show_info
from psychopy_experiment_helpers.triggers_common import TriggerHandler, create_eeg_port
from stroop_task.triggers import TriggerTypes, get_trigger_name

message_dir = pathlib.Path(__file__).parent.parent / "messages"


def prepare_stimuli(win, config):
    incongruent_trials = []
    congruent_trials = []
    for text in ["CZERWONY", "ZIELONY", "NIEBIESKI", "ŻÓŁTY"]:
        for color in ["red", "green", "blue", "yellow"]:
            name = f"{color}_{unidecode(text.lower())}"
            # todo 255 colors
            stimulus = visual.TextStim(
                win=win,
                text=text,
                color=color,
                height=config["Target_size"],
                name=name,
            )
            congruent = name in [
                "red_czerwony",
                "green_zielony",
                "blue_niebieski",
                "yellow_zolty",
            ]  # fmt: off
            trial = dict(
                target=stimulus,
                target_name=name,
                type="congruent" if congruent else "incongruent",
                font_color=color,
                text=text,
                correct_key=config["Response_key"][color],
            )
            if congruent:
                congruent_trials.append(trial)
            else:
                incongruent_trials.append(trial)

    return congruent_trials, incongruent_trials


def stroop_task(exp, config, data_saver):
    # unpack necessary objects for easier access
    win = exp.win
    mouse = exp.mouse
    clock = exp.clock

    congruent_trials, incongruent_trials = prepare_stimuli(win, config)
    # create a fixation cross as a text stim
    fixation = visual.TextStim(
        win=win,
        text="+",
        color="grey",
        height=config["Fixation_size"],
        name="fixation",
        pos=(0, config["Fixation_offset"]),
    )

    # EEG triggers
    port_eeg = create_eeg_port() if config["Send_EEG_trigg"] else None
    trigger_handler = TriggerHandler(port_eeg, data_saver=data_saver)
    exp.trigger_handler = trigger_handler

    for block in config["Experiment_blocks"]:
        trigger_name = get_trigger_name(TriggerTypes.BLOCK_START, block, response="-")
        trigger_handler.prepare_trigger(trigger_name)
        trigger_handler.send_trigger()
        logging.data(f"Entering block: {block}")
        logging.flush()

        if block["type"] == "break":
            text = "Zakończyłeś jeden z bloków sesji eksperymentalnej."
            show_info(exp, text, duration=3)

            text = """\
            Zrób sobie PRZERWĘ.

            Przerwa na odpoczynek nr {num}.

            (wciśnij spację kiedy będziesz gotowy kontynuować badanie)"""
            text = dedent(text).format(num=block["num"])
            show_info(exp, text, duration=None)

            text = """Za chwilę rozpocznie się kolejny blok sesji eksperymentalnej."""
            show_info(exp, text, duration=5)
            continue

        elif block["type"] == "msg":
            # all the other messages, instructions, info
            text = (message_dir / block["file_name"]).read_text()
            text = text.format(**config)
            duration = block.get("duration", None)
            show_info(exp, text, duration=duration)
            continue

        elif block["type"] in ["experiment", "training"]:
            # prepare 24 congruent trials and 12 incongruent trials
            # trials = congruent_trials * 6 + incongruent_trials
            trials = incongruent_trials
            random.shuffle(trials)
            block["trials"] = trials

        else:
            raise ValueError(
                "{} is bad block type in config Experiment_blocks".format(block["type"])
            )

        for trial in block["trials"]:
            response_data = []
            trigger_handler.open_trial()

            # ! draw target
            trigger_name = get_trigger_name(TriggerTypes.TARGET, block, trial)
            target_show_time = 0.2
            event.clearEvents()
            win.callOnFlip(mouse.clickReset)
            win.callOnFlip(clock.reset)
            trigger_handler.prepare_trigger(trigger_name)
            trial["target"].setAutoDraw(True)
            win.flip()
            trigger_handler.send_trigger()
            while clock.getTime() < target_show_time:
                check_response(exp, block, trial, response_data)
                win.flip()
            trial["target"].setAutoDraw(False)
            win.flip()

            # ! draw empty screen and await response
            trigger_name = get_trigger_name(TriggerTypes.FIXATION, block, trial)
            empty_screen_show_time = 0.8
            trigger_handler.prepare_trigger(trigger_name)
            fixation.setAutoDraw(True)
            win.flip()
            trigger_handler.send_trigger()
            while clock.getTime() < target_show_time + empty_screen_show_time:
                check_response(exp, block, trial, response_data)
                win.flip()
            fixation.setAutoDraw(False)
            data_saver.check_exit()

            # check if reaction was correct
            response_side, reaction_time = (
                response_data[0] if response_data != [] else ("-", "-")
            )
            if response_side == trial["correct_key"]:
                reaction = "correct"
            else:
                reaction = "incorrect"

            # if incorrect and training, show feedback
            if reaction == "incorrect" and block["type"] == "training":
                text = "Reakcja niepoprawna.\n\n" + config["Response_instruction"]
                show_info(exp, text, duration=6)
                exp.display_for_duration(2, fixation)

            # save beh
            # fmt: off
            behavioral_data = OrderedDict(
                block_type=block["type"],
                trial_type=trial["type"],
                font_color=trial["font_color"],
                text=trial["text"],
                response=response_side,
                correct_key=trial["correct_key"],
                rt=reaction_time,
                reaction=reaction,
                empty_screen_show_time=empty_screen_show_time,
            )
            # fmt: on
            data_saver.beh.append(behavioral_data)
            trigger_handler.close_trial(response_side)

            # logging.data(f"Behavioral data: {behavioral_data}\n")
            # logging.flush()
