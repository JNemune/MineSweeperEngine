def identify100and0 (inp, line, column):
    if not (inp [line][column] in ['.', '*', '0', '-']):
        neighbor = int (inp [line][column])
        mine_possibility = int ()
        for neighbor_line in [-1, 0, 1]:
            for neighbor_column in [-1, 0, 1]:
                if 8 > line + neighbor_line >= 0 and 7 > column + neighbor_column >= 0:
                    if inp [line + neighbor_line][column + neighbor_column] == '*':
                        neighbor -= 1
                    elif inp [line + neighbor_line][column + neighbor_column] == '-':
                        mine_possibility += 1
        if neighbor == 0:
            for neighbor_line in [-1, 0, 1]:
                for neighbor_column in [-1, 0, 1]:
                    if 8 > line + neighbor_line >= 0 and 7 > column + neighbor_column >= 0 and inp [line + neighbor_line][column + neighbor_column] == '-':
                        inp [line + neighbor_line][column + neighbor_column] = '.'
                        for neighbor2_line in [-1, 0, 1]:
                            for neighbor2_column in [-1, 0, 1]:
                                if 8 > line + neighbor_line + neighbor2_line >= 0 and 7 > column + neighbor_column + neighbor2_column >= 0 and not (inp [line + neighbor_line + neighbor2_line][column + neighbor_column + neighbor2_column] in ['.', '*', '0', '-']) and (neighbor_line + neighbor2_line, neighbor_column + neighbor2_column) != (0, 0):
                                    inp = identify100and0 (inp, line + neighbor_line + neighbor2_line, column + neighbor_column + neighbor2_column)
        elif mine_possibility == neighbor:
            for neighbor_line in [-1, 0, 1]:
                for neighbor_column in [-1, 0, 1]:
                    if 8 > line + neighbor_line >= 0 and 7 > column + neighbor_column >= 0 and inp [line + neighbor_line][column + neighbor_column] == '-':
                        inp [line + neighbor_line][column + neighbor_column] = '*'
                        for neighbor2_line in [-1, 0, 1]:
                            for neighbor2_column in [-1, 0, 1]:
                                if 8 > line + neighbor_line + neighbor2_line >= 0 and 7 > column + neighbor_column + neighbor2_column >= 0 and not (inp [line + neighbor_line + neighbor2_line][column + neighbor_column + neighbor2_column] in ['.', '*', '0', '-']) and (neighbor_line + neighbor2_line, neighbor_column + neighbor2_column) != (0, 0):
                                    inp = identify100and0 (inp, line + neighbor_line + neighbor2_line, column + neighbor_column + neighbor2_column)
    return inp

inp = list ()
#   'number in range (1, 8)': number that showed in field
#   '0': hole
#   '*': mine
#   '-': unknown pixel
#   '.': zero percent mine finding (It will given by program)
for line in range (8):
    inp.append (input ().split ())

for line in range (8):
    for column in range (7):
        inp = identify100and0 (inp, line, column)

print ('\n')
for line in range (8):
    print (' '.join (inp [line]))