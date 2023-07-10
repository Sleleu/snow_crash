J'ai remarqué depuis le level00 quelque chose d'intéressant lorsqu'on liste les users avec `cat /etc/passwd` :

```
level10:x:2010:2010::/home/user/level10:/bin/bash
level11:x:2011:2011::/home/user/level11:/bin/bash
level12:x:2012:2012::/home/user/level12:/bin/bash
level13:x:2013:2013::/home/user/level13:/bin/bash
level14:x:2014:2014::/home/user/level14:/bin/bash
flag00:x:3000:3000::/home/flag/flag00:/bin/bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
flag02:x:3002:3002::/home/flag/flag02:/bin/bash
flag03:x:3003:3003::/home/flag/flag03:/bin/bash
```

Le 'x' dans un second champ signifie en réalité que le mot de passe est stocké et chiffré dans un autre répertoire, généralement dans `/etc/shadow`, qui ne peut être lu que par l'utilisateur root.

Or dans le cas de l'utilisateur flag01, il semble que son mot de passe `42hDRfypTqqnw` est directement affiché et chiffré. On peut quand même tenter dans le doute :

```
level01@SnowCrash:~$ su flag01
Password: 
su: Authentication failure
```

Evidemment 🙂

Après un petit passage sur dcode, je trouve pas grand chose d'aussi simple que sur le level00. Je tente de trouver l'origine de ce mot de passe, jusqu'à tomber sur ce site : https://www.tunnelsup.com/hash-analyzer/ qui m'indique que c'est probablement un chiffrement DES ou 3DES.

Le chiffrement DES est un algorithme de chiffrement symétrique, utilisant des clés de 65 bits (ce qui est peu). Il est aujourd'hui totalement cassable du fait de la faible taille de sa clé. Le 3DES fait surement référence au triple DES, qui augmente la sécurité du chiffrement mais n'est toujours pas recommandé du fait de ses faibles performances.

Bon on peut essayer de péter ça avec un coup de JohnTheRipper : 

```
➜  ~ touch encrypted_password.txt
➜  ~ echo "42hDRfypTqqnw" > encrypted_password.txt 
➜  ~ john encrypted_password.txt 
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 128/128 SSE2-16])
Will run 12 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
abcdefg          (?)
1g 0:00:00:00 100% 2/3 100.0g/s 4915Kp/s 4915Kc/s 4915KC/s 123456..lucky0
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

abcdefg... c'était terminé en moins d'une seconde !

Ici dans ce sujet il s'agit plus spécifiquement d'un hash, qui a été produit par l'algorithme crypt(3) avec DES. Puisque c'est un hash, john réalisé une attaque par force brute jusqu'à pouvoir obtenir le même hash. Si il retrouve exactement `42hDRfypTqqnw` à partir du texte `abcdefg` et du sel `42`, on a donc le mot de passe.

Voici le process inverse avec des_hash.py :

```
➜  resources python3 des_hash.py -t "abcdefg" -s "42"
42hDRfypTqqnw
```

Il ne manque plus qu'à se connecter à flag01 et récuperer le flag.