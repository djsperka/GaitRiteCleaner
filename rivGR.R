library(readr)
library(stringr)
library(fs)
library(dplyr)

# columnsReduced
#
# This is a list of columns found in the raw 'single subject full' export
# files. Each column must exist, and spelling counts!
# 
# This list is used to reduce the dataset to just these columns for subsequent 
# processing (see processGR) 

columnsReduced <- c(
  "Pt Record #",        
  "Leg Length Left",  
  "Leg Length Right",  
  "Comments",
  "Velocity",
  "Cadence",
  "Step Time(sec) L",
  "Step Length(cm) L",
  "Step Time(sec) R",
  "Step Length(cm) R", 
  "Swing Time(sec) L", 
  "Swing Time(sec) R",
  "Step Length",
  "Step Time",
  "Swing Time",
  "Stride Velocity",
  "Step Width",
  "Base of Support"  
)

# columnsToProcess
# 
# This is a list of columns that should undergo the analysis steps
# outlined in the 'Excel' analysis. Each column named here will have
# zeros removed, then mean&sd computed, and outliers removed. 
# See processGR.

columnsToProcess <- c(
  "Step Length",
  "Step Time",
  "Swing Time",
  "Stride Velocity",
  "Step Width",
  "Base of Support"  
)

# processGR
#
# This is the simple pipeline for processing the GaitRite data. 
# 
# Input: csvfile - filename of full export single subject GaitRite data file
#
# Returns: processed data.frame

processGR <- function(csvfile) {
  df <- read_csv(csvfile)
  dfr <- reduceGR(df, columnsReduced)
  df2 <- dezeroGR(dfr, columnsToProcess)
  df3 <- do2sdGR(df2, columnsToProcess)
}

# reduceGR
#
# Return a subset of the the input data.frame, consisting of columns
# in an input list.
#
# Input:
# df - input data.frame
# reduced_column_names - column names from df that are kept. 
#
# Returns: a data.frame, with the reduced set of columns

reduceGR <- function(df, reduced_column_names) {
  dfr <- df[reduced_column_names]
}

# dezeroGR
#
# Replace zeros in a list of columns with NA (not a number)
#
# Input:
# df - data.frame
# cols - list of column names. Each column (assumed to exist)
#        has any zeros replaced with NaN
#
# Returns: a data.frame

dezeroGR <- function(df, cols) {
  df2 <- df
  for (c in cols) {
    df2[c] <- na_if(df[[c]], 0)
  }
  df2
}

# do2sdGR
#
# Compute mean and sd for a list of columns. In each, remove outliers
# (any value more than 2sd from mean). Create two new columns for each - 
# one with the retained values, and the other with any values removed. 
# The original column is not changed. 
# 
# Input:
# df - data.frame
# column_names - names of columns to work on
#
# Returns: data.frame

do2sdGR <- function(df, column_names) {
  
  for (column_name in column_names) {
    # column index of 'column_name'
    column_index <- which(names(df)==column_name)
  
    # Assuming that the column was found....
    # Get mean, sd, then compute z scores
    m <- sapply(df[column_index], mean, na.rm=TRUE)
    s <- sapply(df[column_index], sd, na.rm=TRUE)
    z <- sapply(df[column_index], function(x)(abs((x-m)/s)))
    
      # make two copies of column with name 'column_name'
    # YYY will be values with >2sd removed
    # ZZZ will be the >2sd values that were removed from YYY
    # after all done will rename columns
    df$YYY <- df[column_index]
    df$YYY[z<=2.0] <- NA
    colnames(df)[which(names(df)=="YYY")] <- paste(column_name, "(<=2sd)", sep="")
    
    df$ZZZ <- df[column_index]
    df$ZZZ[z>2.0] <- NA
    colnames(df)[which(names(df)=="ZZZ")] <- paste(column_name, "(>2sd)", sep="")
  }  
  df
}
