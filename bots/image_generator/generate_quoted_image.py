from PIL import Image, ImageFont, ImageDraw
import random
from bots.image_generator import image_getter
from bots.image_generator import image_helper

IMAGE_CATEGORIES = ['animals', 'nature', 'religion', 'backgrounds']
FONT_PATH = 'assets/fonts/'  # '/Library/Fonts/'
FONTS = [
    'Futura.ttc', 'MarkerFelt.ttc', 'Herculanum.ttf', 'Noteworthy.ttc',
    'DINCondensedBold.ttf', 'DINCondensedBold.ttf', 'Moon2.0-Regular.otf'
]


def generate_quoted_image():
    image_details = image_getter.get_image_details(
        random.choice(IMAGE_CATEGORIES)
    )
    source_image = Image.open(image_details['image_path']).convert('RGBA')
    source_width, source_height = source_image.size
    source_image.putalpha(128)

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', source_image.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype(
        FONT_PATH + random.choice(FONTS), 30
    )

    # get a drawing context
    draw = ImageDraw.Draw(txt)

    # append author details to quote
    quote = f'{image_details["quote"]}\n\n- {image_details["author"]}'

    wrapped_text = image_helper.wrap_text_by_width(
        draw, image_details["quote"], fnt, (source_width/1.25)
    )

    final_text = wrapped_text + f'\n {image_details["author"]}'

    dw, dh = draw.textsize(final_text, fnt)

    # draw text with center positioning and alignment
    # 1.05 approximates height from bottom of image
    draw.multiline_text(
        ((source_width-dw)/2, (source_height-dh)/1.06),
        final_text, font=fnt, fill=(255, 255, 255, 255),
        align='center'
    )

    out = Image.alpha_composite(source_image, txt)
    out.save(image_details['image_path'], 'PNG')

    # save details to db
    image_helper.insert_quoted_image(
        image_details['source_id'],
        image_details['image_path'],
        image_details['quote_id']
    )

    out.show()

if __name__ == "__main__":
    generate_quoted_image()
