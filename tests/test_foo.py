from config import ROOT_DIR
from src.foo import jet_last_executed, jet_json_data, output_last_operations
import pytest
import os


def test_jet_json_data_file_not_found():
    FILE_PATH = os.path.join(ROOT_DIR, 'tests', 'test_operation')
    with pytest.raises(FileNotFoundError):
        jet_json_data(FILE_PATH)


def test_jet_json_data():
    FILE_PATH = os.path.join(ROOT_DIR, 'tests', 'test_operations.json')
    assert jet_json_data(FILE_PATH)[0] == {'id': 863064926,
                                           'state': 'EXECUTED',
                                           'date': '08.12.2019',
                                           'operationAmount':
                                               {'amount': '41096.24',
                                                'currency':
                                                    {'name': 'USD',
                                                     'code': 'USD'}
                                                },
                                           'description': 'Открытие вклада',
                                           'to': 'Счет 90424923579946435907'}


def test_jet_last_executed():
    FILE_PATH = os.path.join(ROOT_DIR, 'tests', 'test_operations.json')
    if len(FILE_PATH) > 5:
        assert len(jet_last_executed()) == 5
    else:
        assert len(jet_last_executed()) <= 5


def test_output_last_operations():
    assert len(output_last_operations()) == len(jet_last_executed())


if __name__ == '__main__':
    pytest.main()
