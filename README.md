# CryptoFromScratch: AES-128 & SHA-256 in Python

A lightweight, Python implementation of the **AES-128** symmetric encryption standard and the **SHA-256** cryptographic hash function from scratch. 

This project was built for **educational purposes** to demonstrate low-level data manipulation, including bitwise operations (XOR, bit shifts), byte block chunking, matrix transformations, and finite field arithmetic within the Galois Field $GF(2^8)$, all without relying on external cryptographic libraries.

## Key Features

* **Zero External Dependencies:** Built entirely using native Python (with only the built-in `base64` module for encoding output).
* **Full-Cycle AES-128 (ECB Mode):** Complete implementation of all round transformations (`SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`), the key expansion routine (`KeyExpansion`), and PKCS#7 block padding.
* **Authentic SHA-256:** Features step-by-step bitwise message padding to 512-bit blocks, message schedule generation, and the core 64-round compression function.

## Project Structure

* `aes_128.py` - Script for encrypting and decrypting text using the AES-128 algorithm.
* `sha_256.py` - Script for generating a standard SHA-256 cryptographic hash from an input string.

## Usage

Ensure you have Python 3.x installed. Clone this repository and run the scripts directly from your terminal:

### 1. Testing AES-128.
By default, the script encrypts the string `"abc"` using the key `"mysecretkey12345"`, prints the result in Hex and Base64 formats, and then successfully decrypts it back.

```bash
python3 aes_128.py

Example Output:
Base64 encrypted text: CTrG6bvW8b3y2zX9EbUPRQ==
Hex encrypted text: 093ac6e9bbd6f1bdf2db35fd11b50f45
Decrypted text: abc
```

### 2. Testing SHA-256. The script hashes the substring "abc" repeated 5 times and prints the final 256-bit hash in standard hexadecimal format.

```bash
python3 sha_256.py

Example Output:
a917d2e9c028a69f620f879b34123a1eb67fd13ebc763ab107f99bc2cf599b7c
```

# Implementation Details

AES-128 (aes_128.py)

The algorithm processes data in chunks of 16 bytes, mapping them onto a $4 \times 4$ State matrix. The implementation covers:

1.Padding (PKCS#7): Automatically pads the plaintext to ensure its length is a multiple of 16 bytes.
2.KeyExpansion: Derives 11 round keys (44 words total) from the initial 16-byte user key.
3.10-Round Encryption: Executes non-linear byte substitution via an S-Box, cyclic row shifting, column mixing via matrix multiplication in $GF(2^8)$, and round key XORing.
4.Decryption: Executes the inverse operations (InvSubBytes, InvShiftRows, InvMixColumns) using the round keys in reverse order.

SHA-256 (sha_256.py)

The algorithm processes the input string as a bitstream and executes:

1. Preprocessing & Padding: Appends a single 1 bit followed by 0 bits until the message length is congruent to 448 mod 512.
2. Length Suffixing: Appends a 64-bit big-endian integer representing the original message length in bits to complete the 512-bit block.
3. Message Schedule: Expands each 512-bit block into a 64-word array using the logical helper functions sigma0 and sigma1.
4.Compression Loop: Mutates eight 32-bit working variables (a through h) across 64 rounds using fractional prime constants K and bitwise operations (Ch, Maj, and circular right shifts rotr).

## Disclaimer
Warning: This project is intended solely for educational and portfolio demonstration purposes. The code is not optimized to mitigate side-channel vulnerabilities (such as timing attacks) and should never be used in production environments to secure sensitive data. For production applications, always rely on peer-reviewed, industry-standard libraries like cryptography or PyCryptodome.
