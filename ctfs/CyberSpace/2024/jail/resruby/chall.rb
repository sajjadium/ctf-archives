STDOUT.sync = true
STDOUT.class.send(:remove_method, :<<)

print "safe code > "
code = gets.chomp

if code =~ /[\w?'"`]/
  puts "not safe"
  exit 1
end

puts "ok"
eval code