

from datetime import date
import os
import sys

import inquirer
import aocd
import dotenv
import markdownify


dotenv.load_dotenv()

today = date.today().timetuple()[0:3]

def set_up_directory(today: tuple[int | int | int]):
  (year, month, day) = today
  this_years_path = os.path.join(str(year))

  if not os.path.isdir(this_years_path):
    if not inquirer.confirm(f"Create directory {this_years_path}{os.path.sep}?"):
      print("Goodbye 👋")
      sys.exit()
    
    os.mkdir(this_years_path)

  if month != 12:
    print(f"Not december yet, come back in {(date(year, 12, 1) - date(year, month, day)).days} days 👋")
    sys.exit()

  todays_path = os.path.join(this_years_path, str(day))

  if not os.path.isdir(todays_path):
    if not inquirer.confirm(f"Create directory {todays_path}{os.path.sep}?"):
      print("Goodbye 👋")
      sys.exit()
    
    os.mkdir(todays_path)

def check_and_inquire_overwrite_file(file_path, data, double_check: bool = False):
  if os.path.isfile(file_path):
    file = open(file_path, "r",encoding='utf-8')
    file_contents = file.read()
    file.close()

    if file_contents != data:  
      if not inquirer.confirm(f"⚠️ File ({file_path}) already exists and has different input (Maybe because you unlocked part b). Overwrite?"):
        return False
      if double_check and not inquirer.confirm("⚠️⚠️⚠️ Are you sure? This will delete any changes you've made."):
        return False
  
  return True

def write_file_in_date_folder(date, file_name, data):
  (year, month, day) = date
  date_dir = os.path.join(str(year), str(day))
  file_path = os.path.join(date_dir, file_name)

  if check_and_inquire_overwrite_file(file_path, data):  
    file = open(file_path, "w")
    file.write(data)
    file.close()

def load_data_from_aoc(date: tuple[int | int | int]):
  (year, month, day) = date
  try:
    puzzle = aocd.models.Puzzle(year=year, day=day)
  except (aocd.exceptions.DeadTokenError, aocd.exceptions.AocdError):
    print("Invalid AOC_SESSION token. Get a new one by inspecting network in browser and copying cookie. 👋")
    sys.exit()


  # Instructions
  prose = puzzle._get_prose()
  article = prose[prose.find("<article"):prose.find("</article>") + len("</article>")]
  cleaned_article = markdownify.markdownify(article, heading_style="ATX")
  write_file_in_date_folder(date, "README.md", cleaned_article)
  write_file_in_date_folder(date, "NOTES.md", "# Notes")
  
  # Examples
  if puzzle.examples:
    for i, example in enumerate(puzzle.examples):
      write_file_in_date_folder(date, f"test_input_{i}.txt", example.input_data)
      write_file_in_date_folder(date, f"test_answer_a_{i}.txt", example.answer_a)
      if example.answer_b:
        write_file_in_date_folder(date, f"test_input_b_{i}.txt", example.answer_b)

  write_file_in_date_folder(date, "input.txt", puzzle.input_data)


def copy_template_to_date_folder(date: tuple[int | int | int]):
  (year, month, day) = date

  date_dir = os.path.join(str(year), str(day))
  if not inquirer.confirm(f"Create template in {date_dir}?"):
    return

  templates_dir = os.path.join(os.path.dirname(__file__), "templates")
  template_files = os.listdir(templates_dir)

  template_file = inquirer.list_input("Template", choices=template_files)

  new_file = f"{day}{os.path.splitext(template_file)[1]}"
  file_path = os.path.join(date_dir, new_file) 

  python_template = "python_template.py"
  template_path = os.path.join(templates_dir, python_template)
  
  if not inquirer.confirm(f"Create python template {file_path} from {template_path}?"):
    print("Goodbye 👋")
    sys.exit()

  template_file = open(template_path, "r",encoding='utf-8')
  template = template_file.read()
  template_file.close()

  if check_and_inquire_overwrite_file(file_path, template, True):
      new_file = open(file_path, "w",encoding='utf-8')
      new_file.write(template)
      new_file.close()

  
set_up_directory(today)
load_data_from_aoc(today)
copy_template_to_date_folder(today)