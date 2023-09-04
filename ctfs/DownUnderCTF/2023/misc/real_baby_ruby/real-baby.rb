#!/usr/bin/env ruby

while input = STDIN.gets.chomp do eval input if input.size < 5 && input !~ /`|%/ end
