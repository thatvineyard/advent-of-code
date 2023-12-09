from datetime import date
from genericpath import isdir
import os
import sys
from typing import Callable


# DIRECTORY


def quit_if_dir_missing(dir_path: str, message: str):
    if not os.path.isdir(dir_path):
        print(message)
        sys.exit(0)


def get_year_dir(date: tuple[int | int | int]):
    (year, _, _) = date
    return os.path.join(str(year))


def get_date_dir(date: tuple[int | int | int]):
    (_, _, day) = date
    return os.path.join(get_year_dir(date), str(day))


def set_up_year_directory(
    forDate: tuple[int | int | int], confirm: Callable[[str], bool]
):
    this_years_path = get_year_dir(forDate)

    if not os.path.isdir(this_years_path):
        if not confirm(this_years_path):
            return

        os.mkdir(this_years_path)


def set_up_day_directory(
    forDate: tuple[int | int | int], confirm: Callable[[str], bool]
):
    (year, month, day) = forDate
    if month != 12:
        print(
            f"Not december yet, come back in {(date(year, 12, 1) - date(year, month, day)).days} days 👋"
        )
        return

    date_path = get_date_dir(forDate)

    if not os.path.isdir(date_path):
        if not confirm(date_path):
            return

        os.mkdir(date_path)


# TEMPLATES


def get_template_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "..", "templates")


def get_template_files() -> list[str]:
    return os.listdir(get_template_dir())


def get_template_data(file_name: str) -> bytearray:
    template_path = os.path.join(get_template_dir(), file_name)

    template_file_choice = open(template_path, "r", encoding="utf-8")
    template_data = template_file_choice.read()
    template_file_choice.close()

    return template_data


# WRITING


def write_file_in_date_folder(
    date: tuple[int | int | int],
    file_name: str,
    data: bytearray,
    continueOnDataChanged: Callable[[str], bool],
):
    """Write file with given filename in the date's directory. If continueOnDateChanged is set, when changes are detected run and only continue saving on a True result.

    Args:
        date (tuple[int | int | int]): Date
        file_name (str): Name of the file
        data (bytearray): Date to save
        continueOnDataChanged (Callable[[str], bool]): Callback which takes in a filepath and should returns True if saving should continue if data has changed.

    Raises:
        ValueError:
    """

    if not file_name:
        raise ValueError("Could not save because file name missing")
    if not data:
        raise ValueError("Could not save because data missing")

    date_dir = get_date_dir(date)
    file_path = os.path.join(date_dir, file_name)

    if (
        data_is_different_from_file(file_path, data)
        and continueOnDataChanged
        and not continueOnDataChanged(file_path)
    ):
        print(f"{file_path} is unchanged")
        return

    file = open(file_path, "w", encoding="utf-8")
    file.write(data)
    file.close()


def data_is_different_from_file(file_path, data):
    if os.path.isfile(file_path):
        file = open(file_path, "r", encoding="utf-8")
        file_contents = file.read()
        file.close()

        if file_contents != data:
            return True

    return False
