import argparse
import os
import sys

import inquirer
import aocd
import dotenv
import markdownify

from libraries import file_manager, cli


parser = argparse.ArgumentParser("Advent of Code Setupper")
parser.add_argument("-d", "--date", required=False)
args = parser.parse_args()

dotenv.load_dotenv()


def set_up_directory(for_date: tuple[int | int | int]):
    file_manager.set_up_year_directory(
        for_date, lambda path: inquirer.confirm(f"Create directory {path}?")
    )
    file_manager.quit_if_dir_missing(
        file_manager.get_year_dir(for_date),
        "Can't continue without year directory. Quitting",
    )
    file_manager.set_up_day_directory(
        for_date, lambda path: inquirer.confirm(f"Create directory {path}?")
    )
    file_manager.quit_if_dir_missing(
        file_manager.get_date_dir(for_date),
        "Can't continue without date directory. Quitting",
    )


def load_data_from_aoc(for_date: tuple[int | int | int]):
    (year, _, day) = for_date
    try:
        puzzle = aocd.models.Puzzle(year=year, day=day)
    except (aocd.exceptions.DeadTokenError, aocd.exceptions.AocdError):
        print(
            "Invalid AOC_SESSION token. Get a new one by inspecting network in browser and copying cookie. 👋"
        )
        sys.exit()

    # Instructions
    prose = puzzle._get_prose()
    article_a = prose[
        prose.find("<article") : prose.find("</article>") + len("</article>")
    ]
    prose = prose[prose.find("</article>") + len("</article>") :]
    article_b = prose[
        prose.find("<article") : prose.find("</article>") + len("</article>")
    ]
    cleaned_article = markdownify.markdownify(
        article_a + article_b, heading_style="ATX"
    )
    file_manager.write_file_in_date_folder(
        for_date, "README.md", cleaned_article, cli.check_and_inquire_overwrite_file
    )
    file_manager.write_file_in_date_folder(
        for_date, "NOTES.md", "# Notes", cli.check_and_inquire_overwrite_file
    )

    # Examples
    if puzzle.examples:
        for i, example in enumerate(puzzle.examples):
            if i == 0:
                postfix = ""
            else:
                postfix = f"_extra_{i}"
            if example.input_data:
                file_manager.write_file_in_date_folder(
                    for_date,
                    f"test_input{postfix}.txt",
                    example.input_data,
                    cli.check_and_inquire_overwrite_file,
                )
            if example.answer_a:
                file_manager.write_file_in_date_folder(
                    for_date,
                    f"test_answer_a{postfix}.txt",
                    example.answer_a,
                    cli.check_and_inquire_overwrite_file,
                )
            if example.answer_b:
                file_manager.write_file_in_date_folder(
                    for_date,
                    f"test_answer_b{postfix}.txt",
                    example.answer_b,
                    cli.check_and_inquire_overwrite_file,
                )

    file_manager.write_file_in_date_folder(
        for_date,
        "input.txt",
        puzzle.input_data,
        cli.check_and_inquire_overwrite_file,
    )


def copy_template_to_date_folder(date: tuple[int | int | int]):
    (_, _, day) = date

    template_files = file_manager.get_template_files()
    no_template_choice = "No template (Exit)"

    template_file_choice = inquirer.list_input(
        "Template", choices=[no_template_choice, *template_files]
    )

    if template_file_choice == no_template_choice:
        return

    new_file_name = f"{day}{os.path.splitext(template_file_choice)[1]}"

    template_data = file_manager.get_template_data(template_file_choice)

    file_manager.write_file_in_date_folder(
        date,
        new_file_name,
        template_data,
        cli.check_and_inquire_overwrite_file,
    )


setup_date = cli.get_date()

set_up_directory(setup_date)
load_data_from_aoc(setup_date)
copy_template_to_date_folder(setup_date)
print("Good luck! 🎅")
sys.exit()
