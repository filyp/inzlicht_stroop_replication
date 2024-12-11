class TriggerTypes:
    BLINK = "BLINK"
    TARGET = "TARGET__"
    REACTION = "REACTION"
    SECOND_REACTION = "SECOND_R"
    FIXATION = "FIXATION"
    BLOCK_START = "BLOCK_START"


def get_trigger_name(
    trigger_type,
    block,
    trial=None,
    response="{}",
):
    block_type = block["type"]
    if trial is not None:
        target_name = trial["target_name"]
        correct_side = trial["correct_side"]
    else:
        target_name = "---"
        correct_side = "-"

    return f"{trigger_type}*{block_type[:2]}*{target_name}*{correct_side}*{response}"
