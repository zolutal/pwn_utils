#!/usr/bin/env python3

from pwn import *
import IPython

{bindings}

context.binary = {bin_name}

context.arch = "amd64"
context.encoding = 'latin-1'

def proc(*a, **k):
    if args.REMOTE: return remote(HOST, PORT)
    if args.GDB:  return gdb.debug(*a, **k, gdbscript=gdbscript)
    return process(*a, **k)

attach = lambda: gdb.attach(p) if not args.REMOTE else None
embed  = lambda: IPython.embed(colors="neutral")

lhex = lambda p, v: log.info("%s %#lx" % (p, v))
phex = lambda v: log.info("%#lx" % v)

b2i = lambda b: int.from_bytes(b, 'little')

r   = lambda *a, **k: p.recv(*a, **k)
rl  = lambda *a, **k: p.recvline(*a, **k)
ru  = lambda *a, **k: p.recvuntil(*a, **k)
s   = lambda *a, **k: p.send(*a, **k)
sl  = lambda *a, **k: p.sendline(*a, **k)
sla = lambda *a, **k: p.sendlineafter(*a, **k)
sm  = lambda *a, **k: (ru(MENU_PROMPT), s(*a, **k))
slm = lambda *a, **k: (ru(MENU_PROMPT), sl(*a, **k))

REMOTESTR = " " # e.g. "nc hostname 1337"
REMOTESEP = " "
HOST, PORT = REMOTESTR.split(REMOTESEP)[-2:]

MENU_PROMPT = b"> "

################################################################################

#elf.got['puts'] elf.sym['main']

#shellcode = asm(""" """)
#shellcode = asm(shellcraft.sh())

#alphabet = string.ascii_lowercase
#payload = cyclic(256, alphabet=alphabet)
#offset = cyclic_find(b"", alphabet=alphabet)

#lleak = px.lib_leak(out, idx=0, pid=p.pid)
#bleaks, hleaks, lleaks, sleaks = px.all_leaks(out, pid=p.pid)

#rop_chain = []
#rop_chain = b''.join(map(p64, rop_chain))

gdbscript = """

"""

p = proc({proc_args})

p.interactive()
