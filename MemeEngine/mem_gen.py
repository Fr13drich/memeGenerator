from PIL import Image, ImageDraw, ImageFont
from random import randint
class MemeEngine():

    def __init__(self, out_path) -> None:
        self.out_path = out_path

    def make_meme(self, img_path, text, author, width=500) -> str: #generated image path
        """Create a Postcard With a Text Greeting

        Arguments:
            img_path {str} -- the file location for the input image.
            width {int} -- The pixel width value. Default=500.
        Returns:
            str -- the file path to the output image.
        """
        img = Image.open(img_path)
        ratio = width/float(img.size[0])
        height = int(ratio*float(img.size[1]))
        img = img.resize((width, height), Image.NEAREST)
        draw = ImageDraw.Draw(img)
        # font = ImageFont.load("./fonts/Roboto-Black.ttf")
        font = ImageFont.truetype('./fonts/Roboto-Black.ttf', size=50)
        # draw.text((10, 30), text + ' - ' + author, font=font, fill='white')
        msg = text + ' - ' + author
        loc = (randint(0,img.size[0] - 1), randint(0,img.size[1] - 1))
        draw.text(loc, msg, font=font, fill='white')
        img.save(self.out_path + 'out.jpg')
        return self.out_path + 'out.jpg'
