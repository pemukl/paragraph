import datetime
import logging
import os
import multiprocessing

from tqdm_loggable.auto import tqdm
from tqdm_loggable.tqdm_logging import tqdm_logging


import typer

from paraback import __title__ , util

from pymongo import MongoClient

from paraback.linking.law_linker import LawLinker
from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.linking.regex_ts_linker import RegexTSLinker
from paraback.orchestrator import Orchestrator
from paraback.saving.mongo_connector import MongoConnector
from paraback.scraping.law_builder import LawBuilder
from paraback.scraping.scraper import Scraper

logger = logging.getLogger('paraback')

app = typer.Typer(
    name='paraback',
    help="backend parsing and linking laws"
)


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

    # Set the rate how often we update logs
    # Defaults to 10 seconds - optional
    tqdm_logging.set_log_rate(datetime.timedelta(seconds=5))
    logger.info("All set up. Let's get going!")

    links = Scraper.get_all_links()[:10]

    htmls = (Scraper.download_link(link) for link in links)
    laws = [LawBuilder.build_law(html) for html in htmls]

    io = MongoConnector()
    for law in laws:
        io.write_name(law)

    law_name_searcher = LawNameSearcher()

    for law in laws:
        linker = LawLinker(law)
        linker.set_law_name_searcher(law_name_searcher)
        linker.link()

    for law_linked in laws:
        io.write(law_linked)

    def process_link(link):
        html = Scraper.download_link(link)
        law = LawBuilder.build_law(html)
        law_linked = RegexTSLinker.link_all(law)
        io = MongoConnector()
        io.write(law_linked)

    for link in (pbar:=tqdm(links, total=len(links))):
        pbar.set_description(f"Processing link {str(link.split('/')[-2])[:10].ljust(10,' ')}")
        process_link(link)


    logger.info("All done. Bye!")


@app.command("scrape")
def scrape():
    links = Scraper.get_all_links()

    htmls = (Scraper.download_link(link) for link in links)
    laws = (LawBuilder.build_law(html) for html in htmls)

    io = MongoConnector(collection="unlinked_laws")
    for law in (pbar := tqdm(laws, desc='Scraping links', total=len(links))):
        pbar.set_description(f"Downloading, Building and Saving '{law.stemmedabbreviation.ljust(15,' ')}'")
        if law.abbreviation.endswith("Prot"):
            logger.warning(f"Skipping '{law.stemmedabbreviation}'")
            continue
        io.write(law)
        io.write_name(law)

@app.command("link")
def link():
    io = MongoConnector(collection="laws")
    names_dict = io.read_all_names()
    stem_set = set(names_dict.values())

    law_name_searcher = LawNameSearcher(names_dict)

    for law in (pbar := tqdm(stem_set, desc='Linking laws', total=len(stem_set))):
        pbar.set_description(f"Linking '{law.stemmedabbreviation.ljust(15,' ')}'")
        linker = LawLinker(law)
        linker.set_law_name_searcher(law_name_searcher)
        linker.link()
        io.write(law)

@app.command("eWpG")
def eWpG():
    html = Scraper.download_link("https://www.gesetze-im-internet.de/ewpg/")
    law = LawBuilder.build_law(html)
    io = MongoConnector(collection="unlinked_laws")
    io.write(law)
    names_dict = io.read_all_names()
    law_name_searcher = LawNameSearcher(names_dict)

    io = MongoConnector(collection="laws")
    linker = LawLinker(law)
    linker.set_law_name_searcher(law_name_searcher)
    linker.link()
    io.write(law)

if __name__ == "__main__":
    app()
