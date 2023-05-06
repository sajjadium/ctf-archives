require 'openssl'
require 'json'

class String
  def hex
    return self.unpack("H*")[0]
  end

  def unhex
    return [self].pack("H*")
  end
end


STDOUT.sync = true
key = OpenSSL::Random.random_bytes(32)

while true
  puts "1: create your token\n2: login with your token"
  print "> "

  case gets.strip.to_i
  when 1 then
    iv = OpenSSL::Random.random_bytes(12)
    print "your name: "

    name = gets.strip
    encryptor     = OpenSSL::Cipher.new('AES-256-GCM')
    encryptor.encrypt
    encryptor.key = key
    encryptor.iv  = iv

    token = encryptor.update(JSON.generate({
      "username" => name,
      "is_yoshiking" => false,
    })) + encryptor.final
    puts "your token: #{iv.hex}:#{token.hex}:#{encryptor.auth_tag.hex}"

  when 2 then
    print "your token: "

    begin
      iv, c, tag  = gets.strip.split(":").map(&:unhex)

      decryptor     = OpenSSL::Cipher.new('AES-256-GCM')
      decryptor.decrypt
      decryptor.key = key
      decryptor.iv  = iv
      decryptor.auth_tag = tag

      data = JSON.parse(decryptor.update(c) + decryptor.final)

      if data["username"] == "yoshiking" and data["is_yoshiking"] then
        raise "I know it is fake at all" unless tag.size == 16
        puts "I'm glad you could come, yoshiking. Here is the flag: #{ENV["flag"] || "fakeCTF{yoyooyoyoyyoo_shikiiiiiiiing}"}"
      else
        puts "hello #{data["username"]}"
      end
        
    rescue => e
      p e
    end

  else
    break
  end
end

