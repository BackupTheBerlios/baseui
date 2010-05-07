# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons FileSystem module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================


class iniFile:
    def __init__(self, filename):
        import ConfigParser
        self.filename = filename
        self.parser = ConfigParser.ConfigParser()
        return


    def dictresult(self, section):
        try:
            self.parser.read(self.filename)
            value_lol = self.parser.items(section)
        except:
            raise

        value_dic = {}
        for value in value_lol:
             value_dic[value[0]] = value[1]
        return value_dic


    def save(self, ini_text):
        ini_file = open(self.filename, "w")
        ini_file.write(ini_text)
        ini_file.close()
        return



class xlsFile:
    ''' Helps to get data out of xlsFiles. Needs pyExcelerator, hope someday
        a kind of pyWord will appear! '''

    def __init__(self, filename, encoding='cp1251'):
        try:
            import pyExcelerator
        except:
            raise

        self.filename = filename
        self.encoding = encoding
        self.parser = pyExcelerator.parse_xls

        try:
            self.content = self.parser(self.filename, self.encoding)
        except:
            raise


    def get_sheets(self):
        sheet_list = []
        for sheet_name, values in self.content:
            sheet_list.append(sheet_name)
        return sheet_list


    def get_headers(self, source_sheet_name):
        sheet_content = self.get_sheet_content(source_sheet_name)
        header_list = []
        for row_idx, col_idx in sorted(sheet_content.keys()):
            if row_idx == 0:
                header_list.append(sheet_content[0, col_idx])
        return header_list


    def get_sheet_content(self, source_sheet_name):
        for sheet_name, sheet_content in self.content:
            if sheet_name == source_sheet_name:
                return sheet_content
        return


    def get_cell_content(self, source_sheet_name, row_idx, col_idx):
        sheet_content = self.get_sheet_content(source_sheet_name)
        if sheet_content.has_key((row_idx, col_idx)):
            cell_content = sheet_content[(row_idx, col_idx)]
        else:
            return
        return cell_content


    def get_sheet_lod(self, source_sheet_name):
        sheet_content = self.get_sheet_content(source_sheet_name)
        header_list = self.get_headers(source_sheet_name)

        temp_dict = {}
        sheet_lod = []
        actual_row = 0

        for row_idx, col_idx in sorted(sheet_content.keys()):
            if row_idx > 0:
                if row_idx > actual_row:
                    if temp_dict <> {}:
                        sheet_lod.append(temp_dict)
                    actual_row = row_idx
                    temp_dict = {}
                if row_idx == actual_row:
                    cell_content = sheet_content[(row_idx, col_idx)]
                    temp_dict[header_list[col_idx]] = cell_content
        sheet_lod.append(temp_dict)
        return sheet_lod



class csvFile:
    def __init__(self, filename, encoding='cp1251'):
        self.filename = filename
        self.encoding = encoding



class rtfFile:
    ''' Transforms a string into a suitable rtf-Text and helps to read rtf-Files
        as well as Template them. '''

    def __init__(self, filename, encoding='cp1251'):
        self.filename = filename
        self.encoding = encoding
        self.content = None

        try:
            self.input_file = open(self.filename, 'r')
            self.content = input_file.read()
            self.input_file.close()
        except:
            raise


    def fill_template(self, content_dict):
        self.content = self.content % content_dict

        encoded_text = ''
        for char in self.content:
            if ord(char) > 127:
                char = "\\'" + str(hex(ord(char)))[2:4]
            encoded_text += char
        self.content = encoded_text


    def save_as(self, filename):
        try:
            output_file = open(filename, 'w')
            output_file.write(self.content)
            output_file.close()
        except:
            raise


