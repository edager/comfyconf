import comfyconf.readers as readers
import comfyconf.utils as utils
import comfyconf.validators as validators


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
    """
    Validate a configuration against a schema using a specified validator.

    This function validates a configuration against a schema using a specified validator.
    It supports multiple validators such as 'json' and 'yamale'.

    Args:
        config (utils.DotDict): The configuration to validate.
        schema_path (str): The path to the schema file.
        validator (str, optional): The validator to use. Defaults to 'json'.
        load_args (dict, optional): Optional arguments to pass to the validator constructor when loading the schema.
        val_args (dict, optional): Optional arguments to pass to the validator's validate method.

    Returns:
        None

    Raises:
        ValueError: If the specified validator is not available.
        Exception: If validation fails.

    Examples:
        >>> validate_config(config, 'schema.json', validator='json')
        config was successfully validated
    """
    validator = utils.get_available(
        arg=validator,
        available_args=validators.available_validators,
        arg_type="validator",
    )
    validator = validator(schema_path, load_args, val_args)

    try:
        validator.validate(config)
        print(f"config was successfully validated")
    except Exception as err:
        raise err
