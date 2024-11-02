import os
import copy


def input_recognition(inputs: list[str]) -> list[dict[str, dict[str, set[str]]]]:
    grammars = []

    grammars_to_read = int(inputs[0][0])

    line_index = 1

    for _ in range(grammars_to_read):
        grammar_len = int(inputs[line_index][0])

        grammar = {}

        for i in range(line_index + 1, line_index + 1 + grammar_len):

            non_terminal, *productions = inputs[i]

            if non_terminal not in grammar:
                grammar[non_terminal] = {
                    "productions": set(),
                    "firsts": set(),
                    "follows": set(),
                }

            grammar[non_terminal]["productions"].update(productions)

        grammars.append(grammar)

        line_index += 1 + grammar_len

    return grammars


def wtf_is_this(letter: str) -> str:
    if letter == "e":
        return "epsilon"
    elif letter.isupper():
        return "non-terminal"
    elif len(letter) == 1:
        return "terminal"


def firsts(grammar: dict[str, dict[str, set[str]]]) -> None:
    def first(non_terminal: str, recursion: int = 0, cache: bool = True) -> set:
        # terminal case (1)
        if wtf_is_this(non_terminal) == "terminal":
            return non_terminal

        # non-terminal case (2)
        else:
            # if it has been already calculated and the option is active
            if grammar[non_terminal]["firsts"] and cache:
                return grammar[non_terminal]["firsts"]

            # check for the epsilons first (2.c)
            if "e" in grammar[non_terminal]["productions"]:
                grammar[non_terminal]["firsts"].add("e")

            # if it reached the recursion limit
            elif recursion == 20:
                raise RecursionError

            # for each production of that non-terminal...
            for production in grammar[non_terminal]["productions"]:
                try:
                    non_epsilon_found = False

                    # for each letter of that production...
                    for letter in production:
                        letter_firsts = first(letter, recursion + 1)

                        # if we find an firsts set with no epsilon, we add that set (2.a)
                        if "e" not in letter_firsts:
                            grammar[non_terminal]["firsts"].update(letter_firsts)
                            non_epsilon_found = True
                            break

                    # if every letter has a firsts set with epsilon, we add epsilon (2.b)
                    if non_epsilon_found == False:
                        grammar[non_terminal]["firsts"].add("e")

                # if it reaches the recursion limit, we try with the next production
                except:
                    pass

            return grammar[non_terminal]["firsts"]

    # we will repeat until there's no updates
    while True:
        last_grammar = copy.deepcopy(grammar)

        # we search the firsts for each non-terminal
        for non_terminal in grammar.keys():
            non_terminal_firsts = first(non_terminal, cache=False)

            grammar[non_terminal]["firsts"].update(non_terminal_firsts)

        if grammar == last_grammar:
            break


def follows(grammar: dict[str, dict[str, set[str]]]) -> None:
    def follow(non_terminal: str, recursion: int = 0, cache: bool = True) -> set:
        # if the non-terminal is the initial symbol "S", add $(1)
        if non_terminal == "S":
            grammar[non_terminal]["follows"].add("$")

        # for each production of the non-terminal...
        for production in grammar[non_terminal]["productions"]:

            # for each letter in the production...
            for index, letter in enumerate(production):

                # we will name the non-terminal input as left hand, and the actual letter as right hand letter

                # if we are in a non-terminal right hand...
                if wtf_is_this(letter) == "non-terminal":
                    # there's another letter "beta" after this letter
                    if index != len(production) - 1:

                        beta_firsts = grammar[production[index+1]]["firsts"]
                        
                        # we add beta firsts excepting epsilon (1)
                        grammar[letter]["follows"].update(grammar[production[index+1]]["firsts"]-{'e'})

                        


                    # if the right hand letter is the last one, add the follows of the left hand (3)
                    else:
                        grammar[letter]["follows"].update(
                            grammar[non_terminal]["follows"]
                        )

    # we will repeat until there's no updates
    while True:
        last_grammar = copy.deepcopy(grammar)

        # we search the follows for each non-terminal
        for non_terminal in grammar.keys():
            non_terminal_follows = follow(non_terminal, cache=False)

            grammar[non_terminal]["follows"].update(non_terminal_follows)

        if grammar == last_grammar:
            break


def result_printer(grammar: dict[str, dict[str, set[str]]]) -> None:
    for result in ["firsts", "follows"]:
        for non_terminal in grammar.keys():
            print(
                f"{result.capitalize()[:-1]}({non_terminal}) = {{{','.join(grammar[non_terminal][result])}}}"
            )
    print()


if __name__ == "__main__":

    script_dir = os.path.dirname(__file__)
    input_file_path = os.path.join(script_dir, "input.txt")

    with open(input_file_path, "r") as file:
        inputs = [i.split() for i in file.readlines()]

    grammars = input_recognition(inputs)

    for case_index, grammar in enumerate(grammars):
        firsts(grammar)
        follows(grammar)
        result_printer(grammar)


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /
#    `-'" `"\_  ,_.-;_.-\_ ',
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#
