# RQ2_Script

This folder contains four script files used for RQ2.

### Before start

You need:

- A computer with `Windows 10/11` as operating system
- `Python`  >= 3.8 (through environment path)
- Type4py installed.
  - You can follow the steps provided in this link https://github.com/saltudelft/type4py/wiki/Type4Py's-Local-Model for installation.

The functionality of each script is as follows:

- `S1_trace.py` - in the Type4Py execution environment, the script will automatically invoke Type4Py to analyze the project and obtain the analysis results from Type4Py.

- `S2_code_retrofitted_type.py` - the script utilizes the results obtained from Type4Py analysis to refactor the analyzed source code.

- `S3_call_dependency.py` - generate function call graphs and compare the results of Type4Py with those of PyAnalyzer.

- `pycg_Script.py` - invoke PyCG for analysis and compare the analysis results with PyAnalyzer.
