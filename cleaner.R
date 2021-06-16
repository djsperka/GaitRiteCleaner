
library(readr)

# load data ###
gr_raw <- read_csv("/Users/dan/rivera/gr-raw-full-test-1.csv")
#View(gr_raw)

# look for patient headers ###

for (row in 1:nrow(gr_raw)) {
  recnum <- gr_raw[row, 8];
  if(!is.na(recnum)) {
    print(paste("recnum ", recnum)); 
  }
  # testtime <- gr_raw[row, 9];
  # if (!is.na(testtime)) {
  #   print(paste("Trial header at row ", row, " testtime ", testtime));
  # }
  # 
  # timestamp <- gr_raw[row, 147];
  # if (!is.na(timestamp)) {
  #   print(paste("Trial data start at row ", row));
  # }
}

#print(names(gr_raw))
#print(gr_raw$`Pt Record #`)