## Assembler Simulator

Designed a simple Assembler Simulator in python that can comprehend assembly based on 
a simple ISA and process the instruction.


### Co-Authors
- [@Nalin Arora](https://github.com/Nalin21478)
- [@Mehak Gopal](https://github.com/MehakGopa)


### ISA Description: 

The pdf in This repostiory contains the detailed ISA on which the project
was built.
### Bonus

Command line program to solve questions related to memory organization.
It takes in memory available and how based on how memory is addressed
gives a breakdown instruction memory composition.

Input: 
1. The space in memory (eg 16 MB) Make sure you recognize inputs in this very format Mb should be read as mega bits and MB as mega byte. 
2. Then input how the memory is addressed as mentioned above (either of the four options) QUERIES: Now you have to do processing on these types of queries: ● The first type of question is ISA and Instructions related: 

    Type A: <Q bit opcode> <P-bit address> <7 bit register> 

    Type B: <Q bit opcode> <R bits filler> <7 bit register> <7 bit register> Here, input the following: 

And output the following: 

1. How many minimum bits are needed to represent an address in this 
architecture 

2. Number of bits needed by opcode 

3. Number of filler bits in Instruction type 2 
4. Maximum numbers of instructions this ISA can support 
5. Maximum number of registers this ISA can support
6.  The second type of question is System enhancement related 
