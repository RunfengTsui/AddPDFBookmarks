from pikepdf import OutlineItem, Array, Page
import chardet
from typing import List, Tuple


def get_outlineitem_number(page: OutlineItem) -> int:
    """ Get the page number of OutlineItem.

    Returns: 
        the page number.

    Reference:
        This function is obtained arcording to the `__str__` function of Class OutlineItem 
        in `outlines.py` file. Its' link is
        https://github.com/pikepdf/pikepdf/blob/f97983fa6027fe01166a00f2c9521c5473db5b19/src/pikepdf/models/outlines.py#L182
    """
    if isinstance(page.destination, Array):
        return Page(page.destination[0]).label
    elif isinstance(page.destination, int):
        return page.destination

def identify_encoding(file_path: str) -> str:
    """ Identify the encoding of the given file by chardet package.

    Args:
        file_path: path of the given file to be identified.

    Returns:
        encoding: possible encoding of the given file.
    """
    with open(file_path, mode='rb') as f:
        result_dict = chardet.detect(f.read())
        return result_dict['encoding']

def read_bookmarks_from_file(filepath: str) -> List[Tuple]:
    """ Read bookmarks from the given file.

    Args:
        filepath: path of the given file containing bookmarks.

    Returns:
        bookmarks: The bookmarks list of the PDF file. Every item in the list is a triple 
            with format `(structure, title, page)`. The `structure` represents the structure
            hierarchy of bookmarks. It has three values, one, two and three, representing
            the first layer of bookmarks, the second layer of bookmarks and the third layer
            of bookmarks.
    """
    bookmarks = list()
    # identify the encoding of bookmarks file
    encode = identify_encoding(filepath)
    # open bookmarks file with possible encoding
    try:
        with open(filepath, 'r', encoding=encode) as file:
            for line in file:
                line = line.rstrip()
                if not line:
                    continue
                try:    # use '@' as a separator for bookmarks and page numbers
                    title = line.split('@')[0].rstrip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print(msg)
                    continue
                if title and page:  # add bookmark if title and page are not empty
                    try:
                        page = int(page)# + page_offset
                        # Get the structure hierarchy of bookmarks by counting tab keys
                        structure = title.count('#')
                        title = title.replace('#', '').lstrip()
                        bookmarks.append((structure, title, page))
                    except ValueError as msg:
                        print(msg)
    except UnicodeDecodeError as msg:
        print(msg)

    return bookmarks

