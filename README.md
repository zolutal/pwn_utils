# pwn_utils

A repository of scripts which automate some actions I am constantly repeating for pwn challenges

## Scripts

* dwninit: A script to automatically extract the libc and ld from a docker image into the current directory, you can then use pwninit to relink the binary to the extracted libraries


* pwinit-template: An custom pwninit template with boilerplate to wrap the pwntools process/remote modules into a single 'proc' class with shorthanded i/o function names, defaults to process rather than remote, mostly made to save myself from the suffering that is typing out 'sendlineafter' multiple times. I just stick the boilerplate into a vim fold to get it out of the way.

## dwninit Example
```
┌──(pwn)─(jmiller@ubuntu)-[~/ctf/demo]
└─$ ls
Dockerfile  chall  flag.txt

┌──(pwn)─(jmiller@ubuntu)-[~/ctf/demo]
└─$ dwninit
[+] Using Dockerfile at /home/jmiller/ctf/demo/Dockerfile
[+] Building image...
[+] Starting Container
[+] Copying libc at path /usr/lib/x86_64-linux-gnu/libc.so.6
[+] Extracting libc to libc.so.6
[+] Copying ld at path /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
[+] Extracting ld to ld-linux-x86-64.so.2

┌──(pwn)─(jmiller@ubuntu)-[~/ctf/demo]
└─$ pwninit
bin: ./chall
libc: ./libc.so.6
ld: ./ld-linux-x86-64.so.2

unstripping libc
https://launchpad.net/ubuntu/+archive/primary/+files//libc6-dbg_2.35-0ubuntu3.1_amd64.deb
warning: failed unstripping libc: libc deb error: failed to find file in data.tar
copying ./chall to ./chall_patched
running patchelf on ./chall_patched
writing solve.py stub

┌──(pwn)─(jmiller@ubuntu)-[~/ctf/demo]
└─$ ls
Dockerfile  chall  chall_patched  flag.txt  ld-linux-x86-64.so.2  libc.so.6  solve.py

┌──(pwn)─(jmiller@ubuntu)-[~/ctf/demo]
└─$ ldd chall_patched
        linux-vdso.so.1 (0x00007ffd70be9000)
        libseccomp.so.2 => /lib/x86_64-linux-gnu/libseccomp.so.2 (0x00007fa98c5f4000)
        libc.so.6 => ./libc.so.6 (0x00007fa98c3cc000)
        ./ld-linux-x86-64.so.2 => /lib64/ld-linux-x86-64.so.2 (0x00007fa98c625000)
```
