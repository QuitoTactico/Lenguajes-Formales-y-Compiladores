def input_recognition(inputs : list[str], debug = False) -> list[dict]:
    recogniced_automatas = []

    automatas_to_read = int(inputs[0][0])
    if debug: print('automatas_to_read:', automatas_to_read)

    index = 1
    for automata in range(automatas_to_read):
        automata_len = int(inputs[index][0])

        language = inputs[index+1]
        final_states = list(map(int, inputs[index+2]))
        raw_func = [list(map(int, i)) for i in inputs[index+3 : index+3+automata_len]]
        
        index += automata_len + 3

        recogniced_automatas.append({
            'language'      : language,         # list[str]
            'final_states'  : final_states,     # list[int]
            'raw_func'      : raw_func          # list[list[int]] (needs to be pre-processed)
        })

        if debug:
            print('-'*10)
            print('automata:', automata+1)
            print('index:', index)
            print('final_states:', final_states)
            print('language:', language)
            print('raw_func:', raw_func)
    
    return recogniced_automatas


def function_interpreter(raw_func : list[list[int]], language : list[str]) -> dict[tuple[int, str], int]:
    '''transforms the func/delta matrix into a dict into the [(input_state , input_character) -> output_state] way'''

    func = {} # did you know that a dict can accept tuples as keys? :)

    for i in raw_func:
        # in each row, the first element is the initial state that receives the input character
        input_state = i[0]
    
        # the other elements are the "output states" when the "input state" receives a certain "input character"
        for language_index, output_state in enumerate(i[1:]):

            # those input characters are in the same order that their output states, so...
            input_character = language[language_index]

            # (input_state , input_character) -> output_state
            func[(input_state, input_character)] = output_state
    
    return func


def equivalences_recognicer(language : list[str], final_states : list[int], func : dict[tuple, int]) -> list[list[tuple]]:
    pass


def equivalences_printer(equivalences : list[list[tuple]]) -> None:
    pass


# --------------------------------------------- M A I N ------------------------------------------------------

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        inputs = [i.split() for i in file.readlines()]
    
    debug = True  # set True if u wanna see all the process                 # DEBUG <------------------------

    recogniced_automatas = input_recognition(inputs, debug)

    for automata_case in recogniced_automatas:

        # func (delta) has to be processed to have a [(state, input) -> state] form. Or, well... I wanted it that way.
        func = function_interpreter(automata_case['raw_func'], automata_case['language'])

        '''
        equivalences = equivalences_recognicer(language     = automata_case['language'], 
                                               final_states = automata_case['final_states'], 
                                               func         = func)
        '''

        # equivalences_printer(equivalences)

        if debug: 
            print('-'*10)
            print('automata_case:', automata_case)
            print('func:', func)


'''
    _                ___        _.--.
    \`.|\..----...-'`   `-._.-' _.-'`
    /  ' `         ,       __.-'
    )/' _/     \   `-_,   /              
    `-'" `"\_  ,_.-;_.-\_ ',    
        _.-'_./   {_.'   ; /    E V G
       {_.-``-'         {_/

'''

#dicta = {(2, 'b'): 1, (1, 'a'): 2}