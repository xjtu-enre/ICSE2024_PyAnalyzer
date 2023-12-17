# 2024ICSE-PyAnalyzer
This repository illustrates the tool, data, and scripts of our ICSE2024 under-reviewing work ——`PyAnalyzer: An Effective and Practical Approach for Dependency Extraction from Python Code`. 

We make our tool's source code, datasets and all experimental results publicly available. Due to the file size limit of GitHub, we upload the processed data to this repository. Please connect us for the large-scale raw data if required.

This document introduces:

1. **Appendix.md**. This file provides  supplementary information and explanations regarding the **Study Setup**.

2. **The structure of entire repository**. This repository includes all experimental scripts, dataset, and the experiment results corresponding to each research question (RQ) mentioned in the paper.

## Directory Structure

The whole directory goes like the following:
```
├─README.md 
├─Appendix.md
├─Scripts
├─SourceCode
├─Data
│  ├─RQ1 
│  │  ├─micro-benchmark A
|  |  |  ├─entity
|  |  |  ├─relation
|  |  |  └─Readme
│  │  └─results      
│  │     ├─tests
│  │     ├─Depends
│  │     ├─Enre19
│  │     ├─PyAnalyzer
│  │     ├─PySonar2
│  │     ├─Sourcetrail
│  │     └─Understand 
│  ├─RQ2
│  │  ├─micro-benchmark B
│  │  │  ├─Benchmark-collectedbyPyCG
│  │  │  └─Benchmark-newlyaddedbyPyAnalyzer  
│  │  └─results
│  │     ├─PyAnalyzer
│  │     ├─PyCG
│  │     └─Type4py
│  ├─RQ3
│  │  ├─macro-benchmark C
│  │  │  ├─ground-truth-cgs
│  │  │  └─projects
|  |  ├─macro-benchmark D
│  │  │  └─rq3_project_list.xlsx
│  │  └─results
│  │     └─rq3_projects_results.xlsx
│  └─RQ4
│     ├─list
│     │  └─python_project_list.csv
│     └─results
│        ├─project_results_list.csv
│        ├─less.png
│        └─more.png
|
└─Tools                 

```

## Scripts

We use the following scripts in our experiment. Each RQn_Script directory (where n takes values from 1 to 4) in this folder contains the scripts and documentation used for Research Question RQn. 

### RQ1_Script

This directory contains six subdirectories, each of which includes the script files we used for comparison with the baseline tools in our experiments.

### RQ2_Script

This folder contains four script files used for RQ2.

- `S1_trace.py` - in the Type4Py execution environment, the script will automatically invoke Type4Py to analyze the project and obtain the analysis results from Type4Py.
- `S2_code_retrofitted_type.py` - the script utilizes the results obtained from Type4Py analysis to refactor the analyzed source code.
- `S3_call_dependency.py` - generate function call graphs and compare the results of Type4Py with those of PyAnalyzer.
- `pycg_Script.py` - invoke PyCG for analysis and compare the analysis results with PyAnalyzer.

### RQ3_Script

This folder contains five script files used for RQ3.

- `batch_prcocess.py` - is the format conversion scripts of all tools, including Understand and PyCG (provided that data from each tool is available):
- `analysis.py` -is a script that calculates the accuracy of various tools in covering the ground truth within a single project.
- `run_analysis.py` - calculates the accuracy for all projects and moves the generated CSV files into a designated folder within the "result" directory.
- `pycg.py` - is a script that converts the results from PyCG tool into a standardized format.
- `Understand.py` - is a script that converts the results from Understand tool into a standardized format.

### RQ4_Script

This file is the script used for RQ4. 

#### Before start

You need:

- A computer with `Windows 10/11` as operating system
- `Java` latest installed (>= 15) and can be accessed via the environment path
- `Python`  >= 3.8 (through environment path)

- Allow git to use long file name:

  ```sh
  $ git config --system core.longpaths true
  ```

- `SciTools Understand` installed and can be accessed via the environment path

- `Sourcetrail` installed and can be accessed via the environment path

- Python package `psutil` installed

  > This is used for memory usage profiling

#### Run test, with only one command

```sh
$ python EfficiencyTest.py <lang> <range> [only] [-t --timeout <range(300, 3600)>]
```

* `lang` can be the  `python` 
* `range` can be one of
  * a number `n`, refers to n-th project in the list
  * a range `a-b`, refers to projects from  a-th to b-th
* `only` can be one of the tools (*i.e., pyanalyzer, depends, enre19,  pysonar2, sourcetrail and understand*) to run the tool only. If you set "only" as clone, it just clones the repositories. You can also set "only" as loc to count the loc.

* `-t --timeout` limits the maximum duration a process can take, this feature is activated only when a valid number is given.

We highly encourage you to run this script under `Windows Terminal` + `PowerShell`, this conbination suits the modern world on Windows platform.

#### Submit results

We want all newly generated files under these directories:

* `logs/`
* `records/`

#### Attention

- You should create a Sourcetrail project file first to make sure sourcetrail run normally.
- You should place these executable programs under the folder `records/`
- You should place the `python_project_list.csv` under the folder `lists/

## SourceCode

This directory contains our tool's source code.

## Data

This directory contains all the original data and final results of our four RQs.

### RQ1: What is the accuracy of PyAnalyzer to identify deterministic dependencies?
This folder contains two parts: the micro-benchmark A used in RQ1 study and the output results of each static code dependency analyzers (*i.e., Depends, ENRE19, PyAnalyzer, PySonar2, SourceTrail and Understand*) we selected.

#### micro-benchmark A

##### entity

This folder contains 9 markdown files which record  9 kinds of entities. (*i.e., Package, Module, Variable, Function, Parameter, Class, Attribute, Alias and AnonymousFunction*) Taking the class.md file as an example:

- Each file consists of a set of executable Python code snippets along with entities that are expected to be extracted from the corresponding code.

  ```python
  //// test_global_class.py
  class Base:
      ...
  ```

  ```yaml
  name: GlobalClassDefinition
  entity:
    type: Class
    extra: false
    items:
    - type: Class
      qualified: test_global_class.Base
      name: Base
      loc: '1:6'
  ```

- Groundtruth entities are recorded in text format.
- Each entity is labeled with several properties (*i.e., name, type that depicts the entity kind, location where the entity is declared in the source code, etc.*)
##### relation
This folder contains 9 markdown files which record  9 kinds of dependencies. (*i.e., Define, Use, Set, Import, call, Inherit, Contain, Annotate, Alias*) Taking the call.md file as an example:

- Each file consists of a set of executable Python code snippets along with dependencies that are expected to be extracted from the corresponding code.

  ```python
  //// test_global_function_call.py
  
  def func1():
  
  
      func1()
  
  
      return 0
  
  func1()
  ```

  ```yaml
  name: GlobalFunctionCall
  relation:
    items:
    - type: Call
      to: Function:'test_global_function_call.func1'
      loc: '5:4'
      from: Function:'test_global_function_call.func1'
    - type: Call
      to: Function:'test_global_function_call.func1'
      loc: '10:0'
      from: Module:'test_global_function_call'
  ```

- Groundtruth dependencies are recorded in text format.
	
- Each dependency is labeled with src denoting the depended entity, dest denoting the dependent entity, type denoting the dependency kind, and location denoting the dependency site where the reference relation happens.

#### results

This directory contains the data of collection results of micro-benchmark A and the results of each static code dependency analyzers on tests  for RQ1 study. Following diagrams shows the detail of each folder.

- **tests** contains the collection results of micro-benchmark A. In total, the benchmark consists of **62** entity items and **160 dependency items, which corresponds to **45** tests in total.
- **Depends** contains the results of Depends on tests.
- **PyAnalyzer** contains the results of Pyanalyzer on tests.
- **PySonar2** contains the results of PySonar2 on tests.
- **Sourcetrail** contains the results of Sourcetrai on tests.
- **Understand** contains the results of Understand on tests.
- **ENRE19** contains the results of ENRE19 on tests.

### RQ2: What is the accuracy of PyAnalyzer to identify nondeterministic dependencies?

This folder contains two parts: the micro-benchmark B used in RQ2 study and the output results of each static code dependency analyzers (*i.e., PyCG, PyAnalyzer and Type4py*) we selected.

#### micro-benchmark B

This folder contains two parts: the benchmark collected by the work of PyCG  and the benchmark newly added by our PyAnalyzer. The benchmark covers **17** categories and **233** tests.

##### Benchmark-collectedbyPyCG

This folder contains the original benchmark collected by the work of PyCG. The original benchmark consists of **206** unique tests, each including source code, the corresponding call dependencies, and a short description. The root directory of each folder in this folder contains three files. Taking the files under the directory '\args\assigned_cal' as examples:

- `main.py` - the source code to be analyzed.
- `callgraph.json` - the corresponding call dependencies of the source code.

- `README.md` - a short description of the source code.

##### Benchmark-newlyaddedbyPyAnalyzer

This folder contains the benchmark (**27** tests in total) supplemented by our work, each including source code, the corresponding call dependencie. The root directory of each folder in this folder contains two files. Taking the files under the directory '\lists\list_param' as examples:

- `main.py` - the source code to be analyzed.
- `callgraph.json` - the corresponding call dependencies of the source code.
- `README.md` - a short description of the source code.

#### results

This directory contains the results of each static code dependency analyzers (*i.e., PyCG, PyAnalyzer and Type4py*) we selected on the **233** tests of micro-benchmark B.

##### PyAnalyzer

This folder contains the results of our PyAnalyzer on the benchmark collected by the work of PyCG  and the benchmark newly added by our PyAnalyzer. The root directory of each folder in this folder contains two files. Taking the files under the directory '\Benchmark-collectedbyPyCG\args\assigned_call' as examples:

- `assigned_call-call-graph-PyAnalyzer.json` - the function call relationship output of Pyanalyzer.
- `assigned_call-report-PyAnalyzer.json` - the the explicit dependency output of PyAnalyzer.

##### PyCG

This folder contains the results of PyCG on the benchmark collected by the work of PyCG  and the benchmark newly added by our PyAnalyzer. The root directory of each folder in this folder contains one file. Taking the files under the directory '\Benchmark-collectedbyPyCG\args\assigned_call' as examples:

- `pycg-callgraph.json` - the function call relationship output of PyCG.

##### Type4py

This folder contains the results of Type4py on the benchmark collected by the work of Type4py  and the benchmark newly added by our PyAnalyzer. The root directory of each folder in this folder contains one files. Taking the files under the directory '\Benchmark-collectedbyPyCG\args\assigned_call' as examples:

- `main.json` - the intermediate results used during the analysis
- `main.py` - the source code with added variable types by Type4Py.

**`readme.md`** the document introduces how to convert the results of Type4py into dependent results.

### RQ3: What is the general accuracy of PyAnalyzer to analyze real-world projects? 

This directory contains three parts: the macro-benchmark C and macro-benchmark D used in RQ3 and the results.

#### macro-benchmark C

This directory contains the manual curated macro-benchmark provided by the work of PyCG, containing function-level dependencies from 5 real-world project.

##### projects

This directory contains the 5 projects' source code which are used in PyCG's work. All the five projects are medium sized projects (less than 3.5k LoC). 

##### ground-truth-cgs

This directory contains the manual curated ground-truth provided by the work of PyCG. The first author of PyCG's paper manually inspected the 5 projects and generated their call graphs in JSON format, spending on average 10 hours for each project.

#### macro-benchmark D

This directory contains a list (`rq3_macro-benchmarkD_project_list.xlsx`) of open source projects. 

We finally collected 8,233 ground-truth dependency items at function levels from execution traces of 54 projects. Each column in this file is *the project name, commit_id, loc, testfile number and ground-truth dependency number of every project*. 

In the experiment, all project files are stored on the local computer. Due to GitHub's file size upload limitations, we are unable to upload all project source files. Please connect us for the large-scale raw data if required. 

#### results

This directory contains two lists (`rq3_macro-benchmarkC_projects_results.xlsx`  and `rq3_macro-benchmarkD_projects_results.xlsx`) of the results of each static code dependency analyzers (*i.e.,  Understand, PyCG and PyAnalyzer*).

Each column in this file is *the project name, LoC, testfile number, the accurate number and the accuracy of each static code dependency analyzers and ground-truth dependency number of every project*.

### RQ4: What is the time and memory consumption of PyAnalyzer to analyze real-world projects?

This directory contains two parts: a list of open source projects we collected and the time and memory consumption of each static code dependency analyzers (*i.e., Depends, ENRE19, PyAnalyzer, PySonar2, PyCG, SourceTrail and Understand*) we have selected. 

#### list

This directory contains a list (`python_project_list.csv`) of open source projects. We collected the top-starred projects from GitHub to assess multiple tools’ efficiency for RQ4. Concretely, we programmatically access the GitHub search API endpoint for Python projects that are sorted based on star count descending. 

We initially accessed the top 200 projects. We further excluded the projects that are tutorials, awesome lists, algorithm collections, etc. We finally collected 191 projects with 10M SLOC, diverse sizes ranging from 19 to 700K. Each column in this file is *the project name, stars, github url, clone url, commit_id*. The stars' data is up to January 15, 2023. 

In the experiment, all project files are stored on the local computer. Due to GitHub's file size upload limitations, we are unable to upload all project source files. Please connect us for the large-scale raw data if required. 

#### results

This directory contains a list (`project_results_list.csv`) of the time and memory consumption of each static code dependency analyzers (*i.e., Depends, ENRE19, PyAnalyzer, PySonar2, PyCG, SourceTrail and Understand*) and two figures(`less.png` and`more.png`) which show the comparison results of various tools on a subset of projects with code size less than 10k and greater than 10k.

Each column in this file is *the project name, commit_id, loc and the time and memory consumption of each tools*. The unit of time consumption is seconds and the unit of memory consumption is MB. PyCG only successfully analyzed 38.7% projects, reporting ERROR, MEMORY_ERROR and TIMEOUT.

## Tools

This directory contains some executable programs and a documentation(`Readme.md`) for all the tools we used in this experiment.

|   Tools    | Version               | Url                                                          |
| :--------: | --------------------- | ------------------------------------------------------------ |
| Understand | Understand 6.4.1142   | https://licensing.scitools.com/download/thanks/Windows-64bit.exe |
| SoureTrail | SourceTrail 2021.4.19 | https://github.com/CoatiSoftware/Sourcetrail.git             |
|  Depends   | Depends-0.9.7         | https://github.com/multilang-depends/depends.git             |
|  PySonar   | PySonar-2             | https://github.com/yinwang0/pysonar2.git                     |
|   ENRE19   | v2.0                  | https://github.com/jinwuxia/ENRE/tree/v2.0                   |
|  Type4Py   | v0.1.3                | https://github.com/saltudelft/type4py                        |
|    PyCG    | PyCG 0.0.7            | https://github.com/vitsalis/PyCG.git                         |
| PyAnalyzer | /                     | https://github.com/2024icse/PyAnalyzer                       |
