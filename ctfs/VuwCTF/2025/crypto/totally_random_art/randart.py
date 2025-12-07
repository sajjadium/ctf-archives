import numpy as np
import random

# Generates random ascii art of totally-not-sensitive data!

WIDTH = 10
HEIGHT = 5

PALETTE = ".:-=+*#%@oT0w&8R"

def generate_random_art(data: bytes, width=WIDTH, height=HEIGHT) -> str:
    rng = random.Random(data[0:4])  # Seed with first 4 bytes of data
    remaining_data = data[4:]
    
    image = np.zeros((height, width), dtype=int)
    image.fill(len(PALETTE))  # overflow means unset
    # Randomwalk parameters
    position = np.array([height // 2, width // 2])
    used_positions = {tuple(position)}
    for byte in remaining_data:
        steps, stroke = divmod(byte, len(PALETTE))
        for i in range(steps):
            direction = rng.choice([(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)])
            position += np.array(direction)
            if tuple(position) not in used_positions:
                used_positions.add(tuple(position))
            else:
                # reroll to improve chances
                direction = rng.choice([(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)])
                position += np.array(direction)
                used_positions.add(tuple(position))
            # wrap around
            position[0] = position[0] % height
            position[1] = position[1] % width
        image[position[0], position[1]] += stroke
        image[position[0], position[1]] %= len(PALETTE)

    frame = "+-" + str(len(data)).center(width, "-") + "-+"
    art_lines = [frame]
    for row in image:
        line = "| " + "".join(PALETTE[val] if val < len(PALETTE) else " " for val in row) + " |"
        art_lines.append(line)
    art_lines.append(frame)
    return "\n".join(art_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Expected args: <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file, "rb") as f:
        data = f.read()
    art = generate_random_art(data)
    print("Random art generated:")
    print(art)
    with open(output_file, "w") as f:
        f.write(art)
