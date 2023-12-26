import multiprocessing
import os
import bs4
import multiprocessing

filenames = os.listdir("htmls")

def get_title(filename):
    with open("laws/"+filename) as f:
        html_content = f.read()
        bs = bs4.BeautifulSoup(html_content, "html.parser")
        print(bs.head.title.text)

def main():
    """ Main entry point of the app """
    with multiprocessing.Pool() as p:
        p.map(get_title, filenames)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
