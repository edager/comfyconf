from comfyconf.config import make_config, validate_config
from comfyconf.readers import available_readers
from comfyconf.validators import ValidationError
import pytest
from pathlib import Path


def make_file(test_content, path):
    with open(path, "w") as f:
        f.write(test_content)


class TestMakeConfig:
    def test_simple_config(self):
        path = Path("test.yaml")
        content = """a: b"""
        make_file(content, path)

        try:
            for reader in available_readers.keys():
                config = make_config(path, reader)
                assert config.a == "b"
        finally:
            path.unlink()

    def test_nested_config(self):
        path = Path("test.yaml")
        content = """
        a: 
          b: c 
        """
        make_file(content, path)
        try:
            for reader in available_readers.keys():
                config = make_config(path, reader)
                assert config.a.b == "c"
        finally:
            path.unlink()


class TestValidateConfig:
    def test_raise_on_invalid_validator(self):
        path = Path("test.yaml")
        content = """a: b"""
        make_file(content, path)
        config = make_config(path)

        test_yamale_schema_path = Path("test_schema.yaml")
        test_yaml = """a: str()"""
        make_file(test_yaml, test_yamale_schema_path)

        try:
            with pytest.raises(ValueError):
                validate_config(
                    config=config,
                    schema_path=test_yamale_schema_path,
                    validator="notavalidator",
                )
        finally:
            path.unlink()
            test_yamale_schema_path.unlink()

    def test_valid_config_with_valid_yamaleschema(self):
        path = Path("test.yaml")
        content = """a: b"""
        make_file(content, path)
        config = make_config(path)

        test_yamale_schema_path = Path("test_schema.yaml")
        test_yaml = """a: str()"""
        make_file(test_yaml, test_yamale_schema_path)

        try:
            assert (
                validate_config(
                    config=config,
                    schema_path=test_yamale_schema_path,
                    validator="yamale",
                )
                is None
            )
        finally:
            path.unlink()
            test_yamale_schema_path.unlink()

    def test_valid_config_with_invalid_yamaleschema(self):
        path = Path("test.yaml")
        content = """a: b"""
        make_file(content, path)
        config = make_config(path)

        test_yamale_schema_path = Path("test_schema.yaml")
        test_yaml = """a: str("""
        make_file(test_yaml, test_yamale_schema_path)

        try:
            with pytest.raises(SyntaxError):
                validate_config(
                    config=config,
                    schema_path=test_yamale_schema_path,
                    validator="yamale",
                ) is None
        finally:
            path.unlink()
            test_yamale_schema_path.unlink()

    def test_invalid_config_with_valid_yamaleschema(self):
        path = Path("test.yaml")
        content = """a: 1"""
        make_file(content, path)
        config = make_config(path)

        test_yamale_schema_path = Path("test_schema.yaml")
        test_yaml = """a: str()"""
        make_file(test_yaml, test_yamale_schema_path)

        try:
            with pytest.raises(ValidationError):
                validate_config(
                    config=config,
                    schema_path=test_yamale_schema_path,
                    validator="yamale",
                )
        finally:
            path.unlink()
            test_yamale_schema_path.unlink()

    def test_validate_config_with_valid_yamaleschema_using_optional_parser(self):
        path = Path("test.yaml")
        content = """a: b"""
        make_file(content, path)
        config = make_config(path)

        test_yamale_schema_path = Path("test_schema.yaml")
        test_yaml = """a: str()"""
        make_file(test_yaml, test_yamale_schema_path)

        try:
            validate_config(
                config=config,
                schema_path=test_yamale_schema_path,
                validator="yamale",
                load_args={"parser": "ruamel"},
            ) is None
        finally:
            path.unlink()
            test_yamale_schema_path.unlink()
