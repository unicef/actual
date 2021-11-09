import requests
from tqdm import tqdm


BLOCK_SIZE = 1024 #1 Kibibyte

DEFAULT_RWANDA_POPULATION_URL = 'https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/RWA/rwa_ppp_2020_UNadj.tif'

DEFAULT_BORDER_DATASET_URL = 'https://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip'


def get_file_with_progress(url, target_file, name='file'):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
    response = requests.get(url, stream=True, headers=headers)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    progress_bar.set_description(f"Downloading {name}")
    with open(target_file, 'wb') as file:
        for data in response.iter_content(BLOCK_SIZE):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    assert total_size_in_bytes > 0 and progress_bar.n == total_size_in_bytes, f"Unable to complete download from {url}"

def get_default_rwanda_pop_data(target_file):
    get_file_with_progress(DEFAULT_RWANDA_POPULATION_URL, target_file, 'Rwanda population data')

def get_border_dataset(target_file):
    get_file_with_progress(DEFAULT_BORDER_DATASET_URL, target_file, 'Border dataset')
