#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#define X_MAX 1000
#define Y_MAX 1000



int how_bright_is_it(int light_matrix[X_MAX][Y_MAX]) {
  int count = 0;
  
  for(int x = 0; x < X_MAX; x++) {
    for(int y = 0; y < Y_MAX; y++) {
      count += light_matrix[x][y];
    }
  }
  return count;
}

void execute_instruction(int light_matrix[X_MAX][Y_MAX], std::string instruction) {
  int instruction_code = -1; // 0 = toggle, 1 = turn on, 2 = turn off
  
  int x_start = -1;
  int x_end = -1;
  int y_start = -1;
  int y_end = -1;
 
  // find first word and update cursor
  int cursor = 0;
  std::string word;
  word = instruction.substr(cursor, instruction.find(' ', cursor) - cursor);
  cursor = instruction.find(' ', cursor) + 1;
  
  
  if(word == "toggle") {
    instruction_code = 0;
  } else if(word == "turn") {
    // find next word
    word = instruction.substr(cursor, instruction.find(' ', cursor) - cursor);
    cursor = instruction.find(' ', cursor) + 1;
  
    if(word == "on") {
      instruction_code = 1;
    } else if(word == "off") {
      instruction_code = 2;
    } else {
      instruction_code = -1;
    }
  } else {
    instruction_code = -1;
  }

  // find range bottom
  // find next word
  word = instruction.substr(cursor, instruction.find(' ', cursor) - cursor);
  cursor = instruction.find(' ', cursor) + 1;

  x_start = atoi(word.substr(0, word.find(',')).c_str());
  y_start = atoi(word.substr(word.find(',')+1).c_str());

  // find next word
  word = instruction.substr(cursor, instruction.find(' ', cursor) - cursor);
  cursor = instruction.find(' ', cursor) + 1;
  if(word != "through") {
    printf("Error\n");
  }

  // find range top
  // find next word
  word = instruction.substr(cursor, instruction.find(' ', cursor) - cursor);
  cursor = instruction.find(' ', cursor) + 1;

  x_end = atoi(word.substr(0, word.find(',')).c_str());
  y_end = atoi(word.substr(word.find(',')+1).c_str());
  
  for(int x = x_start; x <= x_end; x++) {
    for(int y = y_start; y <= y_end; y++) {
      switch(instruction_code) {
      case 0:
	light_matrix[x][y] += 2; 
	break;
      case 1:
	light_matrix[x][y] += 1;
	break;
      case 2:
	if(light_matrix[x][y] > 0) {
	  light_matrix[x][y] -= 1;
	}
	break;
      default:
	break;
      }
    }
  }
}

void print_matrix(int matrix[X_MAX][Y_MAX]) {
  for(int x = 0; x < X_MAX; x++) {
    for(int y = 0; y < Y_MAX; y++) {
      printf("%d,%d: %d\n", x, y, matrix[x][y]);
    }
  }
}

int main() {

  int light_matrix[X_MAX][Y_MAX];

  for(int x = 0; x < X_MAX; x++) {
    for(int y = 0; y < Y_MAX; y++) {
      light_matrix[x][y] = 0;
    }
  }
  
  std::ifstream inputfile("input.txt");
  std::string line;
  
  while(std::getline(inputfile, line)) {
    if(line.length() > 0) {
      execute_instruction(light_matrix, line);
    }
  }

  printf("It's this bright: %d!\n", how_bright_is_it(light_matrix));

  return 1;
}
