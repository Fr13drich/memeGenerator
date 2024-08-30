"""Flask app that renders and create memes."""
import random
import os
import requests
from flask import Flask, render_template, abort, request
from PIL import Image
from QuoteEngine.quote import Ingestor
from MemeEngine.mem_gen import MemeEngine

app = Flask(__name__)

meme = MemeEngine('./static/out.jpg')


def setup():
    """ Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes_list = []
    for f in quote_files:
        quotes_list.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs_list = []
    for root, _dirs, files in os.walk(images_path):
        imgs_list = [os.path.join(root, name) for name in files]

    return quotes_list, imgs_list


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme."""
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']
    try:
        img = requests.get(image_url, allow_redirects=True, timeout=10)
        with open('./static/out.jpg', 'wb') as i:
            i.write(img.content)
        path = meme.make_meme('./static/out.jpg', body, author)
    except (requests.exceptions.RequestException, OSError): # requests.exceptions.ConnectionError:
        return render_template('meme_error.html')
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
