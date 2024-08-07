def input_recognition(inputs : list[list[str]], debug = False) -> list[dict]:
    '''interpretes the input file lines into automatas (language, final_states, raw_func).
    gives them in a list of dictionaries, each dict contains the automata info.'''

    recogniced_automatas = []

    automatas_to_read = int(inputs[0][0])
    if debug: print('automatas_to_read:', automatas_to_read)

    index = 1   # this index is where the "reading pointer" is (row)
    
    for automata in range(automatas_to_read):
        automata_func_len = int(inputs[index][0])   # the first automata input being read. it's the Vlen of the int matrix

        language = inputs[index+1]  # right after that, there is the language characters list
        final_states = list(map(int, inputs[index+2]))  # after that, the final states. map is for int formatting
        raw_func = inputs[index+3 : index+3+automata_func_len] # and finally, the func/delta matrix (string format)

        recogniced_automatas.append({
            'language'      : language,         # list[str]
            'final_states'  : final_states,     # list[int]
            'raw_func'      : raw_func          # list[list[str]] (needs to be pre-processed)
        })

        index += automata_func_len + 3  # "keeps walking" towards the next automata

        if debug:
            print('-'*10)
            print('automata:', automata+1)
            print('index:', index)
            print('final_states:', final_states)
            print('language:', language)
            print('raw_func:', raw_func)
    
    return recogniced_automatas


def function_interpreter(raw_func : list[list[str]], language : list[str]) -> dict[tuple[int, str], int]:
    '''transforms the func/delta matrix into a dict in the [(input_state , input_character) -> output_state] way'''

    func = {} # did you know that a dict can accept tuples as keys? :)

    for i in raw_func:
        # in each row, the first element is the initial state that receives the input character
        input_state = int(i[0])
    
        # the other elements are the "output states" when the "input state" receives a certain "input character"
        for language_index, output_state in enumerate(i[1:]):

            # those input characters are in the same order that their output states, so...
            input_character = language[language_index]

            # (input_state , input_character) -> output_state
            func[(input_state, input_character)] = int(output_state)
    
    return func


def equivalences_recognicer(language : list[str], final_states : list[int], func : dict[tuple, int]) -> list[list[tuple]]:
    '''the core of the activity. damn... i don't know how to do this...'''
    
    return [(1,2), (2,4), (7,8), (1,3), (1,4)]  # provisional


def equivalences_printer(equivalences : list[list[tuple]]) -> None:
    '''the printing has a specific format. the tuples need to be lexicographically sorted and then printed without commas between tuples'''

    sorted_equivalences = sorted(equivalences) # i thought i would have to do this manually, lucky me...

    print(*sorted_equivalences) # this * is called depacking operator, it's not a pointer
    # it "unpacks" the tuples from the list, so they are read by the print as multiple inputs, not as a tuples list. 
    # it's perfect, because the default separator parameter for print() is " "


# --------------------------------------------- M A I N ------------------------------------------------------

if __name__ == '__main__':

    debug = False  # set True if u wanna see all the process                  # DEBUG <------------------------

    with open('input.txt', 'r') as file:
        # the input is being read as a string matrix from the start
        inputs = [i.split() for i in file.readlines()]
    
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