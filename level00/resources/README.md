En cherchant comment lister les différents utilisateurs sous un système linux : https://www.cyberciti.biz/faq/linux-list-users-command

On tombe sur ça : 

```
cat /etc/passwd
```

On voit donc tous les users disponbles, dont le user flag00. Maintenant comment trouver des informations sur lui ?
Il suffirait par exemple de trouver les fichiers sur ce système appartenant à ce user, on peut utiliser :

```
find / -user "flag00"
```
On peut aussi y ajouter `2> /dev/null` pour supprimer tous les access denied de la commande.

En affichant le contenu l'un des fichiers auxquels on peut accéder, on trouve :

```
level00@SnowCrash:~$ cat /rofs/usr/sbin/john
cdiiddwpgswtgt
```

Ça ressemble fortement à un cipher. Pour vérifier cela, on peut tenter de bruteforce le déchiffrement de ce cipher avec ce site : https://www.dcode.fr/affine-cipher

Le premier résultat nous retourne : nottoohardhere

On peut donc facilement en déduire qu'il s'agit du mot de passe pour se connecter au user flag00. On peut donc utiliser `su flag00`, et obtenir le flag avec la commande `getflag`.

En essayant le flag comme password pour le user level01, on peut donc passer à l'étape suivante.
