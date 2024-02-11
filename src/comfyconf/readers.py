from abc import ABC, abstractmethod

import yaml

from comfyconf.utils import check_path


class Reader(ABC):
    """
    Abstract base class for configuration file readers.

    This class defines the interface for configuration file readers. Subclasses must implement
    the read method to provide functionality for reading configuration files.

    Attributes:
        config_path (Path): The path to the configuration file.

    Methods:
        __init__(config_path: str) -> None:
            Initialize the Reader with the given configuration file path.

        read() -> dict:
            Abstract method to be implemented by subclasses for reading configuration files.

    """

    def __init__(self, config_path: str) -> None:
        """
        Initialize the Reader with the given configuration file path.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.config_path = config_path

    @abstractmethod
    def read(self) -> dict:
        """
        Abstract method to be implemented by subclasses for reading configuration files.

        Returns:
            dict: A dictionary containing the configuration data.
        """


class PyYaml(Reader):
    """
    Configuration file reader for YAML format using PyYAML library.

    This class inherits from Reader and implements the read method to read configuration
    files in YAML format using the PyYAML library.

    """

    def __init__(self, config_path: str) -> None:
        """
        Initialize the PyYaml reader with the given configuration file path.

        Args:
            config_path (str): The path to the configuration file.
        """
        super().__init__(config_path)

    def read(self) -> dict:
        """
        Read the configuration file in YAML format using PyYAML library.

        Returns:
            dict: A dictionary containing the configuration data.
        """
        check_path(self.config_path)
        with open(self.config_path) as f:
            return yaml.safe_load(f)


# Dictionary to map reader names to reader classes
available_readers = {
    "pyyaml": PyYaml,
}

# Try importing Ruamel YAML library
try:
    from ruamel.yaml import YAML

    class Ruamel(Reader):
        """
        Configuration file reader for YAML format using Ruamel YAML library.

        This class inherits from Reader and implements the read method to read configuration
        files in YAML format using the Ruamel YAML library.

        """

        def __init__(self, config_path: str) -> None:
            """
            Initialize the Ruamel reader with the given configuration file path.

            Args:
                config_path (str): The path to the configuration file.
            """
            super().__init__(config_path)

        def read(self) -> dict:
            """
            Read the configuration file in YAML format using Ruamel YAML library.

            Returns:
                dict: A dictionary containing the configuration data.
            """
            check_path(self.config_path)
            yaml = YAML(typ="safe")
            return yaml.load(self.config_path)

    available_readers["ruamel"] = Ruamel

except ImportError:
    pass
