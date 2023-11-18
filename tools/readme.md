# Tools

The tools, their corresponding versions, and download links used in this experiment are shown in the following table (As of February 15, 2023, all these tools are the latest versions):

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

Attention：

- **Depends：**As the tool "depends" only outputs results at the class level, we made modifications to its source code in the output module and packaged it as an executable program to enable it to export all analysis result information to a JSON file. We have not made any changes to the analysis logic of the tool.