# Wordle Solver

This is a Wordle solver project that helps you find the correct word for the popular game Wordle. It uses a combination of algorithms and word lists to provide accurate solutions.

## Features

- **Wordle Solver**: The main feature of this project is the Wordle solver algorithm. It takes the input of the Wordle puzzle and provides the correct word as the output.

## Technologies Used

- **Python**: The project is implemented in Python, making use of its powerful string manipulation and algorithmic capabilities.
    - **Z3**: The Z3 Theorem Prover is used to solve the Wordle puzzle by formulating it as a constraint satisfaction problem (CSP).

## How to Install

1. `git clone <repo>`
2. `cd wordle_solver`
3. `python wordle_solver/core.py`

### Installing as a python module
Alternatively you can install the package as a python module and use it from anywhere in your system.
1. After cloning the repo, `cd wordle_solver`
2. `pip install .`
3. `python -m wordle_solver`

## How to Use
- The solver will first give you a word to try.
- Input it, and based on the feedback (*g*reen, *y*ellow, g*r*ay), give it back to the solver
    - E.g. you are given the word `about` and you give back the hints `grrry`
    - Alternatively if you choose in input your own word, you can do so by adding a comma after the hints followed by the chosen words
- Repeat the steps until the correct word is found