"""The Meme Engine module.

The Meme Engine module is responsible for manipulating
and drawing text onto images.

"""
import os
import random
import argparse
from .QuoteEngine import Ingestor, QuoteModel
from .MemeEngine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp/out.jpg')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(description="Generate a meme.")
    parser.add_argument('--path', type=str,
                        help="path to an image file")
    parser.add_argument('--body', type=str,
                        help="quote body to add to the image")
    parser.add_argument('--author', type=str,
                        help="quote author to add to the image")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
