
cleansTheBook <- function(book) {
  book <- book[-c(1:12), ]
  book <- book[!grepl(pattern = "CHAPTER", book$text, fixed = T), ]
  book <- book[!grepl(pattern = "THE END", book$text, fixed = T), ]
  book <- book[book$text != "", ] 
  book
}

writesTheBook <- function(book) {
  
  length <- length(book$book)
  print(length)
  
  for(i in 1:6) {
    currentLength <- round(length / 2 ^ (6 - i))
    print(currentLength)
    characters <- paste0(unlist(book[seq(from = 1, to = currentLength), "text"]), collapse = "")
    ## closing the sentence if it is not closed
    if (substring(characters, first = nchar(characters), last = nchar(characters)) != ".") {
      characters <- paste0(characters, ".")
    }
    ##print(substring(characters, first = nchar(characters) - 5, last = nchar(characters)))
    write(characters, file = paste0("texts/", substring(unique(book$book), first = 1, last = 5),
                                    i, ".txt"))
    ##characters
  }
}