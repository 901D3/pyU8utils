#originally coded by 90143
#optimized by Mink

def main():
    print("Some Small nx-u8/100 utils")
    print("     1. Translate hackstring to offset")
    print("     2. Disassembly to instruction (experimental)")

    while True:
        mode = input("Choose mode, q to quit: ")

        if mode == "1":
            translate_hackstring_to_offset()
        elif mode == "2":
            disas_to_instruction()
        elif mode == "q":
            print("Exiting program...")
            break
        else:
            print("Invalid mode")

def translate_hackstring_to_offset():
    while True:
        hackstring_input = input("Enter your hackstring, each hex separated by space (aa bb Xc XX), q to quit: ").upper()

        if hackstring_input.lower() == "q":
            break

        parts = hackstring_input.split()

        if len(parts) < 3:
            print("Not enough hackstring")
            continue

        hbyte_offset = parts[0]
        lbyte_offset = parts[1]
        segment_offset = parts[2][1]

        if segment_offset not in "0123":
            print(f"Segment '{segment_offset}' is not a valid segment.")
        else:
            leftover = lbyte_offset + hbyte_offset
            result = f"{segment_offset}:{leftover}"
            print(result)

def disas_to_instruction():
    while True:
        print("     1. Big endian\n     2. Little endian (beginner?)")
        submode = input("Choose submode, q to quit: ")

        if submode == "1":
            dti_1()
        elif submode == "2":
            dti_2()
        elif submode == "q":
            break
        else:
            print("Invalid submode")

def dti_1():
    while True:
        asm_code_input = input("Enter your assembly code, q to quit: ")

        if asm_code_input.lower() == "q":
            break

        result = asm_code_input[::-1]
        print(result)

def dti_2():
    instructions = []
    while True:
        asm_code_input = input("Enter your little endian assembly code,auto-save, e to complete assembly code and print, q to quit: ").upper()

        if asm_code_input.lower() == "q":
            break

        if asm_code_input.lower() == "e":
            print("Completed assembly code:")
            for instruction in instructions:
                print(instruction)
            instructions = []
            continue

        if len(asm_code_input) > 4:
            print("Invalid assembly code")
            continue

        if not all(c in "0123456789ABCDEFabcdef" for c in asm_code_input):
            print("Only hexadecimal characters are allowed")
            continue

        asm_code_input = asm_code_input.upper()
        asm_code_pA = asm_code_input[:2]
        asm_code_pB = asm_code_input[2:]

        instruction = ""

        #-----------------------------------------------------------------
        #ranges

        add_Rn_ranges = (
            "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F" + 
            "10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F" + 
            "20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F" + 
            "30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F" + 
            "40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F" + 
            "50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F" + 
            "60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F" + 
            "70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F"
            ).split(" ")

        add_Rn_neg_ranges = (
            "80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F "
            "90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F "
            "A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF "
            "B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF "
            "C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF "
            "D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF "
            "E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF "
            "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF"
            ).split(" ")
            
        add_ERn_ranges = (
            "80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F "
            "90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F "
            "A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF "
            "B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF "
            "C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF "
            "D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF "
            "E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF "
            "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF"
            ).split(" ")
            
        dw_ranges = (
            "90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F" +
            "A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF" +
            "B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF" +
            "C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CC CC CD CE CF" +
            "D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DD DD DD DE DF" +
            "E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EE EE EE EE EF"
            ).split(" ")

        dw_exclude_pB = "10 30 50 70 90 B0 D0 F0".split(" ")
        #-----------------------------------------------------------------
        # MOV Rn, #xxH

        if asm_code_pA in "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F".split(" "):
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # ADD Rn, #00 - 7FH

        if asm_code_pA in "10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F".split(" ") and (asm_code_pB in add_Rn_ranges):
            ADD = f"ADD R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {ADD}"
            print(instruction)

        #-----------------------------------------------------------------
        # ADD Rn, #-80 - -1H
        def hex_to_neg_dec(hex_value):
            return int(hex_value, 16) - 256

        if asm_code_pA in "10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F".split() and asm_code_pB in add_Rn_neg_ranges:
            neg_value = hex_to_neg_dec(asm_code_pB)
            ADD = f"ADD R{int(asm_code_pA[1], 16)}, #{neg_value}H"
            instruction = f"{asm_code_input} -> {ADD}"
            print(instruction)

        #-----------------------------------------------------------------
        # AND Rn, #xxH

        if asm_code_pA in "20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F".split(" "):
            AND = f"AND R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {AND}"
            print(instruction)

        #-----------------------------------------------------------------
        # OR Rn, #xxH

        if asm_code_pA in "30 31 32 33 34 35 36 37 08 39 3A 3B 3C 3D 3E 3F".split(" "):
            OR = f"OR R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {OR}"
            print(instruction)

        #-----------------------------------------------------------------
        # XOR Rn, #xxH

        if asm_code_pA in "40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F".split(" "):
            XOR = f"XOR R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {XOR}"
            print(instruction)

        #-----------------------------------------------------------------
        # CMPC Rn, #xxH

        if asm_code_pA in "50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F".split(" "):
            CMPC = f"CMPC R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMPC}"
            print(instruction)

        #-----------------------------------------------------------------
        # ADDC Rn, #xxH

        if asm_code_pA in "60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F".split(" "):
            ADDC = f"ADDC R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {ADDC}"
            print(instruction)

        #-----------------------------------------------------------------
        # CMP Rn, #xxH

        if (asm_code_pA in "70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F".split(" ")):
            CMP = f"CMP R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        #-----------------------------------------------------------------
        # MOV Rn, Rm

        if (asm_code_pA in "80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F".split(" ")) and (asm_code_pB in "00 10 20 30 40 50 60 70 80 90 A0 B0 C0 D0 E0 F0".split(" ")):
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, R{int(asm_code_pB[0], 16)}"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # L Rn, [ERm]

        if (asm_code_pA in "90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F".split(" ")) and (asm_code_pB in "00 20 40 60 80 A0 C0 E0".split(" ")):
            L = f"L R{int(asm_code_pA[1], 16)}, [ER{int(asm_code_pB[0], 16)}]"
            instruction = f"{asm_code_input} -> {L}"
            print(instruction)

        #-----------------------------------------------------------------
        # DW aabbH

        if (asm_code_pA in dw_ranges) and (asm_code_pB not in dw_exclude_pB):
            DW = f"DW {asm_code_input}H"
            instruction = f"{asm_code_input} -> {DW}"
            print(instruction)

        #-----------------------------------------------------------------
        # MOV ERn, #xxH

        if asm_code_pA in "E0 E2 E4 E6 E8 EA EC EE".split(" "):
            MOV = f"MOV ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # MUL ERn, Rm

        if (asm_code_pA in "F0 F2 F4 F6 F8 FA FC FE".split(" ")) and (asm_code_pB in "04 14 24 34 44 54 64 74 84 94 A4 B4 C4 D4 E4 F4".split(" ")):
            MUL = f"MUL ER{int(asm_code_pB[0], 16)}, R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {MUL}"
            print(instruction)

        #-----------------------------------------------------------------
        # CMP ERn, ERm

        if asm_code_pA in "F0 F2 F4 F6 F8 FA FC FE".split(" ") and (asm_code_pB in "07 27 47 67 87 A7 C7 E7"):
            CMP = f"CMP ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP Rn

        if asm_code_pA in "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF".split(" ") and asm_code_pB == "0E":
            POP = f"POP R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP ERn

        if asm_code_pA in "F0 F2 F4 F6 F8 FA FC FE".split(" ") and asm_code_pB == "1E":
            POP = f"POP ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP XRn

        if asm_code_pA in "F0 F4 F8 FC".split(" ") and asm_code_pB == "2E":
            POP = f"POP XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP QRn

        if asm_code_pA in "F0 F8 FC".split(" ") and asm_code_pB == "3E":
            POP = f"POP QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH Rn

        if asm_code_pA in "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF".split(" ") and asm_code_pB == "4E":
            PUSH = f"PUSH R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH ERn

        if asm_code_pA in "F0 F2 F4 F6 F8 FA FC FE".split(" ") and asm_code_pB == "5E":
            PUSH = f"PUSH ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)


        #-----------------------------------------------------------------
        # PUSH XRn

        if asm_code_pA in "F0 F4 F8 FC".split(" ") and asm_code_pB == "6E":
            PUSH = f"PUSH XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH QRn

        if asm_code_pA in "F0 F8 FC".split(" ") and asm_code_pB == "7E":
            PUSH = f"PUSH QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # ADD ERn, #00 - H

        if asm_code_pA in "E0 E2 E4 E6 E8 EA EC EE".split(" ") and (asm_code_pB in add_ERn_ranges):
            ADD = f"ADD ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {ADD}"
            print(instruction)
































































        instructions.append(instruction)

if __name__ == "__main__":
    main()


























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































