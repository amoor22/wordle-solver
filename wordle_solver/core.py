from argparse import ArgumentParser
from pathlib import Path
from typing import List

import pandas as pd
from art import text2art
from rich.box import SQUARE
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from z3 import *

from .utils import Attempt, Hint

console = Console()


def display_title():
    # Display title, centered
    title = Text(text2art("Wordle  Solver"), style="bold cyan")
    console.print(title)


def display_board(attempts: List[Attempt], word_length: int):
    table = Table(show_header=False, border_style="bold", box=SQUARE)
    for attempt in attempts:
        row = []
        for _, letter, hint in attempt:
            if hint == Hint.GREEN:
                color = "green"
            elif hint == Hint.YELLOW:
                color = "yellow"
            else:
                color = "white"
            row.append(f"[{color}]{letter.upper()}[/{color}]")
        table.add_row(*row)

    # Add empty rows if needed
    for _ in range(6 - len(attempts)):
        table.add_row(*[" " * word_length])

    console.print(Panel(table, title="Wordle Board", border_style="cyan"))


def process_attempt(solver: Solver, word_vecs: List[BitVec], attempt: Attempt):
    for index, letter, hint in attempt:
        if hint is Hint.GREY:
            duplicate_with_green = list(
                filter(lambda z: z[2] is Hint.GREEN and z[1] == letter, attempt)
            )
            duplicate_with_yellow = list(
                filter(lambda z: z[2] is Hint.YELLOW and z[1] == letter, attempt)
            )
            cannot_be = set(word_vecs)
            for i, _, _ in duplicate_with_green + duplicate_with_yellow:
                cannot_be -= {word_vecs[i]}
            for char in cannot_be:
                solver.add(char != ord(letter))
        elif hint is Hint.GREEN:
            solver.add(word_vecs[index] == ord(letter))
        elif hint is Hint.YELLOW:
            all_vecs_but_current = word_vecs.copy()
            all_vecs_but_current.remove(word_vecs[index])
            solver.add(Or(*[v == ord(letter) for v in all_vecs_but_current]))
            solver.add(word_vecs[index] != ord(letter))


def check_uniqueness(solver: Solver, bitvectors: List[BitVec]) -> bool:
    solver_copy = Solver()
    solver_copy.add(solver.assertions())
    if solver_copy.check() == sat:
        model = solver_copy.model()
        answer = [model[char] for char in bitvectors]
        solver_copy.add(Or(*[char != ans for char, ans in zip(bitvectors, answer)]))
        return not (solver_copy.check() == sat)
    return False


def filter_valid_words(solver: Solver, words: List[str], bitvectors: List[BitVec]):
    solver_copy = Solver()
    solver_copy.add(solver.assertions())
    valid_words = []
    for word in words:
        solver_copy.push()
        for i, letter in enumerate(word):
            solver_copy.add(bitvectors[i] == ord(letter))
        if solver_copy.check() == sat:
            valid_words.append(word)
        solver_copy.pop()
    return valid_words


def main(length: int):
    display_title()
    word_vecs = [BitVec(f"word_{i}", 8) for i in range(length)]
    solver = Solver()
    for char in word_vecs:
        solver.append(char >= ord("a"), char <= ord("z"))
    frequency_list = pd.read_csv(Path(__file__).parent / "unigram_freq.csv")
    frequency_list = frequency_list[frequency_list["word"].str.len() == length]
    valid_words = frequency_list["word"].tolist()
    color_to_hint_mapping = {"g": Hint.GREEN, "r": Hint.GREY, "y": Hint.YELLOW}
    attempts = []
    while True:
        if not valid_words:
            console.print("[bold red]No valid words left to try![/bold red]")
            exit(1)
        word_to_try = valid_words[0]
        console.print(
            f"[bold cyan]Word to try:[/bold cyan] [yellow]{word_to_try}[/yellow]"
        )
        attempt_input = Prompt.ask(
            "Enter the colors of the letters i.e. hints {(g)reen/g(r)ey/(y)ellow}[, CUSTOM_WORD]"
        )
        if len(attempt_input.strip()) > length:
            attempt_input, word_to_try = attempt_input.split(",")
            word_to_try = word_to_try.strip()
        attempt = Attempt(word_to_try)
        attempt.hints = [
            color_to_hint_mapping[hint] for hint in attempt_input[:length]
        ]
        attempts.append(attempt)
        process_attempt(solver, word_vecs, attempt)
        valid_words = filter_valid_words(solver, valid_words, word_vecs)

        display_board(attempts, length)

        if check_uniqueness(solver, word_vecs):
            console.print("[bold green]Unique solution found![/bold green]")
            break

        console.print(
            f"[bold blue]Remaining valid words:[/bold blue] {len(valid_words)}"
        )


def cli():
    parser = ArgumentParser(
        prog="wordle_solver",
        usage="python/python3 -m wordle_solver",
        description="Wordle Solver using Z3",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=5,
        required=False,
        help="length of the word to solve",
    )
    args = parser.parse_args()

    main(length=args.length)


if __name__ == "__main__":
    cli()
