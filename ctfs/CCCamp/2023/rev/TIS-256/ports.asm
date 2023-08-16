stdin X1 Y1
stdout X3 Y2

tpu X1 Y1
	mov UP, RIGHT
end

tpu X2 Y1
	mov LEFT, DOWN
	mov DOWN, RIGHT
end

tpu X2 Y2
	mov ANY, ACC
	mov ACC, LAST
end

tpu X3 Y1
	mov LEFT, DOWN
end

tpu X3 Y2
	mov UP, DOWN
end

