

def money_to_string(amount):
    amount = str(amount).split('.')[0]
    value_string = ''
    for i, char in enumerate(amount[::-1]):
        value_string += char
        if (i + 1) % 3 == 0 and (i + 1) < len(amount):
            value_string += ','
    return '\$' + value_string[::-1]