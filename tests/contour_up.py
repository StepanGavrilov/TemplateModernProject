"""
Generate env for compose-file
and build first-time then up
service
"""

import os
import time

from testcontainers.compose import DockerCompose  # type: ignore

env_file = os.system(
    f"rm -rf {os.getcwd()}/tests/.env &&"
    f" {os.getcwd()}/docker/env.sh Testing"
    f" >> {os.getcwd()}/tests/.env")

if env_file != 0:
    raise Exception(  # NOSONAR
        f"Error with env file for testing."
        f" RM: {os.getcwd()}/tests/.env"
        f" Command: {os.getcwd()}/docker/env.sh Testing"
        f" >> {os.getcwd()}/tests/.env")

with DockerCompose(
        filepath=f"{os.getcwd()}/tests/",
        pull=True,
        build=True
) as compose:
    time.sleep(32)
    stdout, stderr, code = compose.exec_in_container(
        'inter_test_api', [
            "poetry", "run", "pytest",
            "/src/account/tests/test_account.py",
            "--json-report", "--json-report-file",
            "none"
        ]
    )

    if (code != 0) and stderr:
        raise Exception(  # NOSONAR
            f"Integration tests fails: {stderr}"
        )
