"""Code to handle preparing equation text for image transform."""


def escape_percentage(equation):
    """
    Escape percentage symbols in equations.

    Inputs:
        equation: string containing equation

    Returns string with percentage symbols escaped
    """
    if '%' in equation:
        equation = equation.replace('%', '\\%').replace('\\\\%', '\\%')

    return equation


def equation2png(equation_element):
    """Prepare equation code for conversion to png."""
    # Replace the open and close delimiters with the inline latex delimiters
    # This handles new lines and blank lines better
    equation_element = '\({}\)'.format(equation_element[2:-2])

    # Remove the next line when EdTech has removed all hex colour codes
    # This escapes the # in the colour code
    equation_element = equation_element.replace(r'{#', r'{\#')

    # remove tabs
    equation_element = equation_element.replace('\t', ' ')
    equation_element = escape_percentage(equation_element)
    return equation_element
