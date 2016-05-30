'''Code to handle preparing equation text for image transform'''

def escape_percentage(equation):
    '''
    Escape percentage symbols in equations
    Inputs:
        equation: string containing equation

    Returns string with percentage symbols escaped
    '''
    if not ('%' in equation):
        return equation

    equation = equation.replace('%', '\\%').replace('\\\\%', '\\%')

    return equation


def equation2png(equation_element):
    '''Prepares equation code for conversion to png'''
    # check to see how many lines are in the code - why?
    equation_element = equation_element.replace(r'\[', '\(').replace(r'\]', '\)')
    equation_element = equation_element.replace(r'&', r' &')
    # Remove the next line when EdTech has removed all hex colour codes
    # This escapes the # in the colour code
    equation_element = equation_element.replace(r'{#', r'{\#')
    # remove tabs
    equation_element = equation_element.replace('\t', ' ')
    equation_element = escape_percentage(equation_element)
    return equation_element
