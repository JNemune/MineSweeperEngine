def neighbor (x): #finding neighbors of x (line, column) house
    out = list ()
    (line, column) = x
    for neighbor_line in [-1, 0, 1]:
        for neighbor_column in [-1, 0, 1]:
            if 8 > line + neighbor_line >= 0 and 7 > column + neighbor_column >= 0 and (neighbor_line, neighbor_column) != (0, 0):
                out.append ((line + neighbor_line, column + neighbor_column))
    return out
def common_neighbor_finder (inp): #finding common neighbors between houses in inp
    out = list ()
    neighbors_list = list ()
    for i in inp:
        neighbors_list.append (neighbor (i))
    for i in neighbors_list [0]:
        x = 0
        for j in range (1, len (inp)):
            if not (i in neighbors_list [j]):
                x = 1
                break
        if x == 0:
            out.append (i)
    return (out)
def guess (inp, mine_possibility, house_value):
    changes = list ()
    house_value -= 1
    for i in mine_possibility:
        changes.append (i)
        if len (changes) == house_value + 1:
            
            yield inp
        else:
            guess (inp)
def identify100and0 (inp, item, unknown_valued_list, unknown_valued_mine_possibility):
    if not (inp [item] in ['.', '*', '0', '-']):
        house_value = int (inp [item]) - unknown_valued_mine_possibility
        mine_possibility = list ()
        neighbors_list = neighbor (item)
        for i in unknown_valued_list:
            neighbors_list.remove (i)
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
                        if not (inp [j] in ['.', '*', '0', '-']) and item != j:
                            inp = identify100and0 (inp, j, [], 0)
        elif len (mine_possibility) == house_value:
            for i in mine_possibility:
                inp [i] = '*'
                neighbor2_list = neighbor (i)
                for j in neighbor2_list:
                    if not (inp [j] in ['.', '*', '0', '-']) and item != j:
                        inp = identify100and0 (inp, j, [], 0)
        elif len (mine_possibility) < 5:
            common_neighbors = common_neighbor_finder (mine_possibility)
            common_neighbors.remove (item)
            for i in common_neighbors:
                identify100and0 (inp, i, mine_possibility, house_value)
    return inp
def identify100and0_v2 (inp, item):
    if not (inp [item] in ['.', '*', '0', '-']):
        house_value = int (inp [item])
        mine_possibility = list ()
        neighbors_list = neighbor (item)
        for i in neighbors_list:
            if inp [i] == '*':
                house_value -= 1
            elif inp [i] == '-':
                mine_possibility.append (i)
        if len (mine_possibility) != 0 and house_value != 0:
            new_inp = guess (inp, item, house_value)
            

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
    inp = identify100and0 (inp, item, [], 0)

print ('\n')
out = list ()
for line in range (8):
    for column in range (7):
        out.append (inp [(line, column)])
    print (' '.join (out))
    out = []