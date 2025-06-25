from PIL import Image
import numpy as np
import os

def convert_to_camera_ready(input_path, output_path):
    # Open the image
    img = Image.open(input_path)
    
    # Ensure the image has an alpha channel
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Convert to numpy array for easier manipulation
    img_array = np.array(img)
    
    # Convert RGB to grayscale using standard luminance formula
    # Y = 0.299*R + 0.587*G + 0.114*B
    gray_values = np.dot(img_array[:,:,:3], [0.299, 0.587, 0.114])
    
    # Create new RGBA array with grayscale values
    grayscale_rgba = np.zeros_like(img_array)
    grayscale_rgba[:,:,0] = gray_values  # Red channel
    grayscale_rgba[:,:,1] = gray_values  # Green channel  
    grayscale_rgba[:,:,2] = gray_values  # Blue channel
    grayscale_rgba[:,:,3] = img_array[:,:,3]  # Preserve alpha channel
    
    # Convert back to PIL Image
    result_img = Image.fromarray(grayscale_rgba.astype('uint8'), 'RGBA')
    
    # Save with 300 DPI
    result_img.save(output_path, dpi=(300, 300), quality=95)
    
    print(f"Converted {input_path} to grayscale with alpha: {output_path}")
    print(f"Mode: {result_img.mode}, Size: {result_img.size}")

# Usage
# convert_to_camera_ready('input.png', 'output_300dpi_bw.png')
for img in os.listdir('papers/images'):
    if not img.endswith('.png'):
        continue

    name = img.split('.')[0]+'-300.png'

    convert_to_camera_ready(f'papers/images/{img}', f'papers/camera-ready/{name}')