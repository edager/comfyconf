# comfyconf

## What is it for?

Using YAML configuration files for python require less boilerplate code, and accessing the values by dot notation.

## Installation

```bash
pip install comfyconf
```

## Usage

### Basic

Create a config file in YAML and name it foo.yaml:

```yaml
test:
  title: 'test' 
  ip: '127.0.0.1' 
  port: 5000

production:
  title: 'My amazing server' 
  ip: '1234.255.255.1' 
  port: 1234
```

Now, load it using `make_config`:

```python
>>> from comfyconf import make_config   
>>> config = make_config("foo.yaml")
>>> config.test.ip
'127.0.0.1'
>>> config.production.port
1234  
```

Note that numerical keys are not allowed (even if they're strings in YAML), doing so will raise a `ValueError`.  

### Using ruamel.yaml as parser instead of pyyaml

If you prefer ruamel.yaml or need to parse YAML 1.2 document you can specify `"ruamel"`` as the reader:

```python 
>>> config = make_config("foo.yaml", reader="ruamel")
```

### Validate configuration against a schema 

If you need to be validate that the configuration is compatible with a schema,
you can use validate_config:

First, create a schema:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "additionalProperties": false,
  "$defs": {  
    "connection": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "title": {"type": "string"},
        "ip": {"type": "string", "format":"ipv4"},
        "port": { "type": "integer", "minimum": 1, "maximum": 65535}
      },
      "required": ["title", "ip", "port"]          
    }
  },
  "type": "object",
  "properties": {
    "test": {"$ref": "#/$defs/connection"},
    "production": {"$ref": "#/$defs/connection"}
  }
}
```

```python 
>>> from comfyconf import make_config, validate_config   
>>> config = make_config("foo.yaml", reader="ruamel")
>>> validate_config(config, "schema.json", validator='json')

```
Currently, json-schema (`validator='json'`) is the default but yamale schema can also be used (`validator='yamale'`)  if yamale is installed.

## Contribute

If you find a bug or have a feature request, please raise on issue on [Github](https://github.com/edager/comfyconf/issues). 

Contributions are more than welcome, but please:

 1. Write unittest (pytest) 
 2. Write Numpy styled docstrings     
