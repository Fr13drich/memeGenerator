"""
Loading of a file from disk
Transform image by resizing to a maximum width of 500px while maintaining the input aspect ratio
Add a caption to an image (string input) with a body and author to a random location on the image.
"""
import os
from random import randint
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """
    Loading of a file from disk.
    Transform image by resizing to a maximum width of 500px
    while maintaining the input aspect ratio.
    Add a caption to an image (string input) with a body and
    author to a random location on the image.
    """

    def __init__(self, out_path) -> None:
        self.out_path = out_path

    def make_meme(self, img_path, text: str, author: str, width=500) -> str:
        """Create a Postcard With a Text Greeting

        Arguments:
            img_path {str} -- the file location for the input image.
            width {int} -- The pixel width value. Default=500.
        Returns:
            str -- the file path to the output image.
        """
        # img = Image.new('RGB', (500,500) )
        img = Image.open(img_path)
        ratio = width/float(img.size[0])
        height = int(ratio*float(img.size[1]))
        img = img.resize((width, height), Image.NEAREST)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./fonts/Roboto-Black.ttf', size=30)
        msg = str(text) + ' - ' + str(author)
        loc = (10, randint(0, img.size[1] - 1))
        draw.text(loc, msg, font=font, fill='white')
        img.save(self.out_path)
        return self.out_path
