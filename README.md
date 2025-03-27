# Exercise Workflow Management iCSC 2025
1. Login to lxplus `ssh <username>@lxplus.cern.ch`
2. cd to your eos space for more storage `cd /eos/user/c/cversteg` (replace with your username and initial)
3. Clone the exercise repo `git clone --recurse-submodules https://github.com/cverstege/wfm_iCSC25.git`
4. cd into the exercise directory `cd wfm_iCSC25`
5. Source the environment `source setup.sh`. IMPORTANT! You have to source the environment again in every new shell/ssh session!
6. Initialise law `law index -v`
7. Start the luigi scheduler `luigid` in a tmux session (or always add the `--local-scheduler` flag when running a task)

## Getting started
Do you remember the ´CreateAlphabet´ example from the lecture. Let's start by trying to implement this and understand how workflows and tasks are working.

Once we've done that, you can go on and try to implement a small workflow, that can be used as a part for a full physics analysis. You don't have to understand the underlying physics to be able to implement the workflow. If you still want to know more, just ask!

## What workflow are we trying to run?
We want to simulate particle collissions using Sherpa and/or Herwig and then analyze it with a predefined physics analysis.
For Sherpa the WF looks like this:
1. Define the input file setting up the process we want to simulate. It's located in `data/sherpa/LHC-LO-ZplusJet/RUn.dat`
2. Create a "Gridpack", bascially caluclating integrals. This means we need to execute the following command in the directory of the `Run.dat` file: `["mpirun", "-n", "4", "Sherpa", "-f", self.input().abspath, "-e", "1"]`. This will create a folder called `Process` and the following files, which need to present for the next step: `"Results.db", "MPI_Cross_Sections.dat", "MIG_P+P+_13000_LHA[CT14lo]_1.db"`
4. Run Sherpa to create simulated particle collisions. This means, checking if the files from the previous step are in place and running the following command: `["Sherpa", f"-R {seed}", f"-e {self.events_per_job}", "EVENT_OUTPUT=HepMC3_Short[{}]".format(out_file_name)]`. This step can be implemented as a law workflow, to e.g. execute it with HTCondor in the future. Make sure to encode the branch id in your output file name. Otherwise each branch will overwrite the other.
5. Run Rivet to analyze what we've simulated. Here we can require the SherpaRun workflow and analyse all the simulated events with the following command: `["rivet", f"--histo-file={self.output().abspath}", f"--analysis=ZplusJet_3"] + input_file_paths`

## Some tips
I provide some helper functions in the `utils.py` file. Feel free to use them and ask for help during the exercise :)
