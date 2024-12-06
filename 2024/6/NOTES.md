# Notes
- directions: ^ > v <
- barrier: #
  - check desired location for barrier before move
- robot instructions
  - if barrier: rotate right
  - else: step forward
- when robot leaves the map the calculation can end

- robot behavior:
  1. add position to visited set
  2. check forward
    - if outside of map boundary: exit
    - if barrier: turn right
    - else: move forward