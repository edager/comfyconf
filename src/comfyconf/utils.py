from pathlib import Path


class DotDict(dict):
    """
    A dictionary subclass that allows access to its elements using dot notation.

    This class inherits from the built-in `dict` class and enhances it with dot notation access.
    Dot notation allows accessing dictionary elements as attributes, providing more concise syntax.

    Attributes:
        dictionary (dict): The dictionary to be wrapped by the DotDict instance.

    Methods:
        __init__(dictionary: dict) -> None:
            Initialize the DotDict with the given dictionary.

        error_if_numerical_key(dictionary: dict) -> None:
            Recursively checks the dictionary for numerical keys and raises a ValueError if found.

    Examples:
        >>> d = DotDict({'foo': 1, 'bar': {'baz': 2}})
        >>> d.foo
        1
        >>> d.bar.baz
        2

    Note:
        Numerical keys are not allowed, as they can't be accessed using dot notation.
        Attempting to access or set numerical keys with dot notation will result in a SyntaxError.
    """

    def __init__(self, dictionary: dict) -> None:
        """
        Initialize the DotDict with the given dictionary.

        Args:
            dictionary (dict): The dictionary to be wrapped by the DotDict instance.
        """
        self._error_if_numerical_key(dictionary)
        super().__init__(dictionary)

    def __getattr__(*args):
        """
        Retrieve the value of the given attribute.

        Args:
            *args: Variable-length argument list.

        Returns:
            The value associated with the given attribute.

        Raises:
            KeyError: If the attribute does not exist.
        """
        value = dict.__getitem__(*args)
        return DotDict(value) if isinstance(value, dict) else value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def _error_if_numerical_key(self, dictionary: dict) -> None:
        """
        Recursively checks the dictionary for numerical keys and raises a ValueError if found.

        Args:
            dictionary (dict): The dictionary to be checked.

        Raises:
            ValueError: If a numerical key is found in the dictionary.
        """
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if str(key).isnumeric():
                    raise ValueError(
                        f"Numerical keys are not allowed, however one was found: '{key}'"
                    )
                else:
                    self._error_if_numerical_key(value)


def check_path(filename) -> None:
    """
    Check if the file exists.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"{filename} was not found")

    if not path.is_file():
        raise ValueError(f"{filename} is not a regular file")


def get_available(arg: str, available_args: dict, arg_type: str):
    """
    Get the configuration file reader class based on the provided reader name.

    Args:
        reader (str): The name of the reader.

    Returns:
        Reader: An instance of the configuration file reader class corresponding to the provided name.

    Raises:
        ValueError: If the provided reader name is not valid.
    """
    try:
        return available_args[arg]
    except KeyError:
        raise ValueError(
            f"{arg} is not a {arg_type}, available {arg_type}s are {available_args.keys()}"
        )
