import os
import law


class BaseTask(law.Task):
    def local_path(self, *path):
        path = os.path.join(
            "$ANALYSIS_DATA_PATH", *path
        )
        path = os.path.expandvars(path)
        return path

    def local_target(self, *path):
        return law.LocalFileTarget(self.local_path(*path))

    def local_dir_target(self, *path):
        return law.LocalDirectoryTarget(self.local_path(*path))
