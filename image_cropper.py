import os

from PIL import Image


def extract_5x5_squares_with_stride(image_path, output_dir, padding, stride):
    """
    Extract exactly 25 square images (5x5 layout) with padding and stride.

    Args:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the extracted images.
        padding (int): Padding around the entire image.
        stride (int): Spacing between the images in the grid.
    """
    # Open the input image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the size of each square
    grid_size = 5  # 5x5 grid
    square_width = (width - 2 * padding - (grid_size - 1) * stride) // grid_size
    square_height = (height - 2 * padding - (grid_size - 1) * stride) // grid_size

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Counter for naming the extracted images
    count = 1

    # Loop through the grid
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate the crop box
            left = padding + col * (square_width + stride)
            top = padding + row * (square_height + stride)
            right = left + square_width
            bottom = top + square_height

            # Crop the square
            cropped = image.crop((left, top, right, bottom))

            # Save the cropped image
            output_path = os.path.join(output_dir, f"{count}.jpg")
            cropped.save(output_path)
            print(f"Saved: {output_path}")
            count += 1

    print("Extraction complete!")


image_path = "images/calendar_background.jpg"  # Path to your image
output_dir = "images/output_images"
padding = 40
stride = 17

# Run the extraction
extract_5x5_squares_with_stride(image_path, output_dir, padding, stride)

# display first image
Image.open("images/output_images/1.jpg")
