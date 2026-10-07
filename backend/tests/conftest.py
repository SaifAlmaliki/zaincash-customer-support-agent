import pytest

from app.config import REPO_ROOT
from app.taxonomy import load_taxonomy


@pytest.fixture(scope="session")
def tax():
    return load_taxonomy(REPO_ROOT / "data" / "taxonomy.yaml")
