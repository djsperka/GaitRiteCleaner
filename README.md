# GaitRiteCleaner

Python script for processing data exported from the GaitRite system, 
and preparing file(s) that may be imported to RedCap.

## Getting Started

It is assumed that you are running on Windows, though this script will run on other platforms.

1. Install Python for windows. Download [here](https://www.python.org/downloads/). On the first page of the installer, 
check the box labelled "Add Python to Path". 
2. Check that python is in your path. Open a DOS command window. Type "python -V", you should get back the version number:
```batch
C:\work\rivera>python -V
Python 3.10.8
```

> If the installer did *not* add python to your path, you will get output like this:

```batch
C:\work\rivera>python -V
'python' is not recognized as an internal or external command,
operable program or batch file.
```

> To fix this, follow the instructions [here](https://datatofish.com/add-python-to-windows-path/).

3. Install the packages *pandas* and *openpyxl*. Installing these packages will cause several
other packages to be installed as well. 

```batch
C:\work\rivera>python -m pip install pandas openpyxl
```

4. Now download the code. 
4.1 If you have git, you can clone the repository:
```batch
C:\work\rivera> git clone https://github.com/djsperka/GaitRiteCleaner
```
4.2 You can just download [this zip file](https://github.com/djsperka/GaitRiteCleaner/archive/refs/heads/master.zip) 
with the latest version of the code. Unzip to a local folder. 

## How to run the script
To run the script, open a Windows command prompt and navigate to the folder where
you put the source code in step 4 above. 

Run this command to start the dialog:
```batch
c:\work\rivera\GaitRiteCleaner> python grx.python
```

You should see this dialog:

![GaitRiteCleaner dialog](grx-dialog.png)

1. Click *Select* to choose the input folder. This should be a folder containing
GaitRite export files (in either csv or xlsx format). Filenames must 
start with the pattern NNNNNN-NNN. Any characters may follow this pattern
(which should be the FX ID for the subject). There should be NO OTHER FILES in this folder!

2. Enter the event name to be assigned to this data. No spaces - this should be an EXACT event name as defined
in the RedCap project. 

3. Click *Select* to choose the output filename. If the file already exists you will be asked if you want to overwrite the 
file. 

4. Click this button to start the process. You should see output in your command window that looks like this (my example folder had just 4 input files):

```batch
C:\work\reckup\GaitRiteCleaner-master>python grx.py
This script lives in C:\work\reckup\GaitRiteCleaner-master
Expecting these input files:
Column names: C:\work\reckup\GaitRiteCleaner-master\data\column_names.csv
FX/TRAX List: C:\work\reckup\GaitRiteCleaner-master\data\FX_ID_TRAX_ID_List.xlsx

Dirname set to C:/work/rivera/GaitRiteCleaner/data/test

Input file C:/work/rivera/GaitRiteCleaner/data/test event aaasdfasdf


Input file C:/work/rivera/GaitRiteCleaner/data/test\100398-100_05_23_19.xlsx
FXS from filename: 100398-100
FXS not found in lookup table, use 000: 100398-100/000

Input file C:/work/rivera/GaitRiteCleaner/data/test\100427-100_09_28_21.xlsx
FXS from filename: 100427-100
FXS/TRAX ID: 100427-100/476

Input file C:/work/rivera/GaitRiteCleaner/data/test\500011-572_10_06_21.xlsx
FXS from filename: 500011-572
FXS not found in lookup table, use 000: 500011-572/000

Input file C:/work/rivera/GaitRiteCleaner/data/test\500011-573_11_04_21.xlsx
FXS from filename: 500011-573
FXS/TRAX ID: 500011-573/545
Writing 12 records to output file C:/work/rivera/test_out_5.csv
```

