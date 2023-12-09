import inquirer


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
