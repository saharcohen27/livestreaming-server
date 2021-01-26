# from DataBase import Database
# print(Database().get_username_by_streamkey("cb1bbf7d-2e40-49fa-affe-55987f10bf13"))
# print(len("cb1bbf7d-2e40-49fa-affe-55987f10bf13"))
# from AMF0 import AMFBody
# AMFBody().encode_number(52)

import struct
x = struct.pack("i", 452)
x = x[::-1]
print(x)

# x = """ad 01 21 1a 8e ef ff ff fe 00 e5 6a 67 a3 c8 40 7a
# f6 de 80 00 00 02 a9 41 c0 39 e3 22 e1 3d 0a cd
# 33 88 b1 3d f7 67 b8 a6 c4 dd dd 54 63 c0 15 d6
# a7 a5 b3 cd e2 2d b7 dd ab 21 da 74 8d d7 5b 4d
# d5 37 7c 98 19 4d 43 2a c2 3b 44 f0 d3 69 aa dc
# a5 4b d5 dc 23 4b 01 ab df 62 44 d6 14 f2 22 bd
# 16 67 c6 9a 87 b2 0b 7b bc a5 81 7a 98 5e 21 7c
# 2f 36 37 9f f7 82 bc 44 f6 9b f8 a5 1c e4 19 fc
# 2a 0d d3 38 ab d5 88 c9 70 e6 73 ae a8 0a 4a f4
# ae 21 e3 3a 36 32 57 cc 96 d2 db a7 91 10 6a 0e
# 23 9a f8 d3 41 0a 06 f8 07 2e 12 15 7d 9d 38 0f
# d0 72 29 30 34 ed 85 ed 29 61 fa 70 1a ea cf e4
# 8d ed b8 64 71 52 aa a5 f2 4c e5 5d f4 87 78 f4
# 6e a7 5c cc 63 f1 54 94 85 2b d5 4e 07 2a 5b 3d
# 11 e8 00 de 80 00 00 05 e2 b0 03 32 4c f8 d9 1a
# 88 23 bf bb 0a 16 03 a3 ae f3 e8 4e a6 66 62 b6
# 73 7a df 8b 4f d3 59 5e bd e9 9f cd 40 2a a2 a8
# 3a 38 ed 6b f1 e8 97 50 a6 a0 d7 bb dc af 3d db
# 69 92 d8 05 39 45 12 80 91 8d ae 12 80 8e 76 b5
# 40 68 89 6a c8 30 3b 20 c1 a8 3c 14 cc 7d 12 97
# ba 3a 1c c1 f8 e7 95 a3 4b 68 51 e5 15 db 06 7d
# f8 ec ec 06 4d cb c3 28 81 8d 01 0d 88 44 78 52
# 71 19 da df d8 13 39 3e e0 db 18 d0 33 8f 19 1b
# bb 3e 71 79 57 26 e0"""
# c = 0
# for i in x:
#     if i.isdigit() or i.isalpha():
#         c += 1
# print(c/2)