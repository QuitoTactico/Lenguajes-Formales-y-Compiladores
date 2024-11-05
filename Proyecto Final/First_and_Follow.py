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

    return grammars, line_index


def symbol_categorizer(letter: str) -> str:
    if letter == "e":
        return "epsilon"

    elif letter.isupper():
        return "non-terminal"

    elif len(letter) == 1:
        return "terminal"


def firsts_and_follows(grammar: dict[str, dict[str, set[str]]]) -> None:

    def firsts_for_symbols(
        non_terminal: str,
        recursion: int = 0,
        cache: bool = True,
    ) -> set:
        # terminal case, we return it (1)
        if symbol_categorizer(non_terminal) in ["terminal", "epsilon"]:
            return {non_terminal}

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

                    # for each symbol of that production...
                    for symbol in production:
                        symbol_firsts = firsts_for_symbols(symbol, recursion + 1)

                        # if we find a firsts set with no epsilon, we add that set (2.a)
                        if "e" not in symbol_firsts:
                            grammar[non_terminal]["firsts"].update(symbol_firsts)
                            non_epsilon_found = True
                            break

                    # if every symbol has a firsts set that includes epsilon, we add epsilon (2.b)
                    if not non_epsilon_found:
                        grammar[non_terminal]["firsts"].add("e")

                # if it reaches the recursion limit, we try with the next production
                except RecursionError:
                    pass

            return grammar[non_terminal]["firsts"]

    def firsts_for_words(word: str) -> set:
        word_firsts = set()

        # for every symbol in that word...
        for index, symbol in enumerate(word):
            symbol_firsts = firsts_for_symbols(symbol)

            # add every non-epsilon symbols of that symbol firsts (1)
            word_firsts.update(symbol_firsts - {"e"})

            # we keep adding the firsts of each symbol until there's no epsilon in the search (2, 3)
            if "e" not in symbol_firsts:
                break

            # if we are in the last symbol and epsilon was in every firsts set, we add epsilon (4)
            elif index == len(word) - 1:
                word_firsts.add("e")

        return word_firsts

    # only avaliable for symbols
    def follows(
        non_terminal: str,
        recursion: int = 0,
        cache: bool = True,
    ) -> set:
        # if the non-terminal is the initial symbol "S", add $ (1)
        if non_terminal == "S":
            grammar[non_terminal]["follows"].add("$")

        # for each production of this non-terminal...
        for production in grammar[non_terminal]["productions"]:

            # for each symbol in that production...
            for index, symbol in enumerate(production):

                # if that symbol is a non-terminal and has a word "beta" after itself,
                # add the firsts of beta excepting epsilon to that symbol's follows (2)
                if symbol_categorizer(symbol) == "non-terminal":

                    if index != len(production) - 1:

                        beta = production[index + 1 :]
                        beta_firsts = firsts_for_words(beta)

                        grammar[symbol]["follows"].update(beta_firsts - {"e"})

                        # if epsilon is in that beta firsts, add the non-terminal's follows to this symbol's follows (4)
                        if "e" in beta_firsts:
                            grammar[symbol]["follows"].update(
                                grammar[non_terminal]["follows"]
                            )

                    # if it's the last symbol in that production, also add the non-terminal's follows to this symbol's follows (3)
                    else:
                        grammar[symbol]["follows"].update(
                            grammar[non_terminal]["follows"]
                        )

        return grammar[non_terminal]["follows"]

    def search_select(search: str) -> None:
        # we will repeat until there's no updates
        while True:
            last_grammar = copy.deepcopy(grammar)

            # we search the firsts or follows for each non-terminal
            for non_terminal in grammar.keys():
                if search == "firsts":
                    non_terminal_firsts = firsts_for_symbols(non_terminal, cache=False)
                    grammar[non_terminal]["firsts"].update(non_terminal_firsts)
                elif search == "follows":
                    non_terminal_follows = follows(non_terminal, cache=False)
                    grammar[non_terminal]["follows"].update(non_terminal_follows)

            # if there's no updates in an iteration, if finishes the search
            if grammar == last_grammar:
                break

    # principal search body
    search_select("firsts")
    search_select("follows")


# ======================== MAIN BODY ========================


def get_firsts_and_follows(filename: str) -> list[dict[str, dict[str, set[str]]]]:
    # input needs to be in the same folder of this code
    script_dir = os.path.dirname(__file__)
    input_file_path = os.path.join(script_dir, filename)

    # input is read as a matrix
    with open(input_file_path, "r") as file:
        inputs = [i.split() for i in file.readlines()]

    # matrix is parsed into a list of dictionaries with it's non-terminals as keys
    # each non-terminal value is another dictionary with "productions", "firsts" and "follows"
    grammars, line_index = input_recognition(inputs)

    # we fill the "firsts" and "follows" dictionary of each non-terminal, and """"that's all"""" (horrific XD)
    for grammar in grammars:
        firsts_and_follows(grammar)

    return grammars, line_index


def result_printer(grammars: list[dict[str, dict[str, set[str]]]]) -> None:
    for grammar in grammars:
        for result in ["firsts", "follows"]:
            for non_terminal in grammar.keys():
                print(
                    f"{result.capitalize()[:-1]}({non_terminal}) = {{{','.join(grammar[non_terminal][result])}}}"
                )
        print()


if __name__ == "__main__":
    filename = "input.txt"
    grammars, line_index = get_firsts_and_follows(filename)
    result_printer(grammars)


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /
#    `-'" `"\_  ,_.-;_.-\_ ',
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#
