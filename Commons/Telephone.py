# -*- coding: cp1252 -*-

from pprint import pprint


def encode_phonenumber(ctry_code, area_code, phone_number):
    return "+%s (%s) %s" % (ctry_code, area_code, phone_number)
    
    
def decode_phonenumber(phone_number):
    ctry_code = '' 
    area_code = ''
    
    # Get the "contry code" ---------------------------------------------------
    phone_number = phone_number.lstrip()
    if phone_number.startswith('00') or \
       phone_number.startswith('+'):
        cut_at = phone_number.find(' ')
        ctry_code = phone_number[0:cut_at].replace('00', '+')
        if not ctry_code.startswith('+'):
            ctry_code = '+' + ctry_code
        phone_number = phone_number[cut_at:len(phone_number)]
        cut_at = None
    
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
        
    if cut_at <>  None:
        area_code = phone_number[0:cut_at].replace('(', '')
        phone_number = phone_number[cut_at:len(phone_number)]
        
    if not area_code.startswith('0'):
        area_code = '0' + area_code
        
    # Get the "phone number" --------------------------------------------------
    phone_number = phone_number.replace(')', '').replace('/', '').replace(' ', '')
    
    return ctry_code, area_code, phone_number

        
if __name__ == "__main__":
    phone_number = raw_input('Give PhoneNumber > ').upper()
    
    ctry_code, area_code, phone_number = decode_phonenumber(phone_number)
    print 'International: %s.\nVorwahl: %s.\nTelefon: %s.\n' % (ctry_code, area_code, phone_number)
    
    print; raw_input('... give <RETURN> to exit')
    