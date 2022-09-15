# AddPDFBookmarks
Add bookmarks to the given PDF file in batch.

# Update

## September 15th, 2022
In the function `read_bookmarks_from_file()`, we handled the `UnicodeDecodeError`. We add the function `identify_encoding()` which can identify possible encoding of the given file by package `chardet`.