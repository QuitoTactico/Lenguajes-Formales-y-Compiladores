def cky_algorithm(grammar, word):
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

    # validation
    start_symbol = 'S'  # S is the start symbol everytime
    return start_symbol in table[0][n - 1]

# example
grammar = {
    'S': [('NP', 'VP')],
    'NP': [('Det', 'N')],
    'VP': [('V', 'NP')],
    'Det': ['a'],
    'N': ['dog'],
    'V': ['sees']
}

input_string = "a dog sees".split()
print(cky_algorithm(grammar, input_string))



if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        # the input is being read as a string matrix from the start
        inputs = [i.split() for i in file.readlines()]
    
    # list of dictionaries with each grammar details
    recogniced_grammars_and_words = input_recognition(inputs)

    for n, grammar_and_words in enumerate(recogniced_grammars_and_words):

        grammar = grammar_and_words['grammar']
    
        for word in grammar_and_words['words']:
            # the real core of the activity...
            validation = cky_algorithm(grammar = grammar,
                                       word = word)
            print(validation)
