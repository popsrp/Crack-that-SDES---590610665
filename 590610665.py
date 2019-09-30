FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]



def permutate(original, fixed_key):
    new = ''
    for i in fixed_key:
        new += original[i - 1]
    return new


def left_half(bits):
    return bits[:len(bits)//2]


def right_half(bits):
    return bits[len(bits)//2:]


def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half


def key1(key):
    return permutate(shift(permutate(key, FIXED_P10)), FIXED_P8)


def key2(key):
    return permutate(shift(shift(shift(permutate(key, FIXED_P10)))), FIXED_P8)


def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new


def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, FIXED_EP)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S0) + lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits, FIXED_P4)
    return xor(bits, L)


def decrypt(cipher_text,key):
    bits = permutate(cipher_text, FIXED_IP)
    temp = f_k(bits, key2(key))
    bits = right_half(bits) + temp
    bits = f_k(bits, key1(key))
    return permutate(bits + temp, FIXED_IP_INVERSE)
my_ID = "590610665"

cipher = [0b111,0b101100,0b10110110,0b11111,0b10100010,0b10110110,0b11111,0b11111,0b111,0b10100010,0b10011010,0b11111,0b11110111,0b111,0b1111101,0b10110110,0b101100,0b11011001,0b11110111,0b1111101,0b11110111,0b11110111,0b10100010,0b1111101,0b10011010,0b11110111,0b11011001,0b111100,0b11111,0b11110111,0b10100010,0b101100,0b10110110,0b10110110,0b10110110,0b10100010,0b111,0b1111101,0b101100,0b101100,0b11110111,0b1111101,0b101100,0b10100010,0b11111,0b11111,0b10100010,0b10011010,0b11110111,0b111100,0b111100,0b10100010,0b10110110,0b10110110,0b10100010,0b1111101,0b11011001,0b11111,0b10110110,0b111,0b111100,0b101100,0b10110110,0b11011001,0b10011010,0b101100,0b111,0b10011010,0b10100010,0b111100,0b10110110,0b111,0b11111,0b10011010,0b11110111,0b10011010,0b11110111]

for i in range (1024):
  plain =[]
  Check_false = False
  for j in range (len(cipher)):
    key = '{0:010b}'.format(i)
    current_cipher = '{0:08b}'.format(int(cipher[j]))
    current_plain = int(decrypt(current_cipher,key),2)
    plain.append(current_plain - 48)
 
  for k in range (len(my_ID)):
    if plain[k] != int(my_ID[k]):
      Check_false = True
  if Check_false == False:
    print("KEY : " + key)
    break
  
print (plain)