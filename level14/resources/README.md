This Getflag move was very funny (not at all).

Trying to reverse the operation of getflag we quickly come across this output:
```
You should not reverse this
```

Well, I'm going to do it anyway 🙂

I extracted the binary from the vm and put it on https://dogbolt.org/ to decompile it.
You quickly come across the option you've stumbled into:
```C
  lVar2 = ptrace(PTRACE_TRACEME,0,1,0);
  if (lVar2 < 0) {
    puts("You should not reverse this");
    uVar3 = 1;
  }
```

It finds its asm translation in the following instructions:

```assembly
   0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
   0x0804898e <+72>:	test   %eax,%eax
   0x08048990 <+74>:	jns    0x80489a8 <main+98>
```

To pass this ptrace test, I set a breakpoint to the test instruction `0x0804898e`, then modified the value of the EAX register:
```shell
Breakpoint 1, 0x0804894a in main ()
(gdb) s
Single stepping until exit from function main,
which has no line number information.
You should not reverse this
0xb7e454d3 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
(gdb) b *0x0804898e
Breakpoint 3 at 0x804898e
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /bin/getflag 

Breakpoint 1, 0x0804894a in main ()
(gdb) s
Single stepping until exit from function main,
which has no line number information.

Breakpoint 3, 0x0804898e in main ()
(gdb) i r
eax            0xffffffff	-1
ecx            0xb7e2b900	-1209878272
edx            0xffffffc8	-56
ebx            0xb7fd0ff4	-1208152076
esp            0xbffff620	0xbffff620
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x804898e	0x804898e <main+72>
eflags         0x200282	[ SF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) set $eax = 42
(gdb) s
Single stepping until exit from function main,
which has no line number information.

Breakpoint 2, 0x08048afd in main ()
```

Once we can get to the return of the getuid() function, the strategy is exactly the same as for the level13 flag. We retrieve EAX and add the UID of flag14. After a `cat /etc/passwd`, we see that the UID of flag14 is 3014: `flag14:x:3014:3014::/home/flag/flag14:/bin/bash` which corresponds to the if statement in the source.c file:
```C
              else {
                if (_Var6 != 0xbc6) goto LAB_08048e06;
                pcVar4 = (char *)ft_des("g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|");
                fputs(pcVar4,__stream);
              }
```

Here's the UID retrieval in EAX in asm :

```assembly
   0x08048afd <+439>:	call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:	mov    %eax,0x18(%esp)
   0x08048b06 <+448>:	mov    0x18(%esp),%eax
   0x08048b0a <+452>:	cmp    $0xbbe,%eax
```

So I set a breakpoint at `0x08048b0a` and modify the EAX value:
```shell
(gdb) b *0x08048b0a
Breakpoint 4 at 0x8048b0a
Breakpoint 4, 0x08048b0a in main ()
(gdb) i r
eax            0x7dd	2013
ecx            0xb7fda000	-1208115200
edx            0x20	32
ebx            0xb7fd0ff4	-1208152076
esp            0xbffff620	0xbffff620
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x8048b0a	0x8048b0a <main+452>
eflags         0x200246	[ PF ZF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) set $eax = 3014
(gdb) i r
eax            0xbc6	3014
ecx            0xb7fda000	-1208115200
edx            0x20	32
ebx            0xb7fd0ff4	-1208152076
esp            0xbffff620	0xbffff620
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x8048b0a	0x8048b0a <main+452>
eflags         0x200246	[ PF ZF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) s
Single stepping until exit from function main,
which has no line number information.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
0xb7e454d3 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
```

And here's the flag!
