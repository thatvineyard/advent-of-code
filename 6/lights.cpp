#include <fstream>
#include<stdio.h>
#define X_MAX 10
#define Y_MAX 10



int how_many_are_on(bool light_matrix[X_MAX][Y_MAX]) {
  int count = 0;
  
  for(int i = 0; i < X_MAX; i++) {
    for(int j = 0; j < Y_MAX; i++) {
      count += light_matrix[i][j] == true ? 1 : 0;
    }
  }
}

void execute_instruction(bool light_matrix[X_MAX][Y_MAX], std::string instruction) {
  // find first word and update cursor
  int cursor = 0;
  std::string substring = instruction.substr(cursor, instruction.find(' '));
  cursor = instruction.find(' ', cursor);

  
  if(substring == "toggle\n") {
    printf("toggle");
    
  } else if(substring == "turn") {
    printf("turn");

    // find next word
    substring = instruction.substr(cursor, instruction.find(' '));
    cursor = instruction.find(' ', cursor);

    if(substring == "on") {
      printf("on\n");      
    } else if(substring == "off") {
      printf("off\n");      
    }
  }
}

int main() {

  bool light_matrix[X_MAX][Y_MAX];

  std::ifstream inputfile("input.txt");
  std::string line;
  
  while(std::getline(inputfile, line)) {
    if(line.length() > 0) {
      execute_instruction(light_matrix, line);
    }
  }
  

  
  return 1;
}
