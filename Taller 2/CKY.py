import os

def input_recognition(inputs: list[list[str]]) -> list[dict]:
    '''interpretes the input file lines into grammars and words.
    gives them in a list of dictionaries, each dict contains the grammar and words.'''
    
    recogniced_grammars_and_words = []

    grammars_to_read = int(inputs[0][0])

    index = 1

    for _ in range(grammars_to_read):
        grammar_len = int(inputs[index][0])
        words_len = int(inputs[index][1])

        grammar = {}
        for i in range(index + 1, index + 1 + grammar_len):
            lhs, *rhs = inputs[i] # lhs is the first element, rhs is the rest. rhs are the productions of lhs
            if lhs not in grammar:
                grammar[lhs] = []
            grammar[lhs].extend(rhs)

        words = []
        for i in range(index + 1 + grammar_len, index + 1 + grammar_len + words_len):
            words.append(inputs[i][0])

        recogniced_grammars_and_words.append({
            'grammar': grammar,
            'words': words
        })

        index += 1 + grammar_len + words_len

    return recogniced_grammars_and_words


def cky_algorithm(grammar: dict[str, list[str]], word: str, debug: bool) -> bool:
    '''CYK algorithm to validate if a word is generated by a given grammar.
    returns True if the word is generated by the grammar, False otherwise.'''

    n = len(word)
    table = [[set() for _ in range(n)] for _ in range(n)]

    # initialize
    for i in range(n):
        for lhs, rhs in grammar.items():
            if word[i] in rhs:
                table[i][i].add(lhs)

    # table filling
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for lhs, rhs in grammar.items():
                    for production in rhs:
                        if len(production) == 2:
                            B, C = production
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)

    if debug: print(table)

    # validation
    start_symbol = 'S'  # S is the start symbol everytime
    return start_symbol in table[0][n - 1]


if __name__ == '__main__':

    debug = False  # set True if u wanna see all the process                  # DEBUG <------------------------

    # actual directory of the script
    # this is to use the input file in the same directory independent of the terminal path
    script_dir = os.path.dirname(__file__)
    input_file_path = os.path.join(script_dir, 'input.txt')

    with open(input_file_path, 'r') as file:
        # the input is being read as a string matrix from the start
        inputs = [i.split() for i in file.readlines()]
    
    # list of dictionaries with each grammar details
    recogniced_grammars_and_words = input_recognition(inputs)

    for n, grammar_and_words in enumerate(recogniced_grammars_and_words):

        if debug: print(grammar_and_words)

        grammar = grammar_and_words['grammar']
    
        for word in grammar_and_words['words']:
            # the real core of the activity...
            validation = cky_algorithm(grammar=grammar, 
                                       word=word, 
                                       debug=debug)
            validation_str = 'yes' if validation else 'no'
            print(validation_str)