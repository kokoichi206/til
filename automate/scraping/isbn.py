import isbnlib
import sys

isbn = isbnlib.isbn_from_words(sys.argv[1])
book = isbnlib.meta(isbn)
title = book['Title']
authors = book['Authors']
print("{isbn}-{title}-{author}".format(isbn=isbn, title=title, author=authors))
