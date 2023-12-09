# Notes

## Part A
- Each line is a history of a single value
- Predict next step
  - By creating a new sequence from the difference in each step
    - Note this means the list gets shorter, because you're looking at what's between each step 
  - Break on all zeroes
  - Then add a new zero and go back up, calculating what would be next