def calculate_ribbon(box_dimensions)

  biggest_dimension = 0

  ribbon = 0
  bow = 0
  
  for i in 0..2
    if box_dimensions[i] > box_dimensions[biggest_dimension]
      biggest_dimension = i
    end
  end

  for i in 0..2
    if i != biggest_dimension
      ribbon += 2 * box_dimensions[i]
    end
    if bow == 0
      bow = box_dimensions[i]
    else
      bow *= box_dimensions[i]
    end
  end

  ribbon += bow
  
  return ribbon
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
      sum += calculate_ribbon(box_dimensions)
    end
  end

  puts "#{sum}"
  
else
  box_dimensions = Array.new(3)

  for i in 0..2
    box_dimensions[i] = ARGV[i].to_i
  end

  puts "#{calculate_ribbon(box_dimensions)}"
end

