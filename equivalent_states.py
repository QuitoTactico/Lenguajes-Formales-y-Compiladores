def input_recognition(inputs : list[str], debug = False) -> list[dict]:
    '''interpretes the input file lines into automatas (language, final_states, raw_func).
    gives them in a list of dictionaries, each dict contains the automata info.'''

    recogniced_automatas = []

    automatas_to_read = int(inputs[0][0])
    if debug: print('automatas_to_read:', automatas_to_read)

    index = 1
    for automata in range(automatas_to_read):
        automata_func_len = int(inputs[index][0])

        language = inputs[index+1]
        final_states = list(map(int, inputs[index+2]))
        raw_func = [list(map(int, i)) for i in inputs[index+3 : index+3+automata_func_len]] # this one needs explanation, probably
        
        index += automata_func_len + 3

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
    '''transforms the func/delta matrix into a dict in the [(input_state , input_character) -> output_state] way'''

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
    '''the core of the activity. damn... i don't know how to do this...'''
    
    return [(1,2), (2,4), (7,8), (1,3), (1,4)]  # provisional


def equivalences_printer(equivalences : list[list[tuple]]) -> None:
    '''the printing has a specific format. the tuples need to be lexicographically sorted and then printed without commas between tuples'''

    sorted_equivalences = sorted(equivalences) # i thought i would have to do this manually, lucky me...

    print(*sorted_equivalences) # this * is called depacking operator
    # it "unpacks" the tuples from the list, so they are read by the print as multiple inputs, not as a tuples list. 
    # it's perfect, because the default separator parameter for print() is " "


# --------------------------------------------- M A I N ------------------------------------------------------

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        inputs = [i.split() for i in file.readlines()]
    
    debug = False  # set True if u wanna see all the process                  # DEBUG <------------------------

    recogniced_automatas = input_recognition(inputs, debug)

    for automata in recogniced_automatas:

        # func (delta) has to be processed to have a [(state, input) -> state] form. Or, well... I wanted it that way.
        func = function_interpreter(automata['raw_func'], automata['language'])

        # the real core of the activity. what a headache...
        equivalences = equivalences_recognicer(language     = automata['language'], 
                                               final_states = automata['final_states'], 
                                               func         = func)

        equivalences_printer(equivalences)

        if debug: 
            print('-'*10)
            print('automata:', automata)
            print('func:', func)
            print('equivalences (pre-formatting):', equivalences)


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /              
#    `-'" `"\_  ,_.-;_.-\_ ',    
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#