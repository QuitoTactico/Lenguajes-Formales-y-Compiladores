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
    def first(letter: str):
        if wtf_is_this(letter) == "terminal":
            grammar

    for i in grammar.keys():
        print(i)


def follows(grammar: dict[str, dict[str, set[str]]]) -> None:
    pass


def result_printer(grammar: dict[str, dict[str, set[str]]]) -> None:
    pass


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
