import PIL
import random
from utils.quoted_image_generator import image_getter
from utils.quoted_image_generator import image_helper

IMAGE_CATEGORIES = ['animals', 'nature', 'religion', 'backgrounds']
FONTS = ['/Library/Fonts/Futura.ttc']


def generate_quoted_image():
    image_details = image_getter.get_image_details(
        random.choice(IMAGE_CATEGORIES)
    )
    source_image = PIL.Image.open(image_details['image_path']).convert('RGBA')
    source_width, source_height = source_image.size
    source_image.putalpha(128)

    # make a blank image for the text, initialized to transparent text color
    txt = PIL.Image.new('RGBA', source_image.size, (255, 255, 255, 0))

    # get a font
    fnt = PIL.ImageFont.truetype(
        random.choice(FONTS), 30
    )

    # get a drawing context
    draw = PIL.ImageDraw.Draw(txt)

    # append author details to quote
    quote = f'{image_details["quote"]}\n\n- {image_details["author"]}'

    wrappedText = image_helper.wrapTextByWidth(
        draw, quote, fnt, (source_width/1.05)
    )

    dw, dh = draw.textsize(wrappedText, fnt)

    # draw text with center positioning and alignment
    # 1.05 approximates height from bottom of image
    draw.multiline_text(
        ((source_width-dw)/2, (source_height-dh)/1.05),
        wrappedText, font=fnt, fill=(255, 255, 255, 255),
        align='center'
    )

    out = PIL.Image.alpha_composite(source_image, txt)
    out.show()

if __name__ == "__main__":
    generate_quoted_image()
