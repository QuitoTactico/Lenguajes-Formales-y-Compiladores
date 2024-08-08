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


def equivalences_recognicer(language : list[str], final_states : list[int], func : dict[tuple[int, str], int], debug : bool) -> list[list[tuple]]:
    '''the core of the activity. we recognize the equivalent states using Hopcroft's algorithm in O(n log n)
    https://en.wikipedia.org/wiki/Hopcroft-Karp_algorithm#Pseudocode'''

    states = set(state for state, _ in func.keys()) # the start of each tuple key is a state. set deletes the duplicates
    final_states_set = set(final_states)    # the same list of final states, but making it a set allows us to...
    non_final_states_set = states - final_states_set    # get the non final states

    # they are just a list with both sets. the union of a list, creates the states universe.
    equivs_partitions = [final_states_set, non_final_states_set]     # at the end, it will have sets of equivalent states
    work_partition    = [final_states_set, non_final_states_set]     # we will iterate on this one until it empties

    # if we make smaller and smaller partitions until it's not possible to create more
    # and that partitions are made taken in count to where the states go
    # at the end, the sets with more than one state, will be sets of equivalent states.

    while work_partition:   # while the work partition is not empty...

        extracted_set = work_partition.pop()    # extracts the LAST set of the work list

        for character in language:
            # for each character in the languaje, it gets all the states that receiving
            # that character as input, outputs a state in the extracted set. basically backtracking
            X = {state for state in states if func.get((state, character)) in extracted_set} # BACKTRACK STATES

            # for each set in the equivs partition (starting with the final states)
            for Y in equivs_partitions[:]: # [:] creates a copy, so we don't worry if the original one is modified

                intersection = X & Y    # states in both (states that go to the selected set)
                difference = Y - X      # states in Y, not in X (states that doesn't)

                if intersection and difference: # if both are not empty...

                    equivs_partitions.remove(Y)            # we just accept the new partition
                    equivs_partitions.append(intersection) # and replace the set with the states that go
                    equivs_partitions.append(difference)   # and the states that doesn't

                    # if that set was also in the work partition, we replace it there too to keep iterating
                    if Y in work_partition:
                        work_partition.remove(Y)
                        work_partition.append(intersection)
                        work_partition.append(difference)
                    else:
                        # if not, we append the shorter part of the new partition. there resides the O(n log n)
                        if len(intersection) <= len(difference):
                            work_partition.append(intersection)
                        else:
                            work_partition.append(difference)

                # if one of them was empty, we can't accept that as a valid partition, so it doesn't matter
                # the recursiveness stops in that case

    if debug: print(equivs_partitions)

    # at the end, the equivs partition has all the sets with equivalent states
    # but we need pairs, so we distribute them in all the possible pairs with brute force XD
    equivalences = []
    for group in equivs_partitions:
        group_list = sorted(group)  # set -> sorted list

        # this is like when you multiply (x,y,z) * (a,b,c)
        # you do x*a, x*b, x*c, y*a, ... , z*c (first first, first second, first third, second first, and so on)
        for i in range(len(group_list)):
            for j in range(i + 1, len(group_list)):
                equivalences.append((group_list[i], group_list[j]))

    # what a headache... 
    return equivalences


def equivalences_printer(equivalences : list[list[tuple]]) -> None:
    '''the printing has a specific format. the tuples need to be lexicographically sorted and then printed without commas between tuples'''

    # they were probably sorted since the start (line 117), but whatever-
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
    
    # list of dictionaries with each automata details
    recogniced_automatas = input_recognition(inputs, debug)

    for automata in recogniced_automatas:

        # func (delta) has to be processed to have a [(state, input) -> state] form. Or, well... I wanted it that way.
        func = function_interpreter(automata['raw_func'], automata['language'])

        # the real core of the activity. what a headache...
        equivalences = equivalences_recognicer(language     = automata['language'], 
                                               final_states = automata['final_states'], 
                                               func         = func,
                                               debug        = debug)

        # just the formatting
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