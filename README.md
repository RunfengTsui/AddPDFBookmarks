# AddPDFBookmarks

Add bookmarks to the given PDF file in batch. You can also export bookmarks from the given PDF file.

## Download

You can clone the repository by `git`:

```git
git clone https://github.com/RunfengTsui/AddPDFBookmarks.git
```

You can also download zip file and then unzip it.

## Dependencies

Use [Poetry](https://python-poetry.org) to manage dependencies. Run `poetry install --no-root` command to create virtual environment and install dependencies.

Of course, you can use `pip` install the packages:

```
pip3 install pikepdf, chardet
```

## Example

Create file `main.py` and export the bookmarks from the given file.

```python
from src.pdfhandler import PDFHandler

pdf = PDFHandler("filename.pdf")
pdf.export_bookmarks("bookmarks.txt")
```

Then, you can modify the `bookmarks.txt` file and add it to the PDF file.

```python
from src.pdfhandler import PDFHandler

pdf = PDFHandler("filename.pdf")
pdf.add_bookmarks_from_file("bookmarks.txt", "filename_bookmarks.pdf", page_offset=0)
```

## Update

### File Encoding

In the function `read_bookmarks_from_file()`, we handled the `UnicodeDecodeError`. We add the function `identify_encoding()` which can identify possible encoding of the given file by package `chardet`.

### Export Bookmarks

Now, you can use the method `export_bookmarks()` to export the bookmarks from the given file. At the same time, move the function `read_bookmarks_from_file()` from the class `PDFHandler` to file `src/tools.py`.
