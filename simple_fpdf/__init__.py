from fpdf import FPDF


class SimpleFPDF(FPDF):
    
    def __init__(self, *args, **kwargs):
        
        # settings
        self.pdf_width = kwargs.pop('width', 210)
        self.pdf_height = kwargs.pop('height', 297)
        
        # set format of pdf
        kwargs['format'] = self.format = (self.pdf_width, self.pdf_height)
        
        # init the parent class
        super().__init__(*args, **kwargs)
        
        # row & page management
        self.total_pages = 0
        self.current_page_number = 0
        self.rows = []
        self.row_settings = []
        
        # initialize
        self.set_font('Arial', '', 8)
        self.set_xy(0.0, 0.0)

    def add_page(self, rows=None):
        if not rows: raise ValueError('rows is required.')
        
        if type(rows) == list:
            self.rows.append([])
            self.row_settings.append(rows)
            
            self.total_pages += 1
            self.current_page_number += 1
            for row in rows:
                self.add_row(page=self.current_page_number, columns=row['columns'])
            
        return super().add_page()
    
    def get_row_setting(self, row, setting, page=None, default=None):
        if not page: page = self.current_page_number
        try:
            setting_value = self.row_settings[page-1][row-1][setting]
            return setting_value
        except KeyError:
            return default
    
    def get_row_start_y(self, row, page=None):
        if not page: page = self.current_page_number
        row_height = self.get_row_height(page)
        
        y = 0
        length = row
        for i in range(0, length):
            top_margin = self.get_row_setting(i+1, 'top-margin', page=page, default=0)
            if top_margin == 0 and i == 0: top_margin = self.t_margin
            if i == (row-1):
                y += top_margin
            else:
                y += top_margin + row_height
        
        return y
    
    def get_row(self, row, page=None):
        try:
            if not page: page = self.current_page_number
            return self.rows[page-1][row-1]
        except IndexError:
            raise IndexError('Row {0} or page {1} does not exist. Maximum amount for rows is {2} and pages {3}.'.format(row, page, len(self.rows), self.total_pages))
    
    def get_column(self, row, column, page=None):
        try:
            if not page: page = self.current_page_number
            max_columns = len(self.rows[page-1][row-1])
            return self.rows[page-1][row-1][column-1]
        except IndexError:
            raise IndexError('Column {0} for row {1} on page {2} does not exist. Maximum amount of columns is {3}.'.format(column, row, page, max_columns))
    
    def set_column_text(self, row, column, txt, page=None):
        try:
            if not page: page = self.current_page_number
            max_columns = len(self.rows[page-1][row-1])
            self.rows[page-1][row-1][column-1] = txt
        except IndexError:
            raise IndexError('Column {0} for row {1} on page {2} does not exist. Maximum amount of columns is {3}.'.format(column, row, page, max_columns))
    
    def get_column_width(self, page, row):
        current_row = self.get_row(row, page=page)
        columns = len(current_row)
        
        column_width = (self.pdf_width - self.l_margin - self.r_margin) / columns
        return column_width
    
    def get_row_height(self, page):
        amount_of_rows = len(self.rows[page-1])
        row_height = (self.pdf_height - self.t_margin - self.b_margin) / amount_of_rows
        return row_height
    
    def add_row(self, page=None, columns=1):
        if not page: page = self.current_page_number
        self.rows[page-1].append([])
        current_row = len(self.rows[page-1])
        
        for _ in range(0, columns):
            self.add_column(page=page, row=current_row)
    
    def add_column(self, page, row):
        current_row = self.get_row(row, page=page)
        current_row.append('')
        
    def set_row_cursor(self, row, page=None, column=1):
        if not page: page = self.current_page_number
        y = self.get_row_start_y(row, page)
        x = (self.get_column_width(page, row) * (column-1)) + self.l_margin
        self.set_xy(x, y)
    
    def write_text(self, row, txt, column=1, page=None, align='J'):
        if not page: page = self.current_page_number
        self.set_column_text(row, column, txt, page=page)
        self.set_row_cursor(row, page=page, column=column)
        max_width = self.get_column_width(page, row)
        return self.multi_cell(max_width, self.font_size, txt, 0, align=align)