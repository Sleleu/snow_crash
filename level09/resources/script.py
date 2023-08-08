#!/usr/bin/python3
import sys

def decrypt(cipher):
    hex_values = cipher.split()
    message = ""
    i = 0
    for hex_value in hex_values:   
        reverse_hex = hex_value[2:] + hex_value[:2] # Inverse l'ordre des octets
        value_a = int(reverse_hex[0:2], 16) - i # Récupère la première moitié
        value_b = int(reverse_hex[2:4], 16) - (i + 1) # Puis la seconde
        value_a = max(value_a, 0) # Pour assurer qu'on reste dans une plage unicode valide
        value_b = max(value_b, 0)
        message += chr(value_a) + chr(value_b) # On ajoute dans le bon ordre les caractères
        i += 2
    return message

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One argument required")
        sys.exit(1)

    cipher = sys.argv[1]
    message = decrypt(cipher)
    print(message)
