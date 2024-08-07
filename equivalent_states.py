def automata_creation(inputs, debug = False):
    automatas_to_read = int(inputs[0][0])
    if debug: print('automatas_to_read:', automatas_to_read)

    index = 1
    for automata in range(automatas_to_read):
        automata_len = int(inputs[index][0])
        language = inputs[index+1]
        final_states = list(map(int, inputs[index+2]))
        func = [list(map(int, i)) for i in inputs[index+3 : index+3+automata_len]]

        index += automata_len + 3

        if debug:
            print('-'*10)
            print('automata:', automata+1)
            print('index:', index)
            print('final_states:', final_states)
            print('language:', language)
            print('func:', func)


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        inputs = [i.split() for i in file.readlines()]
    
    #automata_creation(inputs, debug=True)
    automata_creation(inputs)

