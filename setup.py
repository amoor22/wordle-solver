from setuptools import find_packages, setup

setup(
    name="wordle-solver",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wordle-solver=wordle_solver.cli:run",
        ],
    },
)
