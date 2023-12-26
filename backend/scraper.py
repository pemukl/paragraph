#!/usr/bin/env python3
"""
Module Docstring
"""
from datetime import datetime
import multiprocessing
import os

from requests_html import HTMLSession

__author__ = "Marc Schneider"

import tqdm


def get_lists():
    session = HTMLSession()
    r = session.get('https://www.gesetze-im-internet.de/aktuell.html')

    c = r.html.find('#container', first=True)

    lists = ["https://www.gesetze-im-internet.de/" + elm.get("href")[2:] for elm in
             c.lxml.findall(".//a[@class='alphabet']")]
    return lists


def get_targets(list_url, leave=False):
    session = HTMLSession()
    r = session.get(list_url)

    c = r.html.find('#container', first=True)

    pars = c.lxml.findall(".//p")
    landings = []
    for par in pars:
        first = par.findall(".//a")[0]
        if first is not None:
            landings.append("https://www.gesetze-im-internet.de/" + first.get("href")[2:])

    r.close()
    session.close()

    with multiprocessing.Pool() as p:
        list(tqdm.tqdm(p.imap(landing_to_target, landings), total=len(landings), desc=list_url.split("/")[-1], leave=leave, position=1))



def landing_to_target(landing_url):
    base = "/".join(landing_url.split("/")[:-1]) + "/"
    session = HTMLSession()
    r = session.get(landing_url)
    heading = r.html.find('h2', containing='Gesamtausgabe der Norm im Format', first=True)
    links = heading.lxml.findall(".//a")
    if (len(links) == 0):
        return

    for link in links:
        if (len(link) == 0):
            continue
        text = link[0].text
        if text is not None and text.startswith("HTML"):
            res = base + link.get("href")
            download_target(res)


def download_target(target_url):
    """Download the target url and save the html to a file"""
    session = HTMLSession()
    r = session.get(target_url)
    name = target_url.split("/")[-2]
    with open("laws/" + target_url.split("/")[-2] + ".html", "w") as f:
        tag = f"<! -- \n Law \n{name}\n scraped by LexLynk on \n{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}\n from \n{target_url}\n -->\n"
        f.write(tag+r.html.html)
    r.close()
    session.close()

def main():
    """ Main entry point of the app """
    lists = get_lists()
    #delete all files in laws folder
    dir = 'htmls'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    print("Indexing download links.")

    with tqdm.tqdm(lists, position=0, desc='Total') as outter_range:
        for i,tar in enumerate(outter_range):
            leave = i == len(outter_range) - 1
            get_targets(tar, leave=leave)








if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
