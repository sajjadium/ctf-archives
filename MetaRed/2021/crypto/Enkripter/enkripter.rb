require "base64"

module Enkripter
  class << self
    def enkripter(input, key)
      output = ''
      for i in 0..input.length-1
        output << (input[i].ord ^ key[i%key.length].ord)
      end
      return Base64.encode64(output)
    end

    def dekripter(input, key)
      return input
    end
  end
end

key = ''
en = Enkripter::enkripter('Ecuador Amazonico, Desde siempre y hasta siempre', key)
puts en
puts Enkripter::dekripter(en, key)
