import os


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
    else:
        return "terminal"


def firsts(grammar: dict[str, dict[str, set[str]]]) -> None:
    def first(non_terminal: str, recursion: int = 0) -> set:
        # terminal case (1)
        if wtf_is_this(non_terminal) == "terminal":
            return non_terminal

        # non-terminal case (2)
        else:
            # if it has been already calculated
            if grammar[non_terminal]["firsts"]:
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

                # if it reaches the recursion limit, we return the firsts we were capable of obtain
                except:
                    # return grammar[non_terminal]['firsts']
                    pass

            return grammar[non_terminal]["firsts"]

    for non_terminal in grammar.keys():
        non_terminal_firsts = first(non_terminal)

        grammar[non_terminal]["firsts"].update(non_terminal_firsts)


def follows(grammar: dict[str, dict[str, set[str]]]) -> None:
    pass


def result_printer(grammar: dict[str, dict[str, set[str]]]) -> None:
    for result in ["firsts", "follows"]:
        for non_terminal in grammar.keys():
            print(
                f"{result.capitalize()[:-1]}({non_terminal}) = {{{','.join(grammar[non_terminal][result])}}}"
            )


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
        print()


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /
#    `-'" `"\_  ,_.-;_.-\_ ',
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#
