import os
import copy
from collections import defaultdict

# ==========================================  Config ========================================

#                                          [ THE ORIGINAL INPUT DOESN'T HAVE LL(1) ]
filename = "input.txt"  # <--------------- [      CHANGE THIS TO "input2.txt"      ]
#                                          [   IF YOU WANT TO SEE ANOTHER EXAMPLE  ]

# =================================  Grammars List Structure: ================================


""" 
grammars = [                                    list,                   values: dicts
    {                                           dict,   keys: strings,  values: dicts
        <non-terminal X> : {                    dict,   keys: strings,  values: sets
            "productions" : (                   set,                    values: strings
                <production Y1Y2Y3..Yk>,        string
                ...
            ),
            "firsts" : (                        set,                    values: strings
                <first a>,                      string
                ...
            ),
            "follows" : (                       set,                    values: strings
                <follow b>,                     string
                ...
            ),
            "productions_firsts" : (            set,                    values: tuples
                (                               tuple,                  values: string, tuple
                    <production Y1Y2Y3..Yk>,     
                    (                           tuple,                  values: strings
                        <production_first c>,   string
                        ...
                    )
                ),
                ...
            },
        },
        ...
    },
    ...  
]
"""


# =================================== FIRSTS AND FOLLOWS =====================================


def input_grammar_recognition(
    inputs: list[list[str]],
) -> tuple[list[dict[str, dict[str, set]]], int]:
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
                    "productions_firsts": set(),  # useful for the SAM
                }

            grammar[non_terminal]["productions"].update(productions)

        grammars.append(grammar)

        line_index += 1 + grammar_len

    return grammars, line_index


def get_all_firsts_and_follows(
    filename: str,
) -> tuple[list[dict[str, dict[str, set]]], int]:
    """master function that executes the first and follow function for each grammar"""

    # get inputs as a matrix
    inputs = get_raw_inputs(filename)

    # matrix is parsed into a list of dictionaries with it's non-terminals as keys
    # each non-terminal value is another dictionary with "productions", "firsts" and "follows"
    grammars, line_index = input_grammar_recognition(inputs)

    # we fill the "firsts" and "follows" dictionary of each non-terminal, and """"that's all"""" (horrific XD)
    for grammar in grammars:
        firsts_and_follows(grammar)

    return grammars, line_index


def symbol_categorizer(letter: str) -> str:
    if letter == "e":
        return "epsilon"

    elif letter.isupper():
        return "non-terminal"

    elif len(letter) == 1:
        return "terminal"


def firsts_and_follows(
    grammar: dict[str, dict[str, set]], words_firsts: bool = False
) -> None:

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

    # only available for symbols
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
            if search == "firsts":
                for non_terminal in grammar.keys():
                    non_terminal_firsts = firsts_for_symbols(non_terminal, cache=False)
                    grammar[non_terminal]["firsts"].update(non_terminal_firsts)
            elif search == "follows":
                for non_terminal in grammar.keys():
                    non_terminal_follows = follows(non_terminal, cache=False)
                    grammar[non_terminal]["follows"].update(non_terminal_follows)
            elif search == "productions_firsts":
                for non_terminal in grammar.keys():
                    for production in grammar[non_terminal]["productions"]:
                        production_firsts = firsts_for_words(production)
                        prod_firsts_tuple = (production, tuple(production_firsts))
                        grammar[non_terminal]["productions_firsts"].add(
                            prod_firsts_tuple
                        )

            # if there's no updates in an iteration, if finishes the search
            if grammar == last_grammar:
                break

    # principal search body
    search_select("firsts")
    search_select("follows")
    search_select("productions_firsts")  # useful for the SAM


def result_printer_first_and_follow(grammars: list[dict[str, dict[str, set]]]) -> None:
    """just prints the first and follows result according to the proposed output syntax"""
    for grammar in grammars:
        for result in ["firsts", "follows"]:
            for non_terminal in grammar.keys():
                print(
                    f"{result.capitalize()[:-1]}({non_terminal}) = {{{','.join(grammar[non_terminal][result])}}}"
                )
        print()


# ==================================== TOP-DOWN PARSER =======================================


def LL1_validation(grammar: dict[str, dict[str, set]]) -> bool:
    pass


def create_syntax_analysis_matrix(
    grammar: dict[str, dict[str, set]]
) -> dict[tuple, str]:
    """creates the syntax analysis matrix (SAM) for a specific grammar, based on its productions, and the firsts and follows of each non-terminal
    it's used for the top-down parsing in the table-driven predictive parsing algorithm
    it also provides an additional proof of not being LL(1) if an intersection has more that one value
    """

    SAM = defaultdict(list)
    is_LL1 = True

    for non_terminal in grammar.keys():
        non_terminal_follows = grammar[non_terminal]["follows"]
        # for each A → α...
        for production, production_firsts in grammar[non_terminal][
            "productions_firsts"
        ]:

            # for a in Pr(α)...
            for first in production_firsts:
                if first != "e":

                    # add A → α to M[A,a]
                    if production not in SAM[(non_terminal, first)]:
                        SAM[(non_terminal, first)].append(production)

            # if epsilon in Pr(α)
            if "e" in production_firsts:

                # for terminal b in Sig(A)
                for follow in non_terminal_follows:
                    if symbol_categorizer(follow) == "terminal":

                        # add A → α to M[A,b]
                        if production not in SAM[(non_terminal, follow)]:
                            SAM[(non_terminal, follow)].append(production)

            # if epsilon in Pr(α) and $ in Sig (A)
            if "e" in production_firsts and "$" in non_terminal_follows:

                # add A → α to M[A,$]
                if production not in SAM[(non_terminal, "$")]:
                    SAM[(non_terminal, "$")].append(production)

    # additional to the LL(1) direct verification,
    # if an intersetion has two or more values, it's not LL(1)
    for i in SAM.values():
        if len(i) > 1:
            is_LL1 = False

    return SAM, is_LL1


def SAM_printer(
    SAM: dict[tuple, str], grammar: dict[str, dict[str, set]], is_LL1_extra: bool
) -> None:
    """eh... yeah, prints the SAM, duuuh
    maybe it will look strange if an intersection has 2 or more productions, but that's for non LL(1) grammars
    """

    # get every terminal and non-terminal
    # non-terminals on input order
    non_terminals = grammar.keys()
    # terminals on reverse alphanumeric order (just to have the $ at the end)
    terminals = sorted(set(key[1] for key in SAM.keys()), reverse=True)

    # let's create a matrix to print this shit (aaaaaaah)
    # initialize with ""
    matrix = [[""] * (len(terminals) + 1) for _ in range(len(non_terminals) + 1)]

    # put the terminals up there
    matrix[0][1:] = terminals

    for i, non_terminal in enumerate(non_terminals, start=1):
        # put the non-terminals at the left
        matrix[i][0] = non_terminal

        # put everything else in the middle
        for j, terminal in enumerate(terminals, start=1):

            # separate productions on the same intersection with commas (hoping it doesn't look bad)
            # if an intersection doesn't exist, put "" again
            matrix[i][j] = ", ".join(SAM.get((non_terminal, terminal), ""))

    # print that matrix separating every item with a tab
    for row in matrix:
        print("\t".join(row))

    if not is_LL1_extra:
        print(
            "\nYou see?, there's two or more values in the same intersection\nit's not LL(1) and this table can't be used."
        )

    print()


def input_words_recognition(
    inputs: list[list[str]],
) -> list[tuple[str, int]]:
    pass


def get_all_parsing(filename: str, line_index: int) -> list[bool]:
    pass


def result_printer_parsing():
    pass


# ======================================= MAIN BODY ==========================================


def get_raw_inputs(filename: str) -> list[list[str]]:
    """returns the contents of the input file as a string matrix"""

    # input file needs to be in the same folder of this code
    script_dir = os.path.dirname(__file__)
    input_file_path = os.path.join(script_dir, filename)

    # input is read as a matrix
    with open(input_file_path, "r") as file:
        inputs = [i.split() for i in file.readlines()]

    return inputs


if __name__ == "__main__":

    grammars, line_index = get_all_firsts_and_follows(filename)
    result_printer_first_and_follow(grammars)

    print("\n", "=" * 15, "Extra: Top-Down parser", "=" * 15)
    SAMs = {}
    for grammar_index, grammar in enumerate(grammars, start=1):
        print("=" * 10, "Grammar", grammar_index, "=" * 10)
        is_LL1 = LL1_validation(grammar)
        print(
            "It's LL(1)"
            if is_LL1
            else "It's NOT LL(1), we can't top-down parse it with this code."
        )

        SAM, is_LL1_extra = create_syntax_analysis_matrix(grammar)
        SAM_printer(SAM, grammar, is_LL1_extra)
        SAMs[grammar_index] = SAM

    # syntax_analysis = get_all_parsing(filename)
    # result_printer_parsing(syntax_analysis)


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /
#    `-'" `"\_  ,_.-;_.-\_ ',
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#
