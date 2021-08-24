from itertools import combinations
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
def checker (inp):
    for item in inp:
        if not (inp [item] in ['.', '*', '0', '-']):
            house_value = int (inp [item])
            mine_possibility = int ()
            neighbors_list = neighbor (item)
            for i in neighbors_list:
                if inp [i] == '*':
                    house_value -= 1
                elif inp [i] == '-':
                    mine_possibility += 1
            if house_value < 0 or mine_possibility < house_value:
                return False
    return True
def guess (inp, mine_possibility, house_value):
    changes = list ()
    out = list ()
    for i in combinations (mine_possibility, house_value):
        new_inp = inp.copy ()
        x = bool ()
        for j in i:
            if new_inp [j] != '.':
                new_inp [j] = '*'
                for k in neighbor (j):
                    new_inp = identify100and0 (new_inp, k)
                if checker (new_inp):
                    x = True
                else:
                    x = False
                    break
            else:
                x = False
                break
        if x:
            changes.append (i)
    for i in changes [0]:
        y = True
        for j in range (1, len (changes)):
            if not (i in changes [j]):
                y = False
                break
        if y:
            out.append (i)
    for i in out:
        if inp [i] != '*':
            inp [i] = '*'
            for j in neighbor (i):
                inp = identify100and0 (inp, j)
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
            inp = guess (inp, mine_possibility, house_value)
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

inp_saver = inp.copy ()
while True:
    for item in inp:
        inp = identify100and0 (inp, item)
    if inp == inp_saver:
        break
    inp_saver = inp.copy ()
while True:    
    if '-' in inp.values ():
        for item in inp:
            inp = identify100and0_v2 (inp, item)
    if inp == inp_saver:
        break
    inp_saver = inp.copy ()

print ('\n')
out = list ()
for line in range (8):
    for column in range (7):
        out.append (inp [(line, column)])
    print (' '.join (out))
    out = []