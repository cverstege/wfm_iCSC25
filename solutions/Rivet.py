import os

import law
import luigi

from .utils import set_environment_variables, run_command
from .base import BaseTask

from .Sherpa import SherpaRun

class RivetCode(law.ExternalTask):
	def output(self):
		return law.LocalFileTarget(
			os.path.join(
				os.environ.get("ANALYSIS_DATA_PATH"),
				"rivet", "analyses", "Rivet_ZplusJet_3.so"
			)
		)


class RivetRun(BaseTask):
    def requires(self):
        return {"events": SherpaRun(), "analysis": RivetCode()}

    def output(self):
        return self.local_target("rivet", "SherpaZJet.yoda")

    def run(self):
        rivet_env = set_environment_variables(
            os.path.expandvars("$ANALYSIS_PATH/setup/setup_rivet.sh")
        )
        cmd = ["rivet", f"--histo-file={self.output().abspath}", f"--analysis=ZplusJet_3"]
        for target in self.input()["events"]["collection"].targets.values():
            cmd += [target.abspath]
        run_command(cmd, env=rivet_env)

class RivetPlots(BaseTask):
    pass  # not done yet
