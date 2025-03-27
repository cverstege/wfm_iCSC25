import os

import law
import luigi
from .utils import set_environment_variables, run_command
from .base import BaseTask

class SherpaConfig(law.ExternalTask):
    def output(self):
        # YOUR CODE HERE
        pass


class SherpaBuild(BaseTask):
    campaign = luigi.Parameter(default="LHC-LO-ZplusJet")

    def requires(self):
        # YOUR CODE HERE
        pass

    def output(self):
        # YOUR CODE HERE
        pass

    def run(self):
        # get Sherpa env
        sherpa_env = set_environment_variables(
            os.path.expandvars("$ANALYSIS_PATH/setup/setup_sherpa.sh")
        )
        # YOUR CODE HERE
        pass


class SherpaRun(BaseTask, law.LocalWorkflow):
    # configuration variables
    start_seed = luigi.IntParameter(
        default=42,
        description="Start seed for random generation of individual job seeds. Currently not used!",
    )
    number_of_jobs = luigi.IntParameter(
        default=2,
        description="Number of individual generation jobs. Each will generate statistically independent events.",
    )
    events_per_job = luigi.IntParameter(
        default=10000, description="Number of events generated in each job."
    )

    def workflow_requires(self):
        # YOUR CODE HERE
        pass

    def create_branch_map(self):
        # each run job is refrenced to a seed
        # YOUR CODE HERE
        pass

    def output(self):
        # YOUR CODE HERE
        pass

    def run(self):
        # YOUR CODE HERE
        pass
