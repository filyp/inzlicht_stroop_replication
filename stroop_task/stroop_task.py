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

color_dict = dict(
    red="#FF0000",
    green="#00FF00",
    blue="#0000FF",
    yellow="#FFFF00",
)


def prepare_stimuli(win, config):
    incongruent_trials = []
    congruent_trials = []
    for text in ["CZERWONY", "ZIELONY", "NIEBIESKI", "ŻÓŁTY"]:
        for color in ["red", "green", "blue", "yellow"]:
            name = f"{color}_{unidecode(text.lower())}"
            stimulus = visual.TextStim(
                win=win,
                text=text,
                color=color_dict[color],
                height=config["Target_size"],
                name=name,
            )
            congruent = name in ["red_czerwony", "green_zielony", "blue_niebieski", "yellow_zolty" ]  # fmt: skip
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


def check_response(config, trial, clock, trigger_handler, block):
    key = event.getKeys(keyList=config["Response_key"].values())
    reaction_time = clock.getTime()
    if not key:
        return
    if trial["response"] != "-":
        # there already was a response
        return

    trial["rt"] = reaction_time
    trial["response"] = key[0]
    print(reaction_time, key)
    if trial["correct_key"] == key[0]:
        trial["reaction"] = "correct"
    else:
        trial["reaction"] = "incorrect"

    trigger_name = get_trigger_name(
        trigger_type=TriggerTypes.REACTION,
        block=block,
        trial=trial,
    )
    trigger_handler.prepare_trigger(trigger_name)
    trigger_handler.send_trigger()


def stroop_task(exp, config, data_saver):
    # unpack necessary objects for easier access
    win = exp.win
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
        trigger_name = get_trigger_name(TriggerTypes.BLOCK_START, block)
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
            raise ValueError("{} is a bad block type in config".format(block["type"]))

        for trial in block["trials"]:
            trigger_handler.open_trial()
            trial["response"] = "-"
            trial["rt"] = "-"
            trial["reaction"] = "-"

            # ! draw empty screen
            core.wait(1)

            # ! draw fixation
            trigger_name = get_trigger_name(TriggerTypes.FIXATION, block, trial)
            trigger_handler.prepare_trigger(trigger_name)
            fixation.setAutoDraw(True)
            win.flip()
            trigger_handler.send_trigger()
            core.wait(0.5)
            fixation.setAutoDraw(False)

            data_saver.check_exit()

            # ! draw target
            trigger_name = get_trigger_name(TriggerTypes.TARGET_START, block, trial)
            trigger_handler.prepare_trigger(trigger_name)
            event.clearEvents()
            win.callOnFlip(clock.reset)
            trial["target"].setAutoDraw(True)
            win.flip()
            trigger_handler.send_trigger()
            while clock.getTime() < 0.2:
                check_response(config, trial, clock, trigger_handler, block)
                win.flip()
            trial["target"].setAutoDraw(False)

            # ! draw fixation and await response
            trigger_name = get_trigger_name(TriggerTypes.TARGET_END, block, trial)
            trigger_handler.prepare_trigger(trigger_name)
            fixation.setAutoDraw(True)
            win.flip()
            trigger_handler.send_trigger()
            while clock.getTime() < 0.2 + 0.8:
                check_response(config, trial, clock, trigger_handler, block)
                win.flip()
            fixation.setAutoDraw(False)
            win.flip()

            # if incorrect and training, show feedback
            if trial["reaction"] != "correct" and block["type"] == "training":
                text = "Reakcja niepoprawna.\nWciskaj klawisz odpowiadający KOLOROWI CZCIONKI."
                show_info(exp, text, duration=6)
                exp.display_for_duration(2, fixation)

            # save beh
            # fmt: off
            behavioral_data = OrderedDict(
                # predefined
                block_type=block["type"],
                trial_type=trial["type"],
                font_color=trial["font_color"],
                text=trial["text"],
                correct_key=trial["correct_key"],
                # based on response
                response=trial["response"],
                rt=trial["rt"],
                reaction=trial["reaction"],
            )
            # fmt: on
            data_saver.beh.append(behavioral_data)
            trigger_handler.close_trial(trial["response"])

            logging.data(f"Behavioral data: {behavioral_data}\n")
            logging.flush()
