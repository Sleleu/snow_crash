#!/usr/bin/python3
import sys

def decrypt(cipher):
    message = ""
    for i, char in enumerate(cipher):
        message += chr(ord(char) - i)
    return message

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One argument required")
        sys.exit(1)

    cipher = sys.argv[1]
    message = decrypt(cipher)
    print(message)