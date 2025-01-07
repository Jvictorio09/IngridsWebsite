from PIL import Image
import os

# Path to the static files directory
IMAGE_DIR = r'C:\Users\My Computer\Desktop\ingridwebsite\myProject\myApp\static'

def convert_to_webp(directory):
    """
    Batch converts all .jpg, .jpeg, and .png images in a directory to .webp format.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):  # Convert these formats
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'

                # Skip if WebP file already exists
                if os.path.exists(output_path):
                    print(f"WebP already exists for {file}, skipping...")
                    continue

                try:
                    # Open the image and convert it to WebP
                    with Image.open(input_path) as img:
                        img = img.convert('RGB')  # Ensure compatibility
                        img.save(output_path, 'webp', quality=85)  # Save as WebP with quality 85
                        print(f"Converted {input_path} to {output_path}")
                except Exception as e:
                    print(f"Error converting {input_path}: {e}")

# Run the conversion
if __name__ == "__main__":
    convert_to_webp(IMAGE_DIR)
