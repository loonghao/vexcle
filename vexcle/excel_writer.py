"""The ExcelWriter wrapper function for export ExcelWriter."""

# Import third-party modules
import xlsxwriter
from xlsxwriter.exceptions import FileCreateError


class ExcelWriter(object):
    def __init__(self, excel_file_name, context):
        self._context = context
        self._workbook = xlsxwriter.Workbook(excel_file_name)
        self.worksheet = self._workbook.add_worksheet()
        self.worksheet.set_default_row(10)
        self.worksheet.set_row(0, 120)
        self.worksheet.set_column(0, 0, 42)
        self.worksheet.set_column(1, 6, 30)
        self.format = self._workbook.add_format()
        self.format.set_align("center")
        self.format.set_bold()
        self.format.set_align("vcenter")
        self.file_path = excel_file_name

    @property
    def bold(self):
        return self._workbook.add_format(self._context.excel_workbook_format)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._workbook.close()
        except FileCreateError:
            raise FileCreateError("The file is already open, please close and "
                                  "try again.")

    def write(self, row, column, data):
        self.set_row(row)
        self.worksheet.write(row, column, data, self.format)

    def write_string(self, row, column, data):
        self.set_row(row)
        self.worksheet.write_string(row, column, data, self.format)

    def set_row(self, row_num):
        self.worksheet.set_row(row_num, 120)

    def insert_image(self, row_num, column, image_path):
        self.set_row(row_num)
        self.worksheet.insert_image(row_num, column, image_path)
