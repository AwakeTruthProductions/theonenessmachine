from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
from bots.image_generator import image_getter
from bots.image_generator import image_helper
from bots.image_generator import post_image

IMAGE_CATEGORIES = ['animals', 'nature', 'religion', 'source_imagegrounds']
FONT_PATH = 'assets/fonts/'  # '/Library/Fonts/'
FONTS = [
    'MarkerFelt.ttc', 'DINCondensedBold.ttf'
]


def start(overlay_flag=True):
    image_details = image_getter.get_image_details(
        random.choice(IMAGE_CATEGORIES)
    )

    image = None
    status = None
    if (overlay_flag):
        image = post_image_quote_overlay(image_details)
    else:
        image = post_image_alongside_quote(image_details)
        status = f'{image_details["quote"]}\n\n- {image_details["author"]}'

    # save details to db
    image_helper.insert_quoted_image(
        image_details['source_id'],
        image_details['image_path'],
        image_details['quote_id']
    )

    # post image to social media (just twitter for now)
    post_image.tweet_image(image_details['image_path'], status)
    image.show()


def post_image_alongside_quote(image_details):
    source_image = Image.open(image_details['image_path']).convert('RGBA')
    return source_image


def post_image_quote_overlay(image_details):
    source_image = Image.open(image_details['image_path']).convert('RGBA')
    source_image.putalpha(220)
    source_width, source_height = source_image.size

    # get a font
    rando_font = random.choice(FONTS)
    fnt = ImageFont.truetype(
        FONT_PATH + rando_font, 36
    )

    # append author details to quote
    quote = f'{image_details["quote"]}\n\n- {image_details["author"]}'

    img_draw = ImageDraw.Draw(source_image)
    wrapped_text = image_helper.wrap_text_by_width(
        img_draw, image_details["quote"], fnt, (source_width/1.1)
    )

    final_text = wrapped_text + f'\n {image_details["author"]}'

    dw, dh = img_draw.multiline_textsize(final_text, fnt)

    text_overlay_size = (dw + 20, dh + 10)

    # create image with correct size and black source_imageground
    text_overlay = Image.new('RGBA', text_overlay_size, "black")
    text_overlay.putalpha(0)

    draw = ImageDraw.Draw(text_overlay)
    # draw text with center positioning and alignment
    # 1.05 approximates height from bottom of image
    print(final_text)
    draw.multiline_text(
        (10, 0),
        final_text, font=fnt, fill=(255, 255, 255, 255),
        align='center'
    )

    x = round((source_width-dw)/2)
    y = round((source_height-dh)/1.06)
    postion = (x, y)
    source_image.paste(text_overlay, postion, mask=text_overlay)

    # Create paste mask
    radius = 10
    diam = 2*radius
    mask = Image.new('L', source_image.size, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0 = 0, 0
    x1, y1 = source_image.size
    for d in range(diam+radius):
        x1, y1 = x1-1, y1-1
        alpha = 255 if d < radius else int(255*(diam+radius-d)/diam)
        draw.rectangle([x0, y0, x1, y1], outline=alpha)
        x0, y0 = x0+1, y0+1

    # Blur image and paste blurred edge according to mask
    blur = source_image.filter(ImageFilter.GaussianBlur(radius/2))
    source_image.paste(blur, mask=mask)
    source_image.save(image_details['image_path'], 'PNG')

if __name__ == "__main__":
    start()
