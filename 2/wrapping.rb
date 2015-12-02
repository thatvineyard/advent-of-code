def calculate_box(box_dimensions)
  box_sides = Array.new(3)
  smallest_side = 0

  for i in 0..2
    box_sides[i] = box_dimensions[i] * box_dimensions[(i+1) % 3]
    if box_sides[i] < box_sides[smallest_side]
      smallest_side = i
    end
  end

  wrapping_paper = 0

  for i in 0..2
    wrapping_paper += box_sides[i] * 2
  end
  wrapping_paper += box_sides[smallest_side] 

  return wrapping_paper
end


if ARGV.length() != 3
  puts "Either input three values as arguments or continue by adding values in the form AxBxC where A, B and C are integers (ex: 2x3x4). Enter an empty line when done."

  box_dimensions = Array.new(3, 0)
  new_box = ""

  sum = 0
  
  done = false
  while !done do
    print "> "
    new_box = gets.chomp
    if new_box == "" 
         done = true
    else
      box_dimensions = new_box.split('x')
      for i in 0..2
        box_dimensions[i] = box_dimensions[i].to_i
      end
      sum += calculate_box(box_dimensions)
    end
  end

  puts "#{sum}"
  
else
  box_dimensions = Array.new(3)

  for i in 0..2
    box_dimensions[i] = ARGV[i].to_i
  end

  puts "#{calculate_box(box_dimensions)}"
end

