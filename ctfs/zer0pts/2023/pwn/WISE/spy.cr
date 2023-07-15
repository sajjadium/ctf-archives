suspect = nil
id_list = [] of UInt64
name_list = [] of String

puts "1. Add new citizen",
     "2. Update personal information",
     "3. Print list of citizen",
     "4. Mark as spy",
     "5. Give memorable ID to spy",
     "6. Print information of spy"

loop do
  print "> "
  STDOUT.flush
  case gets.not_nil!.chomp.to_i
  when 1
    id = Random.rand(UInt64)
    print "Name of person: "
    STDOUT.flush
    name = gets.not_nil!.chomp

    id_list.push(id)
    name_list.push(name)
    puts "ID: #{id}"

  when 2
    print "ID: "
    STDOUT.flush
    index = id_list.index gets.not_nil!.chomp.to_u64
    if index.nil?
      puts "[-] Invalid ID"
    else
      print "New name: "
      STDOUT.flush
      name_list[index] = gets.not_nil!.chomp
    end

  when 3
    id_list.zip(name_list) { | id, name |
      puts "----------------",
           "ID: #{id}",
           "Name: #{name}"
    }

  when 4
    print "ID of suspect: "
    STDOUT.flush
    index = id_list.index gets.not_nil!.chomp.to_u64
    if index.nil?
      puts "[-] Invalid ID"
    else
      puts "[+] Marked '#{name_list[index]}' as possible spy"
      suspect = id_list.to_unsafe + index
    end

  when 5
    if suspect.nil?
      puts "[-] No spy marked"
    else
      print "New ID: "
      STDOUT.flush
      suspect.value = gets.not_nil!.chomp.to_u64
    end

  when 6
    if suspect.nil?
      puts "[-] No spy marked"
    else
      puts "ID: #{suspect.value}"
      index = id_list.index suspect.value
      if index.nil?
        puts "Name: <unknown>"
      else
        puts "Name: #{name_list[index]}"
      end
    end

  else
    break
  end
end
