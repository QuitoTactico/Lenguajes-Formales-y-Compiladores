# README.md

- **Group Members**: 
  - Esteban Vergara Giraldo

- **Operating System**: Windows 10 Pro (x64)
- **Programming Language**: Python 3.12.6 (x64)
- **Tools Used**: 
  - Visual Studio Code 1.93 (Windows x64) [Code Editor]
  - Git 2.46.1 (Windows x64) [Version Control System]

## Instructions for Running the Implementation on Replit

1. Open the following link:   
[![Run on Replit](https://replit.com/badge)](https://replit.com/@QuitoTactico/Lenguajes-Formales-y-Compiladores#Taller%202/CKY.py)  
https://replit.com/@QuitoTactico/Lenguajes-Formales-y-Compiladores#Taller%202/CKY.py

2. (OPTIONAL) Change the input.txt file to the desired input (or use the default one). The input string must be in the following format:

    ```
    <number_of_grammars>
    <number_of_productions_for_grammar_1> <number_of_words_for_grammar_1>
    <lhs_1> <rhs_1>
    <lhs_2> <rhs_2>
    ...
    <word_1>
    <word_2>
    ...
    <number_of_productions_for_grammar_2> <number_of_words_for_grammar_2>
    <lhs_1> <rhs_1>
    <lhs_2> <rhs_2>
    ...
    <word_1>
    <word_2>
    ...
    ```

3. Hit the green "Run" button at the top of the screen.

## Instructions for Running the Implementation Locally

1. Download and decompress the ZIP file, or clone the repository to your local machine using git.

    ```bash
    # If you want to clone the repository.
    # You need to download and install Git from https://git-scm.com/downloads
    git clone https://github.com/QuitoTactico/Lenguajes-Formales-y-Compiladores
    ```

2. Open CMD (command prompt) in the folder you decompressed the zip or cloned the repository, and navigate to the directory where the implementation is located.

    ```bash
    # If you downloaded and decompressed the ZIP file
    cd "Taller 2"
    ```

    ```bash
    # If you cloned the repository
    cd Lenguajes-Formales-y-Compiladores
    cd "Taller 2"
    ```

4. (OPTIONAL) Change the input.txt file to the desired input (or just use the default one). The input string must be in the following format:

    ```
    <number_of_grammars>
    <number_of_productions_for_grammar_1> <number_of_words_for_grammar_1>
    <lhs_1> <rhs_1>
    <lhs_2> <rhs_2>
    ...
    <word_1>
    <word_2>
    ...
    <number_of_productions_for_grammar_2> <number_of_words_for_grammar_2>
    <lhs_1> <rhs_1>
    <lhs_2> <rhs_2>
    ...
    <word_1>
    <word_2>
    ...
    ```

5. Run the `CKY.py` file using.
    
    ```bash
    # On Windows:
    python CKY.py
    ```

    ```bash
    # On Linux:
    python3 CKY.py
    ```

# Proposed CNF Grammar and its Generated Language

The grammar proposed is the $a^n b^n$ (with n >= 1) grammar on CNF.

## Grammar Specifications
```
G = (N, Σ, P, S)

N = {S, C, A, B}  
Σ = {a, b}  
P = {  
    S -> AB | AC,  
    C -> SB,  
    A -> a,  
    B -> b  
}  
S = S  
```
## Generated Language

It generates the context-free language $L(G) =$ { $a^n b^n | n \geq 1$ }.  
L(G) = { a^n b^n | n >= 1 }, if you can't see the LaTeX formula.


For example, some words in the language are:  
L(G) = { ab, aabb, aaabbb, aaaabbbb, ... }

As you see, the language is composed of words with the same number of 'a's and 'b's, and the number of 'a's or 'b's is always greater than 0. So, the language cannot generate the empty string.

## Sucess and Failure Cases

Success cases:
- aabb
- aaaabbbb
- ab
- aaabbb

Failure cases:
- aaaaaaaabbbb
- abab
- aaabbbaabbab
- aabab
- aaababbb
- aabbab
- ε


## Changes in input.txt and their meaning or output

```
4                   # Now there are 4 grammars, not 3
...
4 8                 # Grammar 4: 4 productions, 8 words
S AB AC             # S -> AB | AC
C SB                # C -> SB
A a                 # A -> a
B b                 # B -> b
aabb                # yes
aaaabbbb            # yes
ab                  # yes
aaaaaaaabbbb        # no
abab                # no
aaabbbaabbab        # no
aabab               # no
aaabbb              # yes
```