from abc import ABC, abstractmethod
import json
import jsonschema
from comfyconf.utils import check_path, DotDict


class SchemaValidator(ABC):
    def __init__(
        self, schema_path: str, load_args: dict = None, val_args: dict = None
    ) -> None:
        self.schema_path = schema_path
        self.load_args = load_args or {}
        self.val_args = val_args or {}
        check_path(self.schema_path)
        self.schema = self._make_schema()

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def _make_schema(self) -> dict:
        ...


class JSONSchema(SchemaValidator):
    def __init__(
        self, schema_path, load_args: dict = None, val_args: dict = None
    ) -> None:
        super().__init__(schema_path, load_args, val_args)

    def validate(self, config: DotDict) -> None:
        try:
            jsonschema.validate(instance=config, schema=self.schema, **self.val_args)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)

    def _make_schema(self):
        with open(self.schema_path) as fn:
            return json.load(fn, **self.load_args)


available_validators = {
    "json": JSONSchema,
}

try:
    import yamale

    class YamaleSchema(SchemaValidator):
        def __init__(
            self, schema_path, load_args: dict = None, val_args: dict = None
        ) -> None:
            super().__init__(schema_path, load_args, val_args)

        def validate(self, config: DotDict) -> None:
            data = [(config, None)]  # the structure of return value of yamale.make_data
            try:
                yamale.validate(schema=self.schema, data=data, **self.val_args)
            except yamale.yamale_error.YamaleError as e:
                raise ValidationError(e.message)

        def _make_schema(self):
            return yamale.make_schema(path=self.schema_path, **self.load_args)

    available_validators["yamale"] = YamaleSchema

except ImportError:
    pass


class ValidationError(Exception):
    pass
