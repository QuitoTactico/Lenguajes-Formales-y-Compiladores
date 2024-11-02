import os


def input_recognition(inputs: list[str]) -> list[dict[str, list[str]]]:
    grammars = []

    grammars_to_read = int(inputs[0][0])

    line_index = 1

    for _ in range(grammars_to_read):
        grammar_len = int(inputs[line_index][0])

        grammar = {}
        for i in range(line_index + 1, line_index + 1 + grammar_len):
            non_terminal, *productions = inputs[i]
            if non_terminal not in grammar:
                grammar[non_terminal] = []
            grammar[non_terminal].extend(productions)

        grammars.append(grammar)

        line_index += 1 + grammar_len

    return grammars


if __name__ == "__main__":

    # actual directory of the script
    # this is to use the input file in the same directory independent of the terminal path
    script_dir = os.path.dirname(__file__)
    input_file_path = os.path.join(script_dir, "input.txt")

    with open(input_file_path, "r") as file:
        # the input is being read as a string matrix from the start
        inputs = [i.split() for i in file.readlines()]

    # list of dictionaries with each grammar details
    grammars = input_recognition(inputs)

    for case_index, grammar in enumerate(grammars):
        print(grammar)


#
#    _                ___        _.--.
#    \`.|\..----...-'`   `-._.-' _.-'`
#    /  ' `         ,       __.-'
#    )/' _/     \   `-_,   /
#    `-'" `"\_  ,_.-;_.-\_ ',
#        _.-'_./   {_.'   ; /    E V G
#       {_.-``-'         {_/
#
