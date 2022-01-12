def readInput(path="input.txt"):
        f = open(path, "r")
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')]
                          for line in lines[1:6]]

        board = [[int(x) for x in line.rstrip('\n')]
                 for line in lines[6: 12]]

        f.close()

        return piece_type, previous_board, board