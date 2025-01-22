player = {name = "Player1", health = 100}

function attack(target)
    target.health = target.health - 10
    print(target.name .. " attacked! Health is now " .. target.health)
    if target.health <= 0 then
        print(target.name .. " has been defeated!")
    end
end

enemy = {name = "Enemy1", health = 50}

attack(enemy)
