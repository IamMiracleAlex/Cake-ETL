from itertools import groupby


def split_text(s):
    '''split str with number and yield result'''

    for k, g in groupby(s, str.isalpha):
        yield ''.join(g)


def get_base_unit(unit):
    '''Resolves the unit to one'''

    return {
        'm':'m', 'metres': 'm',
        'mm': 'mm', 'millimeters': 'm',
        'in': 'in', 'inches': 'in'
        }.get(unit)


def is_number(n):
    '''Validates if a string is a number'''

    try:
        float(n)  
        return True
    except ValueError:
        return False


def value_to_mm(value, unit):
    '''Convert values to millimeters'''
   
    return {'in': 25.4, 'm': 1000}[unit] * value