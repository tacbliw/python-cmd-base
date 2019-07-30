# -*- coding: utf-8 -*-

"""
Functions to manage Wildcat's input data, including checking,
formatting
"""
import socket
import re

"""
CHECKING
"""

def is_host(text=''):
    """Check if a string is a host"""
    if not text:
        return False
    try:
        socket.gethostbyname(text)
    except socket.gaierror:
        return False
    return True

def is_port(number):
    """Check if a number is a port (in range  1 - 65535)"""
    if 1 <= number <= 65535:
        return True
    else:
        return False

def is_port_list(text=''):
    """Check if a string is in a port format (e.g. 123 or 12-34 or 12,34 or 12-34,56)"""
    if not text:
        return False

    if not all(char in '0123456789-, ' for char in text):
        return False

    for elem in text.split(','):
        if '-' in elem and len(elem.split('-')) != 2:
            return False

    for number in map(int, re.findall(r"\d{1,5}", text)):
        if not is_port(number):
            return False

    return True

def is_number(maybe_text):
    try:
        int(maybe_text)
    except ValueError:
        return False
    return True

"""
FORMATTING
"""
def no_space(text=''):
    """Delete all spaces in a text string"""
    result = []
    for char in text:
        if char != ' ':
            result.append(char)
    return ''.join(result)

def to_port_list(text=''):
    """Convert a text string to a list of ports"""
    temp = no_space(text).split(',')
    port_list = []
    for port in temp:
        if '-' in port:  # it is a port range
            rng = port.split('-')  # range 
            if rng[0] == '' or rng[1] == '':
                continue
            
            rng = list(map(int, rng))
            if rng[1] >= rng[0]:
                for num in range(rng[0], rng[1] + 1):
                    port_list.append(num)
            else:
                for num in range(rng[1], rng[0] + 1):
                    port_list.append(num)
        else:
            port_list.append(int(port))
    return port_list


