#!/usr/bin/env python3

from pwn import *

{bindings}

context.binary = {bin_name}

context.arch = "amd64"
context.encoding = 'latin-1'

MENU_PROMPT = b"> "

HOST=""
PORT=1337
class proc(object):
    def __init__(self, **kwargs):
        if args.REMOTE:
            self.__class__ = type('proc', (self.__class__, remote), dict())
            remote.__init__(self, HOST, PORT, **kwargs)
        else:
            self.__class__ = type('proc', (self.__class__, process), dict())
            process.__init__(self,{proc_args}, **kwargs)
            if args.DEBUG:
                gdb.attach(self.p)
    def r(self, length: int):
        return self.recv(length)
    def rl(self): # recvline
        return self.recvline(keepends=False)
    def ru(self, until: bytes): # recvuntil
        return self.recvuntil(until)
    def s(self, data: bytes): # send
        self.sendline(data)
    def sl(self, data: bytes): # sendline
        self.sendline(data)
    def sa(self, after: bytes, data: bytes): # sendlineafter
        self.ru(after)
        self.s(data)
    def sla(self, after: bytes, data: bytes): # sendlineafter
        self.sendlineafter(after, data)
    def slm(self, data: bytes): # sendlineafter for menu
        self.sendlineafter(MENU_PROMPT, data)
    def sm(self, data: bytes): # sendafter for menu
        self.ru(MENU_PROMPT)
        self.send(data)
    def gdb(self):
        gdb.attach(self)
    @staticmethod
    def embed():
        import IPython; IPython.embed(colors="neutral")

########################################################
# pwn below the line ^

#shellcode = asm(""" """)

#rop_chain = []
#rop_chain = b''.join([ p64(r) for r in rop_chain ])

p = proc()

p.interactive()
