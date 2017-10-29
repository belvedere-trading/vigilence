# Vigilence

Vigilence is a simple command-line tool meant to ensure code quality metrics are met within codebases.

## Quickstart

Vigilence can be installed with `pip`.

```bash
pip install vigilence --user
```

The tool has only a few options:

```bash
vigilence --help
Usage: vigilence [OPTIONS] QUALITY_REPORT

Options:
  --type [cobertura|doxygen]
  --config FILENAME
  --help                      Show this message and exit.
```

For example, you could run vigilence on its own code coverage report by calling

```bash
pip install .
python setup.py coverage
vigilence coverage.xml --type cobertura
```

from the root of the source directory. If the quality enforcement succeeds, Vigilence will exit with a return code of 0; any other return code indicates a problem. A negative return code means that the tool failed while a positive code means that the quality metrics of the code base do not meet the configured constraints.

The two required arguments are the path to the quality report and the type of the quality suite that should be applied to that report. The quality report is a single file generated by running some code quality tool (test coverage, linter, documentation generator, etc.). The type allows vigilence to read its dynamic configuration file within the context of the code quality tool that was used to generate the report.

For example, the configuration for a Cobertura coverage report could look like:

```yaml
constraints:
  -
    type: global
    line: 80
    branch: 80
  -
    type: ignore
    paths:
      - vigilence/suite.py
  -
    type: file
    path: vigilence/constraint.py
    branch: 50
  -
    type: package
    name: vigilence
    branch: 75
```

This is actually the configuration file for the code coverage report of Vigilence itself. In this configuration file, each stanza contains the type of constraint that should be applied to the coverage report in addition to the metrics that should be set on each constraint. For more detail about Vigilence configuration, please see the configuration section below.

## Concepts in detail

### Quality items

### Constraints

### Configuration

## Plugins

Coming soon.

### API documentation

Coming soon.
