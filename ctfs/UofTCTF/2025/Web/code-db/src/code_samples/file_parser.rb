filename = ARGV[0]

unless File.exist?(filename)
  puts "File not found!"
  exit
end

word_count = 0
line_count = 0

File.foreach(filename) do |line|
  line_count += 1
  word_count += line.split.size
end

puts "Lines: #{line_count}, Words: #{word_count}"
