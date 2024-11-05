import First_and_Follow

#def input



if __name__ == "__main__":
    filename = "input.txt"
    grammars, line_index = First_and_Follow.get_firsts_and_follows(filename)

    print(grammars)
    print(line_index)