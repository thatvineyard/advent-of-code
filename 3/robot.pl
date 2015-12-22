#!/usr/local/bin/perl
use Switch;

print "Captain Eggnog's Directions: \n";


$real_x = 0;
$real_y = 0;
$robot_x = 0;
$robot_y = 0;

$x_min = 0;
$y_min = 0;

$real_or_robot = 0; # 0 -> real, 1 -> robot

# get input string
$directions = <>;
$get_minimum_values = $directions;

#get minimum value for x and y
while(length($get_minimum_values) > 1) {
    # check first char, and update coordinates appropriately
    if($real_or_robot == 0) {
	switch(substr($get_minimum_values, 0, 1)) {
	    case "^" {$real_y++}
	    case "v" {$real_y--; if($real_y < $y_min) {$y_min = $real_y;}}
	    case "<" {$real_x--; if($real_x < $x_min) {$x_min = $real_x;}}
	    case ">" {$real_x++}	
	}
	$real_or_robot = 1;
    } else {
	switch(substr($get_minimum_values, 0, 1)) {
	    case "^" {$robot_y++}
	    case "v" {$robot_y--; if($robot_y < $y_min) {$y_min = $robot_y;}}
	    case "<" {$robot_x--; if($robot_x < $x_min) {$x_min = $robot_x;}}
	    case ">" {$robot_x++}	
	}
	$real_or_robot = 0;
    }
    # cut first character from string
    $get_minimum_values = substr($get_minimum_values, 1);
    
}

# reset coordinates
$real_x = -$x_min;
$real_y = -$y_min;
$robot_x = -$x_min;
$robot_y = -$y_min;

# create matrix and gift first house
@house_matrix;
$house_matrix[$real_x][$real_y] = 1;
$houses_visited = 1;

while(length($directions) > 1) {
    # check first char, and update coordinates appropriately
    if($real_or_robot == 0) {
	switch(substr($directions, 0, 1)) {
	    case "^" {$real_y++}
	    case "v" {$real_y--}
	    case "<" {$real_x--}
	    case ">" {$real_x++}	
	}
	# check house and update values
	if($house_matrix[$real_x][$real_y] != 1) {
	    $house_matrix[$real_x][$real_y] = 1;
	    $houses_visited++;
	}
	$real_or_robot = 1;
    } else {
	switch(substr($directions, 0, 1)) {
	    case "^" {$robot_y++}
	    case "v" {$robot_y--}
	    case "<" {$robot_x--}
	    case ">" {$robot_x++}	
	}
	# check house and update values
	if($house_matrix[$robot_x][$robot_y] != 1) {
	    $house_matrix[$robot_x][$robot_y] = 1;
	    $houses_visited++;
	}
	$real_or_robot = 0;
    }
    # cut first character from string
    $directions = substr($directions, 1);
}

# print houses visited
print $houses_visited . "\n";
