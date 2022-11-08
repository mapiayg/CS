# CISCA

import random

HexChar = "0123456789ABCDEF"

HexDic = {
    '0':'0000','1':'0001','2':'0010','3':'0011',
    '4':'0100','5':'0101','6':'0110','7':'0111',
    '8':'1000','9':'1001','A':'1010','B':'1011',
    'C':'1100','D':'1101','E':'1110','F':'1111',
}

Flags = {
    'Z':'0','S':'0','C':'0','V':'0',    
}

Cout = '0'

def SetFlags(A, B, res, c = 'x', v = 'x'):
    if Bin32ToDec(res) < 0:
        Flags['S'] = '1'
    else:
        Flags['S'] = '0'
    
    if Bin32ToDec(res) == 0:
        Flags['Z'] = '1'
    else:
        Flags['Z'] = '0'
    
    if c == 'x':
        Flags['C'] = Cout
    elif c != '-':
            Flags['C'] = c
        
    if v == 'x':
        if A[0] == B[0] and res[0] != A[0]:
            Flags['V'] = '1'
        else:
            Flags['V'] = '0'
    elif v != '-':    
            Flags['V'] = v

def PrintFlags():
    for i in Flags:
        print(i + '=' + Flags[i],end = ' ')
    print('')
    print('')

def PrintJumps():
    print('JE:',JE32(),' JNE:',JNE32(),' JL:',JL32(),' JLE:',JLE32(),' JG:',JG32(),' JGE:',JGE32())
    print('')

def PrintReg(name, A, NoFlags = False):
    print(name, end = ' ')
    Print32(A, NoFlags)

def Print32(A, NoFlags = False):
    for i in range(32):
        if (i+1) % 4 == 0:
            print(A[i], end = ' ')
        else:
            print(A[i], end = '')
    print(Bin32ToHex8(A)+'h', Bin32ToDec(A))
    if not NoFlags:
        PrintFlags()

def Rand32():
    return ''.join(str(random.randint(0,1)) for _ in range(32))

def DecToBin32(d):
    res = ['0'] * 32
    p = abs(d)
    for i in range(32):
        w = 2 ** (31 - i)
        if p >= w:
            p = p - w
            res[i] = '1'
        else:
            res[i] = '0'
    if d >= 0:
        res = ''.join(res)
    else:
        res = NEG32(''.join(res),True)
    return res
        
def Bin32ToDec(A):
    res = 0
    for i in range(32):
        if i == 0:
            res = -1 * int(A[i]) * 2 ** (31 - i)
        else:
            res = res + int(A[i]) * 2 ** (31 - i)
    return res
    
def Bin4ToDec(b):
    res = 0
    for i in range(4):
        res = res + int(b[i]) * 2 ** (3 - i)
    return res

def Hex8ToBin32(h):
    res = ''
    for i in range(8):
        res = res + HexDic[h[i]]
    return res

def Bin32ToHex8(A):
    res = ['0'] * 8
    for i in range(8):
        res[i] = HexChar[Bin4ToDec(A[4 * i : 4 * i + 4])]
    res = ''.join(res)
    return res

def DecToHex8(d):
    return Bin32ToHex8(DecToBin32(d))
    
def Hex8ToDec(h):
    return Bin32ToDec(Hex8ToBin32(h))

def AddBit(a, b, c):
    return str((int(a) + int(b) + int(c)) % 2)

def CarBit(a, b, c):
    if int(a) + int(b) + int(c) >= 2:
        return '1'
    else:
        return '0'

def MOV32(A, B):
    return B

def ADD32(A, B, Sub = False, NoFlags = False):
    res = ['0'] * 32
    global Cout
    for i in range(31,-1,-1):
        if i == 31:
            Cin = '0'
            Cout = CarBit(A[i], B[i], Cin)
        else:
            Cin = Cout
            Cout = CarBit(A[i], B[i], Cin)
        res[i] = AddBit(A[i], B[i], Cin)
    res = ''.join(res)
    if Sub:
        if Cout == '0':
            Cout = '1'
        else:
            Cout = '0'
    if not NoFlags:
        SetFlags(A, B, res)
    return res

def SUB32(A, B):
    res = ADD32(A, NEG32(B), True)
    return res

def MUL32(A, B):
    res = DecToBin32(Bin32ToDec(A) * Bin32ToDec(B))
    SetFlags(A, B, res, '-',)
    return res

def DIV32(A, B):
    res = DecToBin32(Bin32ToDec(A) / Bin32ToDec(B))
    SetFlags(A, B, res)
    return res

def INC32(A):
    res= ADD32(A, DecToBin32(1))
    return res

def DEC32(A):
    res = SUB32(A, DecToBin32(1))
    return res

def CMP32(A, B):
    res = SUB32(A, B)

def NEG32(A, NoFlags = False):
    one = ['0'] * 32
    one[31] = '1'
    res = ADD32(NOT32(A), ''.join(one), True, NoFlags)
    return res

def AND32(A, B):
    res = ['0'] * 32
    for i in range(32):
        if A[i] == '1' and B[i] == '1':
            res[i] = '1'
        else:
            res[i] = '0'
    res = ''.join(res)
    SetFlags(A, B, res, '0', '0')
    return res

def OR32(A, B):
    res = ['0'] * 32
    for i in range(32):
        if A[i] == 0 and B[i] == 0:
            res[i] = '0'
        else:
            res[i] = '1'
    res = ''.join(res)
    SetFlags(A, B, res, '0', '0')
    return res

def XOR32(A, B):
    res = ['0'] * 32
    for i in range(32):
        if A[i] != B[i]:
            res[i] = '1'
        else:
            res[i] = '0'
    res = ''.join(res)
    SetFlags(A, B, res, '0', '0')
    return res

def NOT32(A):
    res = list(A)
    for i in range(32):
        if A[i] == '0':
            res[i] = '1'
        else:
            res[i] = '0'
    res = ''.join(res)
    return res

def SAL32(A, n):
    if n == 0:
        return A
    res = ['0'] * 32
    for i in range(32):
        if i <= 31 - n:
            res[i] = A[i + n]
        else:
            res[i] = '0'
    res = ''.join(res)
    SetFlags(A, A, res, '-')
    return res

def SAR32(A, n):
    if n == 0:
        return A
    res = ['0'] * 32
    for i in range(32):
        if i >= n:
            res[i] = A[i - n]
        else:
            res[i] = A[0]
    res = ''.join(res)
    SetFlags(A, A, res, '-', '0')
    return res

def TEST(A, B):
    return AND32(A, B)

def JE32():
    return Flags['Z'] == '1'

def JNE32():
    return Flags['Z'] == '0'

def JL32():
    return Flags['S'] != Flags['V']

def JLE32():
    return Flags['Z'] == '1' or Flags['S'] != Flags['V']

def JG32():
    return Flags['Z'] == '0' and Flags['S'] == Flags['V']

def JGE32():
    return Flags['S'] == Flags['V']
    
def Reset():
    global R0
    R0 = Hex8ToBin32('00000000')
    global R1 
    R1 = Hex8ToBin32('00100100')
    global R2
    R2 = Hex8ToBin32('00200200')
    global R3
    R3 = Hex8ToBin32('00100001')
    global R4 
    R4 = Hex8ToBin32('00200002')
    global M0 
    M0 = Hex8ToBin32('00001111')
    global M1 
    M1 = Hex8ToBin32('FFFF0000')
    global M2 
    M2 = Hex8ToBin32('11110000')
    global M3 
    M3 = Hex8ToBin32('FFFF0000')
    global M4
    M4 = Hex8ToBin32('F000000F')
    global A
    A = Hex8ToBin32('00200200')

def Q(desc):
    print('')
    print('---')
    print(desc)
    print('---')
    print('')

def PrintQTT():
    print('TRACE TABLE:')
    print('-----------')
    print('')

def PrintQMC():
    print('MODIFIED CONTENT:')
    print('----------------')
    print('')

def PrintQF():
    print('')
    print('FLAGS:')
    print('-----')
    print('')

def Q1():
    PrintQTT()

    R0n = R0
    M4n = M4
    
    R0n = MOV32(R0n, M4n)
    PrintReg('R0:',R0n)

    R0n = SAL32(R0n, Hex8ToDec('00000004'))
    PrintReg('R0:',R0n)

    R0n = SUB32(R0n, M0)
    PrintReg('R0:',R0n)

    R0n = NOT32(R0n)
    PrintReg('R0:',R0n)

    PrintQMC()
    
    if R0n != R0:
        PrintReg('R0:',R0n, True)
    if M4n != M4:
        PrintReg('M4:',M4n, True)

    PrintQF()

    PrintFlags()

def Q2():
    PrintQTT()

    R0n = R0
    R1n = R1
    R2n = R2
    R3n = R3
    An = A

    CMP32(R2n, R1n)
    PrintFlags()
    PrintJumps()

    if JL32():
        R0n = MOV32(R0n, An)
        PrintReg('R0:',R0n)

    R3n = SUB32(R3n, R2n)
    PrintReg('R3:',R3n)

    PrintQMC()    
    
    if R0n != R0:
        PrintReg('R0:',R0n, True)
    if R1n != R1:
        PrintReg('R1:',R1n, True)
    if R2n != R2:
        PrintReg('R2:',R2n, True)
    if R3n != R3:
        PrintReg('R3:',R3n, True)
    if An != A:
        PrintReg('A:',An, True)

    PrintQF()    
    
    PrintFlags()

def Q3():
    PrintQTT()
    
    R0n = R0
    R1n = R1
    R2n = R2
    M0n = M0
    
    R1n = MOV32(R1n, Hex8ToBin32('00100100'))
    PrintReg('R1:',R1n)
    
    R2n = MOV32(R2n, DecToBin32(0))
    PrintReg('R2:',R2n)
    
    CMP32(R0n, Hex8ToBin32('00300300'))
    PrintFlags()
    PrintJumps()

    while not JE32():
        R2n = ADD32(R2n, M0n)
        PrintReg('R2:',R2n)

        R0n = ADD32(R0n, R1n)
        PrintReg('R0:',R0n)

        CMP32(R0n, Hex8ToBin32('00300300'))
        PrintFlags()
        PrintJumps()

    PrintQMC()    
    
    if R0n != R0:
        PrintReg('R0:',R0n, True)
    if R1n != R1:
        PrintReg('R1:',R1n, True)
    if R2n != R2:
        PrintReg('R2:',R2n, True)
    if M0n != M0:
        PrintReg('M0:',M0n, True)

    PrintQF()
    
    PrintFlags()

def CAA1():
    Q("Q1a")
    Reset()
    Q1()
    Q("Q1b")
    Reset()
    Q2()
    Q("Q1c")
    Reset()
    Q3()
 
CAA1()
#Print32(SUB32(Hex8ToBin32('00CC3324'),Hex8ToBin32('00CC331D')))
