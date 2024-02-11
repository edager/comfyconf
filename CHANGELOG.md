# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.0.2] 2024-02-11

### Added 
  - Github action for publishing on pypi on new tag (triggered on push) 
  - Add the possibility to validate configs using json-schema and yamale
  - Tests for schema validation   

## [0.0.1] 2024-02-03

### Added
  - Reader using pyymal 
  - Reader using ruamel.yaml
  - Dotdict class as the config object
  - make_config function to generate config object from path
  - tests for readers and config objects
  - pyproject.toml for publishing via pypi
  - Github action for testing new commits (triggered on push)  


[Unreleased]: https://github.com/edager/comfyconf/compare/v0.0.1...HEAD
[0.0.2]: https://github.com/edager/comfyconf/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/edager/comfyconf/releases/tag/v0.0.1
