# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons FileSystem module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import os, ConfigParser


class Base:
    ''' This Base is the parent class of all file objects. '''
    
    def __init__(self, path='', filename=''):
        self.path = path
        self.filename = filename
        
        self.path = self.path.replace('\\', '/')
        if self.path <> '':
            if self.path.endswith('/'):
                self.path += '/'
        self.filepath = self.path + self.filename
        
        
    
class iniFile(ConfigParser.RawConfigParser):
    def __init__(self, filepath):
        ConfigParser.RawConfigParser.__init__(self)
        
        self._filepath = filepath

    
    def get_section(self, section, option_dict):
        ''' section is simply the section as string,
            option_dict is a dict of defaults, f.e.:
            {'engine': 'SQLite',
             'filepath': 'c:\\dummy.db'} '''
             
        self.read(self._filepath)
        section_dict = {}
        
        for option in option_dict:
            section_error = False
            option_error = False
            
            try:
                value = self.get(section, option)
                section_dict[option] = value
            except ConfigParser.NoSectionError:
                section_error = True
            except ConfigParser.NoOptionError:
                option_error = True
            finally:
                if section_error == True:
                    self.add_section(section)
                if section_error == True or option_error == True:
                    self.set(section, option, option_dict[option])
                    section_dict[option] = option_dict[option]
        return section_dict
    
    
    def save_section(self, section, options_dict):
        for key in options_dict:
            self.set(section, key, options_dict[key])
                    
        try:
            self.write(open(self._filepath, 'w'))
        except:
            raise



class xlsFile(Base):
    ''' Helps to get data out of xlsFiles. Needs pyExcelerator, hope someday
        a kind of pyWord will appear! '''

    def __init__(self, filepath='', encoding='cp1251'):
        self.encoding = encoding
        self.filepath = filepath
        
        try:
            import pyExcelerator
        except:
            raise

        self.parser = pyExcelerator.parse_xls

        try:
            self.content = self.parser(self.filepath, self.encoding)
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



class csvFile(Base):
    def __init__(self, path='', filename='', encoding='cp1251'):
        Base.__init__(self, path, filename)
        self.encoding = encoding



class rtfFile(Base):
    ''' Transforms a string into a suitable rtf-Text and helps to read rtf-Files
        as well as Template them. '''

    def __init__(self, path='', filename='', encoding='cp1251'):
        Base.__init__(self, path, filename)
        self.encoding = encoding
        self.content = None

        try:
            self.input_file = open(self.filepath, 'r')
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


def get_filenames(top):
    iter = os.walk(top=top)
    tuple = iter.next()
    file_list = tuple[2]
    return file_list


def makedirs(dirlist):
    for dirname in dirlist:
        try:
            os.mkdir(dirname)
        except:
            pass
    return


