"""rdg{%s}"""

import sys
import os
import struct
import hashlib

if os.name != 'nt':
	print("[ERR] Only Windows")
	exit(-1)

if sys.version.startswith('3.9'):
	import magic
else:
	print("[ERR] Only python 3.9")
	exit(-1)

flag = None
serial = None
while True:
	inp = bytes.fromhex(input("Serial number in hex: "))
	if len(inp) % 4 != 0:
		print("[ERR] Need len(Serial number) % 4 == 0x0")
	else:
		serial = struct.unpack("I"*(len(inp)//4), inp)
		break

ins = [0xd2ff820b, 0x37339d0a, 0x373f2dcf, 0xd539fdd6, 0x15bcf78b, 0x3726c467, 0x37694359, 0xd23652c1, 0x15f9585a, 0x153df12f, 0x15fd2ae5, 0x23c1bbf9, 0x150edcfb, 0x376621d7, 0x220d4767, 0x2314d933, 0x230b8111, 0xd35fc81e, 0x138dfa5b, 0x12e3622b, 0x37886c57, 0x3737bdbe, 0xd2142d76, 0x37230e39, 0x1361d5d8, 0x37de6079, 0x22085d4d, 0xd5050afb, 0x373d5935, 0x37b34ed7, 0x2553d571, 0x120359ea, 0x2587fc6c, 0xd256177a, 0x13c75429, 0x259ff74e, 0xd2fe6926, 0x1272e06c, 0x378858c7, 0x23ef48a0, 0xd230103a, 0x121068c5, 0x37919294, 0x22ef7b6a, 0x23a4c5ee, 0x375bda25, 0x1211453a, 0x237158ec, 0x1578a82a, 0xDEADDEAD]
if len(serial) != len(ins):
	print("[ERR] Need len(serial) == len(ins)")
	exit(-1)

magic.Spell()
for idx, i in enumerate(serial):
	flag = (i == ins[idx])
	if not flag:
		print("[-] Wrong input")
		exit(-1)
magic.Dispell()

if flag and type(flag) == bytes:
	SHA256_flag = hashlib.sha256(flag).digest().hex() 
	if SHA256_flag == '5d6ba0158ffafc93ac2e4053151e47c0694e83677c444f6793749a591b12d3d1':
		print(__doc__ % flag.decode())
	else:
		print("[-] Hash mismatch")
