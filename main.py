def bin_dec(k): #converts decimal to binary
  n=int(k)
  num=''
  while n!=0:
    num+=str(n%2)
    n=n//2
  return num[::-1]
def reg_read(reg): #returns 
  rins=bin_dec(reg[1])
  return '0'*(3-len(rins))+rins
A={'add':'10000','sub':'10001','mul':'10110','EXOR':'11010','AND':'11100','OR':'11011'}
B={'mov':'10010','ls':'11001','rs':'11000',}
C={'mov':'10011','div':'10111','not':'11101','cmp':'11110'}
D={'ld':'10100','st':'10101'}
E={'jlt':'11111','jmp':'01100','jgt':'01101','je':'01111'}
F={'hlt':'01010'}
lbl={}
instructions=["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
registers=["R0","R1","R2","R3","R4","R5","R6"]
def Atype(inst,i):
    y=reg_read(inst[i][1])
    z=reg_read(inst[i][2])
    x=reg_read(inst[i][3])
    opc=A[inst[i][0]]
    print(opc+'0'*2+y+z+x)
def Btype(inst,i):
    x=reg_read(inst[i][1])
    imm=bin_dec(inst[i][2][1::])
    opc=B[inst[i][0]]
    print(opc+x+'0'*(8-len(imm))+imm)
def Ctype(inst,i):
    z=reg_read(inst[i][1])
    x=reg_read(inst[i][2])
    opc=C[inst[i][0]]
    print(opc+'0'*5+z+x)
#read standard input
inp=[]
i=0
print("enter the instructions")
while(True):
  inp.append(input().split())