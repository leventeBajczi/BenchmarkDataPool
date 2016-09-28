library(janeaustenr)
library(dplyr)

source("R/helper_functions.R")

books <- austen_books()
## Data cleaning
book_titles <- c("Sense & Sensibility", "Pride & Prejudice")

lapply(book_titles, function(title){
  books[books$book == title, ] %>%
    cleansTheBook() %>%
    writesTheBook()
  T
})
