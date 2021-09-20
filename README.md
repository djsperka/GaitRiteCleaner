# GaitRiteCleaner

Small set of utilities for processing data from the GaitRite system. 

Processing steps taken from documentation provided by Rivera lab. 

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

## Steps in the pipeline

I've attempted to duplicate steps outlined in the documents provided. Here is a brief explanation of each step.


### reduceGR

This method pulls a subset of columns (with all their data) from a data.frame. 

```
reduced <- reduceGR(df, column_names)
```

### dezeroGR

This method removes zeros (a specific step mentioned in the documents provided) from the columns of interest (the columns in the input list), and replaces them with "NA", not-a-number. 

Input is a reduced data.frame (output from *reduceGR*) and a vector of column names (the columns to work on). 

```
dezero <- dezeroGR(reduced, column_names_to_work_on)
```

### do2sdGR

This method removes outliers from each column of interest. i believe I have followed the instructions, these are the steps:

1. find mean and standard deviation
2. remove outliers (greater than 2 standard deviations from mean)

The instructions seem to indicate that the removed values be retained. I've chosen to add two columns for each value being processed. For example, after processing 
the *Step Length* column, there are two additional columns named *Step Length(>2sd)* and *Step Length(<=2sd)*. 

I've not made this method work with a list of input columns, so instead it works on just a single column at a time. Since we process 6 columns in this way, you 
must run this method 6 times, and you end up with 12 additional columns. 





