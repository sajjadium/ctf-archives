#!/usr/bin/env ruby
# encoding: ascii-8bit
require 'pwn'        # https://github.com/peter50216/pwntools-ruby

STDIN.sync = 0
STDOUT.sync = 0

STDOUT.puts('The binary "start" is listening at 127.0.0.1:31338.')
STDOUT.puts("This is not important, but the Ruby version running is: #{RUBY_VERSION}")
STDOUT.puts('Give me your Ruby script, I would run it for you ;)')
STDOUT.write('> ')

code = STDIN.readpartial(1024)
STDIN.close
eval(code)
