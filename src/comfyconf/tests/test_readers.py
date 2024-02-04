from comfyconf.readers import PyYaml, Ruamel
from pathlib import Path
import pytest


class TestPyYaml:
    test_object = PyYaml("test_path.yaml")

    def test_init(self):
        assert self.test_object.config_path == "test_path.yaml"

    def test_raise_filenotfound(self):
        with pytest.raises(FileNotFoundError):
            self.test_object.read()

    def test_reads_file(self):
        test_content = """line1: 'A'"""
        path = Path("test.yaml")
        obj = PyYaml(path)

        with open(path, "w") as f:
            f.write(test_content)

        try:
            assert obj.read() == {"line1": "A"}
        finally:
            path.unlink()


class TestRuamelYaml:
    test_object = Ruamel("test_path.yaml")

    def test_init(self):
        assert self.test_object.config_path == "test_path.yaml"

    def test_raise_filenotfound(self):
        with pytest.raises(FileNotFoundError):
            self.test_object.read()

    def test_reads_file(self):
        test_content = """line1: 'A'"""
        path = Path("test.yaml")
        obj = Ruamel(path)

        with open(path, "w") as f:
            f.write(test_content)

        try:
            assert obj.read() == {"line1": "A"}
        finally:
            path.unlink()
