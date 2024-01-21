import ymlconf.readers as readers

def make_config(config_path, reader='pyyaml'):
    reader = readers.get_reader(reader)
    yaml_dict = reader(config_path).read()    
    return DotDict(yaml_dict) 

class DotDict(dict):     
    """dot notation access to dictionary keys"""      
    def __init__(self, dictionary: dict)-> None:
        # checks that keys are not numeric, as numerical keys can't be accessed 
        # with dot notation (e.g config.2.key) without giving rise to a SyntaxError    
        self.error_if_numerical_key(dictionary)
        return super().__init__(dictionary)

    def __getattr__(*args):         
        value = dict.__getitem__(*args)         
        return DotDict(value) if isinstance(value, dict) else value      
    __setattr__ = dict.__setitem__     
    __delattr__ = dict.__delitem__     

    def error_if_numerical_key(self, dictionary: dict):
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if str(key).isnumeric():
                    raise ValueError(f"Numerical keys are not allowed, however one was found: '{key}'")
                else:
                    self.error_if_numerical_key(value)