#!/bin/bash

# input="1abc2\npqr3stu8vwx a1b2c3d4e5f treb7uchet"

input=$(tr '\n' ' ' < input.txt)



digit_or_reverse_regex="[0-9]|one|eno|two|owt|three|eerht|four|ruof|five|evif|six|xis|seven|neves|eight|thgie|nine|enin"
get_digits_regex="[^0-9\ ]*([0-9]?)[^\ ]*([0-9]+)[^0-9\ ]*[\ ]?"
first_word_regex="^[^\ ]+"

convert_first_number_string_to_int () {
  input=$1
  if [[ "${input}" =~ $digit_or_reverse_regex ]]; then
    num_string=${BASH_REMATCH[0]}
    num=$(convert_number_string_to_int ${num_string})
    result=$(echo $input | sed "s/${num_string}/${num}/")
  else
    result=$input
  fi

  echo $result
}

convert_last_number_string_to_int () {
  input=$(echo $1 | rev)
  if [[ "${input}" =~ $digit_or_reverse_regex ]]; then
    num_string=${BASH_REMATCH[0]}
    num=$(convert_number_string_to_int $(echo ${num_string} | rev))
    result=$(echo $input | sed "s/${num_string}/${num}/")
  else
    result=$input
  fi

  echo $result | rev
}

convert_number_string_to_int () {
  case $1 in
    one) 
      echo -n "1"
      ;;
    two) 
      echo -n "2"
      ;;
    three) 
      echo -n "3"
      ;;
    four) 
      echo -n "4"
      ;;
    five) 
      echo -n "5"
      ;;
    six) 
      echo -n "6"
      ;;
    seven) 
      echo -n "7"
      ;;
    eight) 
      echo -n "8"
      ;;
    nine) 
      echo -n "9"
      ;;
    *)
      echo -n $1
      ;;
  esac
}

# echo $first_word_regex

left_to_process=$input

sum=0
count=0

while [[ ${#left_to_process} > 0 ]]; do
  amount_of_chars=${#left_to_process}
  
  if [[ "${left_to_process}" =~ $first_word_regex ]]; then 
    word=${BASH_REMATCH[0]}
    string=$word
    string=$(convert_first_number_string_to_int "${string}")
    string=$(convert_last_number_string_to_int "${string}")

    if [[ "${string}" =~ $get_digits_regex ]]; then
      # echo ${BASH_REMATCH[0]}
      num_1=${BASH_REMATCH[1]:-$num_2}
      num_2=${BASH_REMATCH[2]}
      value=$(($num_1 * 10 + $num_2))
      sum=$(($sum + $value))
      echo "${word}: ${num_1} ${num_2} (${value}) --> $sum"
    else 
      echo "no match"
    fi
    left_to_process=$(echo ${left_to_process:${#word}} | xargs)
  fi
  if [[ "$amount_of_chars" -eq "${#left_to_process}" ]]; then
    left_to_process=
  fi
done

echo "sum: ${sum}"
