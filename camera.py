from PIL import Image
import numpy as np
import os

def concat_images_resize_and_pad(image_paths, output_path, target_height=None, spacing=10):
    # Open all images
    images = [Image.open(path) for path in image_paths]
    
    # Determine target height (use tallest image if not specified)
    if target_height is None:
        target_height = max(img.height for img in images)
    
    # Resize images to same height while maintaining aspect ratio
    resized_images = []
    for img in images:
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        resized_img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
        resized_images.append(resized_img)
    
    # Calculate total width including spacing
    total_width = sum(img.width for img in resized_images) + spacing * (len(resized_images) - 1)
    
    # Create new image with transparent background
    concatenated = Image.new('RGBA', (total_width, target_height), (255, 255, 255, 0))
    
    # Paste images with spacing
    x_offset = 0
    for i, img in enumerate(resized_images):
        concatenated.paste(img, (x_offset, 0), img if img.mode == 'RGBA' else None)
        x_offset += img.width
        
        # Add spacing (except after the last image)
        if i < len(resized_images) - 1:
            x_offset += spacing
    
    # Save with 300 DPI
    concatenated.save(output_path, dpi=(300, 300), quality=95)
    
    print(f"Concatenated {len(images)} images:")
    print(f"- Resized to height: {target_height}px")
    print(f"- Spacing between images: {spacing}px") 
    print(f"- Final size: {concatenated.size}")
    
    return concatenated

# Usage with 20px spacing
models = ['bce', 'scratch', 'resnet']
metrics = ['ssim', 'fid', 'psnr']
for metric in metrics:
    imgs = [f'papers/images/{model}-{metric}.png' for model in models]
    concat_images_resize_and_pad(imgs, f'papers/images/models-{metric}.png', spacing=20)

for model in models:
    imgs = [f'papers/images/{model}-{metric}.png' for metric in metrics]
    concat_images_resize_and_pad(imgs, f'papers/images/{model}-metrics.png', spacing=20)


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

