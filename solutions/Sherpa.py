import os

import law
import luigi
from .utils import set_environment_variables, run_command
from .base import BaseTask

class SherpaConfig(law.ExternalTask):
    def output(self):
        return law.LocalFileTarget(
            os.path.join(
                os.environ.get("ANALYSIS_DATA_PATH"),
                "sherpa", "LHC-LO-ZplusJet", "Run.dat"
            )
        )


class SherpaBuild(BaseTask):
    campaign = luigi.Parameter(default="LHC-LO-ZplusJet")

    def requires(self):
        return SherpaConfig.req(self)

    def output(self):
        gridpack = {}
        gridpack["Process"] = self.local_dir_target(
            "sherpa", self.campaign, "Process"
        )
        for fname in ("Results.db", "MPI_Cross_Sections.dat", "MIG_P+P+_13000_LHA[CT14lo]_1.db"):
            gridpack[fname] = self.local_target("sherpa", self.campaign, fname)
        return gridpack
    def run(self):
        # get Sherpa env
        sherpa_env = set_environment_variables(
            os.path.expandvars("$ANALYSIS_PATH/setup/setup_sherpa.sh")
        )
        command = ["mpirun", "-n", "4", "Sherpa", "-f", self.input().abspath, "-e", "1"]
        work_dir = os.path.abspath(self.input().parent.path)
        run_command(command, env=sherpa_env, cwd=work_dir)


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
        # Each job requires the sherpa setup to be present
        req = {}
        req["config"] = SherpaConfig.req(self)
        req["build"] = SherpaBuild.req(self)
        return req

    def create_branch_map(self):
        # each run job is refrenced to a seed
        return {jobnum: seed for jobnum, seed in enumerate(range(self.start_seed, self.start_seed+self.number_of_jobs))}

    def output(self):
        return self.local_target(
    		"sherpa", "events", f"job_{self.branch}.hepmc"
		)

    def run(self):
        seed = int(self.branch_data)
        command = ["Sherpa", f"-R {seed}", f"-e {self.events_per_job}", "EVENT_OUTPUT=HepMC3_Short[{}]".format(self.output().basename)]
        sherpa_env = set_environment_variables(
            os.path.expandvars("$ANALYSIS_PATH/setup/setup_sherpa.sh")
        )
        work_dir = os.path.abspath(self.workflow_input()["config"].parent.path)
        run_command(command, env=sherpa_env, cwd=work_dir)
        self.output().makedirs()
        self.output().move_from(os.path.join(work_dir, self.output().basename))
