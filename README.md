# GaitRiteCleaner

Small set of utilities for processing data from the GaitRite system. 

Processing steps taken from documentation provided by Rivera lab. 

The 'data' folder in this repo has 4 data files: full-single-1,2,3,4.csv - these are taken
from the excel spreadsheets that Ellery sent on 9/17/2021. To generate these files, I open the 
sheets in Google Sheets, then do File > Download > CSV, current sheet. 

Processing steps:

```
source 'rivGR.R'
df <- processGR('./data/newtest.csv')
```
The result 'df' is a data.frame with the reduced, processed, data set. See below for details on the contents of that data.frame. THIS DATA.FRAME IS NOT YET SAVED TO A FILE! I have assumed that some further processing will be done on this data, so I've not taken the small step of writing the data to a file.

I've removed a bunch of code that was related to re-formatting the input files. Now, the processing consists of a short function, processGR, that runs the two steps in the processing. 

## Lists that control the processing

The source file 'rivGR.R' has two string lists that control its behavior. These can be changed, as long as the column names exist in the data, and they are spelled correctly!

### columnsReduced

This is a list of columns that are taken from the raw input file and kept in 
subsequent processing. Each column name must be spelled exactly right! 

### columnsToProcess

These columns are processed according to the 'Excel' analysis instructions (zeros removed, outlier removal). Like the first column, the column names must be spelled exactly right!

## Notes about the processing steps. 

I've attempted to duplicate steps outlined in the documents provided. In earlier versions of this repo I wrote out all the processing steps as a pipeline. In the current version, however, the pipeline is replaced with a single method, *processGR*. The entire analysis is performed in that function -- there are no other steps (other than saving the result to a file, and any other subsequent processing you may do). 


### do2sdGR

This method, which is called from *processGR*, removes outliers from each column of interest. The input columns are named in the array *columnsToProcess*. i believe I have followed the instructions, these are the steps:

1. find mean and standard deviation
2. remove outliers (greater than 2 standard deviations from mean)

The instructions seem to indicate that the removed values be retained. I've chosen to add two columns for each value being processed. For example, after processing 
the *Step Length* column, there are two additional columns named *Step Length(>2sd)* and *Step Length(<=2sd)*. 







