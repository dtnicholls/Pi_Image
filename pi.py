from PIL import Image, ImageDraw, ImageFont

def create_pi_image(circle_radius_mm, pi_text_size_mm, number_pi_size_mm, pi_digits_file, background_choice):
    # Convert mm to pixels (assuming 96 DPI, 1 inch = 25.4 mm)
    dpi = 96
    mm_to_pixels = dpi / 25.4
    txt_pt_size = 0.3528
    circle_radius = int(circle_radius_mm * mm_to_pixels)
    pi_text_size = int((pi_text_size_mm / txt_pt_size) * (mm_to_pixels / 0.6))
    number_pi_size = int((number_pi_size_mm / txt_pt_size) * mm_to_pixels)

    # Load the digits of π from the file
    with open(pi_digits_file, 'r') as file:
        pi_digits = file.read().replace('\n', '')

    # Determine the background color based on user choice
    if background_choice == '1':
        background_color = (255, 255, 255, 255)  # White background
    elif background_choice == '2':
        background_color = (0, 0, 0, 0)  # Transparent background
    else:
        raise ValueError("Invalid choice for background color. Choose 1 for white or 2 for transparent.")

    # Create a blank image with the specified background color
    # Add border: increase size by 10% on each side
    border_size = int(0.1 * circle_radius)
    img_size = (circle_radius * 2 + 2 * border_size, circle_radius * 2 + 2 * border_size)
    image = Image.new('RGBA', img_size, background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font_pi = ImageFont.truetype("GARABD.TTF", pi_text_size)
        font_number = ImageFont.truetype("GARABD.TTF", number_pi_size)
    except IOError:
        font_pi = ImageFont.load_default()
        font_number = ImageFont.load_default()

    # Calculate the position for the Greek letter π
    pi_text = "π"
    text_bbox = draw.textbbox((0, 0), pi_text, font=font_pi)
    text_height = text_bbox[3] - text_bbox[1]
    text_position = img_size[0] // 2, (img_size[1] // 2) - text_height // 5
    
    # Create a mask to define the circle and the area to exclude for the letter π
    mask = Image.new('L', img_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    # Adjust the ellipse to fit inside the new border
    mask_draw.ellipse((border_size, border_size, img_size[0] - border_size, img_size[1] - border_size), fill=255)  # Draw the circle
    mask_draw.text(text_position, pi_text, fill=0, font=font_pi, anchor="mm")  # Mask out the area for the letter π

    # Draw the digits of π around the masked area
    digit_index = 0
    for y in range(0, img_size[1], number_pi_size):
        for x in range(0, img_size[0], number_pi_size):
            if mask.getpixel((x, y)) == 255:  # Only draw where the mask is white
                draw.text((x, y), pi_digits[digit_index], fill='black', font=font_number)
                digit_index = (digit_index + 1) % len(pi_digits)

    # Save the final image
    image.save('pi_image.png')

if __name__ == "__main__":
    circle_radius_mm = float(input("Enter the radius of the circle in mm: "))
    pi_text_size_mm = float(input("Enter the text size for the Greek letter π in mm: "))
    number_pi_size_mm = float(input("Enter the text size for the number π in mm: "))
    background_choice = input("Enter 1 for a white background or 2 for a transparent background: ")
    pi_digits_file = "pi.txt"
    create_pi_image(circle_radius_mm, pi_text_size_mm, number_pi_size_mm, pi_digits_file, background_choice)
