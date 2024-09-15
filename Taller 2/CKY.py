def input_recognition(inputs):
    '''interpretes the input file lines into grammars and words.
    gives them in a list of dictionaries, each dict contains the grammar and words.'''
    
    recogniced_grammars_and_words = []

    grammars_to_read = int(inputs[0][0])

    index = 1

    for grammar in range(grammars_to_read):
        grammar_len = int(inputs[index][0])
        words_len = int(inputs[index][1])

        grammar = {}
        for i in range(index+1, index+1+grammar_len):
            lhs, *rhs = inputs[i]
            grammar[lhs] = rhs

        words = []
        for i in range(index+1+grammar_len, index+1+grammar_len+words_len):
            words.append(inputs[i])

        recogniced_grammars_and_words.append({
            'grammar' : grammar,
            'words' : words
        })

        index += 1 + grammar_len + words_len

    return recogniced_grammars_and_words


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

'''
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
'''


if __name__ == '__main__':

    debug = False  # set True if u wanna see all the process                  # DEBUG <------------------------

    with open('input.txt', 'r') as file:
        # the input is being read as a string matrix from the start
        inputs = [i.split() for i in file.readlines()]
    
    # list of dictionaries with each grammar details
    recogniced_grammars_and_words = input_recognition(inputs)

    for n, grammar_and_words in enumerate(recogniced_grammars_and_words):

        print(grammar_and_words)

        grammar = grammar_and_words['grammar']
    
        for word in grammar_and_words['words']:
            # the real core of the activity...
            validation = cky_algorithm(grammar = grammar,
                                       word = word)
            print(validation)
