#!/usr/sbin/julia
import Primes: nextprime

struct Data
  g::BigInt
  q::BigInt
  sks::Array{Array{BigInt}}
  pks::Array{BigInt}
  secret::Array{UInt8}
end

function create_key(len::Int, data::Data)
  sk::Array{BigInt} = []
  pk::BigInt = 1

  if length(data.pks) ≥ 10
    println("Enough of key creation!")
    return
  end

  for i in 1:len
    push!(sk, rand(1:data.q))
    pk = powermod(data.g, sk[i], data.q) * pk % data.q
  end
  push!(data.sks, sk)
  push!(data.pks, pk)
  println("Key created sucessfully!")
end

function create_secret(len::Int, data::Data)
  println("Tell me your secret: ")
  readbytes!(stdin, data.secret, len)
end

function show_data(data::Data)
  println("g = ", data.g)
  println("q = ", data.q)
  println("secret = ", data.secret)
  println("pks = ", data.pks)
end

function encrypt(flag::String, data::Data)
  i::Int = 0
  c::BigInt = 1
  d::BigInt = 1
  r::BigInt = 1
  s::Int = 0

  if length(data.pks) < 4
    println("Error: You don't have enough keys to encrypt.")
    return
  end

  if length(data.secret) ≠ length(flag)
    println("Error: Invalid secret. Make sure you create a secret first!")
    return
  end

  println("Which char index you want to encrypt?")
  try i = parse(Int, readline()) catch e i = -1 end
  if !(1 ≤ i ≤ length(flag))
    println("Error: Invalid char index!")
    return
  end

  for ki in 1:2:(length(data.pks)-1)
    c = powermod(data.pks[ki], data.sks[ki + 1][i], data.q) * c % data.q
    d = powermod(data.pks[ki + 1], data.sks[ki][i], data.q) * d % data.q
  end

  r = rand(1:data.q)
  s = data.secret[i] ⊻ Int(flag[i])
  c = powermod(data.g, s + r, data.q) * c % data.q
  d = powermod(data.g, r, data.q) * d % data.q

  println("Here we go: ", (c, d))
end

function menu()::Int
  println()
  println("1- Create Key")
  println("2- Create Secret")
  println("3- Show data")
  println("4- Encrypt Flag")
  println("5- Exit")
  println()
  option::Int = 0
  try option = parse(Int, readline()) catch e return -1 end
  return option
end

function main()
  flag::String = strip(open(f->read(f, String), "flag.txt"))
  data::Data = Data(2, nextprime(rand(0: big(2)^1024)), [], [], [])
  @assert length(flag) == 40

  println("\nWelcome! What's your plan for today?")
  while true
    option::Int = menu()
    if option == 1
      create_key(length(flag), data)
    elseif option == 2
      create_secret(length(flag), data)
    elseif option == 3
      show_data(data)
    elseif option == 4
      encrypt(flag, data)
    elseif option == 5
      println("Bye!")
      return
    else
      println("Invalid option!")
    end
  end
end

main()
