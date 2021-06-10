#!/usr/bin/env ruby
# encoding: ascii-8bit

require 'elftools' # gem install elftools
require 'fileutils'
require 'securerandom'
require 'tempfile'

def setup
  STDIN.sync = 0
  STDOUT.sync = 0
end

def err(msg)
  STDOUT.puts msg
rescue Errno::EPIPE
ensure
  exit! 2
end

def check_valid_elf(data)
  return 'Invalid magic' unless data.start_with?("\x7fELF\x02\x01\x01" + "\x00" * 9)
  return 'Headless?' if data.size < 0x40

  elf_hdr = ELFTools::Structs::ELF_Ehdr.new(endian: :little, elf_class: 64).read(data)
  return 'Normal x86_64 plz' unless elf_hdr.e_machine == ELFTools::Constants::EM_X86_64 &&
    elf_hdr.e_version == 1 && elf_hdr.e_flags == 0

  return 'Invalid program header' unless elf_hdr.e_phoff == 0x40 && elf_hdr.e_ehsize == 0x40 &&
    elf_hdr.e_phentsize == 56 && elf_hdr.e_phnum > 0

  return 'Too small' if data.size < elf_hdr.e_phoff + elf_hdr.e_phentsize * elf_hdr.e_phnum

  phdrs = Array.new(elf_hdr.e_phnum) do |i|
    ELFTools::Structs::ELF64_Phdr.new(endian: :little).read(data[0x40 + 56 * i, 56])
  end
  return 'Un-executable only' unless phdrs.all? { |p| p.p_flags == 4 || p.p_flags == 6 }

  gnu_stack = phdrs.find { |p| p.p_type == ELFTools::Constants::PT_GNU_STACK }
  return 'Stack should be un-executable as well' unless gnu_stack && gnu_stack.p_flags == 6
  true
rescue EOFError
  'EOFError'
end

def main
  setup
  puts <<-EOS
Give me your un-executable file, I will run it for you :D

  EOS

  puts 'Length?'
  len = STDIN.gets.to_i
  err('Invalid length') if len <= 0 || len > 0x2000

  puts 'Data?'
  data = STDIN.read(len)
  err('Read fail') if data.nil? || data.size != len

  result = check_valid_elf(data)
  err(result) if result.is_a?(String)
  puts 'Wait..'
  sleep(3)
  puts "Let's go!"

  Dir.chdir('/home/unexecutable')
  path = "files/unexecutable-#{SecureRandom.hex(16)}"
  IO.binwrite(path, data)
  FileUtils.chmod(0o700, path)
  syscall(3, 0) # close(stdin), rock!
  system('./nsjail',
         '--quiet',
         '-Mo',
         '--chroot', Dir.pwd,
         '--disable_proc', '-Q',
         '-t', '1', '--', path)
end

main
