import io
from importlib.metadata import version
from PIL import Image, ImageDraw, ImageFont


def get_font_width(font, text):
    if int(version("Pillow").split(".")[0]) < 10:
        return font.getsize(text)[0]
    else:
        return font.getlength(text)


def get_resized_font(font_path, desired_width, max_height, text):
    # Check how wide the text is
    fontsize = 100
    font = ImageFont.truetype(font_path, fontsize)
    textwidth = get_font_width(font, text)

    # Adjust width so that it fits the page
    fontsize = min(max_height, int(desired_width / textwidth * 100))
    font = ImageFont.truetype(font_path, fontsize)
    return font, fontsize


def make_certificate(template_path, font_path, name) -> bytes:
    img = Image.open(template_path)
    width, height = img.size
    editable = ImageDraw.Draw(img)
    text_color = (0x17, 0x41, 0x68)

    x_lower = 0.072
    x_upper = 0.596
    y_lower = 0.436
    max_height = (y_lower-0.310)
    max_height_px = int(height * max_height)

    relative_width = x_upper - x_lower
    desired_width = relative_width * width
    font, fontsize = get_resized_font(font_path, desired_width, max_height_px, name)

    textwidth = get_font_width(font, name)
    xpos = int(((x_upper - x_lower) * width - textwidth)/2 + x_lower * width)
    ypos = int(y_lower * height - 1.1*fontsize)
    location = (xpos, ypos)
    editable.text(location, name, fill=text_color, font=font)

    bytes_io = io.BytesIO()
    img.save(bytes_io, format="PNG")

    return bytes_io.getvalue()
