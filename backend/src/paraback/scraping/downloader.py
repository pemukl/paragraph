#!/usr/bin/env python3
"""
Module Docstring
"""
import shutil
from datetime import datetime
import multiprocessing
import os

from requests_html import HTMLSession

__author__ = "Marc Schneider"

import tqdm

data_path = os.path.join("/Users", "marc", "Code", "paragraph", "backend", "data")

def get_lists():
    session = HTMLSession()
    r = session.get('https://www.gesetze-im-internet.de/aktuell.html')

    c = r.html.find('#container', first=True)

    lists = ["https://www.gesetze-im-internet.de/" + elm.get("href")[2:] for elm in
             c.lxml.findall(".//a[@class='alphabet']")]
    return lists


def get_and_download_targets(list_url):
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
        list(tqdm.tqdm(p.imap(landing_to_target, landings), total=len(landings), desc=list_url.split("/")[-1], leave=False, position=1))

def get_targets(list_url):
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

    return landings


def landing_to_target(landing_url):
    base = "/".join(landing_url.split("/")[:-1]) + "/"
    session = HTMLSession()
    r = session.get(landing_url)
    heading = r.html.find('h2', containing='Gesamtausgabe der Norm im Format', first=True)
    links = heading.lxml.findall(".//a")
    if (len(links) == 0):
        return None

    for link in links:
        if (len(link) == 0):
            continue
        text = link[0].text
        if text is not None and text.startswith("HTML"):
            res = base + link.get("href")
            return res
    return None


def download_target(target_url,save=False):
    """Download the target url and save the html to a file"""
    session = HTMLSession()
    r = session.get(target_url)
    name = target_url.split("/")[-2]
    if save:
        filename = os.path.join(folder_path(), name + ".html")
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        with open(filename,'w') as f:
            tag = f"<! -- \n Law \n{name}\n scraped by Paragraph on \n{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}\n from \n{target_url}\n -->\n"
            f.write(tag+r.html.html)
        r.close()
        session.close()
    return r.html.html

def folder_path():
    return os.path.join(data_path,'html_dump')

def get_all_links():
    all = []
    lists = get_lists()
    for tar in tqdm.tqdm(lists, desc='Scraping links'):
        all += get_targets(tar)
    return all


def main():

    print("Indexing download links.")
    lists = get_lists()
    with tqdm.tqdm(lists, position=0, desc='Total', leave=True) as outter_range:
        for i,tar in enumerate(outter_range):
            get_and_download_targets(tar)

    if not os.path.exists(folder_path()):
        os.makedirs(folder_path())
    print("Copying files to htmls folder.")
    for file in os.listdir(folder_path()):
        shutil.copy(os.path.join(data_path,'html_dump',file), os.path.join(get_project_root(),'data','htmls',file))




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
