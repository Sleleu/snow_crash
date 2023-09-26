```
level13@SnowCrash:~$ ./level13 
UID 2013 started us but we we expect 4242
```

Okay, it's pretty clear; we need to change the UID. Ltrace doesn't give us any more clues since we exit the program right after checking the UID. We can see that the assembly code for this is very short:

```assembly
(gdb) disass main
Dump of assembler code for function main:
   0x0804858c <+0>:		push   %ebp
   0x0804858d <+1>:		mov    %esp,%ebp
   0x0804858f <+3>:		and    $0xfffffff0,%esp
   0x08048592 <+6>:		sub    $0x10,%esp
   0x08048595 <+9>:		call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    $0x80486c8,%edx
   0x080485ab <+31>:	movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:	mov    %eax,0x4(%esp)
   0x080485b7 <+43>:	mov    %edx,(%esp)
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	movl   $0x1,(%esp)
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave  
   0x080485e9 <+93>:	ret    
End of assembler dump.
```

We can see getuid, which returns the UID in the EAX register, which is then compared with `0x1092`, which is 4242, the UID required to jump to `0x080485cb`:

```assembly
   0x08048595 <+9>:		call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
```

If we fulfill this condition, we can proceed to the `ft_des` function, which likely allows us to progress in the challenge:

```assembly
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
```

So, we can try to rewrite the value of EAX after its passage through `getuid()`. Oh well, it's already the flag... :

```
Breakpoint 2, 0x0804859a in main ()
(gdb) set $eax = 4242
(gdb) s
Single stepping until exit from function main,
which has no line number information.
your token is 2A31L79asukciNyi8uppkEuSx
```