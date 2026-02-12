# Read in a Fahrenheit temperature. Calculate and display the equivalent centigrade temperature. 
# The following formula is used for the conversion: C = (5 / 9) * (F – 32)
def celsius_to_fahrenheit(fahrenheit):
    return ((5/9) * (fahrenheit-32))

print(celsius_to_fahrenheit(33))