from pikepdf import Pdf, OutlineItem
from .tools import get_outlineitem_number, read_bookmarks_from_file
from typing import List, Tuple


class PDFHandler(object):
    """ Class of PDF file handler.
    """
    def __init__(self, filepath: str) -> None:
        """ Initialize a PDF file object.

        Args:
            pdf_file_path: the path of the PDF file to be handled.
        """
        # open the PDF file
        self.__pdf = Pdf.open(filepath)
        # Get the totle number of pages
        self.pages_num = len(self.__pdf.pages)

        # create a writable PDF file
        self.__writable = Pdf.new()
        self.__writable.pages.extend(self.__pdf.pages)

    def export_bookmarks(self, filepath: str = "bookmarks.txt") -> None:
        """ Export PDF's bookmarks to file.
        This function is only applicable to cases where there are no more than three levels
        of bookmarks.

        Args:
            filepath: the file to save bookmarks.
        """
        with open(filepath, "w") as f:
            with self.__pdf.open_outline() as outline:
                for item in outline.root:
                    f.write(f"# {item.title} @ {get_outlineitem_number(item)}\n")
                    if item.children != None:
                        for item2 in item.children:
                            f.write(f"## {item2.title} @ {get_outlineitem_number(item2)}\n")
                            if item2.children != None:
                                for item3 in item2.children:
                                    f.write(f"### {item3.title} @ {get_outlineitem_number(item3)}\n")
                    f.write("\n")

    def _add_bookmarks(self, bookmarks: List[Tuple], page_offset:int = 0) -> None:
        """ Add bookmarks for the given PDF file.

        Args:
            bookmarks: A list of triples tuple with format `(structure, title, page)`, where
                `structure` represents the structure hierarchy of bookmarks.
                For example, [(1, title1, 0), (2, title2, 3), (3, title3, 7), (2, title4, 10), (1, title5, 15), ...].
                `(2, title2, 3)` is the children of `(1, title1, 0)` and the father of `(3, title3, 7)`.
            page_offset: Due to the existence of pages such as the cover page and the table
                of contents, the actual page number in the PDF is more than the page number
                written in the table of contents.
        """
        with self.__writable.open_outline() as outline:
            for structure, title, page in bookmarks:
                if page+page_offset > self.pages_num:
                    raise("There is no destination of the OutlineItem!")
                else:
                    oi = OutlineItem(title, page+page_offset-1)
                if structure == 1:
                    outline.root.append(oi)
                elif structure == 2:
                    outline.root[-1].children.append(oi)
                elif structure == 3:
                    outline.root[-1].children[-1].children.append(oi)
                else:
                    print('The bookmarks structure is Out Of Range!')
                    continue

    def add_bookmarks_from_file(self, bookmarks_path: str, savepath:str, page_offset:int = 0) -> None:
        """ Add bookmarks for the PDF file from the given file.

        Args:
            bookmarks_path: path of the given file containing bookmarks.
            page_offset: int, default value is 0.
            savepath: file path to save.
        """
        # Get the bookmarks from the given file.
        bookmarks = read_bookmarks_from_file(bookmarks_path)
        # self._add_bookmarks(bookmarks)
        self._add_bookmarks(bookmarks, page_offset)
        # Save the PDF file having been handled in savepath.
        self.__writable.save(savepath)

