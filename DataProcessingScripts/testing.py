import pytest
from unittest.mock import patch, Mock
from processDataManager import downloadFile
from OrganizeData import readFileName
from processData import tempConversion

@pytest.mark.parametrize("status_code, expected_result, link", [
    (200, True, "https://e4ftl01.cr.usgs.gov//ECOB/ECOSTRESS/ECO2LSTE.001/2024.03.10/ECOSTRESS_L2_LSTE_32186_001_20240310T061757_0601_01.h5"),
    (404, False, "https://dummylink.com/fileeee"),
])

def test_downloadFile(status_code, expected_result, link):
    with patch('requests.Session.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.iter_content = lambda chunk_size: [b'data']
        mock_get.return_value = mock_response
        result = downloadFile(link, 'dummyfile')
        assert result == expected_result


def test_readFileNameNegative():
    assert readFileName("") == False

def test_readFileNamePositive():
    assert readFileName("ECOSTRESS_L2_LSTE_02922_002_20190110T181332_0601_02.geojson") == True

def test_tempConversion():
    assert tempConversion( 100 ) == -456.07
