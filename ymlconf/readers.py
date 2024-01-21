from abc import ABC, abstractmethod
from pathlib import Path
import yaml

class Reader(ABC):        
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        
    def _check_path(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"{self.config_path} was not found")

    @abstractmethod 
    def read(self) -> dict:
        ...

class PyYaml(Reader):
    def __init__(self, config_path):
        super().__init__(config_path)

    def read(self) -> dict:
        self._check_path()
        with open(self.config_path) as f:
            return yaml.safe_load(f)


available_readers = {
    'pyyaml': PyYaml,
}

try:
    from ruamel.yaml import YAML 
    
    class Ruamel(Reader):
        def __init__(self, config_path) -> None:
            super().__init__(config_path)

        def read(self) -> dict:
            self._check_path()
            yaml=YAML(typ='safe')
            return yaml.load(self.config_path)   
    
    available_readers['ruamel'] = Ruamel

except ImportError:
    pass


def get_reader(reader):
    try:
        return available_readers[reader]
    except KeyError:
        raise ValueError(f'{reader} is not a reader, available readers are {available_readers.keys()}')