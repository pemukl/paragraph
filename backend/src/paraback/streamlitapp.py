# UPDATED: 5-MAY-2023
from multiprocessing import Pool
from typing import Iterable, Optional, Callable

from paraback.main import scrape, find_names

import streamlit as st

# https://discuss.streamlit.io/t/stqdm-a-tqdm-like-progress-bar-for-streamlit/10097
# pip install stqdm
from stqdm import stqdm

from paraback.models.law_model import Law

import streamlit as st
import os
import signal

num_p = 20
message = st.empty()

def get_run_on_all(pane, verb):
    container = pane.container()
    def st_run_on_all(function : Callable[[Law], None], laws : Iterable[Law], count : Optional[int]=None, workers: int=8):
        if count is None:
            count = len(list(laws))
        with container:
            with Pool(processes=workers) as pool:
                for name in stqdm(pool.imap(function, laws), total=count):
                    message.success(f"{verb}: {name}")

    return st_run_on_all


if __name__ == '__main__':

    col1, col2 = st.columns([1, 3])
    if col1.button("Scrape"):
        scrape(get_run_on_all(col2, "Scraped"))

    col1, col2 = st.columns([1, 3])
    if col1.button("Find Names"):
        find_names(get_run_on_all(col2, "Found Names"))

    col1, col2 = st.columns([1, 3])
    if col1.button("Link"):
        find_names(get_run_on_all(col2, "Linked"))

