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
        hackstring_input = input("Enter your hackstring, each hex separated by space (aa bb Xc XX), q to quit: ")

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

        if len(asm_code_input) < 3:
            print("Invalid assembly code")
            continue

        result = asm_code_input[::-1]
        print(result)

def dti_2():
    instructions = []
    while True:
        asm_code_input = input("Enter your little endian assembly code,auto-save, e to complete assembly code and print, q to quit: ")

        if asm_code_input.lower() == "q":
            break

        if asm_code_input.lower() == "e":
            print("Completed assembly code:")
            for instruction in instructions:
                print(instruction)
            instructions = []
            continue

        if len(asm_code_input) < 4:
            print("Invalid assembly code")
            continue

        if not all(c in "0123456789ABCDEFabcdef" for c in asm_code_input):
            print("Only hexadecimal characters are allowed")
            continue

        asm_code_input = asm_code_input.upper()
        asm_code_pA = asm_code_input[:2]
        asm_code_pB = asm_code_input[2:]


        if asm_code_input.lower() == "q":
            break

        if asm_code_input.lower() == "e":
            print("Completed Assembly Instructions:")
            for instruction in instructions:
                print(instruction)
            instructions = []  # Clear the list for the next use
            continue  # Continue to accept more inputs

        if len(asm_code_input) < 4:
            print("Invalid assembly code")
            continue

        if not all(c in "0123456789ABCDEFabcdef" for c in asm_code_input):
            print("Only hexadecimal characters are allowed")
            continue

        asm_code_input = asm_code_input.upper()
        asm_code_pA = asm_code_input[:2]
        asm_code_pB = asm_code_input[2:]

        #-----------------------------------------------------------------
        # MOV Rn, #xxH

        if asm_code_pA in "00 01 02 03 04 05 06 07 08 09".split(" "):
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        elif asm_code_pA in ["0A", "0B", "0C", "0D", "0E", "0F"]:
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # MOV Rn, Rm

        elif (asm_code_pA in "80 81 82 83 84 85 86 87 88 89".split(" ")) and (asm_code_pB in "00 10 20 30 40 50 60 70 80 90".split(" ") or asm_code_pB in ["A0", "B0", "C0", "D0", "E0", "F0"]):
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, R{int(asm_code_pB[0], 16)}"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        elif (asm_code_pA in ["8A", "8B", "8C", "8D", "8E", "8F"]) and (asm_code_pB in "00 10 20 30 40 50 60 70 80 90".split(" ") or asm_code_pB in ["A0", "B0", "C0", "D0", "E0", "F0"]):
            MOV = f"MOV R{int(asm_code_pA[1], 16)}, R{int(asm_code_pB[0], 16)}"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # CMP Rn, #xxH

        elif asm_code_pA in "70 71 72 73 74 75 76 77 78 79".split(" "):
            CMP = f"CMP R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        elif asm_code_pA in ["7A", "7B", "7C", "7D", "7E", "7F"]:
            CMP = f"CMP R{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        #-----------------------------------------------------------------
        # MOV ERn, #xxH

        elif asm_code_pA in "E0 E2 E4 E6 E8".split(" "):
            MOV = f"MOV ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        elif asm_code_pA in ["EA", "EC", "EE"]:
            MOV = f"MOV ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # MOV ERn, ERm

        elif (asm_code_pA in ["F0", "F2", "F4", "F6", "F8"] and asm_code_pB in "00 20 40 60 80".split(" ")) or asm_code_pB in ["A0", "C0", "E0"]:
            MOV = f"MOV ER{int(asm_code_pA[1], 16)}, ER{int(asm_code_pB[0], 16)}"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        elif asm_code_pA in ["FA", "FC", "FE"] and (asm_code_pB in "00 20 40 60 80".split(" ") or asm_code_pB in ["A0", "C0", "E0"]):
            MOV = f"MOV ER{int(asm_code_pA[1], 16)}, ER{int(asm_code_pB[0], 16)}"
            instruction = f"{asm_code_input} -> {MOV}"
            print(instruction)

        #-----------------------------------------------------------------
        # CMP ERn, ERm

        elif asm_code_pA in ["F0", "F2", "F4", "F6", "F8"]:
            CMP = f"CMP ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        elif asm_code_pA in ["7A", "7C", "7E"]:
            CMP = f"CMP ER{int(asm_code_pA[1], 16)}, #{asm_code_pB}H"
            instruction = f"{asm_code_input} -> {CMP}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH Rn

        elif asm_code_pA in "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9".split(" ") and asm_code_pB == "4E":
            PUSH = f"PUSH R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        elif asm_code_pA in ["FA", "FB", "FC", "FD", "FE", "FF"] and asm_code_pB == "4E":
            PUSH = f"PUSH R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP Rn

        elif asm_code_pA in "F0 F1 F2 F3 F4 F5 F6 F7 F8 F9".split(" ") and asm_code_pB == "0E":
            POP = f"POP R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        elif asm_code_pA in ["FA", "FB", "FC", "FD", "FE", "FF"] and asm_code_pB == "0E":
            POP = f"POP R{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH ERn

        elif asm_code_pA in "F0 F2 F4 F6 F8".split(" ") and asm_code_pB == "5E":
            PUSH = f"PUSH ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        elif asm_code_pA in ["FA", "FC", "FE"] and asm_code_pB == "5E":
            PUSH = f"PUSH ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP ERn

        elif asm_code_pA in "F0 F2 F4 F6 F8".split(" ") and asm_code_pB == "1E":
            POP = f"POP ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        elif asm_code_pA in ["FA", "FC", "FE"] and asm_code_pB == "1E":
            POP = f"POP ER{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH XRn

        elif asm_code_pA in "F0 F4 F8".split(" ") and asm_code_pB == "6E":
            PUSH = f"PUSH XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        elif asm_code_pA in "FC" and asm_code_pB == "6E":
            PUSH = f"PUSH XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP XRn

        elif asm_code_pA in "F0 F4 F8".split(" ") and asm_code_pB == "2E":
            POP = f"POP XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        elif asm_code_pA in "FC" and asm_code_pB == "2E":
            POP = f"POP XR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        #-----------------------------------------------------------------
        # PUSH QRn

        elif asm_code_pA in "F0 F8".split(" ") and asm_code_pB == "7E":
            PUSH = f"PUSH QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        elif asm_code_pA in "FC" and asm_code_pB == "7E":
            PUSH = f"PUSH QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {PUSH}"
            print(instruction)

        #-----------------------------------------------------------------
        # POP QRn

        elif asm_code_pA in "F0 F8".split(" ") and asm_code_pB == "3E":
            POP = f"POP QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)

        elif asm_code_pA in "FC" and asm_code_pB == "3E":
            POP = f"POP QR{int(asm_code_pA[1], 16)}"
            instruction = f"{asm_code_input} -> {POP}"
            print(instruction)








































        else:
            instruction = f"{asm_code_input} -> Unknown instruction"
            print(instruction)

        instructions.append(instruction)

if __name__ == "__main__":
    main()


























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































