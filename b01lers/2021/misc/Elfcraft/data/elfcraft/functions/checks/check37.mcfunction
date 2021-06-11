scoreboard players set @a localChecks 0

execute as @a[scores={search=1}] if block ~0 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~223 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~223 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~225 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~225 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~5 ~-1 ~225 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~222 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~223 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~223 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~224 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~225 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~225 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~226 minecraft:white_concrete run scoreboard players add @a localChecks 1

execute as @a[scores={search=1}] if score @s localChecks matches 29 run scoreboard players add @s checksPassed 1