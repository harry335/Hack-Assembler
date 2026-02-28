# Hack Assembler (Python)

## Project Overview
This project is a complete implementation of the **Hack Assembler**, as specified in Project 6 of the "Nand2Tetris" curriculum (The Elements of Computing Systems). It serves as a software bridge that translates symbolic Hack assembly language into binary machine code executable by the Hack hardware platform[cite: 7, 61].

I chose to implement this using **Python** to leverage its string processing capabilities, ensuring a modular and efficient translation process.

---

## Technical Workflow
The translation process follows a structured pipeline to ensure accuracy and handle symbolic references:

1. **File I/O & Pre-processing**: Loads `.asm` files and performs code sanitization.
2. **Code Sanitization**: Removes comments (e.g., `// comment`) and whitespaces to isolate functional instructions.
3. **Instruction Classification**: Identifies each line as an **A-instruction**, **C-instruction**, or a **Label**.
4. **Symbol Resolution**: Utilizing a two-pass approach (or dynamic lookup) to map symbolic labels and variables to specific memory addresses.
5. **Binary Generation**: Converts logical components into 16-bit machine language.



---

## Software Architecture
To ensure high maintainability and logical clarity, the system is designed with four core classes:

| Class | Responsibility |
| :--- | :--- |
| **`Assembler`** | The main driver that orchestrates the overall translation flow. |
| **`Parser`** | Handles text stream input, removes noise, and categorizes instruction types. |
| **`Analysis`** | Deconstructs C-instructions into `dest`, `comp`, and `jump` fields for binary mapping. |
| **`Symbol Table`** | Manages the mapping between symbolic identifiers and RAM/ROM addresses. |

---

## How to Use
1. Place your `.asm` file in the project directory.
2. Run the assembler:
   ```bash
   python hack_assembler.py YourProgram.asm
   ```git add README.md
3. The resulting .hack file will be generated in the same

## Demo Video
Click the image below to watch the implementation demo on YouTube:

[![Hack Assembler Demo](https://img.youtube.com/vi/YM4vuUjm3WM/0.jpg)](https://www.youtube.com/watch?v=YM4vuUjm3WM)