import datetime
import logging
import os
from collections.abc import Iterable
from multiprocessing import Pool
from typing import Callable, Optional

from openai import OpenAI

import requests


from tqdm_loggable.auto import tqdm
from tqdm_loggable.tqdm_logging import tqdm_logging
import time
from itertools import chain




import typer

from paraback import __title__ , util
from paraback.llmconnection.name_preprocessor import NamePreprocessor
from paraback.models.law_model import Law
from paraback.scraping.nltk_downloader import download_punkt
from paraback.scraping.scraper import Scraper


from paraback.linking.law_linker import LawLinker
from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.saving.mongo_connector import MongoConnector
from paraback.scraping.law_builder import LawBuilder



logger = logging.getLogger('paraback')

app = typer.Typer(
    name='paraback',
    help="backend parsing and linking laws"
)




@app.command("scrape")
def scrape(run_on_all_laws = None):
    if run_on_all_laws is None:
        run_on_all_laws = console_run_on_all

    links = Scraper.get_all_links()

    htmls = (Scraper.download_link(link) for link in links)
    laws = (LawBuilder.build_law(html) for html in htmls)

    run_on_all_laws(function= Scraper.scrape_and_save_law, laws=laws, count=len(links), workers=20)


@app.command("find_names")
def find_names(run_on_all_laws = None):
    if run_on_all_laws is None:
        run_on_all_laws = console_run_on_all
    io = MongoConnector(db="unlinked_laws")
    essential = io.read_essential()
    total = len(essential) + io.count_important() + io.count_all()
    laws = chain(essential, io.read_important(), io.read_all())
    run_on_all_laws(function= LawNameSearcher.find_and_save_name, laws= laws, count= total, workers=100)


@app.command("link")
def link(run_on_all_laws = None):
    if run_on_all_laws is None:
        run_on_all_laws = console_run_on_all
    io = MongoConnector(db="unlinked_laws", collection="de")
    count = io.count_all()
    target_laws = io.read_all()
    run_on_all_laws(LawLinker.link_and_save_law, target_laws, count)


@app.command("eWpG")
def ewpg():
    html = Scraper.download_link("https://www.gesetze-im-internet.de/ewpg/")
    law = LawBuilder.build_law(html)
    io = MongoConnector(collection="unlinked_laws")
    io.write(law)
    names_dict = io.read_all_names()
    law_name_searcher = LawNameSearcher(names_dict)

    io = MongoConnector(collection="laws")
    linker = LawLinker(law)
    linker.link()
    io.write(law)

@app.command("test")
def test():
    all_working = True
    logger.info("Testing the connection to the database")
    conn = MongoConnector()
    if (conn.test_connection()):
        logger.info("Connection to the database successful")
    else:
        logger.error("Connection to the database failed")
        all_working = False

    logger.info("Testing the connection to the openai api")
    try:
        OpenAI().models.list()
    except Exception as e:
        logger.error(e)
        logger.error("Connection to the openai api failed")
        all_working = False
    else:
        logger.info("Connection to the openai api successful")

    if all_working:
        logger.warning("Everything is working as expected")



def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__}")
        raise typer.Exit()

ConfigOption = typer.Option(
    os.getcwd()+"/config/config.yml",
    '-c',
    '--config',
    metavar='PATH',
    help="path to the program configuration"
)

VersionOption = typer.Option(
    None,
    '-v',
    '--version',
    callback=version_callback,
    is_eager=True,
    help="print the program version and exit"
)

@app.command()
def main(config_file: str = ConfigOption, version: bool = VersionOption):
    """
    The values of the CLI params that are passed to this application will show up als parameters to this function.
    """
    config = util.load_config(config_file)
    util.logging_setup(config)
    tqdm_logging.set_level(logging.INFO)
    logger.setLevel(logging.DEBUG)

    # Set the rate how often we update logs
    # Defaults to 10 seconds - optional
    tqdm_logging.set_log_rate(datetime.timedelta(seconds=5))
    logger.info("All set up. Let's get going.")

def console_run_on_all(function : Callable[[Law], str], laws : Iterable[Law], count : Optional[int]=None, workers: int=8):
    if count is None:
        count = len(list(laws))
    with Pool(50) as p:
        for name in (pbar := tqdm(p.imap(function, laws), total=count)):
            pbar.set_description(f"Processed: {name.rjust(30)}")


if __name__ == "__main__":
    app()

