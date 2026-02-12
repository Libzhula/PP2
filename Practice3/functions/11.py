def is_palindrome(stroka):
    return True if stroka == stroka[::-1] else False
print(is_palindrome("шалаш"))