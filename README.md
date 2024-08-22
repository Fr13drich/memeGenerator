# memeGenerator

Overview:

A multimedia application to dynamically generate memes, including an image with an overlaid quote.

The Quote Engine module is responsible for ingesting the quote files located in _data/DogQuotes in csv, txt, pdf or docx format. It uses the following modules: pandas, docx and subprocess to call the pdftotext CLI utility.

The Meme Engine Module is responsible for manipulating and drawing text onto images. 

Instructions:

Command line: meme.py [-h] [--path PATH] [--body BODY] [--author AUTHOR]

options:
  -h, --help       show this help message and exit
  --path PATH      path to an image file
  --body BODY      quote body to add to the image
  --author AUTHOR  quote author to add to the image

  Example: python.exe ./meme.py --path=_data\photos\dog\xander_1.jpg --body="Hi" --author="Me"

Web interface:

Put your images in _data/photos in jpg format.
Put your quotes files in _data/DogQuotes in csv, txt, pdf or docx format.
Run the flask app: python.exe app.py
Open http://127.0.0.1:5000 in a web browser.



