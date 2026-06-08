H = [
    0x6a09e667,  # sqrt(2)
    0xbb67ae85,  # sqrt(3)
    0x3c6ef372,  # sqrt(5)
    0xa54ff53a,  # sqrt(7)
    0x510e527f,  # sqrt(11)
    0x9b05688c,  # sqrt(13)
    0x1f83d9ab,  # sqrt(17)
    0x5be0cd19   # sqrt(19)
]

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

def first_step(text):
    
    binary = ''.join(f'{ord(c):08b}' for c in text)
    original_lenth = len(binary)
    binary += '1'
    k = (448 - len(binary)) % 512
    binary += '0' * k
    binary += f'{original_lenth:064b}'

    binary_blocks = [binary[i:i+512] for i in range(0, len(binary), 512)]
    
    return binary_blocks

def second_step(binary_blocks):
    w_blocks = []
    for block in binary_blocks:
        words = []
        for i in range(0, 512, 32):
            words.append(block[i:i+32])
        w_blocks.append(words)
    
    return w_blocks

def message_schedule(w_blocks):
    for block in w_blocks:
        while len(block) < 64:
            i = len(block)
            val = (sigma1(int(block[i-2], 2)) + int(block[i-7], 2) + sigma0(int(block[i-15], 2)) + int(block[i-16], 2)) & 0xffffffff
            block.append(f"{val:032b}")
    return w_blocks 

def final_64_rounds(w_blocks):
        
    for block in w_blocks:
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
    
        for i in range(64):
            S1  = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
            ch  = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + K[i] + int(block[i], 2)) & 0xffffffff

            S0  = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        H[0] = (H[0] + a) & 0xffffffff
        H[1] = (H[1] + b) & 0xffffffff
        H[2] = (H[2] + c) & 0xffffffff
        H[3] = (H[3] + d) & 0xffffffff
        H[4] = (H[4] + e) & 0xffffffff
        H[5] = (H[5] + f) & 0xffffffff
        H[6] = (H[6] + g) & 0xffffffff
        H[7] = (H[7] + h) & 0xffffffff
    final_hash = ''.join(f'{h:08x}' for h in H)
    print(final_hash)
    return(final_hash)

def use_func(text):
    a = first_step(text)
    b = second_step(a)
    c = message_schedule(b)
    final_64_rounds(c)

use_func("abc"*5)
