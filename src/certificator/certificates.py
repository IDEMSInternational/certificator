import io
from collections import namedtuple

from PIL import Image, ImageFont
from PIL.ImageDraw import Draw

Point = namedtuple("Point", ["x", "y"])
Area = namedtuple("Area", ["width", "height"])


class TextBox:
    def __init__(self, start, end, image_size):
        assert start[0] < end[0], "Start and end must be positioned left to right"
        assert start[1] < end[1], "Start and end must be positioned top to bottom"

        self.start = Point(*start)
        self.end = Point(*end)
        self.image = Area(*image_size)

    @property
    def height(self):
        return int((self.end.y - self.start.y) * self.image.height)

    @property
    def width(self):
        return int((self.end.x - self.start.x) * self.image.width)

    def font_size(self, text_width):
        w, h = self.width, self.height

        return int(min(h, w / text_width * h))

    def text_start(self, textwidth, font_size):
        return Point(
            int((self.width - textwidth) / 2 + self.start.x * self.image.width),
            int(self.end.y * self.image.height - 1.1 * font_size),
        )


def get_resized_font(path, box, text):
    """
    Fetch the specified font at a size that will allow the given text to fit within the
    given area.
    """
    text_width = ImageFont.truetype(path, box.height).getlength(text)

    return ImageFont.truetype(
        font=path,
        size=box.font_size(text_width),
    )


def load_template(path) -> Image:
    with Image.open(path) as img:
        return img.convert(mode="RGBA")


def make_certificate(template_path, font_path, name, box, color) -> bytes:
    template = load_template(template_path)
    tbox = TextBox(box[:2], box[2:], template.size)
    font = get_resized_font(font_path, tbox, name)
    pos = tbox.text_start(
        font.getlength(name),
        font.size,
    )
    cert = io.BytesIO()

    Draw(template).text(pos, name, fill=color, font=font)
    template.convert(
        mode="P",
        palette=Image.Palette.ADAPTIVE,
    ).save(
        cert,
        format="PNG",
        optimize=True,
    )

    return cert.getvalue()
