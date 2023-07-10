#!/usr/bin/env python3
import crypt
import argparse

parser = argparse.ArgumentParser(description='Hash text with crypt(3) / DES')
parser.add_argument('-t', '--text', type=str, required=True, help='Text to be hashed')
parser.add_argument('-s', '--salt', type=str, required=True, help='Salt for hashing')

args = parser.parse_args()

print(crypt.crypt(args.text, args.salt))