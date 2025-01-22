require 'socket'
require 'thread'

server = TCPServer.new(4000)
puts "Multithreaded Server started on port 4000"

loop do
  client = server.accept
  Thread.new(client) do |conn|
    conn.puts "Hello! Type 'bye' to exit."
    loop do
      input = conn.gets.chomp
      break if input.downcase == 'bye'
      conn.puts "You said: #{input}"
    end
    conn.puts "Goodbye!"
    conn.close
  end
end
