##if you do not have it installed:
## install.packages("validate")

library(validate)

path <- "benchmark_files/"
csv_files <- list.files(path = path, pattern = ".csv", full.names = T)
csv_files <- csv_files[!grepl(pattern = "example", x = csv_files)]

## Validation ##
v <- validator(
  kind %in% c("Start", "End"),
  name %in% c("Tokenize", "Collect", "ComputeScalar", "ComputeCosine"),
  gsub(pattern = "Pride|Sense|[1-6]|\\_", "", id) == ""
)

files_to_merge <- list()

lapply(csv_files, function(file){
  csv <- read.csv(file, stringsAsFactors = F)
  files_to_merge[[file]] <<- csv
  cf <- confront(csv, v)
  print(unique(csv$team))
  print(summary(cf))
  stopifnot(summary(cf)$fails == 0)
  T
})

## Merge the data files together
large_csv <- do.call(rbind, files_to_merge)

save(large_csv, file = "benchmark_files/large_output.RData")

