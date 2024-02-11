from pathlib import Path

import pytest
import yamale

from comfyconf.utils import DotDict
from comfyconf.validators import JSONSchema, ValidationError, YamaleSchema


class TestJSONSchema:
    test_path = "foo.json"
    test_json = """{"type": "object", "properties": {"a": {"type": "string"}}}"""

    def test_init(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_json)

        test_obj = JSONSchema(self.test_path)

        try:
            assert test_obj.schema_path == self.test_path

        finally:
            Path(self.test_path).unlink()

    def test_make_schema(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_json)

        test_obj = JSONSchema(self.test_path)

        try:
            assert test_obj.schema == {
                "type": "object",
                "properties": {"a": {"type": "string"}},
            }

        finally:
            Path(self.test_path).unlink()

    def test_validate_valid_config(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_json)

        test_obj = JSONSchema(self.test_path)
        test_dict = DotDict({"a": "foo"})
        try:
            assert test_obj.validate(test_dict) is None
        finally:
            Path(self.test_path).unlink()

    def test_validate_invalid_conf(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_json)

        test_obj = JSONSchema(self.test_path)
        test_dict = DotDict({"a": 1})
        try:
            with pytest.raises(ValidationError):
                test_obj.validate(test_dict)
        finally:
            Path(self.test_path).unlink()


class TestYamaleSchema:
    test_path = "foo.yaml"
    test_yaml = """a: str()"""

    def test_init(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_yaml)

        test_obj = YamaleSchema(self.test_path)

        try:
            assert test_obj.schema_path == self.test_path

        finally:
            Path(self.test_path).unlink()

    def test_make_schema(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_yaml)

        test_obj = YamaleSchema(self.test_path)

        try:
            assert test_obj.schema.dict == {"a": yamale.validators.validators.String()}

        finally:
            Path(self.test_path).unlink()

    def test_validate_valid_config(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_yaml)

        test_obj = YamaleSchema(self.test_path)
        test_dict = DotDict({"a": "foo"})
        try:
            assert test_obj.validate(test_dict) is None
        finally:
            Path(self.test_path).unlink()

    def test_validate_invalid_conf(self):
        with open(self.test_path, "w") as f:
            f.write(self.test_yaml)

        test_obj = YamaleSchema(self.test_path)
        test_dict = DotDict({"a": 1})
        try:
            with pytest.raises(ValidationError):
                test_obj.validate(test_dict)
        finally:
            Path(self.test_path).unlink()
