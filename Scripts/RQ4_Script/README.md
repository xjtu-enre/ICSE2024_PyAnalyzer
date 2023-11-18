# Automated Efficiency Test

## Before start

You need:

- A computer with `Windows 10/11` as operating system

- `Java` latest installed (>= 15) and can be accessed via the environment path
  
  > Some tools depends on JRE to run.
  
- `SciTools Understand` installed and can be accessed via the environment path
  
- `Sourcetrail` installed and can be accessed via the environment path
  
  > **WARNING** SourceTrail depends on Python **^3.8** to analyze python projects, if you don'y explicitly assign a python executable path while creating a project, then you would better make sure a Python 3.8 is accessable via the environment.
  
- Allow git to use long file name:

  ```sh
  $ git config --system core.longpaths true
  ```

- Python package `psutil` installed
  > This is used for memory usage profiling

## Run test, with only one command

```sh
$ python EfficiencyTest.py <lang> <range> [only] [-t --timeout <range(300, 3600)>]
```

where,

* `lang` can be the  `python` 
* `range` can be one of
  * a number `n`, refers to n-th project in the list
  * a range `a-b`, refers to projects from  a-th to b-th

> * Usually you don't need to set this, `only` can be one of
>   * `pyanalyzer: Runs `PyAnalyzer` only
>   * `depends`: Runs `Depends` only
>   * `understand`: Runs `Understand` only
>   * `sourcetrail`: Runs `SourceTrail` only
>   * `pycg`: Runs `PyCG` only
>   * `pysonar2`: Runs `Pysonar2` only
>   * `enre19`: Runs `enre19` only
>   * `clone`: Just clone the repositories
>   * `loc`: Just count the LoC

* `-t --timeout` limits the maximum duration a process can take, this feature is activated only when a valid number is given.

We highly encourage you to run this script under `Windows Terminal` + `PowerShell`, this conbination suits the modern world on Windows platform.

## Submit results

We want all newly generated files under these directories:

* `logs/`
* `records/`

## Attention

- You should create a Sourcetrail project file first to make sure sourcetrail run normally.
- You should place these executable programs under the folder `records/`
- You should place the `python_project_list.csv` under the folder `lists/`
