local gravity = -9.81
local velocity = 0
local position = 100
local dt = 0.1

for t = 0, 10, dt do
    velocity = velocity + gravity * dt
    position = position + velocity * dt
    print(string.format("Time: %.1f s, Position: %.2f m, Velocity: %.2f m/s", t, position, velocity))
    if position <= 0 then
        print("Object has hit the ground.")
        break
    end
end
