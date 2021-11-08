import os
from pathlib import Path

from giga.utils.parameters import GigaParameters
from giga.utils.parse import DEFAULT_DOCID
from giga.utils.web import get_default_rwanda_pop_data
from giga.utils.logging import LOGGER


POPULATION_DATASETS = {'Rwanda': get_default_rwanda_pop_data}


def create_workspace(dir, country, docid=DEFAULT_DOCID):
    assert country in POPULATION_DATASETS, f"Country {country} is not supported, try one of {list(POPULATION_DATASETS.keys())}"
    Path(dir).mkdir(parents=True, exist_ok=True)
    population_file = os.path.join(dir, 'population.tiff')
    config_file = os.path.join(dir, 'parameters.json')
    get_default_rwanda_pop_data(population_file)
    LOGGER.info(f'Fetching parameters from google sheet with ID {docid}')
    parameters = GigaParameters.from_google_sheet(docid)
    parameters.to_json(config_file)
    return config_file, population_file


