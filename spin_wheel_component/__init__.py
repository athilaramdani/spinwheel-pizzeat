import os
import streamlit.components.v1 as components

# Get the directory where this file resides
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Declare the Streamlit custom component
_component_func = components.declare_component(
    "spin_wheel_component",
    path=PARENT_DIR
)

def spin_wheel_component(
    target_prize_index,
    trigger_id,
    prizes,
    spin_sound_b64="",
    win_sound_b64="",
    jackpot_sound_b64="",
    key=None
):
    """
    Renders the PizzEat Lucky Spin Wheel HTML5 Canvas component.
    
    Parameters:
    - target_prize_index (int): The index of the prize to land on.
    - trigger_id (str/int): A unique ID to trigger a new spin when changed.
    - prizes (list): List of prize objects containing name, color, is_jackpot, and emoji.
    - spin_sound_b64 (str): Base64-encoded spinning audio.
    - win_sound_b64 (str): Base64-encoded win audio.
    - jackpot_sound_b64 (str): Base64-encoded jackpot audio.
    - key (str): Streamlit key for the component instance.
    
    Returns:
    - dict: The state from the component, e.g., {"status": "finished", "trigger_id": "...", "prize_index": 2}
    """
    return _component_func(
        target_prize_index=target_prize_index,
        trigger_id=trigger_id,
        prizes=prizes,
        spin_sound_b64=spin_sound_b64,
        win_sound_b64=win_sound_b64,
        jackpot_sound_b64=jackpot_sound_b64,
        key=key,
        default={"status": "idle"},
        height=500
    )
