# Importing Image and ImageOps module from PIL package
import random

import PIL.Image
import numpy as np
from PIL import Image, ImageOps
import base64
from io import BytesIO


def get_image(frame, mask, background):
    # creating a image1 object

    frame = Image.fromarray(frame)
    mask = Image.fromarray(mask)
    # applying fit method
    im2 = ImageOps.fit(background, (952, 567), method=0,
                       bleed=0.0, centering=(0.5, 0.5))
    im = Image.composite(im2, Image.new('RGBA', (952, 567)), mask)

    im.paste(frame.convert('RGB'), (0, 0), frame)
    im = im.resize((475, 284), resample=Image.ANTIALIAS)

    buffered = BytesIO()
    im.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str
