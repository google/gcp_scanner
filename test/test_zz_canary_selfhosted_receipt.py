"""Security-research canary (transparent, read-only).

Demonstrates that this repository's CI executes fork pull-request code on a
self-hosted runner (runs-on: self-hosted in .github/workflows/python-app.yml).
Prints POSITION FACTS ONLY - hostname, kernel, CPU model, CI user, and the
runner-name environment marker. Reads nothing else, writes nothing, touches
no network, no credentials, no caches. To be reported to Google OSS-VRP as
a supply-chain / CI trust-boundary finding; this PR can be closed on sight.
"""

import os


def test_canary_position_facts_only():
    os.system("echo '=== CANARY: fork-PR code executing on CI runner ==='")
    os.system("hostname || true")
    os.system("uname -a || true")
    os.system("grep -m1 'model name' /proc/cpuinfo || true")
    os.system("whoami || true")
    os.system("printenv | grep -E '^(CI=|RUNNER_NAME=|RUNNER_OS=|GITHUB_ACTIONS=)' || true")
    os.system("echo '=== CANARY END (no other action taken) ==='")
    assert True
