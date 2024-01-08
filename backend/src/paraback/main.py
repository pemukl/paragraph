import logging
import os
import multiprocessing
import tqdm

import typer

from paraback import __title__ , __version__, util
from paraback.scraping.nltk_downloader import download_punkt


from pymongo import MongoClient

from paraback.orchestrator import Orchestrator
from paraback.scraping.downloader import get_all_links

logger = logging.getLogger('paraback')

app = typer.Typer(
    name='paraback',
    help="backend parsing and linking laws"
)


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
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
    logger.info("All set up! Let's get going!")

    links = get_all_links()[:10]

    def process_link(link):
        orchestrator = Orchestrator(link)
        orchestrator.run()
    print(links)

    for link in tqdm.tqdm(links, total=len(links), desc="scraping laws"):
        process_link(link)

    #with multiprocessing.Pool() as p:
    #    list(tqdm.tqdm(p.imap(process_link, links), total=len(links), desc="scraping laws"))

    logger.info("All done. Bye!")


if __name__ == "__main__":
    app()
