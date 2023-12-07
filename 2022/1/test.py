import os

print(os.path.splitext(os.path.basename(__file__))[0])
# print(os.path.dirname(__file__).split(os.path.sep)[-3:])
[year, day] = os.path.dirname(__file__).split(os.path.sep)[-2:]
print(year)
print(day)