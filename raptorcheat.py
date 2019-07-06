#!/usr/bin/python3
#	raptor-cheat - Cheat program for Raptor: Call of the Shadows
#	Copyright (C) 2019-2019 Johannes Bauer
#
#	This file is part of raptor-cheat.
#
#	raptor-cheat is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	raptor-cheat is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with raptor-cheat; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import shutil
import struct
from FriendlyArgumentParser import FriendlyArgumentParser
from RaptorCrypto import RaptorCrypto

parser = FriendlyArgumentParser()
parser.add_argument("savegame", metavar = "savegame", type = str, help = "Savegame file to edit.")
args = parser.parse_args(sys.argv[1:])

with open(args.savegame, "rb") as f:
	original_savegame = f.read()

savegame = bytearray(RaptorCrypto.decrypt(original_savegame))
#with open("decrypted.bin", "wb") as f:
#	f.write(savegame)

# Set money to a bunch
money_offset = 0x24
patch = struct.pack("<L", 100000000)
for (offset, value) in enumerate(patch, money_offset):
	savegame[offset] = value

# Create a copy
with open(args.savegame + ".bak", "wb") as f:
	f.write(original_savegame)

# Overwrite savegame
with open(args.savegame, "wb") as f:
	f.write(RaptorCrypto.encrypt(savegame))

