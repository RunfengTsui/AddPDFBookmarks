import os
import pikepdf
from pikepdf import Pdf, OutlineItem


class PDFHandler(object):
    """
    Class of PDF file handler.
    """
    def __init__(self, pdf_file_path):
        """
        Initialize a PDF file object.

        Args:
            pdf_file_path: the path of the PDF file to be handled.
        """
        # open the PDF file
        self.__pdf = Pdf.open(pdf_file_path)

        # get the name of PDF file without path and file extension
        self.file_name = os.path.basename(pdf_file_path).split('.')[0]
        # get the number of pages
        self.pages_num = len(self.__pdf.pages)

        # create a writable PDF file
        self.__writable = Pdf.new()
        self.__writable.pages.extend(self.__pdf.pages)

    def read_bookmarks_from_file(self, file_path, page_offset=0):
        """
        Read bookmarks from the given file.
    
        Args:
            file_path: path of the given file containing bookmarks.

            page_offset: int, default value is 0. Due to the existence of pages such as the cover page and the table of contents, the actual page number in the PDF is more than the page number written in the table of contents.

        Returns:
            bookmarks: list. The bookmarks list of the PDF file. Every item in the list is a triple with format `(structure, title, page)`. The `structure` represents the structure hierarchy of bookmarks. It has three values, one, two and three, representing the first layer of bookmarks, the second layer of bookmarks and the third layer of bookmarks.
        """
        bookmarks = list()
        with open(file_path, 'r') as file:
            for line in file:
                line = line.rstrip()
                if not line:
                    continue
                # use '@' as a separator for bookmarks and page numbers
                try:
                    title = line.split('@')[0].rstrip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print(msg)
                    continue
                # add bookmark if title and page are not empty
                if title and page:
                    try:
                        page = int(page) + page_offset
                        # get the structure hierarchy of bookmarks by counting tab keys
                        structure = title.count('#')
                        title = title.replace('#', '').lstrip()
                        bookmarks.append((structure, title, page))
                    except ValueError as msg:
                        print(msg)
            
        return bookmarks

    def add_bookmarks(self, bookmarks):
        """
        Add bookmarks for the given PDF file.

        Args:
            bookmarks: list. A list of triples with format `(structure, title, page)`, where `structure` represents the structure hierarchy of bookmarks. For example, [(1, title1, 0), (2, title2, 3), (3, title3, 7), (2, title4, 10), (1, title5, 15), ...]. `(2, title2, 3)` is the children of `(1, title1, 0)` and the father of `(3, title3, 7)`.

        Returns:
            None
        """
        with self.__writable.open_outline() as outline:
            for structure, title, page in bookmarks:
                oi = OutlineItem(title, page-1)
                if structure == 1:
                    outline.root.append(oi)
                elif structure == 2:
                    outline.root[-1].children.append(oi)
                elif structure == 3:
                    outline.root[-1].children[-1].children.append(oi)
                else:
                    print('The bookmarks structure is Out Of Range!')
                    continue

    def add_bookmarks_from_file(self, file_path, page_offset=0):
        """
        Add bookmarks for the PDF file from the given file.

        Args:
            file_path: path of the given file containing bookmarks.
            page_offset: int, default value is 0.

        Returns:
            None
        """
        bookmarks = self.read_bookmarks_from_file(file_path, page_offset)
        self.add_bookmarks(bookmarks)

    def save2pdf(self, file_path):
        """
        Save the PDF file having been handled in file_path.

        Args:
            file_path: file path to save.

        Returns:
            None
        """
        path = os.path.join(file_path, f"{self.file_name}_addbookmarks.pdf")
        self.__writable.save(path)