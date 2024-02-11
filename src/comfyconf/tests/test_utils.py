from pathlib import Path

import pytest

from comfyconf.readers import available_readers
from comfyconf.utils import DotDict, check_path, get_available
from comfyconf.validators import available_validators


class TestDotDict:
    def test_simple_dict(self):
        test = DotDict({"a": "b"})
        assert test.a == "b"

    def test_nested_dict(self):
        test = DotDict({"a": {"b": "c"}})
        assert test.a.b == "c"

    def test_key_not_present(self):
        test = DotDict({"a": "b"})
        with pytest.raises(KeyError):
            test.c

    def test_numerical_key_error(self):
        with pytest.raises(ValueError):
            DotDict({1: "b"})

    def test_nested_numerical_key_error(self):
        with pytest.raises(ValueError):
            DotDict({"a": {1: "b"}})


class TestCheckPath:
    def test_raise_if_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            check_path("NOT_A_PATH")

    def test_raise_if_not_regular_file(self):
        test_name = "./test_dir"
        test_case = Path(test_name)
        test_case.mkdir()

        try:
            with pytest.raises(ValueError):
                check_path(test_name)

        finally:
            test_case.rmdir()

    def test_file_exist_and_is_regular(self):
        test_content = """line1: 'A'"""
        path = Path("test.yaml")

        with open(path, "w") as f:
            f.write(test_content)

        try:
            assert check_path(path) is None
        finally:
            path.unlink()


class TestGetAvailable:
    reader_args = {"available_args": available_readers, "arg_type": "reader"}
    validator_args = {"available_args": available_validators, "arg_type": "validators"}

    def test_valid_readers(self):
        for key, value in available_readers.items():
            assert get_available(key, **self.reader_args) == value

    def test_invalid_reader(self):
        with pytest.raises(ValueError):
            get_available("not_a_reader", **self.reader_args)

    def test_valid_validators(self):
        for key, value in available_validators.items():
            assert get_available(key, **self.validator_args) == value

    def test_invalid_validator(self):
        with pytest.raises(ValueError):
            get_available("not_a_validator", **self.validator_args)
