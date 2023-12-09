import argparse
from datetime import datetime
import dotenv
import inquirer

# ARGS

parser = argparse.ArgumentParser("Advent of Code Setupper")
parser.add_argument("-d", "--date", required=False)
args = parser.parse_args()


def get_date() -> tuple[int, int, int]:
    if not args.date:
        return datetime.date.today().timetuple()[0:3]

    return datetime.strptime(args.date, "%Y-%m-%d").date().timetuple()[0:3]


# ENV

dotenv.load_dotenv()

# PROMPTS


def check_and_inquire_overwrite_file(file_path: str):
    if not inquirer.confirm(
        f"⚠️ File ({file_path}) already exists and has different input (Maybe because you unlocked part b). Overwrite?"
    ):
        return False
    if not inquirer.confirm(
        "⚠️⚠️⚠️ Are you sure? This will delete any changes you've made."
    ):
        return False

    return True
