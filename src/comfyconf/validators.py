import json
from abc import ABC, abstractmethod

import jsonschema

from comfyconf.utils import DotDict, check_path


class SchemaValidator(ABC):
    """
    Abstract base class for schema validators.

    This class defines the interface for schema validators. Subclasses must implement
    the validate and _make_schema methods to provide functionality for validating
    configuration data against a schema.

    Attributes:
        schema_path (str): The path to the JSON schema file.
        load_args (dict): Optional arguments to pass to json.load when loading the schema file.
        val_args (dict): Optional arguments to pass to jsonschema.validate method.

    Methods:
        __init__(schema_path: str, load_args: dict = None, val_args: dict = None) -> None:
            Initialize the SchemaValidator with the given schema file path and optional arguments.

        validate(config: DotDict) -> None:
            Validate the given configuration data against the schema.

        _make_schema() -> dict:
            Abstract method to be implemented by subclasses for loading the schema.

    """

    def __init__(
        self, schema_path: str, load_args: dict = None, val_args: dict = None
    ) -> None:
        """
        Initialize the SchemaValidator with the given schema file path and optional arguments.

        Args:
            schema_path (str): The path to the schema file.
            load_args (dict, optional): Optional arguments to pass to load when loading the schema file.
            val_args (dict, optional): Optional arguments to pass to validate method.
        """
        self.schema_path = schema_path
        self.load_args = load_args or {}
        self.val_args = val_args or {}
        check_path(self.schema_path)
        self.schema = self._make_schema()

    @abstractmethod
    def validate(config: DotDict) -> None:
        """
        Validate the given configuration data against the schema.

        Args:
            config (DotDict): The configuration data to validate.

        Raises:
            ValidationError: If the configuration data does not conform to the schema.
        """

    @abstractmethod
    def _make_schema(self) -> dict:
        """
        Abstract method to be implemented by subclasses for loading the schema.

        Returns:
            dict: The loaded schema.
        """


class JSONSchema(SchemaValidator):
    """
    Validator for JSON schema.

    This class inherits from SchemaValidator and implements the validate method
    for validating configuration data against a JSON schema.

    """

    def __init__(
        self, schema_path, load_args: dict = None, val_args: dict = None
    ) -> None:
        """
        Initialize the JSONSchema validator with the given schema file path and optional arguments.

        Args:
            schema_path (str): The path to the JSON schema file.
            load_args (dict, optional): Optional arguments to pass to json.load when loading the schema file.
            val_args (dict, optional): Optional arguments to pass to jsonschema.validate method.
        """
        super().__init__(schema_path, load_args, val_args)

    def validate(self, config: DotDict) -> None:
        """
        Validate the given configuration data against the JSON schema.

        Args:
            config (DotDict): The configuration data to validate.

        Raises:
            ValidationError: If the configuration data does not conform to the schema.
        """
        try:
            jsonschema.validate(instance=config, schema=self.schema, **self.val_args)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)

    def _make_schema(self):
        """
        Load the JSON schema from the specified file.

        Returns:
            dict: The loaded JSON schema.
        """
        with open(self.schema_path) as fn:
            return json.load(fn, **self.load_args)


available_validators = {
    "json": JSONSchema,
}

try:
    import yamale

    class YamaleSchema(SchemaValidator):
        """
        Validator for YAML schemas using Yamale library.

        This class inherits from SchemaValidator and implements the validate method
        for validating configuration data against a YAML schema using the Yamale library.

        Attributes:
            schema_path (str): The path to the YAML schema file.
            load_args (dict): Optional arguments to pass to yamale.make_schema method when loading the schema.
            val_args (dict): Optional arguments to pass to yamale.validate method.

        Methods:
            __init__(schema_path: str, load_args: dict = None, val_args: dict = None) -> None:
                Initialize the YamaleSchema validator with the given schema file path and optional arguments.

            validate(config: DotDict) -> None:
                Validate the given configuration data against the YAML schema.

            _make_schema() -> dict:
                Load the YAML schema using yamale.make_schema.

        """

        def __init__(
            self, schema_path, load_args: dict = None, val_args: dict = None
        ) -> None:
            """
            Initialize the YamaleSchema validator with the given schema file path and optional arguments.

            Args:
                schema_path (str): The path to the YAML schema file.
                load_args (dict, optional): Optional arguments to pass to yamale.make_schema method when loading the schema.
                val_args (dict, optional): Optional arguments to pass to yamale.validate method.
            """
            super().__init__(schema_path, load_args, val_args)

        def validate(self, config: DotDict) -> None:
            """
            Validate the given configuration data against the YAML schema.

            Args:
                config (DotDict): The configuration data to validate.

            Raises:
                ValidationError: If the configuration data does not conform to the schema.
            """
            data = [(config, None)]  # the structure of return value of yamale.make_data
            try:
                yamale.validate(schema=self.schema, data=data, **self.val_args)
            except yamale.yamale_error.YamaleError as e:
                raise ValidationError(e.message)

        def _make_schema(self):
            """
            Load the YAML schema from the specified file using yamale.make_schema.

            Returns:
                dict: The loaded YAML schema.
            """
            return yamale.make_schema(path=self.schema_path, **self.load_args)

    available_validators["yamale"] = YamaleSchema

except ImportError:
    pass


class ValidationError(Exception):
    pass
