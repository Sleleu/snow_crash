On trouve un fichier level09, et token dans le home, SUID bit actif sur level09.

Avec ltrace on trouve ceci :

```
level09@SnowCrash:~$ ltrace ./level09
__libc_start_main(0x80487ce, 1, 0xbffff7d4, 0x8048aa0, 0x8048b10 <unfinished ...>
ptrace(0, 0, 1, 0, 0xb7e2fe38)                            = -1
puts("You should not reverse this"You should not reverse this
)                       = 28
```

En lançant level09 sur token on trouve ça :

```
level09@SnowCrash:~$ ./level09 token
tpmhr
```

On se rend vite compte que le programme ne fait que récupérer une string, et lui applique un décalage ASCII équivalent à l'index de position dans la string :

```
level09@SnowCrash:~$ ./level09 aaaaa
abcde
```

Le même décalage a probablement été réalisé sur le token :

```
level09@SnowCrash:~$ cat token
f4kmm6p|=?p?n??DB?Du{??
```

Ok donc on peut faire un petit script qui soustrait le décalage pour retourner le texte original :

```python
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
```

Ça fonctionne avec une phrase normale mais pas avec le token :

```
python3 script.py f4kmm6p|=?p?n??DB?Du{??
zsh: ?p?n??DB?Du{?? not found
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>            
BrokenPipeError: [Errno 32] Broken pipe
```

Forcément il doit y avoir des caractères non imprimables. On peut sûrement remanier le script pour récupérer les valeurs hexadécimales du fichier et appliquer directement la soustraction de l'index sur chaque caractère. On peut récupérer les valeurs hexa sur fichier avec `hexdump` :

```
level09@SnowCrash:~$ hexdump token
0000000 3466 6d6b 366d 7c70 823d 707f 6e82 8283
0000010 4244 4483 7b75 8c7f 0a89               
000001a
```

Les valeurs sont inversées, par exemple si on écrit dans un fichier "abcd" :

```
level09@SnowCrash:~$ echo "abcd" > /tmp/toast
level09@SnowCrash:~$ hexdump /tmp/toast
0000000 6261 6463 000a                         
0000005
```

On voit qu'on peut lire en valeur ASCII "badc" (0a correspondant à un '\n' ajouté à la fin par la commande echo) donc on devra inverser l'ordre de ces valeurs. Ça nous donne le script suivant : 

```python
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
```

Testons donc avec le fichier token :

```
level09@SnowCrash:~$ hexdump token
0000000 3466 6d6b 366d 7c70 823d 707f 6e82 8283
0000010 4244 4483 7b75 8c7f 0a89               
000001a
```

Puis on lance le script en retirant les adresses :

```
python3 script.py "3466 6d6b 366d 7c70 823d 707f 6e82 8283 4244 4483 7b75 8c7f 0a89"
f3iji1ju5yuevaus41q1afiuq
```

On peut maintenant se connecter à l'utilisateur flag09 et utiliser `getflag`