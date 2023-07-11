On trouve dans le home de ce user un fichier `level02.pcap`, ça sent le wireshark tout ça 🐸

Il faut trouver le moyen d'extraire le fichier de cette vm vers notre pc hôte, pour ça on peut utiliser la commande `scp`

```
➜  ~ scp -P 4242 level02@127.0.0.1:/home/user/level02/level02.pcap .
	   _____                      _____               _     
	  / ____|                    / ____|             | |    
	 | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
	  \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
	  ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
	 |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          10.0.2.15 
level02@127.0.0.1's password: 
level02.pcap                                  100% 8302    17.4MB/s   00:00 
```

scp, ou **secure copy**, permet comme son nom l'indique permet de copier des fichiers entre différents posts en utilisant le protocole SSH pour établir une connexion chiffrée. Le port par défaut étant le port 22 (port par défaut pour ssh), il faut spécifier avec `-P` qu'on souhaite utiliser le port 4242, puisque la vm utilise ce port pour établir une connexion ssh.

On peut maintenant analyser ce fichier à l'aide de wireshark : 

![Capture d’écran du 2023-07-11 01-33-33](https://github.com/Sleleu/snow_crash/assets/93100775/de6e3f0e-0019-46f3-ba80-2871205af312)

Wireshark est un outil de capture et d'analyse de paquets réseau qui s'avère très utile dans la sécurité, mais aussi le dépannage réseau. On peut notamment appliquer des filtres, suivre certains protocoles ou échanges entre services, et on va par exemple ici suivre le flux tcp ayant été capturé dans ce .pcap :

![Capture d’écran du 2023-07-11 01-53-56](https://github.com/Sleleu/snow_crash/assets/93100775/396a9a63-9af6-4064-82a3-c04e10695a6c)

On trouve donc le mot de passe suivant en retirant les points : ft_wandrNDReL0L

Sauf que non ça marche pas. En réalité, on voit que certains inputs sont répétés avec des majuscules, donc on pourrait soit bruteforcer en ajoutant ou retirant les majuscules pour trouver la bonne combinaison, ou chercher un moyen de trouver le bon mot de passe du premier coup.

Des caractères non printables sont représentés par des points dans le mot de passe : `ft_wandr...NDRel.L0L`
Il suffit alors de mettre `show data as hexdump` afin de vérifier leur valeur qui correspond à 7f en hexadécimale = 127 en valeur décimale, donc un `DEL` en ascii.
Si on écrit littéralement le mot de passe en prenant en compte les DEL, cela donne : `ft_waNDReL0L`

Il ne reste plus qu'à se connecter au user flag02 et à utiliser `getflag`.
