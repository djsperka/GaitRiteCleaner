library(readr)
library(stringr)
library(fs)

# find first element in list l that has nonzero length 
findfirstnonzerolength <- function(l) {
  i <- 0
  for (i in 1:length(l)) {
    if (str_length(l[[i]]) > 0)
      break;
  }
  if (i == length(l)) 
    i <- 0
  i
}

# expecting a  line from a csv file. Truncate to the given number of elements.
trunc_or_pad_csvline <- function(line, ntokens) {
  l <- str_split(line, ",")
  if (length(l[[1]]) < ntokens) {
    # pad input line with commas
    output <- paste(line, strrep(",", ntokens-length(l[[1]])), sep="")
  } else {
    output <- paste(head(l[[1]],ntokens), collapse=",")  
  }
  output
}


alignGR <- function(fulldumpfile) {
  
  # make sure file exists
  if (!file_exists(fulldumpfile))
  {
    stop('file not found')
  }
  
  # form output filename by removing extension, appending "-aligned.csv"
  # outfile <- paste(file_path_sans_ext(fulldumpfile), "-aligned.csv", sep="")
  
  # open input 
  con <- file(fulldumpfile, "r")

  # the aligned data will be written to this character vector, line by line
  outlines <- character(0)
  
  # read a line at a time from input file
  # two empty lines (just commas) are taken to be the end of the data
  bDone <- FALSE
  bLastWasZero <- FALSE
  linenumber <- 0
  while(!bDone) {
    line <- readLines(con, 1)
    linenumber <- linenumber + 1
    if(length(line) == 0) break
    l <- str_split(line, ",")
    f <- findfirstnonzerolength(l[[1]])
    if (f == 0) {
      if (bLastWasZero)
        bDone <- TRUE
      else {
        bLastWasZero <- TRUE
        next
      }
    }
    else {
      bLastWasZero <- FALSE
      if (f == 186) {
        line <- substring(line, 44)   # peel off the extra commas
      } else if (f == 229) {
        line <- substring(line, 87)
      } else if (f == 272) {
        line <- substring(line, 130)
      } else if (f %in% c(1, 7, 143)) {
        # let it pass
      } else {
        stop(paste("UNKNOWN line ", linenumber, " first nonzero ", f))
        bDone <- TRUE
      }
    }
    
    if (!bDone) {
      outlines <- c(outlines, line)
    }
  }
  close(con)
  
  # truncate all lines at 228 elements
  outlines_truncated <- unlist(lapply(outlines, trunc_or_pad_csvline, ntokens=228))

  df <- read_csv(outlines_truncated)
}

reduceGR <- function(df) {
  dfr <- tibble(df[1], df[5], df[6], df[49], df[12], df[14], df[15], df[16], df[17], df[18], df[29], df[30], df[162], df[165], df[167], df[171], df[175], df[164])
}

dezeroGR <- function(df, cols) {
  df2 <- df
  for (c in cols) {
    df2[c] <- na_if(df[[c]], 0)
  }
  df2
}
