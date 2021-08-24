def neighbor (x): #finding newborn of x (line, column) house
    out = list ()
    (line, column) = x
    for neighbor_line in [-1, 0, 1]:
        for neighbor_column in [-1, 0, 1]:
            if 8 > line + neighbor_line >= 0 and 7 > column + neighbor_column >= 0 and (neighbor_line, neighbor_column) != (0, 0):
                out.append ((line + neighbor_line, column + neighbor_column))
    return out
def identify100and0 (inp, item):
    if not (inp [item] in ['.', '*', '0', '-']):
        house_value = int (inp [item])
        mine_possibility = list ()
        neighbors_list = neighbor (item)
        for i in neighbors_list:
            if inp [i] == '*':
                house_value -= 1
            elif inp [i] == '-':
                mine_possibility.append (i)
        if house_value == 0:
            for i in neighbors_list:
                if inp [i] == '-':
                    inp [i] = '.'
                    neighbor2_list = neighbor (i)
                    for j in neighbor2_list:
                        if not (inp [j] in ['.', '*', '0', '-']) and i != j:
                            inp = identify100and0 (inp, j)
        elif len (mine_possibility) == house_value:
            for i in neighbors_list:
                if inp [i] == '-':
                    inp [i] = '*'
                    neighbor2_list = neighbor (i)
                    for j in neighbor2_list:
                        if not (inp [j] in ['.', '*', '0', '-']) and i != j:
                            inp = identify100and0 (inp, j)
    return inp

inp = dict ()
#   'number in range (1, 8)': number that showed in field
#   '0': hole
#   '*': mine
#   '-': unknown pixel
#   '.': zero percent mine finding (It will given by program)
for line in range (8):
    pre_inp = input ().split ()
    for column in range (7):
        inp [(line, column)] = pre_inp [column]

for item in inp:
    inp = identify100and0 (inp, item)

print ('\n')
out = list ()
for line in range (8):
    for column in range (7):
        out.append (inp [(line, column)])
    print (' '.join (out))
    out = []