""" Collection of useful helper functions.
"""
import os
from subprocess import PIPE

from law.logger import get_logger
from law.util import interruptable_popen

logger = get_logger(__name__)

source_env = dict()
for var in (
    "X509_USER_PROXY",
    "HOME",
    "ANALYSIS_PATH",
    "ANALYSIS_DATA_PATH",
    "RIVET_ANALYSIS_PATH",
):
    try:
        source_env[var] = os.environ[var]
    except KeyError as e:
        logger.warning(f"KeyError: {e}, variable undefined on local host!")


def _convert_env_to_dict(env):
    my_env = {}
    for line in env.splitlines():
        if line.find(" ") < 0:
            try:
                key, value = line.split("=", 1)
                my_env[key] = value
            except ValueError:
                pass
    return my_env


def set_environment_variables(source_script_path):
    """Creates a subprocess readable environment dict

    Args:
        source_script_path (str): Path to the file sourcing the environment

    Raises:
        RuntimeError: Raised when environment couldn't be sourced

    Returns:
        dict: Environment variables
    """
    code, out, error = interruptable_popen(
        "source {}; env".format(source_script_path),
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        env=source_env,
    )
    if code != 0:
        raise RuntimeError(
            "Sourcing environment from {source_script_path} failed with error code {code}!\n".format(
                source_script_path=source_script_path, code=code
            )
            + "Output:\n{}\n".format(out)
            + "Error:\n{}\n".format(error)
        )
    my_env = _convert_env_to_dict(out)
    return my_env

def run_command(executable, env, *args, **kwargs):
    """Helper function for execution of a command in a subprocess.

    Args:
        executable (List[str]): Command to execute
        env (Dict): Environment for the execution

    Raises:
        RuntimeError: Terminate when subprocess failed. Throw command, error and output streams.

    Returns:
        tuple[int | Any, Any | str, Any | str]: execution code, output string and error string
    """
    command_str = " ".join(executable)
    logger.info(f"Running: {' '.join(executable[:3])}...")
    logger.debug(f'Full command:\n"{command_str}"')
    code, out, error = interruptable_popen(
        executable, *args, stdout=PIPE, stderr=PIPE, env=env, **kwargs
    )
    if code != 0:
        import pprint

        pretty_env = pprint.pformat(env, indent=4)
        logger.debug("Env:\n{}".format(pretty_env))
        logger.error("Output:\n{}".format(out))
        logger.error("Error:\n{}".format(error))
        raise RuntimeError(
            "Command {command} returned non-zero exit status {code}!\n".format(
                command=executable, code=code
            )
        )
    logger.info("Output:\n{}".format(out))
    if error:
        logger.warning(f"Error:\n{error}")
    return code, out, error
