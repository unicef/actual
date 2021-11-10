import os
import zipfile
import tempfile
import shutil
from pathlib import Path
import geopandas as gpd

from giga.utils.parameters import GigaParameters
from giga.utils.parse import DEFAULT_DOCID
from giga.utils.web import get_border_dataset, get_file_with_progress
from giga.utils.logging import LOGGER
from giga.utils.commons import SUPPORTED_COUNTRIES


SHAPEFILE_NAME = 'TM_WORLD_BORDERS-0.3.shp'


def get_country_border_data(country, target_file):
    assert country in SUPPORTED_COUNTRIES, f"Country {country} is not supported try one of {list(SUPPORTED_COUNTRIES.keys())}"
    # download to a tmp directory
    tmp = tempfile.mkdtemp()
    tmpzip = os.path.join(tmp, 'borders.zip')
    get_border_dataset(tmpzip)
    with zipfile.ZipFile(tmpzip, "r") as zip_ref:
        zip_ref.extractall(tmp)
    # load in file and write to target
    shapefile = os.path.join(tmp, SHAPEFILE_NAME)
    borders = gpd.read_file(shapefile)
    border = borders[borders['FIPS'] == SUPPORTED_COUNTRIES[country]['FIPS']]
    border.to_file(target_file, driver='ESRI Shapefile')
    #cleanup
    shutil.rmtree(tmp)

def create_workspace(dir, country, docid=DEFAULT_DOCID):
    assert country in SUPPORTED_COUNTRIES, f"Country {country} is not supported, try one of {list(SUPPORTED_COUNTRIES.keys())}"
    # setup
    Path(dir).mkdir(parents=True, exist_ok=True)
    population_file = os.path.join(dir, 'population.tiff')
    config_file = os.path.join(dir, 'parameters.json')
    border_file = os.path.join(dir, 'border.shp')
    # fetch population
    popurl = SUPPORTED_COUNTRIES[country]['population']
    get_file_with_progress(popurl, population_file, f'{country} population data')
    # fetch border data
    get_country_border_data(country, border_file)
    LOGGER.info(f'Fetching parameters from google sheet with ID {docid}')
    parameters = GigaParameters.from_google_sheet(docid)
    parameters.to_json(config_file)
    return config_file, population_file, border_file


