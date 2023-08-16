from PIL import Image
import sys
import glob

TILE_SIZE = 24

if len(sys.argv) < 2:
    print("Usage: merge_dino_tileset.py <path_to_to_dino>")
    print("Example: merge_dino_tileset.py assets/dinos/male/mono")
    exit(-1)

base_path = sys.argv[1] + "/base/"
images = sorted(glob.glob(base_path + "*.*"))

print(f"Found Images: {len(images)}")

result_image = Image.new("RGBA", (20*TILE_SIZE, len(images)*TILE_SIZE))

# Process each tiled image
for index, img_path in enumerate(images):
    img = Image.open(img_path)
    num_tiles_in_image = int(img.width / TILE_SIZE)

    for i in range(num_tiles_in_image):
        tmp_img = img.crop((TILE_SIZE*i,0,TILE_SIZE*i+24,24))
        transposed = tmp_img.transpose(Image.FLIP_LEFT_RIGHT)
        result_image.paste(tmp_img, (TILE_SIZE*i, TILE_SIZE*index))
        result_image.paste(transposed, (TILE_SIZE*i+num_tiles_in_image*TILE_SIZE, TILE_SIZE*index))

result_image.save(sys.argv[1] + "/combined_tileset.png")