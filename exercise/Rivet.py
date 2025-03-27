import os

import law
import luigi

from .utils import set_environment_variables, run_command
from .base import BaseTask

from .Sherpa import SherpaRun

class RivetCode(law.ExternalTask):
	def output(self):
        # YOUR CODE HERE
        pass


class RivetRun(BaseTask):
    def requires(self):
        # YOUR CODE HERE
        pass

    def output(self):
        # YOUR CODE HERE
        pass

    def run(self):
        # YOUR CODE HERE
        pass

class RivetPlots(BaseTask):
    pass  # not done yet
