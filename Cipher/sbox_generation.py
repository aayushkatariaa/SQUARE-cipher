from sympy import Matrix, GF

# Constants
AES_MODULUS = 0x11b  # Irreducible polynomial for GF(2^8)

# Step 1: Compute multiplication in GF(2^8)
def gf_mult(a, b):
    """Multiply two numbers in GF(2^8) and reduce modulo AES_MODULUS."""
    product = 0
    for _ in range(8):  
        if b & 1:
            product ^= a  
        carry = a & 0x80 
        a <<= 1  
        if carry:
            a ^= AES_MODULUS  
        b >>= 1  
    return product & 0xFF  

# Step 2: Compute multiplicative inverse in GF(2^8)
def gf_inverse(x):
    if x == 0:
        return 0  
    result = 1
    power = x
    for _ in range(7):  
        power = gf_mult(power, power)  
        result = gf_mult(result, power)  
    return result

# Step 3: Affine transformation matrix and constant vector
A = Matrix([
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1],
], domain=GF(2))  # Affine transformation matrix over GF(2)

b = Matrix([1, 1, 0, 0, 0, 1, 1, 0])  # Constant vector

# Function to apply affine transformation
def affine_transform(byte):
    vector = Matrix([[int(bit)] for bit in f"{byte:08b}"])  
    if vector.shape != (8, 1):
        raise ValueError(f"Expected (8, 1) shape, got {vector.shape} with byte {byte}")
    transformed = A @ vector + b  
    transformed = transformed.applyfunc(lambda x: x % 2)  
    return int("".join(map(str, transformed)), 2)  

# Step 4: Generate S-box
def generate_sbox():
    sbox = []
    for x in range(256):  
        inv = gf_inverse(x)  
        transformed = affine_transform(inv)  
        sbox.append(transformed)
    return sbox

# Save S-box to file in hex format
def save_sbox_to_file(sbox, filename="sbox.txt"):
    with open(filename, "w") as f:
        hex_sbox = [f"0x{val:02x}" for val in sbox]
        f.write("[ " + ", ".join(hex_sbox) + " ]\n")
    print(f"S-box saved to {filename}")

# Generate and print the S-box
print(f"A shape: {A.shape}, b shape: {b.shape}")  # Debug: Check dimensions
sbox = generate_sbox()
print(sbox)

# Save the generated S-box to a file
save_sbox_to_file(sbox)
