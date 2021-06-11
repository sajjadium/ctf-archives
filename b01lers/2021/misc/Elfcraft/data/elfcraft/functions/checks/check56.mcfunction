scoreboard players set @a localChecks 0

execute as @a[scores={search=1}] if block ~0 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~337 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~337 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~339 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~339 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~5 ~-1 ~339 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~336 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~337 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~337 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~338 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~339 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~339 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~340 minecraft:white_concrete run scoreboard players add @a localChecks 1

execute as @a[scores={search=1}] if score @s localChecks matches 29 run scoreboard players add @s checksPassed 1