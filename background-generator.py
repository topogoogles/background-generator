from PIL import Image  # type: ignore
import random
import time


def generate_dynamic_mosaic(base_tile_path, output_path, num_tiles):
    """
    Creates a mosaic with randomized tile sizes, transparencies, and rotations.

    Args:
        base_tile_path (str): Path to 150x150px transparent PNG
        output_path (str): Output path for 1110x600px mosaic
        num_tiles (int): Number of tiles to render
    """
    tile = Image.open(base_tile_path).convert("RGBA")
    if tile.size != (300, 300):  # Adjust to the input file size
        raise ValueError("Base tile must be 300x300 pixels")

    canvas = Image.new("RGBA", (1500, 500), (0, 0, 0, 255))

    for _ in range(num_tiles):
        # Random scaling and rotation parameters
        scale = random.uniform(
            0.1, 0.4
        )  # Adjust the scaling threshold as desired between 0.1 and on
        rotation = random.uniform(0, 360)
        new_size = (int(300 * scale), int(300 * scale))

        if min(new_size) < 5:
            continue

        # Resize with high-quality filter
        resized = tile.resize(new_size, Image.Resampling.LANCZOS)

        # Apply random rotation with transparent background
        rotated = resized.rotate(
            rotation,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            fillcolor=(0, 0, 0, 0),  # Transparent fill for rotated areas
        )

        # Random transparency adjustment
        alpha = rotated.split()[3]
        new_alpha = alpha.point(
            lambda p: int(p * random.uniform(0.6, 1.0))
        )  # Adjust the transparency threshold
        rotated.putalpha(new_alpha)

        # Position calculation with boundary checks
        max_x = 1500 - new_size[0]
        max_y = 500 - new_size[1]
        if max_x < 0 or max_y < 0:
            continue

        position = (random.randint(0, max_x), random.randint(0, max_y))

        canvas.alpha_composite(rotated, position)

    canvas.convert("RGB").save(output_path, "PNG")


# Generate a unique filename using the current Unix timestamp
timestamp = int(time.time())
output_filename = f"creations/dynamic_mosaic_{timestamp}.png"


def main():
    print(
        f"Hello from background-generator User!\nHold tight while your new {output_filename} is generated!"
    )
    # base_tile_path to the input tiles, num_tiles can adjust the amount of tiles as desired
    generate_dynamic_mosaic(
        base_tile_path="assets/python.png", output_path=output_filename, num_tiles=60
    )


if __name__ == "__main__":
    main()
