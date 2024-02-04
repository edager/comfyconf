import comfyconf.readers as readers
import comfyconf.validators as validators
import comfyconf.utils as utils


def make_config(config_path: str, reader: str = "pyyaml") -> utils.DotDict:
    """
    Create a DotDict configuration object from a configuration file.

    This function reads a configuration file using the specified reader and returns
    a DotDict object representing the configuration.

    Args:
        config_path (str): The path to the configuration file.
        reader (str, optional): The name of the reader to use. Defaults to 'pyyaml'.

    Returns:
        DotDict: A DotDict object representing the configuration read from the file.

    Raises:
        ValueError: If the specified reader is not available.

    Examples:
        >>> config = make_config('config.yaml')
        >>> config.foo.bar
        'value_of_bar'
    """
    reader = utils.get_available(
        arg=reader, available_args=readers.available_readers, arg_type="reader"
    )
    yaml_dict = reader(config_path).read()
    return utils.DotDict(yaml_dict)


def validate_config(
    config: utils.DotDict,
    schema_path: str,
    validator: str = "json",
    load_args: dict = None,
    val_args: dict = None,
) -> None:
    validator = utils.get_available(
        arg=validator,
        available_args=validators.available_validators,
        arg_type="validator",
    )
    validator = validator(schema_path, load_args, val_args)

    try:
        validator.validate(config)
        print("config was successfully validated")
    except Exception as err:
        raise err
