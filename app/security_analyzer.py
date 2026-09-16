import subprocess
import tempfile
import os


def run_bandit(filename, code):
    if not filename.endswith(".py"):
        return []

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [
                "bandit",
                "-f",
                "json",
                "-q",
                temp_file
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)