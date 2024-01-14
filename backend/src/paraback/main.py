import datetime
import logging
import os
import multiprocessing

from tqdm_loggable.auto import tqdm
from tqdm_loggable.tqdm_logging import tqdm_logging


import typer

from paraback import __title__ , util

from pymongo import MongoClient

from paraback.orchestrator import Orchestrator
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


    def process_link(link):
        orchestrator = Orchestrator(link)
        orchestrator.run()

    for link in (pbar:=tqdm(links, total=len(links))):
        pbar.set_description(f"Processing link {str(link.split('/')[-2])[:10].ljust(10,' ')}")
        process_link(link)


    logger.info("All done. Bye!")


if __name__ == "__main__":
    app()
