import pytest
from pathlib import Path

from giga.models.giga import GigaNode, REQUIRED_ARGUMENTS
from giga.utils.parameters import GigaParameters


#DEFAULT_CONFIG = 'defaults.json'

DEFAULT_CONFIG = Path(__file__).resolve().parent / 'defaults.json'


def test_giga_model(giga_params):
    """
        Initialize the giga model and check it for all required parameters
    """
    node = GigaNode.from_giga_parameters('giga-node', giga_params, 'test.tiff')
    assert all([req in node.__dict__ for req in REQUIRED_ARGUMENTS])

@pytest.fixture
def giga_params():
    print(DEFAULT_CONFIG)
    return GigaParameters.from_json(DEFAULT_CONFIG)