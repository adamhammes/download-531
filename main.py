import os

from lxml import html
import requests


def download_file(link, dest, verbose=True):
    directory, file_name = os.path.split(dest)
    os.makedirs(directory, exist_ok=True)

    if verbose:
        print('Downloading {}'.format(file_name))

    file = requests.get(link).content
    with open(dest, 'wb') as f:
        f.write(file)


def download_homework():
    homework_names = ['hw{}'.format(i) for i in range(1, 6)]
    urls = ['http://web.cs.iastate.edu/~cs531/{}.pdf'.format(name) for name in homework_names]

    for name, url in zip(homework_names, urls):
        file_name = 'homework/{}.pdf'.format(name)
        download_file(url, file_name)


def download_notes():
    # here we actually scrape the page because I'm too lazy to write the name of the notes
    page = requests.get('http://web.cs.iastate.edu/~cs531/notes.html').content
    tree = html.fromstring(page)

    # links are in reverse chronological order on the website
    names = [elem.text for elem in tree.cssselect('p > a')][::-1]
    links = ['http://web.cs.iastate.edu/~cs531/notes/notes{}.pdf'.format(i) for i in range(1, 13)]

    for name, link in zip(names, links):
        file_name = 'notes/{}.pdf'.format(name)
        download_file(link, file_name)


def main():
    download_homework()
    download_notes()

if __name__ == '__main__':
    main()
