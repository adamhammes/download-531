import os

from lxml import html
import requests


def download_file(link, dest, verbose=True):
    if verbose:
        _, file_name = os.path.split(dest)
        print('Downloading {}'.format(file_name))

    file = requests.get(link).content
    with open(dest, 'wb') as f:
        f.write(file)


def download_homework():
    dir_name = 'homework'
    os.makedirs(dir_name, exist_ok=True)

    homework_names = ['hw{}'.format(i) for i in range(1, 6)]
    urls = ['http://web.cs.iastate.edu/~cs531/{}.pdf'.format(name) for name in homework_names]

    for name, url in zip(homework_names, urls):
        file_name = '{}/{}.pdf'.format(dir_name, name)

        download_file(url, file_name)


def download_notes():
    dir_name = 'notes'
    os.makedirs(dir_name, exist_ok=True)

    # here we actually scrape the page because I'm too lazy to write the name of the notes
    page = requests.get('http://web.cs.iastate.edu/~cs531/notes.html').content
    tree = html.fromstring(page)

    a_elems = tree.cssselect('p > a')

    # links are in reverse chronological order on the website
    names = [elem.text for elem in a_elems][::-1]
    links = ['http://web.cs.iastate.edu/~cs531/notes/notes{}.pdf'.format(i) for i in range(1, 13)]

    for name, link in zip(names, links):
        file_name = '{}/{}.pdf'.format(dir_name, name)

        download_file(link, file_name)


def main():
    download_homework()
    download_notes()

if __name__ == '__main__':
    main()
