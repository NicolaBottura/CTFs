#!/usr/bin/python3

from pwn import *
from ctypes import *

libc = CDLL("libc.so.6")
libc.srand(libc.time(0))

dictionary = b'abcdefghijklmnopqrstuvwxyz'

#target = process('./challs')
target = remote("gamebox3.reply.it", 2692)

def gen_passwd(n):
	password = b""
	for i in range(n):
		password += dictionary[libc.rand() % 26].to_bytes(1, "little")
	return password


target.recvuntil(b"Passwd:")
target.sendline(b"secret_passwd_anti_bad_guys")
target.recvuntil(b">")
target.sendline(b"Admin")

for i in range(5 * 11):
	libc.rand()

password = gen_passwd(30)

target.sendline(password)
target.interactive()
