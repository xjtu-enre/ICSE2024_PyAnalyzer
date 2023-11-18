## Introduction to type analysis and type annotation using type4py

### 1. Analysing types using type4py

​		(1) First of all, type4py will be deployed to the server through docker, the specific deployment method refer to the [Type4Py's Local Model](https://github.com/saltudelft/type4py/wiki/Type4Py's-Local-Model),Tested via [Using Type4Py Rest API](https://github.com/saltudelft/type4py/wiki/Using-Type4Py-Rest-API) after successful deployment

​		(2) The code in the project will be analysed sequentially by type4py, and the output json results will be saved according to the structure of the project

### 2. Generate source code with type annotations

​		The process of type annotation for source code is to first read the python source code, convert the source code to ast object, generate the corresponding ast syntax tree, then edit the type type in the json to the ast object, and finally convert the ast object to the python source code, the specific implementation process is as follows.

​		(1) Read the json data in the first step respectively

​		(2) Read the source code of the project through the path of the json data (the storage structure of the json data is exactly the same as the storage structure of the project code).

​		(3) Converting project source code to ast objects

​		(4) Extract the parameter type and return value type of the function in the json and edit it into the ast object

​		(5) Converting ast objects to source code with type annotations





