# -*- coding: cp1252 -*-

from pprint import pprint


def encode_phonenumber(ctry_code='', area_code='', phone_number='', 
                       string_format='+%(ctry_code)s (%(area_code)s) %(phone_number)s'):
    ''' string_format = +%(ctry_code)s (%(area_code)s) %(phone_number)s '''
    
    phone_number_dict = {}
    
    if ctry_code.startswith('00'): 
        ctry_code = ctry_code[2:]
    if ctry_code.startswith('+'):
        ctry_code = ctry_code[1:]
    if ctry_code <> '':
        phone_number_dict['ctry_code'] = ctry_code
        
    if area_code.startswith('0'):
        area_code = area_code[1:]
    if area_code <> '':
        phone_number_dict['area_code'] = area_code
        
    if phone_number <> '':
        phone_number_dict['phone_number'] = phone_number
        
    phone_number_str = string_format % phone_number_dict
    return phone_number_str
    
    
def decode_phonenumber(phone_number):
    ctry_code = '' 
    area_code = ''
    cut_at = -1
    
    # Get the "contry code" ---------------------------------------------------
    phone_number = phone_number.lstrip()
    if phone_number.startswith('00') or \
       phone_number.startswith('+'):
        cut_at = phone_number.find(' ')
        
        if cut_at <> -1:
            ctry_code = phone_number[0:cut_at].replace('00', '+')
            if not ctry_code.startswith('+'):
                ctry_code = '+' + ctry_code
            phone_number = phone_number[cut_at:len(phone_number)]
            cut_at = -1
    
    # Get the "area code" -----------------------------------------------------
    phone_number = phone_number.lstrip()
    if phone_number.find(')') <> -1:
        cut_at = phone_number.find(')')
    elif phone_number.find('/') <> -1:
        cut_at = phone_number.find('/')
    elif phone_number.find(' ') <> -1:
        cut_at = phone_number.find(' ')
    elif phone_number.find('-') <> -1:
        cut_at = phone_number.find('-')
    
        
    if cut_at <> -1:
        area_code = phone_number[0:cut_at].replace('(', '')
        phone_number = phone_number[cut_at:len(phone_number)]
        
    if not area_code.startswith('0') and area_code <> '':
        area_code = '0' + area_code
        
    # Get the "phone number" --------------------------------------------------
    phone_number = phone_number.replace(')', '').replace('/', '').replace(' ', '')
    
    return ctry_code, area_code, phone_number

        
if __name__ == "__main__":
    phone_number = raw_input('Give PhoneNumber > ').upper()
    
    ctry_code, area_code, phone_number = decode_phonenumber(phone_number)
    print 'International: %s.\nVorwahl: %s.\nTelefon: %s.\n' % (ctry_code, area_code, phone_number)
    
    ctry_code = raw_input('International: ')
    area_code = raw_input('Vorwahl: ')
    phone_number = raw_input('Telefonnummer: ')
    
    print
    print encode_phonenumber(ctry_code, area_code, phone_number)
    
    print; raw_input('... give <RETURN> to exit')
    quit()
    