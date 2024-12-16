import argparse
from datetime import datetime
import dotenv
import inquirer

# ARGS

parser = argparse.ArgumentParser("Advent of Code Setupper")
parser.add_argument("-d", "--date", required=False)
parser.add_argument("-a", "--forcea", action="store_true", required=False)
parser.add_argument("-b", "--forceb", action="store_true", required=False)
args = parser.parse_args()


def get_date() -> tuple[int, int, int]:
    if not args.date:
        now = datetime.today()
        print(f"⚙️  Using today's date ({now.date()})")
        return now.timetuple()[0:3]

    return datetime.strptime(args.date, "%Y-%m-%d").date().timetuple()[0:3]


def get_force_a() -> bool:
    if not args.forcea:
        return False
    return args.forcea

def get_force_b() -> bool:
    if not args.forceb:
        return False
    return args.forceb

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
