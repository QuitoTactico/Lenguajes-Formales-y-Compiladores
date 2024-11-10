# README.md

- **Group Members**: 
    - Esteban Vergara Giraldo ([QuitoTactico](https://github.com/QuitoTactico))

- **Operating System**: Windows 10 Pro (x64)
- **Programming Language**: Python 3.13.0 (x64)
- **Tools Used**: 
    - Visual Studio Code 1.93 (Windows x64) [Code Editor]
    - Git 2.46.1 (Windows x64) [Version Control System]

- **Project links**:
    - [GitHub Repository](https://github.com/QuitoTactico/Lenguajes-Formales-y-Compiladores/tree/main/Proyecto%20Final)
    - [Replit Repository](https://replit.com/@QuitoTactico/Lenguajes-Formales-y-Compiladores#Proyecto%20Final)

# Instructions for Running

## OPTION 1: On Replit

1. Open the following link:   
[![Run on Replit](https://replit.com/badge)](https://replit.com/@QuitoTactico/Lenguajes-Formales-y-Compiladores#Proyecto%20Final/First_and_Follow.py)  
https://replit.com/@QuitoTactico/Lenguajes-Formales-y-Compiladores#Proyecto%20Final/First_and_Follow.py

2. (OPTIONAL) Change the input.txt file to `set the desired input` (or use the default one). The input string must be in the following format:

    ```
    <number_of_grammars>
    <number_of_productions_for_grammar_1>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_productions_for_grammar_2>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_words>
    <word 1> <target_grammar_1>
    <word 2> <target_grammar_2>
    ...
    ```

3. (OPTIONAL) Change the script's config to `set the used input file` and set if the word analysis process `also prints the productions` used

   ![image](https://github.com/user-attachments/assets/88bf91a2-d790-44af-a0ab-e37a2a4120c6)

4. Hit the green `Run` button at the top of the screen.

## Locally

### OPTION 2: Cloning from GitHub

1. Download Git from [https://git-scm.com/downloads](https://git-scm.com/downloads) and install it.

2. Clone the repository to your local machine using git.

    ```bash
    git clone https://github.com/QuitoTactico/Lenguajes-Formales-y-Compiladores
    ```

3. Navigate to the directory where the implementation is located and locate yourself on the code folder.

    ```bash
    cd Lenguajes-Formales-y-Compiladores
    cd "Proyecto Final"
    ```

4. (OPTIONAL) Change the input.txt file to `set the desired input` (or just use the default one). The input string must be in the following format:

    ```
    <number_of_grammars>
    <number_of_productions_for_grammar_1>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_productions_for_grammar_2>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_words>
    <word 1> <target_grammar_1>
    <word 2> <target_grammar_2>
    ...
    ```
    
5. (OPTIONAL) Change the script's config to `set the used input file` and set if the word analysis process `also prints the productions` used

   ![image](https://github.com/user-attachments/assets/88bf91a2-d790-44af-a0ab-e37a2a4120c6)

6. Run the `First_and_Follow.py` file using:
    
    ```bash
    # On Windows:
    python First_and_Follow.py
    ```

    ```bash
    # On Linux:
    python3 First_and_Follow.py
    ```

### OPTION 3: Decompressing the ZIP file

1. Download and decompress the ZIP file.

2. Open CMD (command prompt) in the folder you decompressed the zip, and locate yourself into the code folder.

    ```bash
    cd "Proyecto Final"
    ```

3. (OPTIONAL) Change the input.txt file to `set the desired input` (or just use the default one). The input string must be in the following format:

    ```
    <number_of_grammars>
    <number_of_productions_for_grammar_1>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_productions_for_grammar_2>
    <non-terminal_1> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    <non-terminal_2> <rhs_1> <rhs_2> <rhs_3> ... <rhs_n>
    ...
    <number_of_words>
    <word 1> <target_grammar_1>
    <word 2> <target_grammar_2>
    ...
    ```

4. (OPTIONAL) Change the script's config to `set the used input file` and set if the word analysis process `also prints the productions` used

   ![image](https://github.com/user-attachments/assets/88bf91a2-d790-44af-a0ab-e37a2a4120c6)

5. Run the `First_and_Follow.py` file using:
    
    ```bash
    # On Windows:
    python First_and_Follow.py
    ```

    ```bash
    # On Linux:
    python3 First_and_Follow.py
    ```

# Proposed alternative input
The first input file, `input.txt`, doesn't have LL(1) grammars, so I designed an alternative input file, `input2.txt`:

![image](https://github.com/user-attachments/assets/0049e9a2-816a-4741-aaf9-983bcadea6a4)

It also provides some words to be syntax analyzed. The scripts need LL(1) grammars to create correctly the syntax analysis matrix and the top down parse the word, so the first input file couldn't be used.

You can use this input file by setting the filename to "input2.txt" in the script's config section:

![image](https://github.com/user-attachments/assets/236ae12b-56b1-467f-90c4-1ee4dcf07300)



