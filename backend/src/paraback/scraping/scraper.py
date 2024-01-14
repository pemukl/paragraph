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

from tqdm_loggable.auto import tqdm


data_path = os.path.join("/Users", "marc", "Code", "paragraph", "backend", "data")

class Scraper:

    @staticmethod
    def get_all_links():
        links = []
        lists = Scraper._get_all_lists()

        for tar in (pbar := tqdm(lists, desc='Scraping links')):
            pbar.set_description(f"Scraping links from letter '{tar.split('/')[-1][-6].upper()}'")
            links += Scraper._get_all_landings(tar)
        return links

    @staticmethod
    def download_link(link):
        target = Scraper._landing_to_target(link)
        if target is None:
            raise Exception("No target found for landing " + link)
        return Scraper._download_target(target)

    @staticmethod
    def _get_all_lists():
        session = HTMLSession()
        r = session.get('https://www.gesetze-im-internet.de/aktuell.html')

        c = r.html.find('#container', first=True)

        lists = ["https://www.gesetze-im-internet.de/" + elm.get("href")[2:] for elm in
                 c.lxml.findall(".//a[@class='alphabet']")]
        return lists

    @staticmethod
    def _get_all_landings(list_url):
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

    @staticmethod
    def _landing_to_target(landing_url):
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

    @staticmethod
    def _download_target(target_url):
        """Download the target url and return the html"""
        session = HTMLSession()
        r = session.get(target_url)
        return r.html.html

