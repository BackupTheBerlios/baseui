# -*- coding: cp1252 -*-

from pprint import pprint


def encode_phonenumber(ctry_code, area_code, phone_number):
    return "+%i (%i) %i"
    
    
def decode_phonenumber(phone_number):
    ctry_code = '' 
    area_code = ''
    last_number = ''
    
    is_international = False
    is_separated = False
    
    separator_list = ['-', '(', ')', '/']
    
    if phone_number.startswith('00') or \
       phone_number.startswith('+'):
        cut_at = phone_number.find(' ')
        ctry_code = phone_number[0:cut_at]
        phone_number = phone_number[cut_at:len(phone_number)]
        print 'rest:', phone_number
        
    for separator in separator_list:
        if separator in phone_number:
            is_separated = True
            print 'Separated'
        
    if is_separated == False:
        print 'Hopefully separated by blank'
        
    return ctry_code, area_code, last_number
            
        
    
    phone_number.split('-')
    
        
        
if __name__ == "__main__":
    phone_number = raw_input('Give PhoneNumber > ').upper()
    
    ctry_code, area_code, phone_number = decode_phonenumber(phone_number)
    print 'International: %s\nVorwahl: %s\nTelefon: %s\n' % (ctry_code, area_code, phone_number)
    
    print; raw_input('... give <RETURN> to exit')
    