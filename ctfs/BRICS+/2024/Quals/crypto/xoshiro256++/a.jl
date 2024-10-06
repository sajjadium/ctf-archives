flag = read("flag.txt") # brics+{...}
for _ in 1:1500
	println(bytes2hex(flag .⊻ rand(UInt8, length(flag))))
end
