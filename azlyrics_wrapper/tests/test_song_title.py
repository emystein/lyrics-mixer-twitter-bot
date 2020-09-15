import pytest
from azlyrics_wrapper.model import SongTitle


@pytest.mark.slow_integration_test
def test_random():
	title = SongTitle.random()

	assert title.artist != ''
	assert title.title != ''
