import os
import zipfile
import tempfile
import shutil
from pathlib import Path
import geopandas as gpd

from giga.utils.parameters import GigaParameters
from giga.utils.parse import DEFAULT_DOCID
from giga.utils.web import get_default_rwanda_pop_data, get_border_dataset
from giga.utils.logging import LOGGER


POPULATION_DATASETS = {'Rwanda': get_default_rwanda_pop_data}
FIPS_COUNTRY_CODES = {'Rwanda': 'RW'}
SHAPEFILE_NAME = 'TM_WORLD_BORDERS-0.3.shp'


def get_country_border_data(country, target_file):
    assert country in FIPS_COUNTRY_CODES, f"Country {country} is not supported try one of {list(FIPS_COUNTRY_CODES.keys())}"
    # download to a tmp directory
    tmp = tempfile.mkdtemp()
    tmpzip = os.path.join(tmp, 'borders.zip')
    get_border_dataset(tmpzip)
    with zipfile.ZipFile(tmpzip, "r") as zip_ref:
        zip_ref.extractall(tmp)
    # load in file and write to target
    shapefile = os.path.join(tmp, SHAPEFILE_NAME)
    borders = gpd.read_file(shapefile)
    border = borders[borders['FIPS'] == FIPS_COUNTRY_CODES[country]]
    border.to_file(target_file, driver='ESRI Shapefile')
    #cleanup
    shutil.rmtree(tmp)

def create_workspace(dir, country, docid=DEFAULT_DOCID):
    assert country in POPULATION_DATASETS, f"Country {country} is not supported, try one of {list(POPULATION_DATASETS.keys())}"
    Path(dir).mkdir(parents=True, exist_ok=True)
    population_file = os.path.join(dir, 'population.tiff')
    config_file = os.path.join(dir, 'parameters.json')
    border_file = os.path.join(dir, 'border.shp')
    POPULATION_DATASETS[country](population_file)
    get_country_border_data(country, border_file)
    LOGGER.info(f'Fetching parameters from google sheet with ID {docid}')
    parameters = GigaParameters.from_google_sheet(docid)
    parameters.to_json(config_file)
    return config_file, population_file, border_file


