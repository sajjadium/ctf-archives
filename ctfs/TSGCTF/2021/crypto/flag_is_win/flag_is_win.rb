require 'openssl'
require 'digest'

STDOUT.sync = true

class OpenSSL::PKey::EC::Point
  def xy
    n = to_bn(:uncompressed).to_i
    mask = (1 << group.degree) - 1
    return (n >> group.degree) & mask, n & mask
  end
  alias_method :+, :add
  alias_method :*, :mul
end

class ECDSA
  def initialize
    @curve = OpenSSL::PKey::EC::Group.new('secp256k1')
    @G = @curve.generator
    @n = @curve.order.to_i
    @d = OpenSSL::BN.rand(@curve.degree).to_i
    @Q = @G * @d
  end

  def inv(x)
    x.pow(@n - 2, @n)
  end

  def sign(msg)
    z = Digest::SHA256.hexdigest(msg).hex
    k = OpenSSL::BN.rand(@curve.degree / 3).to_s.unpack1('H*').hex
    x, y = (@G * k).xy

    # We should discourage every evil hacks
    s = (z + x * @d) * inv(k) % @n

    return x, s
  end

  def verify(msg, x, s)
    return false if x % @n == 0 || s % @n == 0
    z = Digest::SHA256.hexdigest(msg).hex

    # ditto
    x2, y2 = (@G * (z * inv(s)) + @Q * (x * inv(s))).xy

    return x == x2
  end
end

ecdsa = ECDSA.new

5.times do
  puts <<~EOS
    1. Sign
    2. Find rule
    3. Exit
  EOS

  print 'choice? '

  case gets.chomp
  when '1'
    x, s = ecdsa.sign('Baba')
    puts 'Baba is:'
    puts "x = #{x}"
    puts "s = #{s}"
  when '2'
    print 'Which rule do you want to know? '; msg = gets.chomp
    print 'x? '; x = gets.to_i
    print 's? '; s = gets.to_i

    if ecdsa.verify(msg, x, s)
      if msg == 'Baba'
        puts 'Baba is you'
      elsif msg == 'Flag'
        puts "Flag is #{ENV['FLAG']}"
      else
        puts 'Not Found :('
      end
    else
      puts 'Invalid :('
    end
  else
    exit
  end
end

puts 'You is defeat.'
