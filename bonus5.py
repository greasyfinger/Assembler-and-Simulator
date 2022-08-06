from audioop import add
import math
meminp = input("Enter size of memory:")
adtyp = int(input(
'''
1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)
'''
))
adtyp = 2**adtyp
adtyp = 1 if adtyp == 2 else adtyp 
adtyp = 0 if adtyp == 16 else adtyp
cpu = 0
size = {'b':1,'nibble':4,'B':8,'word':cpu,'G':2**30,'K':2**10,'M':2**30}
def convert(meminp):
    ans = 0
    bb = meminp[-1]
    bb = 8 if bb=='B' else 1
    meminp = meminp[:-1:]
    bruh = 1
    if meminp[-1].isalpha():
        bruh = size[meminp[-1].upper()]
        meminp = meminp[:-1:]
    meminp = int(meminp)*bruh*bb
    return meminp
#query 1
meminp = convert(meminp)
typeA = int(input("Enter size of 1 instruction:"))
register = int(input("Enter size of register:"))
address = int(math.log(meminp,2))
opcode = int(typeA-(address+register))
filler = typeA - opcode - 2*(register)
print(address,'bits are required to represent an address')
print(opcode,'bits needed by opcode')
print(filler,'bits are filler in type B')
print(2**opcode,'instructions can be supported')
print(2**register,'registers can be supported')

# type 1
cpu = int(input("cpu bits:"))
bdtyp = int(input(
'''
1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)
'''
))
bdtyp = 2**bdtyp
bdtyp = 1 if bdtyp == 2 else bdtyp 
bdtyp = cpu if adtyp == 16 else bdtyp
ans = math.log(meminp,2)/math.log(adtyp,2) - math.log(meminp,2)/math.log(bdtyp,2)
print(int(ans),'pins')

#type 3
cpu = int(input("cpu bits:"))
addr = int(input("address pins:"))
cdtyp = int(input(
'''
1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)
'''
))
ans = math.log((2**addr)/(8*cdtyp),2)
print(ans,'B')