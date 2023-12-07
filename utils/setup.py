

import argparse
from datetime import date, datetime
import os
import sys

import inquirer
import aocd
import dotenv
import markdownify


parser = argparse.ArgumentParser("Advent of Code Setupper")
parser.add_argument("-d", "--date", required=False)
args = parser.parse_args()

dotenv.load_dotenv()

if args.date:
  setup_date = datetime.strptime(args.date, '%Y-%m-%d').date().timetuple()[0:3]
else:
  setup_date = date.today().timetuple()[0:3]

def get_year_dir(date: tuple[int | int | int]):
  (year, _, _) = date
  return os.path.join(str(year))

def get_date_dir(date: tuple[int | int | int]):
  (_, _, day) = date
  return os.path.join(get_year_dir(date), str(day))

def set_up_directory(date: tuple[int | int | int]):
  (year, month, day) = date
  this_years_path = get_year_dir(date)

  if not os.path.isdir(this_years_path):
    if not inquirer.confirm(f"Create directory {this_years_path}{os.path.sep}?"):
      print("Goodbye 👋")
      sys.exit()
    
    os.mkdir(this_years_path)

  if month != 12:
    print(f"Not december yet, come back in {(date(year, 12, 1) - date(year, month, day)).days} days 👋")
    sys.exit()

  date_path = get_date_dir(date)

  if not os.path.isdir(date_path):
    if not inquirer.confirm(f"Create directory {date_path}{os.path.sep}?"):
      print("Goodbye 👋")
      sys.exit()
    
    os.mkdir(date_path)

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
  date_dir = get_date_dir(date)
  file_path = os.path.join(date_dir, file_name)

  if check_and_inquire_overwrite_file(file_path, data):  
    if file_path and data:
      file = open(file_path, "w")
      file.write(data)
      file.close()

def load_data_from_aoc(date: tuple[int | int | int]):
  (year, _, day) = date
  try:
    puzzle = aocd.models.Puzzle(year=year, day=day)
  except (aocd.exceptions.DeadTokenError, aocd.exceptions.AocdError):
    print("Invalid AOC_SESSION token. Get a new one by inspecting network in browser and copying cookie. 👋")
    sys.exit()


  # Instructions
  prose = puzzle._get_prose()
  article_a = prose[prose.find("<article"):prose.find("</article>") + len("</article>")]
  prose = prose[prose.find("</article>") + len("</article>"):]
  article_b = prose[prose.find("<article"):prose.find("</article>") + len("</article>")]
  cleaned_article = markdownify.markdownify(article_a + article_b, heading_style="ATX")
  write_file_in_date_folder(date, "README.md", cleaned_article)
  write_file_in_date_folder(date, "NOTES.md", "# Notes")
  
  # Examples
  if puzzle.examples:
    for i, example in enumerate(puzzle.examples):
      if i == 0:
        postfix = ""
      else:
        postfix = f"_extra_{i}"
      write_file_in_date_folder(date, f"test_input{postfix}.txt", example.input_data)
      write_file_in_date_folder(date, f"test_answer_a{postfix}.txt", example.answer_a)
      write_file_in_date_folder(date, f"test_answer_b{postfix}.txt", example.answer_b)

  write_file_in_date_folder(date, "input.txt", puzzle.input_data)


def copy_template_to_date_folder(date: tuple[int | int | int]):
  (_, _, day) = date

  date_dir = get_date_dir(date)
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

  
set_up_directory(setup_date)
load_data_from_aoc(setup_date)
copy_template_to_date_folder(setup_date)