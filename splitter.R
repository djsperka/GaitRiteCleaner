library(tidyverse)

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

con <- file("data/test2.csv", "r")
out <- file("data/test2-reduced.csv", "w")
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
      print(paste("UNKNOWN line ", linenumber, " first nonzero ", f))
      print(line)
      bDone <- TRUE
    }
  }
    
  if (!bDone) {
    writeLines(line, out)
    print(paste("Wrote line f ", f))
  }
  # l is a list. 
  # First element of l ( l[[1]] ) is a list of char strings
  # Find first element of that list with nonzero length
  # print(paste(findfirstnonzerolength(l[[1]]), "/",length(l[[1]])))
}
close(con)
close(out)
