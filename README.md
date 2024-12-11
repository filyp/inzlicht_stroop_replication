# Installation on windows

1. Install PsychoPy - [Installation — PsychoPy](https://www.psychopy.org/download.html)
2. Clone this repository (run this command in windows cmd or in [git bash](https://git-scm.com/downloads)):
```
git clone --recurse-submodules https://github.com/filyp/hajcak_stroop_replication.git
```
3. Run the `install.bat` script (just click it).
4. Verify installation by running test script: `run_short_test_experiment_without_triggers.bat`

# Running the experiment

Click `run_red_left.bat` or `run_red_right.bat` to run the experiments.

The first one, as the name suggests, will run the experiment where participants should respond to red text with the left mouse button and to green text with the right mouse button. The second one is the opposite.

You may need to adapt the mechanism of sending triggers to your setup. Edit the file `psychopy_experiment_helpers/triggers_common.py` to do so.
