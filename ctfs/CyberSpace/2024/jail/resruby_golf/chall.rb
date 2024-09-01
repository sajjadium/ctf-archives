STDOUT.sync = true
STDOUT.class.send(:remove_method, :<<)

print "safe (and short) code > "
code = gets.chomp

if code =~ /[\w?'"`%]/
  puts "not safe"
  exit 1
end

if code.size > 35
  puts "not short"
  exit 1
end

# NOTE: flag is stored in ./flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag.txt

puts "ok"
eval code
