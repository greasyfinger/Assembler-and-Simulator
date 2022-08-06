import matplotlib.pyplot as plt
cycle = 1
x_coord = []
y_coord = []
R0 = '0' * 16
R1 = '0' * 16
R2 = '0' * 16
R3 = '0' * 16
R4 = '0' * 16
R5 = '0' * 16
R6 = '0' * 16
FLAGS = '0' * 16
reglist = [R0, R1, R2, R3, R4, R5, R6, FLAGS, '\n']
#simulator components
PC = '00000000'
cycle = 0


def RegisterFile(RF):
    try:
        return reglist[RF[1]]
    except:
        return reglist[7]


def regconv(reg):
    if reg == '000':
        return 0
    elif reg == '001':
        return 1
    elif reg == '010':
        return 2
    elif reg == "011":
        return 3
    elif reg == "100":
        return 4
    elif reg == "101":
        return 5
    elif reg == "110":
        return 6
    elif reg == "111":
        return 7


def dec_bin(k):  #decimal to binary
    n = int(k)
    num = ''
    while n != 0:
        num += str(n % 2)
        n = n // 2
    return num[::-1]


def bin_dec(n):  #binary to decimal
    n = str(n)
    b = list(n[::-1])
    num = 0
    for i in range(len(b)):
        num += int(b[i]) * (2**i)
    return num


def proc(inst):
    val = dec_bin(inst)
    otpt = "0" * (8 - len(val)) + val
    print(otpt, end=' ')
    global PC
    PC = otpt


def divide(a, b):
    val1 = dec_bin(bin_dec(reglist[a]) / bin_dec(reglist[b]))
    val2 = dec_bin(bin_dec(reglist[a]) % bin_dec(reglist[b]))
    reglist[0]= '0' * (16 - len(val1)) + val1
    reglist[1] = '0' * (16 - len(val2)) + val2
    reglist[7] = '0'*16


def mul(a, b, c):
    val = dec_bin(bin_dec(reglist[a]) * bin_dec(reglist[b]))
    reglist[c] = '0' * (16 - len(val)) + val
    lena = len(dec_bin(bin_dec(reglist[a])))
    lenb = len(dec_bin(bin_dec(reglist[b])))
    reglist[7] = '0'*16
    if len(val) > 16:
        reglist[7] = reglist[7][:12] + '1' + reglist[7][13:]


def rs(a, b):
    #a is the value of the register and b is immediate
    val = dec_bin(int(bin_dec(reglist[a]))>>int(bin_dec(b)))
    reglist[a] = '0' * (16 - len(val)) + val
    reglist[7] = '0'*16


def ls(a, b):
    val = dec_bin(int(bin_dec(reglist[a]))>>int(bin_dec(b)))
    reglist[a] = val + '0' * (16 - len(val))
    reglist[7] = '0'*16


def add(a, b, c):
    val = dec_bin(bin_dec(reglist[a]) + bin_dec(reglist[b]))
    reglist[c] = '0' * (16 - len(val)) + val
    reglist[7] = '0'*16
    if len(val) > 16:
        reglist[7] = reglist[7][:12] + '1' + reglist[7][13:]
        return
        #reglist[c] = '0'*16


def sub(a, b, c):
    if bin_dec(reglist[b]) > bin_dec(reglist[a]):
        reglist[7] = '0'*16
        reglist[7] = reglist[7][:12] + '1' + reglist[7][13:]
        reglist[c] = '0' * 16
    else:
        val = dec_bin(bin_dec(reglist[a]) - bin_dec(reglist[b]))
        reglist[c] = '0' * (16 - len(val)) + val
        reglist[7] = '0'*16


def movimm(reg, imm):
    reglist[reg] = (16 - len(imm)) * '0' + imm
    reglist[7] = '0'*16
    return reg
def movreg(reg1, reg2):
    reglist[reg2] = reglist[reg1]
    reglist[7] = '0'*16


def XOR(reg1, reg2, reg3):
    val = ''
    for i in range(16):
        if (reglist[reg1][i] == reglist[reg2][i]): val += '0'
        else: val += '1'
    reglist[reg3] = val
    reglist[7] = '0'*16


def OR(reg1, reg2, reg3):
    l1 = (reglist[reg1])
    l2 = (reglist[reg2])
    l3 = ''
    for i in range(16):
        l3 += (l1[i] or l2[i])
    reglist[reg3] = l3
    reglist[7] = '0'*16
    #val = dec_bin(bin_dec(reglist[reg1]) | bin_dec(reglist[reg2]))
    #reglist[reg3] = '0' * (16 - len(val)) + val


def AND(reg1, reg2, reg3):
    l1 = (reglist[reg1])
    l2 = (reglist[reg2])
    l3 = ''
    for i in range(16):
        l3 += (l1[i] and l2[i])
    reglist[reg3] = l3
    reglist[7] = '0'*16
    #val = dec_bin(bin_dec(reglist[reg1]) & bin_dec(reglist[reg2]))
    #reglist[reg3] = '0' * (16 - len(val)) + val


def NOT(reg1, reg2):
    reglist[reg2] = ''
    for i in range(len(reglist[reg1])):
        if reglist[reg1][i] == '0': reglist[reg2] += '1'
        else: reglist[reg2] += '0'
    reglist[7] = '0'*16


def cmp(reg1, reg2):
    reglist[7] = '0'*16
    if bin_dec(reglist[reg1]) < bin_dec(reglist[reg2]):
        reglist[7] = reglist[7][:13] + '1' + reglist[7][14:]
    elif bin_dec(reglist[reg1]) > bin_dec(reglist[reg2]):
        reglist[7] = reglist[7][:14] + '1' + reglist[7][15]
    elif bin_dec(reglist[reg1]) == bin_dec(reglist[reg2]):
        reglist[7] = reglist[7][:15] + '1'


def st(reg1, mem_addr):
    global cycle
    y_coord.append(bin_dec(mem_addr))
    x_coord.append(cycle)
    inp[bin_dec(mem_addr)][0] = reglist[reg1]
    reglist[7] = '0'*16


def ld(reg1, mem_addr):
    global cycle
    y_coord.append(bin_dec(mem_addr))
    x_coord.append(cycle)
    reglist[reg1] = inp[bin_dec(mem_addr)][0]
    reglist[7] = '0'*16

def uncdjmp(mem_addr):
    val = bin_dec(mem_addr)
    reglist[7] = '0'*16
    return val


def lesjmp(mem_addr, i):
    if (reglist[7][13] == '1'):
        val = bin_dec(mem_addr)
        reglist[7] = '0'*16
        return val
    reglist[7] = '0'*16
    return i + 1


def grtjmp(mem_addr, i):
    if (reglist[7][14] == '1'):
        val = bin_dec(mem_addr)
        reglist[7] = '0'*16
        return val
    reglist[7] = '0'*16
    return i + 1


def eqjmp(mem_addr, i):
    if (reglist[7][15] == '1'):
        val = bin_dec(mem_addr)
        reglist[7] = '0'*16
        return val
    reglist[7] = '0'*16
    return i + 1


#decimal to float
#should ideally be between 0 and 31 the number because if it's 32 than it's exponent is 8 which is 4 bit number so error
def fl(a, y):
    k = float(a)
    num = ''
    i = 0
    while i <= int(y):
        k *= 2
        b = str(k)
        m, n = b.split('.')
        if (i == int(y)):
            num = num[:-1:] + m if num[-1] != '1' else num
        else:
            num += m
            k = float('.' + n)
        i += 1

    return '.' + num


def ex(a):
    k = int(a)
    return dec_bin(str(k))


def dec_float(a):
    if float(a) > 63 or float(a) < 0:
        print("Error")
        return
    if float(a) == 0:
        exp = 3 * '0'
        mant = 5 * '0'
    elif int(float(a)) == float(a):  #checks if number has no decimal point
        a = dec_bin(str(int(float(a))))
        exp = ex(str(len(str(a)) - 1))
        mant = a[1::] + '0' * (5 - (len(a) - 1))
    else:
        #two strings,m = non decimal n = decimal point
        m, n = str(a).split('.')
        m = dec_bin(m)  #convert m to decimal
        n = fl('.' + n, 6 - len(m))  #convert decimal part to binary
        exp = '0' * (3 - len(ex(str(len(m) - 1)))) + ex(str(len(m) - 1))
        fin = m + n  #final binary number
        fin2 = fin[1::]  #mantissa with decimal point
        fin2 = fin2.replace('.', '')  #mantissa
        mant = fin2 + '0' * (5 - len(fin2))
    return exp + mant

def fl_dec(n):
    n = list(n[::])
    num = 0
    for i in range(len(n)):
        num += int(n[i]) * 1 / (2**(i + 1))
    return num


def float_dec(a):
    if a == '0' * 8:
        return 0
    else:
        exp = (bin_dec(a[:3:]))
        mant = a[3::]
        num = '1.' + mant
        num = num[0] + num[2:exp + 2:] + '.' + num[exp + 2::]
        m, n = num.split('.')
        m = bin_dec(m)
        n = fl_dec(n)
        return n + m


def hlt(inp, rlen):
    for i in range(0, 256):
        try:
            if rlen == i:
                AssertionError
            print(inp[i][0])
        except:
            print('0' * 16)

def addf(a,b,c):
    reglist[7] = '0'*16
    val = float(float_dec(reglist[b][-8::])) + float(float_dec(reglist[c][-8::]))
    if str(val) != float_dec(dec_float(str(val))):
        reglist[7] = reglist[7][:12] + '1' + reglist[7][13:]
    reglist[a] = reglist[a][:8:]+dec_float(str(val))

def subf(a,b,c):
    reglist[7] = '0'*16
    val = float(float_dec(reglist[b][-8::])) - float(float_dec(reglist[c][-8::]))
    if str(val) != float_dec(dec_float(str(val))):
        reglist[7] = reglist[7][:12] + '1' + reglist[7][13:]
    reglist[a] = reglist[a][:8:]+dec_float(str(val))
    
def movimmf(reg, imm):
    reglist[7] = '0'*16
    reglist[reg] = reglist[reg][:8:]+ imm

import sys

inpu = [i.strip().split() for i in sys.stdin.readlines()]
inp = []
for i in range(0,256):
    try:
        if inpu[i] != []:
            inp.append(inpu[i])
    except:
        inp.append(['0'*16])
rlen = len(inp)
out = []
for pc in range(0, len(inp)):
    bpc = str(bin(pc))
    out.append(['0' * (8 - len(bpc)) + bpc])
i = 0
while (i < rlen):
    x_coord.append(cycle)
    y_coord.append(int(i))
    if (inp[i][0][0:5]) == '10000':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = add((x), (y), (z))
    elif (inp[i][0][0:5]) == '10001':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = sub((x), (y), (z))
    elif (inp[i][0][0:5]) == '10110':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = mul((x), (y), (z))
    elif (inp[i][0][0:5]) == '11010':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = XOR((x), (y), (z))
    elif (inp[i][0][0:5]) == '11011':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = OR((x), (y), (z))
    elif (inp[i][0][0:5]) == '11100':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = AND((x), (y), (z))
    elif (inp[i][0][0:5]) == '10010':
        y = (inp[i][0][8:16])
        z = regconv(inp[i][0][5:8])
        z = movimm(z, y)
    elif (inp[i][0][0:5]) == '11000':
        z = regconv(inp[i][0][5:8])
        y = inp[i][0][8:16]
        z = rs(z, y)
    elif (inp[i][0][0:5]) == '11001':
        z = regconv(inp[i][0][5:8])
        y = (inp[i][0][8:16])
        z = ls(z, y)
    elif (inp[i][0][0:5]) == '10011':
        y = regconv((inp[i][0][10:13]))
        z = regconv((inp[i][0][13:16]))
        z = movreg(y, z)
    elif (inp[i][0][0:5]) == '10111':
        y = regconv((inp[i][0][10:13]))
        z = regconv((inp[i][0][13:16]))
        z = divide(y, z)
    elif (inp[i][0][0:5]) == '11101':
        y = regconv((inp[i][0][10:13]))
        z = regconv((inp[i][0][13:16]))
        z = NOT(y, z)
    elif (inp[i][0][0:5]) == '11110':
        y = regconv((inp[i][0][10:13]))
        z = regconv((inp[i][0][13:16]))
        cmp(y, z)
    elif (inp[i][0][0:5]) == '10100':
        y = regconv((inp[i][0][5:8]))
        z = inp[i][0][8:]
        ld(y, z)
    elif (inp[i][0][0:5]) == '10101':
        y = regconv((inp[i][0][5:8]))
        z = inp[i][0][8:]
        st(y, z)
    elif (inp[i][0][0:5]) == '00000':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = addf((x), (y), (z))
    elif (inp[i][0][0:5]) == '00001':
        x = regconv(inp[i][0][7:10])
        y = regconv(inp[i][0][10:13])
        z = regconv(inp[i][0][13:16])
        z = subf((x), (y), (z))
    elif (inp[i][0][0:5]) == '00010':
        y = (inp[i][0][8:16])
        z = regconv(inp[i][0][5:8])
        z = movimmf(z, y)
    proc(i)
    if (inp[i][0][0:5]) == '11111':
        i = int(uncdjmp(inp[i][0][8:])) - 1
    elif (inp[i][0][0:5]) == '01100':
        i = int(lesjmp(inp[i][0][8:], i)) - 1
        mem = inp[i][0][8:]
    elif (inp[i][0][0:5]) == '01101':
        i = int(grtjmp(inp[i][0][8:], i)) - 1
        mem = inp[i][0][8:]
    elif (inp[i][0][0:5]) == '01111':
        i = int(eqjmp(inp[i][0][8:], i)) - 1
        mem = inp[i][0][8:]
    elif ((inp[i][0][0:5]) == '01010'):
        reglist[7] = '0'*16  
    for j in reglist:
        if j != '\n':
            print(j, end=' ')
        else:
            print()
    if ((inp[i][0][0:5]) == '01010'):
        hlt(inp, rlen)
        break
    i += 1
    cycle +=1

plt.scatter(x_coord, y_coord, c='blue')
plt.title("Memory access vs cycles")
plt.xlabel("Cycle Number")
plt.ylabel("Memory address(line no.)")
plt.show()