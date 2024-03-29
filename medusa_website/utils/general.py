import logging
import subprocess
from pathlib import Path
from typing import Dict, Iterable, Sized, Union

import colorlog


def get_pretty_logger(name: str):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    _logger = colorlog.getLogger(name)
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)
    _logger.propagate = True
    return _logger


logger = get_pretty_logger(__name__)


def traces_sampler(sampling_context: Dict):
    # https://docs.sentry.io/platforms/python/guides/django/configuration/sampling/
    # Always inherit parent
    if sampling_context["parent_sampled"] is not None:
        return sampling_context["parent_sampled"]
    if sampling_context.get("wsgi_environ", {}).get("PATH_INFO") == "/martor/markdownify/":
        return 0.0
    return 1.0


def run_cmd(cmd: str, cwd: Union[Path, str] = None, capture_output=False, check=True, shell=True, timeout=30):
    from django.conf import settings

    cwd = cwd or settings.ROOT_DIR
    if isinstance(cwd, Path):
        cwd = str(cwd.absolute())

    logger.debug(f"Running cmd: \n{cmd}")
    r = subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        shell=shell,
        capture_output=capture_output,
        timeout=timeout,
        executable="/bin/bash",
    )
    if r.returncode != 0 and check is False:
        logger.error(r.stderr)
        raise Exception(
            f"Exception raised when calling cmd: {cmd}\n"
            f"stderr: {r.stderr if r.stderr else 'None'}\n"
            f"stdout: {r.stdout if r.stdout else 'None'}"
        )
    if capture_output:
        logger.info(f"Captured output\n{r.stdout}")
    return r


def chunks(l: Sized, n: int):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]
