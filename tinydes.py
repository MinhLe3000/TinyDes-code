class TinyDES:
    """
    TinyDES - A miniature version of DES algorithm
    - 3 rounds Feistel cipher
    - 8-bit block size (split into 4-bit halves)
    - 8-bit key (split into KL0 and KR0, each 4 bits)
    - 6-bit subkeys for each round
    """
    
    def __init__(self):
        # S-box table from the images (4x16 matrix)
        self.sbox = [
            [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7],
            [0x0, 0xF, 0x7, 0x4, 0xE, 0x2, 0xD, 0x1, 0xA, 0x6, 0xC, 0xB, 0x9, 0x5, 0x3, 0x8],
            [0x4, 0x1, 0xE, 0x8, 0xD, 0x6, 0x2, 0xB, 0xF, 0xC, 0x9, 0x7, 0x3, 0xA, 0x5, 0x0],
            [0xF, 0xC, 0x8, 0x2, 0x4, 0x9, 0x1, 0x7, 0x5, 0xB, 0x3, 0xE, 0xA, 0x0, 0x6, 0xD]
        ]
    
    def int_to_binary(self, value, bits):
        """Convert integer to binary string with specified bit length"""
        return format(value, f'0{bits}b')
    
    def binary_to_int(self, binary_str):
        """Convert binary string to integer"""
        return int(binary_str, 2)
    
    def expand(self, r):
        """
        Expand function: 4 bits -> 6 bits
        Input: b0b1b2b3
        Output: b2b3b1b2b1b0
        """
        # Convert to binary string if needed
        if isinstance(r, int):
            r_bin = self.int_to_binary(r, 4)
        else:
            r_bin = r
        
        # Ensure we have 4 bits
        if len(r_bin) != 4:
            r_bin = r_bin.zfill(4)
        
        # Extract bits
        b0, b1, b2, b3 = r_bin[0], r_bin[1], r_bin[2], r_bin[3]
        
        # Apply expansion: b2b3b1b2b1b0
        expanded = b2 + b3 + b1 + b2 + b1 + b0
        
        return expanded
    
    def sbox_lookup(self, input_6bit):
        """
        S-box lookup: 6 bits -> 4 bits
        Row index: first and last bits (b0b5)
        Column index: middle 4 bits (b1b2b3b4)
        """
        # Convert to binary string if needed
        if isinstance(input_6bit, int):
            input_bin = self.int_to_binary(input_6bit, 6)
        else:
            input_bin = input_6bit
        
        # Ensure we have 6 bits
        if len(input_bin) != 6:
            input_bin = input_bin.zfill(6)
        
        # Extract row and column indices
        b0, b1, b2, b3, b4, b5 = input_bin[0], input_bin[1], input_bin[2], input_bin[3], input_bin[4], input_bin[5]
        
        row = self.binary_to_int(b0 + b5)  # b0b5
        col = self.binary_to_int(b1 + b2 + b3 + b4)  # b1b2b3b4
        
        # Lookup in S-box
        result = self.sbox[row][col]
        
        return self.int_to_binary(result, 4)
    
    def pbox_permute(self, input_4bit):
        """
        P-box permutation: b0b1b2b3 -> b2b0b3b1
        """
        # Convert to binary string if needed
        if isinstance(input_4bit, int):
            input_bin = self.int_to_binary(input_4bit, 4)
        else:
            input_bin = input_4bit
        
        # Ensure we have 4 bits
        if len(input_bin) != 4:
            input_bin = input_bin.zfill(4)
        
        # Extract bits
        b0, b1, b2, b3 = input_bin[0], input_bin[1], input_bin[2], input_bin[3]
        
        # Apply permutation: b2b0b3b1
        permuted = b2 + b0 + b3 + b1
        
        return permuted
    
    def compress_key(self, kl, kr):
        """
        Compress key: 8 bits (KL + KR) -> 6 bits
        Input: k0k1k2k3k4k5k6k7
        Output: k5k1k3k2k7k0
        """
        # Combine KL and KR
        if isinstance(kl, int):
            kl_bin = self.int_to_binary(kl, 4)
        else:
            kl_bin = kl
        
        if isinstance(kr, int):
            kr_bin = self.int_to_binary(kr, 4)
        else:
            kr_bin = kr
        
        # Ensure we have 4 bits each
        kl_bin = kl_bin.zfill(4)
        kr_bin = kr_bin.zfill(4)
        
        # Combine to get 8 bits: k0k1k2k3k4k5k6k7
        combined = kl_bin + kr_bin
        
        # Extract bits for compression: k5k1k3k2k7k0
        k0, k1, k2, k3, k4, k5, k6, k7 = combined[0], combined[1], combined[2], combined[3], combined[4], combined[5], combined[6], combined[7]
        
        compressed = k5 + k1 + k3 + k2 + k7 + k0
        
        return compressed
    
    def left_circular_shift(self, value, shift_amount, bit_length=4):
        """
        Left circular shift
        """
        # Convert to binary string if needed
        if isinstance(value, int):
            value_bin = self.int_to_binary(value, bit_length)
        else:
            value_bin = value
        
        # Ensure we have the right bit length
        value_bin = value_bin.zfill(bit_length)
        
        # Perform circular shift
        shifted = value_bin[shift_amount:] + value_bin[:shift_amount]
        
        return shifted
    
    def generate_subkeys(self, key):
        """
        Generate subkeys for all 3 rounds
        """
        # Convert key to binary string if needed
        if isinstance(key, int):
            key_bin = self.int_to_binary(key, 8)
        else:
            key_bin = key
        
        # Ensure we have 8 bits
        key_bin = key_bin.zfill(8)
        
        # Split key into KL0 and KR0 (4 bits each)
        kl0 = key_bin[:4]
        kr0 = key_bin[4:]
        
        subkeys = []
        kl_current = kl0
        kr_current = kr0
        
        # Round 1: shift by 1 bit
        kl1 = self.left_circular_shift(kl_current, 1, 4)
        kr1 = self.left_circular_shift(kr_current, 1, 4)
        k1 = self.compress_key(kl1, kr1)
        subkeys.append(k1)
        
        # Round 2: shift by 2 bits
        kl2 = self.left_circular_shift(kl1, 2, 4)
        kr2 = self.left_circular_shift(kr1, 2, 4)
        k2 = self.compress_key(kl2, kr2)
        subkeys.append(k2)
        
        # Round 3: shift by 1 bit
        kl3 = self.left_circular_shift(kl2, 1, 4)
        kr3 = self.left_circular_shift(kr2, 1, 4)
        k3 = self.compress_key(kl3, kr3)
        subkeys.append(k3)
        
        return subkeys
    
    def feistel_function(self, r, subkey):
        """
        Feistel function F(R, K)
        """
        # Expand R from 4 bits to 6 bits
        expanded_r = self.expand(r)
        
        # XOR with subkey
        xor_result = self.binary_to_int(expanded_r) ^ self.binary_to_int(subkey)
        xor_result_bin = self.int_to_binary(xor_result, 6)
        
        # S-box lookup
        sbox_result = self.sbox_lookup(xor_result_bin)
        
        # P-box permutation
        pbox_result = self.pbox_permute(sbox_result)
        
        return pbox_result
    
    def feistel_function_detailed(self, r, subkey):
        """
        Feistel function F(R, K) with detailed steps
        Returns: dict with all intermediate steps
        """
        # Expand R from 4 bits to 6 bits
        expanded_r = self.expand(r)
        
        # XOR with subkey
        xor_result = self.binary_to_int(expanded_r) ^ self.binary_to_int(subkey)
        xor_result_bin = self.int_to_binary(xor_result, 6)
        
        # S-box lookup (with row and column)
        b0, b1, b2, b3, b4, b5 = xor_result_bin[0], xor_result_bin[1], xor_result_bin[2], xor_result_bin[3], xor_result_bin[4], xor_result_bin[5]
        row = self.binary_to_int(b0 + b5)
        col = self.binary_to_int(b1 + b2 + b3 + b4)
        sbox_value = self.sbox[row][col]
        sbox_result = self.int_to_binary(sbox_value, 4)
        
        # P-box permutation
        pbox_result = self.pbox_permute(sbox_result)
        
        return {
            'input_r': r,
            'expanded': expanded_r,
            'subkey': subkey,
            'xor_result': xor_result_bin,
            'sbox_input': xor_result_bin,
            'sbox_row': row,
            'sbox_col': col,
            'sbox_value': sbox_value,
            'sbox_output': sbox_result,
            'pbox_output': pbox_result,
            'final_output': pbox_result
        }
    
    def feistel_round(self, left, right, subkey):
        """
        Single Feistel round
        """
        new_left = right
        f_result = self.feistel_function(right, subkey)
        new_right = self.binary_to_int(left) ^ self.binary_to_int(f_result)
        new_right_bin = self.int_to_binary(new_right, 4)
        
        return new_left, new_right_bin
    
    def encrypt(self, plaintext, key):
        """
        Encrypt 8-bit plaintext with 8-bit key
        """
        # Convert to binary strings if needed
        if isinstance(plaintext, int):
            pt_bin = self.int_to_binary(plaintext, 8)
        else:
            pt_bin = plaintext
        
        if isinstance(key, int):
            key_bin = self.int_to_binary(key, 8)
        else:
            key_bin = key
        
        # Ensure we have 8 bits
        pt_bin = pt_bin.zfill(8)
        key_bin = key_bin.zfill(8)
        
        # Split plaintext into left and right halves
        left = pt_bin[:4]
        right = pt_bin[4:]
        
        # Generate subkeys
        subkeys = self.generate_subkeys(key_bin)
        
        # Perform 3 Feistel rounds
        for i in range(3):
            left, right = self.feistel_round(left, right, subkeys[i])
        
        # Final result is L3 || R3
        ciphertext = left + right
        
        return ciphertext
    
    def encrypt_detailed(self, plaintext, key):
        """
        Encrypt 8-bit plaintext with 8-bit key - detailed version
        Returns: dict with all intermediate steps
        """
        # Convert to binary strings if needed
        if isinstance(plaintext, int):
            pt_bin = self.int_to_binary(plaintext, 8)
        else:
            pt_bin = plaintext
        
        if isinstance(key, int):
            key_bin = self.int_to_binary(key, 8)
        else:
            key_bin = key
        
        # Ensure we have 8 bits
        pt_bin = pt_bin.zfill(8)
        key_bin = key_bin.zfill(8)
        
        # Split plaintext into left and right halves
        left = pt_bin[:4]
        right = pt_bin[4:]
        
        # Split key into KL0 and KR0
        kl0 = key_bin[:4]
        kr0 = key_bin[4:]
        
        # Generate subkeys with details
        subkeys = []
        subkey_details = []
        kl_current = kl0
        kr_current = kr0
        
        # Round 1: shift by 1 bit
        kl1 = self.left_circular_shift(kl_current, 1, 4)
        kr1 = self.left_circular_shift(kr_current, 1, 4)
        k1 = self.compress_key(kl1, kr1)
        subkeys.append(k1)
        subkey_details.append({
            'round': 1,
            'kl': kl_current,
            'kr': kr_current,
            'kl_shifted': kl1,
            'kr_shifted': kr1,
            'subkey': k1,
            'shift_amount': 1
        })
        
        # Round 2: shift by 2 bits
        kl2 = self.left_circular_shift(kl1, 2, 4)
        kr2 = self.left_circular_shift(kr1, 2, 4)
        k2 = self.compress_key(kl2, kr2)
        subkeys.append(k2)
        subkey_details.append({
            'round': 2,
            'kl': kl1,
            'kr': kr1,
            'kl_shifted': kl2,
            'kr_shifted': kr2,
            'subkey': k2,
            'shift_amount': 2
        })
        
        # Round 3: shift by 1 bit
        kl3 = self.left_circular_shift(kl2, 1, 4)
        kr3 = self.left_circular_shift(kr2, 1, 4)
        k3 = self.compress_key(kl3, kr3)
        subkeys.append(k3)
        subkey_details.append({
            'round': 3,
            'kl': kl2,
            'kr': kr2,
            'kl_shifted': kl3,
            'kr_shifted': kr3,
            'subkey': k3,
            'shift_amount': 1
        })
        
        # Perform 3 Feistel rounds with details
        rounds = []
        current_left = left
        current_right = right
        
        for i in range(3):
            round_num = i + 1
            # Get feistel function details
            feistel_details = self.feistel_function_detailed(current_right, subkeys[i])
            
            # Calculate new left and right
            new_left = current_right
            f_result = feistel_details['final_output']
            new_right_int = self.binary_to_int(current_left) ^ self.binary_to_int(f_result)
            new_right = self.int_to_binary(new_right_int, 4)
            
            rounds.append({
                'round': round_num,
                'input_left': current_left,
                'input_right': current_right,
                'subkey': subkeys[i],
                'expansion': feistel_details['expanded'],
                'xor_with_key': feistel_details['xor_result'],
                'sbox_input': feistel_details['sbox_input'],
                'sbox_row': feistel_details['sbox_row'],
                'sbox_col': feistel_details['sbox_col'],
                'sbox_value': feistel_details['sbox_value'],
                'sbox_output': feistel_details['sbox_output'],
                'pbox_output': feistel_details['pbox_output'],
                'f_result': f_result,
                'new_left': new_left,
                'new_right': new_right,
                'output_left': new_left,
                'output_right': new_right
            })
            
            current_left = new_left
            current_right = new_right
        
        # Final result
        ciphertext = current_left + current_right
        
        return {
            'plaintext': pt_bin,
            'plaintext_hex': hex(int(pt_bin, 2)),
            'plaintext_decimal': int(pt_bin, 2),
            'key': key_bin,
            'key_hex': hex(int(key_bin, 2)),
            'key_decimal': int(key_bin, 2),
            'kl0': kl0,
            'kr0': kr0,
            'initial_left': left,
            'initial_right': right,
            'subkey_details': subkey_details,
            'rounds': rounds,
            'ciphertext': ciphertext,
            'ciphertext_hex': hex(int(ciphertext, 2)),
            'ciphertext_decimal': int(ciphertext, 2),
            'final_left': current_left,
            'final_right': current_right
        }
    
    def decrypt_detailed(self, ciphertext, key):
        """
        Decrypt 8-bit ciphertext with 8-bit key - detailed version
        Returns: dict with all intermediate steps
        """
        # Convert to binary strings if needed
        if isinstance(ciphertext, int):
            ct_bin = self.int_to_binary(ciphertext, 8)
        else:
            ct_bin = ciphertext
        
        if isinstance(key, int):
            key_bin = self.int_to_binary(key, 8)
        else:
            key_bin = key
        
        # Ensure we have 8 bits
        ct_bin = ct_bin.zfill(8)
        key_bin = key_bin.zfill(8)
        
        # Split ciphertext into left and right halves
        left = ct_bin[:4]
        right = ct_bin[4:]
        
        # Split key into KL0 and KR0
        kl0 = key_bin[:4]
        kr0 = key_bin[4:]
        
        # Generate subkeys with details (same as encryption)
        subkeys = []
        subkey_details = []
        kl_current = kl0
        kr_current = kr0
        
        # Round 1: shift by 1 bit
        kl1 = self.left_circular_shift(kl_current, 1, 4)
        kr1 = self.left_circular_shift(kr_current, 1, 4)
        k1 = self.compress_key(kl1, kr1)
        subkeys.append(k1)
        subkey_details.append({
            'round': 1,
            'kl': kl_current,
            'kr': kr_current,
            'kl_shifted': kl1,
            'kr_shifted': kr1,
            'subkey': k1,
            'shift_amount': 1
        })
        
        # Round 2: shift by 2 bits
        kl2 = self.left_circular_shift(kl1, 2, 4)
        kr2 = self.left_circular_shift(kr1, 2, 4)
        k2 = self.compress_key(kl2, kr2)
        subkeys.append(k2)
        subkey_details.append({
            'round': 2,
            'kl': kl1,
            'kr': kr1,
            'kl_shifted': kl2,
            'kr_shifted': kr2,
            'subkey': k2,
            'shift_amount': 2
        })
        
        # Round 3: shift by 1 bit
        kl3 = self.left_circular_shift(kl2, 1, 4)
        kr3 = self.left_circular_shift(kr2, 1, 4)
        k3 = self.compress_key(kl3, kr3)
        subkeys.append(k3)
        subkey_details.append({
            'round': 3,
            'kl': kl2,
            'kr': kr2,
            'kl_shifted': kl3,
            'kr_shifted': kr3,
            'subkey': k3,
            'shift_amount': 1
        })
        
        # Perform 3 Feistel rounds in reverse order with details
        # For decryption: process rounds in reverse order (subkey[2], subkey[1], subkey[0])
        rounds = []
        current_left = left
        current_right = right
        
        for i in range(2, -1, -1):  # Reverse order: 2, 1, 0 (use subkeys[2], subkeys[1], subkeys[0])
            round_num = 3 - i  # Display round number (1, 2, 3)
            
            # Save current state before processing
            input_left = current_left
            input_right = current_right
            
            # For decryption: F function uses current_left as input (not current_right like encryption)
            feistel_details = self.feistel_function_detailed(current_left, subkeys[i])
            
            # Calculate new values for decryption
            f_result = feistel_details['final_output']
            # R_new = R_old XOR F(L_old, K)
            new_right_int = self.binary_to_int(current_right) ^ self.binary_to_int(f_result)
            new_right = self.int_to_binary(new_right_int, 4)
            # L_new = L_old (left stays the same, becomes right in next round)
            new_left = current_left
            
            rounds.append({
                'round': round_num,
                'input_left': input_left,
                'input_right': input_right,
                'subkey': subkeys[i],
                'subkey_round': i + 1,  # Which subkey is used
                'expansion': feistel_details['expanded'],
                'xor_with_key': feistel_details['xor_result'],
                'sbox_input': feistel_details['sbox_input'],
                'sbox_row': feistel_details['sbox_row'],
                'sbox_col': feistel_details['sbox_col'],
                'sbox_value': feistel_details['sbox_value'],
                'sbox_output': feistel_details['sbox_output'],
                'pbox_output': feistel_details['pbox_output'],
                'f_result': f_result,
                'xor_left_with_f': f"{current_right} XOR {f_result} = {new_right}",
                'new_left': new_left,
                'new_right': new_right,
                'output_left': new_left,
                'output_right': new_right
            })
            
            # Update for next iteration: swap left and right
            # L_next = R_new, R_next = L_old
            current_left = new_right
            current_right = new_left
        
        # Final result: current_left and current_right are already swapped, so combine them
        plaintext = current_left + current_right
        
        return {
            'ciphertext': ct_bin,
            'ciphertext_hex': hex(int(ct_bin, 2)),
            'ciphertext_decimal': int(ct_bin, 2),
            'key': key_bin,
            'key_hex': hex(int(key_bin, 2)),
            'key_decimal': int(key_bin, 2),
            'kl0': kl0,
            'kr0': kr0,
            'initial_left': left,
            'initial_right': right,
            'subkey_details': subkey_details,
            'rounds': rounds,
            'plaintext': plaintext,
            'plaintext_hex': hex(int(plaintext, 2)),
            'plaintext_decimal': int(plaintext, 2),
            'final_left': current_left,
            'final_right': current_right
        }
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt 8-bit ciphertext with 8-bit key
        """
        # Convert to binary strings if needed
        if isinstance(ciphertext, int):
            ct_bin = self.int_to_binary(ciphertext, 8)
        else:
            ct_bin = ciphertext
        
        if isinstance(key, int):
            key_bin = self.int_to_binary(key, 8)
        else:
            key_bin = key
        
        # Ensure we have 8 bits
        ct_bin = ct_bin.zfill(8)
        key_bin = key_bin.zfill(8)
        
        # Split ciphertext into left and right halves
        left = ct_bin[:4]
        right = ct_bin[4:]
        
        # Generate subkeys (same as encryption)
        subkeys = self.generate_subkeys(key_bin)
        
        # Perform 3 Feistel rounds in reverse order
        for i in range(2, -1, -1):  # Reverse order: 2, 1, 0
            # For decryption, we need to reverse the Feistel operation
            f_result = self.feistel_function(left, subkeys[i])
            new_right = self.binary_to_int(right) ^ self.binary_to_int(f_result)
            new_right_bin = self.int_to_binary(new_right, 4)
            
            # Update for next iteration
            right = left
            left = new_right_bin
        
        # Final result is L0 || R0
        plaintext = left + right
        
        return plaintext


def test_tinydes():
    """
    Test function with the example from the images
    """
    tinydes = TinyDES()
    
    print("=== TinyDES Test ===")
    
    # Test individual functions
    print("\n1. Testing individual functions:")
    
    # Test Expand function
    r0 = "1100"
    expanded = tinydes.expand(r0)
    print(f"Expand({r0}) = {expanded}")
    
    # Test S-box
    sbox_input = "100101"
    sbox_output = tinydes.sbox_lookup(sbox_input)
    print(f"S-box({sbox_input}) = {sbox_output}")
    
    # Test P-box
    pbox_input = "1000"
    pbox_output = tinydes.pbox_permute(pbox_input)
    print(f"P-box({pbox_input}) = {pbox_output}")
    
    # Test key compression
    kl1 = "0011"
    kr1 = "0101"
    compressed = tinydes.compress_key(kl1, kr1)
    print(f"Compress({kl1}, {kr1}) = {compressed}")
    
    print("\n2. Testing encryption/decryption:")
    
    # Test with example values (inferred from the images)
    # From the example: L0=0101, R0=1100, KL0=0110, KR0=1010
    plaintext = "01011100"  # L0 || R0
    key = "01101010"        # KL0 || KR0
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Encrypt
    ciphertext = tinydes.encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt
    decrypted = tinydes.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    if decrypted == plaintext:
        print("✓ Encryption/Decryption successful!")
    else:
        print("✗ Encryption/Decryption failed!")
    
    print("\n3. Testing with different values:")
    
    # Test with hex values
    plaintext_hex = 0x5C  # 01011100
    key_hex = 0x6A        # 01101010
    
    ciphertext_hex = tinydes.encrypt(plaintext_hex, key_hex)
    decrypted_hex = tinydes.decrypt(ciphertext_hex, key_hex)
    
    print(f"Plaintext (hex): {hex(plaintext_hex)}")
    print(f"Key (hex): {hex(key_hex)}")
    print(f"Ciphertext (hex): {hex(int(ciphertext_hex, 2))}")
    print(f"Decrypted (hex): {hex(int(decrypted_hex, 2))}")


def interactive_mode():
    """
    Chế độ tương tác để người dùng nhập dữ liệu
    """
    tinydes = TinyDES()
    
    print("=" * 50)
    print("           TINYDES ENCRYPTION SYSTEM")
    print("=" * 50)
    print("Thuật toán TinyDES - Phiên bản thu nhỏ của DES")
    print("- 8-bit block size")
    print("- 8-bit key size") 
    print("- 3 rounds Feistel cipher")
    print("=" * 50)
    
    while True:
        print("\n📋 MENU CHÍNH:")
        print("1. Mã hóa dữ liệu")
        print("2. Giải mã dữ liệu")
        print("3. Test các hàm riêng lẻ")
        print("4. Hiển thị thông tin về TinyDES")
        print("5. Thoát chương trình")
        
        choice = input("\n🔸 Chọn chức năng (1-5): ").strip()
        
        if choice == "1":
            encrypt_mode(tinydes)
        elif choice == "2":
            decrypt_mode(tinydes)
        elif choice == "3":
            test_functions_mode(tinydes)
        elif choice == "4":
            show_info()
        elif choice == "5":
            print("\n👋 Cảm ơn bạn đã sử dụng TinyDES!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 1-5.")


def encrypt_mode(tinydes):
    """
    Chế độ mã hóa
    """
    print("\n🔐 CHẾ ĐỘ MÃ HÓA")
    print("-" * 30)
    
    while True:
        print("\n📝 Nhập dữ liệu cần mã hóa:")
        print("(Có thể nhập dưới dạng: nhị phân 8-bit, hex 2 ký tự, hoặc decimal)")
        
        plaintext_input = input("🔸 Plaintext: ").strip()
        
        if not plaintext_input:
            print("❌ Không được để trống!")
            continue
            
        # Chuyển đổi plaintext
        plaintext = convert_input(plaintext_input, 8)
        if plaintext is None:
            print("❌ Định dạng dữ liệu không hợp lệ!")
            continue
            
        print("\n🔑 Nhập khóa:")
        print("(Có thể nhập dưới dạng: nhị phân 8-bit, hex 2 ký tự, hoặc decimal)")
        
        key_input = input("🔸 Key: ").strip()
        
        if not key_input:
            print("❌ Không được để trống!")
            continue
            
        # Chuyển đổi key
        key = convert_input(key_input, 8)
        if key is None:
            print("❌ Định dạng khóa không hợp lệ!")
            continue
        
        # Thực hiện mã hóa
        try:
            ciphertext = tinydes.encrypt(plaintext, key)
            
            print("\n✅ KẾT QUẢ MÃ HÓA:")
            print(f"📄 Plaintext:  {plaintext} (binary)")
            print(f"🔑 Key:        {key} (binary)")
            print(f"🔐 Ciphertext: {ciphertext} (binary)")
            print(f"🔐 Ciphertext: {hex(int(ciphertext, 2))} (hex)")
            print(f"🔐 Ciphertext: {int(ciphertext, 2)} (decimal)")
            
        except Exception as e:
            print(f"❌ Lỗi mã hóa: {e}")
        
        # Hỏi có tiếp tục không
        continue_choice = input("\n🔄 Tiếp tục mã hóa? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', 'có']:
            break


def decrypt_mode(tinydes):
    """
    Chế độ giải mã
    """
    print("\n🔓 CHẾ ĐỘ GIẢI MÃ")
    print("-" * 30)
    
    while True:
        print("\n📝 Nhập dữ liệu cần giải mã:")
        print("(Có thể nhập dưới dạng: nhị phân 8-bit, hex 2 ký tự, hoặc decimal)")
        
        ciphertext_input = input("🔸 Ciphertext: ").strip()
        
        if not ciphertext_input:
            print("❌ Không được để trống!")
            continue
            
        # Chuyển đổi ciphertext
        ciphertext = convert_input(ciphertext_input, 8)
        if ciphertext is None:
            print("❌ Định dạng dữ liệu không hợp lệ!")
            continue
            
        print("\n🔑 Nhập khóa:")
        print("(Có thể nhập dưới dạng: nhị phân 8-bit, hex 2 ký tự, hoặc decimal)")
        
        key_input = input("🔸 Key: ").strip()
        
        if not key_input:
            print("❌ Không được để trống!")
            continue
            
        # Chuyển đổi key
        key = convert_input(key_input, 8)
        if key is None:
            print("❌ Định dạng khóa không hợp lệ!")
            continue
        
        # Thực hiện giải mã
        try:
            plaintext = tinydes.decrypt(ciphertext, key)
            
            print("\n✅ KẾT QUẢ GIẢI MÃ:")
            print(f"🔐 Ciphertext: {ciphertext} (binary)")
            print(f"🔑 Key:        {key} (binary)")
            print(f"📄 Plaintext:  {plaintext} (binary)")
            print(f"📄 Plaintext:  {hex(int(plaintext, 2))} (hex)")
            print(f"📄 Plaintext:  {int(plaintext, 2)} (decimal)")
            
        except Exception as e:
            print(f"❌ Lỗi giải mã: {e}")
        
        # Hỏi có tiếp tục không
        continue_choice = input("\n🔄 Tiếp tục giải mã? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', 'có']:
            break


def test_functions_mode(tinydes):
    """
    Chế độ test các hàm riêng lẻ
    """
    print("\n🧪 TEST CÁC HÀM RIÊNG LẺ")
    print("-" * 30)
    
    while True:
        print("\n📋 Chọn hàm cần test:")
        print("1. Expand (4 bit → 6 bit)")
        print("2. S-box lookup (6 bit → 4 bit)")
        print("3. P-box permutation (4 bit → 4 bit)")
        print("4. Key compression (8 bit → 6 bit)")
        print("5. Quay lại menu chính")
        
        choice = input("🔸 Chọn (1-5): ").strip()
        
        if choice == "1":
            test_expand(tinydes)
        elif choice == "2":
            test_sbox(tinydes)
        elif choice == "3":
            test_pbox(tinydes)
        elif choice == "4":
            test_compress(tinydes)
        elif choice == "5":
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")


def test_expand(tinydes):
    """Test hàm Expand"""
    print("\n🔍 TEST HÀM EXPAND")
    input_4bit = input("🔸 Nhập 4 bit (VD: 1100): ").strip()
    
    if len(input_4bit) != 4 or not all(c in '01' for c in input_4bit):
        print("❌ Phải nhập đúng 4 bit (0 hoặc 1)!")
        return
    
    result = tinydes.expand(input_4bit)
    print(f"✅ Expand({input_4bit}) = {result}")


def test_sbox(tinydes):
    """Test hàm S-box"""
    print("\n🔍 TEST HÀM S-BOX")
    input_6bit = input("🔸 Nhập 6 bit (VD: 100101): ").strip()
    
    if len(input_6bit) != 6 or not all(c in '01' for c in input_6bit):
        print("❌ Phải nhập đúng 6 bit (0 hoặc 1)!")
        return
    
    result = tinydes.sbox_lookup(input_6bit)
    print(f"✅ S-box({input_6bit}) = {result}")


def test_pbox(tinydes):
    """Test hàm P-box"""
    print("\n🔍 TEST HÀM P-BOX")
    input_4bit = input("🔸 Nhập 4 bit (VD: 1000): ").strip()
    
    if len(input_4bit) != 4 or not all(c in '01' for c in input_4bit):
        print("❌ Phải nhập đúng 4 bit (0 hoặc 1)!")
        return
    
    result = tinydes.pbox_permute(input_4bit)
    print(f"✅ P-box({input_4bit}) = {result}")


def test_compress(tinydes):
    """Test hàm Compress"""
    print("\n🔍 TEST HÀM COMPRESS")
    kl = input("🔸 Nhập KL (4 bit): ").strip()
    kr = input("🔸 Nhập KR (4 bit): ").strip()
    
    if len(kl) != 4 or len(kr) != 4 or not all(c in '01' for c in kl+kr):
        print("❌ Phải nhập đúng 4 bit cho KL và KR!")
        return
    
    result = tinydes.compress_key(kl, kr)
    print(f"✅ Compress({kl}, {kr}) = {result}")


def convert_input(user_input, expected_bits):
    """
    Chuyển đổi input từ người dùng thành binary string
    """
    user_input = user_input.strip().lower()
    
    try:
        # Nếu là binary
        if all(c in '01' for c in user_input):
            if len(user_input) == expected_bits:
                return user_input
            elif len(user_input) < expected_bits:
                return user_input.zfill(expected_bits)
            else:
                return None
        
        # Nếu là hex
        elif user_input.startswith('0x'):
            hex_value = user_input[2:]
            if len(hex_value) <= 2 and all(c in '0123456789abcdef' for c in hex_value):
                decimal = int(hex_value, 16)
                return format(decimal, f'0{expected_bits}b')
        
        # Nếu là decimal
        elif user_input.isdigit():
            decimal = int(user_input)
            if 0 <= decimal < 2**expected_bits:
                return format(decimal, f'0{expected_bits}b')
        
        return None
        
    except ValueError:
        return None


def show_info():
    """
    Hiển thị thông tin về TinyDES
    """
    print("\n📚 THÔNG TIN VỀ TINYDES")
    print("=" * 50)
    print("🔹 TinyDES là phiên bản thu nhỏ của thuật toán DES")
    print("🔹 Đặc điểm:")
    print("   • 3 rounds Feistel cipher")
    print("   • Block size: 8 bit (chia thành 2 phần 4-bit)")
    print("   • Key size: 8 bit (chia thành KL0 và KR0)")
    print("   • Subkey size: 6 bit cho mỗi round")
    print()
    print("🔹 Các thành phần chính:")
    print("   • Expand: mở rộng 4 bit → 6 bit")
    print("   • S-box: tra cứu bảng 4x16")
    print("   • P-box: hoán vị bit")
    print("   • Key schedule: sinh khóa con")
    print()
    print("🔹 Ví dụ sử dụng:")
    print("   Plaintext: 01011100 (binary) hoặc 5C (hex) hoặc 92 (decimal)")
    print("   Key:       01101010 (binary) hoặc 6A (hex) hoặc 106 (decimal)")
    print("   Ciphertext: sẽ được tính toán bởi thuật toán")


if __name__ == "__main__":
    print("Chọn chế độ chạy:")
    print("1. Chế độ tương tác (nhập dữ liệu)")
    print("2. Chế độ test tự động")
    
    mode = input("Chọn (1-2): ").strip()
    
    if mode == "1":
        interactive_mode()
    else:
        test_tinydes()
