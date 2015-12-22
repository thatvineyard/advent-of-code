#!/usr/local/bin/perl
use Switch;

print "Captain Eggnog's Directions: \n";


$x = 0;
$y = 0;

$x_min = 0;
$y_min = 0;

# get input string
$directions = <>;
$get_minimum_values = $directions;

#get minimum value for x and y
while(length($get_minimum_values) > 1) {
    # check first char, and update coordinates appropriately
    switch(substr($get_minimum_values, 0, 1)) {
	case "^" {$y++}
	case "v" {$y--; if($y < $y_min) {$y_min = $y;}}
	case "<" {$x--; if($x < $x_min) {$x_min = $x;}}
	case ">" {$x++}	
    }
    # cut first character from string
    $get_minimum_values = substr($get_minimum_values, 1);
}

# reset coordinates
$x = -$x_min;
$y = -$y_min;

# create matrix and gift first house
@house_matrix;
$house_matrix[$x][$y] = 1;
$houses_visited = 1;

while(length($directions) > 1) {
    # check first char, and update coordinates appropriately
    switch(substr($directions, 0, 1)) {
	case "^" {$y++}
	case "v" {$y--}
	case "<" {$x--}
	case ">" {$x++}	
    }

    # check house and update values
    if($house_matrix[$x][$y] != 1) {
	$house_matrix[$x][$y] = 1;
	$houses_visited++;
    }
    
    # cut first character from string
    $directions = substr($directions, 1);
}

# print houses visited
print $houses_visited . "\n";
