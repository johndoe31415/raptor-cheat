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

class RaptorCrypto():
	_KEYBYTE_OFFSETS = [ 0xad, 0xac, 0xb4, 0xbb, 0xbd, 0xbf ]

	@classmethod
	def generate_keystream(cls, length):
		value = 0x82
		index = 0
		for i in range(length):
			yield value
			value = (value - cls._KEYBYTE_OFFSETS[index]) & 0xff
			index += 1
			if index == len(cls._KEYBYTE_OFFSETS):
				index = 0

	@classmethod
	def encrypt(cls, plaintext):
		ciphertext = bytearray()
		offset = 0
		for (plainbyte, streambyte) in zip(plaintext, cls.generate_keystream(len(plaintext))):
			cipherbyte = plainbyte + streambyte + offset
			offset += plainbyte
			ciphertext.append(cipherbyte & 0xff)
		return bytes(ciphertext)

	@classmethod
	def decrypt(cls, ciphertext):
		plaintext = bytearray()
		offset = 0
		for (cipherbyte, streambyte) in zip(ciphertext, cls.generate_keystream(len(ciphertext))):
			plainbyte = cipherbyte - streambyte - offset
			offset += plainbyte
			plaintext.append(plainbyte & 0xff)
		return bytes(plaintext)


if __name__ == "__main__":
	assert(bytes(RaptorCrypto.generate_keystream(16)) == bytes.fromhex("82 d5 29 75 ba fd 3e 91 e5 31 76 b9 fa 4d a1 ed"))

	ciphertext = bytes.fromhex("c3 65 01 8e 21 b2 38 de  32 7e c3 06 47 9a ee 3a")
	plaintext = b"AOHANNES\x00\x00\x00\x00\x00\x00\x00\x00"
	assert(RaptorCrypto.decrypt(ciphertext) == plaintext)
	assert(RaptorCrypto.encrypt(plaintext) == ciphertext)
