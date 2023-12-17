# PyAnalyzer

PyAnalyzer is a tool for extraction of code entity dependencies or relationships from source code. 

## Features
PyAnalyzer can resolve symbol-level dependencies for Python code via enhanced points-to relation propagation and the use of type annotation features. The method tackles the four challenges attributed to object changes, first-class citizens, varying call sites, and libraries.

## Supported Language
|Language|Supported Version|
|-|-|
|Python|3.x|

## Getting Started
> PyAnalyzer has been tested to be worked with python3.x.

## Building

Use Pyinstaller to build PyAnalyzer into executable binary:

```shell
pyinstaller -F .\pyanalyzer\__main__.py
```

Or use the following command to build PyAnalyzer into executable binary

```shell
pyinstaller PyAnalyzer.spec 
```


## Usage
Use `-h` or `--help` option to check usable options.
```shell
usage: PyAnalyzer.exe [-h] [--profile] [--cfg] [--compatible] [--builtins BUILTINS] [--cg] [root path]

positional arguments:
  root path            root package path

options:
  -h, --help           show this help message and exit
  --profile            output consumed time in json format
  --cfg                turn on the analysis to handle Python advanced features
  --compatible         output compatible format
  --builtins BUILTINS  builtins module path
  --cg                 dump call graph into json files

```

- You can use PyAnalyzer to analyze a python package:
```
PyAnalyzer.exe <dir>
```

- Analyzing a single python module:
```
PyAnalyzer.exe <py-file>
```

- Use the improved points-to analysis to resolve non-deterministic dependencies.
```shell
PyAnalyzer.exe <dir> --cfg
```

- Output call graph 
```shell
PyAnalyzer.exe <dir> --cfg --cg
```
