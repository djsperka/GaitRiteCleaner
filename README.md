# GaitRiteCleaner

Small set of utilities for processing data from the GaitRite system. 

Processing steps taken from documentation provided by Rivera lab. 

Processing steps:

```
source 'rivGR.R'
'filename' %>% alignGR %>% reduceGR %>% dezeroGR(c(13,14,15,16,17,18)) %>% do2sdGR('Step Length') %>% do2sdGR('Step Time') %>% do2sdGR('Swing Time') %>% do2sdGR('Stride Velocity') %>% do2sdGR('Step Width') %>% do2sdGR('Base of Support')
```

Same steps, more pedantic and more easily understood:

```
source 'rivGR.R'
df <- alignGR('filename')
df1 <- reduceGR(df)
df2 <- dezeroGR(df1, c(13, 14, 15, 16, 17, 18))

# just rewrite df2 from now on.
df2 <- do2sdGR(df2, 'Step Length')
df2 <- do2sdGR(df2, 'Step Time')
df2 <- do2sdGR(df2, 'Swing Time')
df2 <- do2sdGR(df2, 'Stride Velocity')
df2 <- do2sdGR(df2, 'Step Width')
df2 <- do2sdGR(df2, 'Base of Support')
```

## Steps in the pipeline

I've attempted to duplicate steps outlined in the documents provided. Here is a brief explanation of each step.

### alignGR

This method aligns the columns of the raw csv file obtained from GaitRite. In the sample files provided, some columns were shifted out of alignment. 
After some discussion, we determined that those shifts were errors in the output format, not bad data. This method removes empty rows, shifts columns, and 
truncates empty elements from the end of rows to make all columns line up with their headers, and to make each row the same length. No data is removed in this step!

I've assumed that the input to this step is a full export (all fields) from GaitRite.

```
aligned <- alignGR('/Users/dan/raw_export_from_gaitrite.csv')
```

### reduceGR

This method strips all columns not found in the documents provided. The "example cleaned data" spreadsheet contains a subset 
of the columns in the original (raw) export. This method simply removes all other columns and keeps only those found in "example cleaned data". 

Input is a data.frame that has already been aligned (i.e. output from #alignGR#)

```
reduced <- reduceGR(aligned)
```

### dezeroGR

This method removes zeros (a specific step mentioned in the documents provided) from the columns of interest (there are 6), and replaces them with "NA", not-a-number. 

Input is a reduced data.frame (output from *reduceGR*) and a vector of column indices (the columns to work on). 

```
dezero <- dezeroGR(reduced, c(13, 14, 15, 16, 17, 18))
```

### do2sdGR

This method removes outliers from each column of interest. i believe I have followed the instructions, these are the steps:

1. find mean and standard deviation
2. remove outliers (greater than 2 standard deviations from mean)

The instructions seem to indicate that the removed values be retained. I've chosen to add two columns for each value being processed. For example, after processing 
the *Step Length* column, there are two additional columns named *Step Length(>2sd)* and *Step Length(<=2sd)*. 

I've not made this method work with a list of input columns, so instead it works on just a single column at a time. Since we process 6 columns in this way, you 
must run this method 6 times, and you end up with 12 additional columns. 





