#general functions and registers
import sys
def bin_dec(k):  #binary to decimal
    n = int(k)
    num = ''
    while n != 0:
        num += str(n % 2)
        n = n // 2
    return num[::-1]


def reg_read(reg):  #reads register
    if reg == "FLAGS":
        return "111"
    rins = bin_dec(reg[1])
    return '0' * (3 - len(rins)) + rins


def check(l, i, list):
    l = l + ":"
    for j in (0, i - 1, 1):
        if l in list[j][0]:
            return True
        else:
            return False


def check_var(l, i, list):
    for j in (0, i - 1, 1):
        if l in list[j][1]:
            return True
        else:
            return False


def dgtchk(n):  #checks for negative as well
    try:
        int(n)
        return int(n)==float(n)
    except ValueError:
        return False


#all lists and dictionaries
A = {
    'add': '10000',
    'sub': '10001',
    'mul': '10110',
    'EXOR': '11010',
    'AND': '11100',
    'OR': '11011'
}
B = {
    'mov': '10010',
    'ls': '11001',
    'rs': '11000',
}
C = {'mov': '10011', 'div': '10111', 'not': '11101', 'cmp': '11110'}
D = {'ld': '10100', 'st': '10101'}
E = {'jlt': '11111', 'jmp': '01100', 'jgt': '01101', 'je': '01111'}
F = {'hlt': '01010'}
lbl = {}
vars = {}
instructions = [
    "add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or",
    "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt", "var"
]
registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]
out = []


#labels and variables
def varchk(varr):
    if varr in vars or varr in lbl:
        return True
    return False


def lblstr(label, cntr):
    rins = bin_dec(str(cntr))
    lbl[label] = '0' * (8 - len(rins)) + rins


#actual intructions
def Atype(inst, i):
    y = reg_read(inst[i][1])
    z = reg_read(inst[i][2])
    x = reg_read(inst[i][3])
    opc = A[inst[i][0]]
    out.append(opc + '0' * 2 + y + z + x)


def Btype(inst, i):
    x = reg_read(inst[i][1])
    imm = bin_dec(inst[i][2][1::])
    opc = B[inst[i][0]]
    out.append(opc + x + '0' * (8 - len(imm)) + imm)


def Ctype(inst, i):
    z = reg_read(inst[i][1])
    if inst[i][2] == "FLAGS":
        x = "111"
    else:
        x = reg_read(inst[i][2])
    opc = C[inst[i][0]]
    out.append(opc + '0' * 5 + z + x)


def Dtype(inst, i):
    opc = D[inst[i][0]]
    y = reg_read(inst[i][1])
    if inst[i][2] in vars: addr = vars[inst[i][2]]
    elif inst[i][2] in lbl: addr = lbl[inst[i][2]]
    out.append(opc + y + addr)


def Etype(inst, i):
    opc = E[inst[i][0]]
    if inst[i][1] in vars: addr = vars[inst[i][1]]
    elif inst[i][1] in lbl: addr = lbl[inst[i][1]]
    out.append(opc + '0' * 3 + addr)


def Ftype(inst, i):
    opc = F[inst[i][0]]
    out.append(opc + "0" * 11)


#errors
i = 0
Errors = [
    "ERROR! TYPOS IN INSTRUCTION NAME", "ERROR! TYPOS IN REGISTERS",
    "Error!General Syntax error", "Error! Illegal immediate values",
    "Error! Misuse of labels as variables", "Error! Undefined Variables",
    "Misuse of variables as labels", "Error! Undefined Label",
    "Error!Variable not defined at the start", "ERROR!MISSING HLT STATEMENT",
    "ERROR!HLT STATEMENT IN THE MIDDLE", "Illegal Variable name","Illegal label name"
]
# with open('test.txt', 'r') as test:
#     inptmp = [i.split() for i in test.readlines()]
inptmp=[i.split() for i in sys.stdin.readlines()]
# asycd = "" 
# for inptmp in sys.stdin:
#     if asycd == "":
#         break
inp = []
for i in inptmp:
  try:
    if i != []:
        if i[0] == 'var':
            if len(inp) != 0 and inp[-1][0] != 'var':
                print(Errors[8])
                quit()
            if i[1].isidentifier() and i[1] not in instructions and i[1] not in registers:
                vars[i[1]] = 'NULL'
            else:
                print(inptmp.index(i), end=':')
                print(Errors[11])
                quit()
        elif i[0][-1] == ':':
            lbn=i[0][:-1:]
            if lbn.isidentifier() and lbn not in instructions and lbn not in registers:
              lblstr(i[0][:-1], len(inp) + 1)
              inp.append(i[1::])
              inptmp[inptmp.index(i)]=i[1::]
            else:
                print(inptmp.index(i), end=':')
                print(Errors[12])
                quit()
        else:
            inp.append(i)
  except:
    print(Errors[2])
    quit()
if len(inp)>256 or len(vars)>256:
    print(Errors[2])
    quit()
nv = 0  #number of variables
for v in vars:
    rins = bin_dec(str(len(inp) + nv))
    vars[v] = '0' * (8 - len(rins)) + rins
    nv += 1
try:
    if inp[-1][0] != "hlt":
        out.append(Errors[9])
except IndexError:
    print('No file input')
    quit()
for i in range(len(inp)):
    try:
        if inp[i][0] == "hlt" and i != len(inp) - 1:
            out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[10])
            break
        elif inp[i][0] not in instructions:
            out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[0])
            break
        elif inp[i][0] in A:
            if inp[i][1] not in registers or inp[i][2] not in registers or inp[
                    i][3] not in registers:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                break
        elif inp[i][0] == "mov":
            if inp[i][1] not in registers and inp[i][1]!='FLAGS':
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                break
            elif inp[i][1] not in registers or inp[i][2] not in registers:
                if inp[i][1] == "FLAGS" and inp[i][2] in registers: pass
                elif inp[i][2][0] in '!@#$%^&*-+=':
                    if inp[i][1] == "FLAGS":
                        out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                    elif dgtchk(inp[i][2][1::]) and inp[i][2][0] == '$':
                        if int(inp[i][2][1::]) < 0 or int(
                                inp[i][2][1::]) > 255:
                            out.append(
                                str(inptmp.index(inp[i]) + 1) + ':' +
                                Errors[3])
                            break
                    else:
                        out.append(
                            str(inptmp.index(inp[i]) + 1) + ':' + Errors[3])
                        break
                else:
                    out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                    break
        elif inp[i][0] in B:
            if inp[i][1] not in registers:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                break
            if inp[i][2][0] != "$":
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[2])
                break
            if int(inp[i][2][1::]) < 0 or int(inp[i][2][1::]) > 255:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[3])
                break
        elif inp[i][0] in C:
            if inp[i][1] not in registers or inp[i][2] not in registers:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                break
            if inp[i][1] not in registers:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[1])
                break
        elif inp[i][0] in D:
            if varchk(inp[i][2]) == False:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[5])
                break
            if inp[i][2] not in vars:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[4])
                break
        elif inp[i][0] in E:
            if inp[i][1] in vars:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[6])
                break
            elif inp[i][1] not in lbl:
                out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[7])
                break
        #elif inp[i][-1] != "hlt":
        #out.append(str(i+1+nv)+':'+Errors[9])
        if inp[i][0] in A:
            Atype(inp, i)
        elif inp[i][0] == "mov":
            if inp[i][1] in registers and inp[i][
                    2] not in registers and inp[i][2] != "FLAGS":
                Btype(inp, i)
            elif (inp[i][1]
                  and inp[i][2] in registers) or (inp[i][1] in registers
                                                  and inp[i][2] == "FLAGS"):
                Ctype(inp, i)
        elif inp[i][0] in B:
            Btype(inp, i)
        elif inp[i][0] in C:
            Ctype(inp, i)
        elif inp[i][0] in D:
            Dtype(inp, i)
        elif inp[i][0] in E:
            Etype(inp, i)
        elif inp[i][0] in F:
            Ftype(inp, i)
    except:
        out.append(str(inptmp.index(inp[i]) + 1) + ':' + Errors[2])
        break
for i in out:
    if i[-1] != '0' and i[-1] != '1':
        print(i)
        exit()
for i in out:
    print(i)