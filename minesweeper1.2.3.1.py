from itertools import combinations
def neighbor (x):
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
                    for j in neighbor (i):
                        if not (inp [j] in ['.', '*', '0', '-']) and item != j:
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
            mines=list(inp.values()).count('*')
            if house_value < 0 or mine_possibility < house_value or mines>15 or list(inp.values()).count('-')<15-mines:
                return False
    return True
def guess (inp, mine_possibility, house_value):
    change_to_100, change_to_0, out_100, out_0 = list (), list (), list (), list ()
    for i in combinations (mine_possibility, house_value):
        new_inp = inp.copy ()
        x = bool ()
        for j in i:
            if new_inp [j] != '.':
                new_inp [j] = '*'
                for k in neighbor (j):
                    new_inp = identify100and0 (new_inp, k)
                if checker (new_inp): x = True
                else: x = False; break
            else: x = False; break
        if x:
            change_to_100.append (i)
            pre_change_to_0 = list ()
            for i in inp:
                if new_inp [i] == '.' and new_inp [i] != inp [i]: pre_change_to_0.append (i)
            change_to_0.append (pre_change_to_0)
    for i in change_to_100 [0]:
        x = True
        for j in range (1, len (change_to_100)):
            if not (i in change_to_100 [j]): x = False; break
        if x: out_100.append (i)
    for i in change_to_0 [0]:
        x = True
        for j in range (1, len (change_to_0)):
            if not (i in change_to_0 [j]): x = False; break
        if x: out_0.append (i)
    for i in out_100:
        if inp [i] != '*':
            inp [i] = '*'
            for j in neighbor (i): inp = identify100and0 (inp, j)
    for i in out_0:
        if inp [i] != '.':
            inp [i] = '.'
            for j in neighbor (i): inp = identify100and0 (inp, j)
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
def total_mine (inp):
    likely_houses, big_mine_possibility, free_houses, mines = dict (), list (), list (), list (inp.values ()).count ('*')
    for i in inp:
        if inp[i]=='-':free_houses.append(i)
    for item in inp:
        if not (inp [item] in ['.', '*', '0', '-']):
            house_value, mine_possibility=int(inp[item]), list()
            for i in neighbor(item):
                if inp [i] == '*': house_value -= 1
                elif inp [i] == '-': mine_possibility.append (i)
            if len (mine_possibility) != 0 and house_value != 0:
                likely_houses [tuple (mine_possibility)]= house_value
                big_mine_possibility.extend (mine_possibility)
                for i in mine_possibility:
                    try: free_houses.remove(i)
                    except: pass
    min_guess, free_len = 15 - mines - sum(likely_houses.values()), len (free_houses)
    max_guess = min_guess + len (big_mine_possibility) - len (set (big_mine_possibility))
    if min_guess == max_guess == free_len:
        for i in free_houses: inp [i] = '*'
        identify100and0 (inp, i), identify100and0_v2 (inp, i)
        return inp
    if max_guess==0:
        for i in free_houses: inp[i]='.'
        for i in inp: identify100and0(inp,i);identify100and0_v2(inp,i)
        return inp
    if len(likely_houses)!=0 and free_len<max_guess:
        def total_guess(likely_houses_keys, likely_houses_values, mine, out=list (), pre_out=list (), c=0):
            for i in combinations(likely_houses_keys[c], likely_houses_values[c]):
                for j in i: pre_out.append(j)
                if c==len(likely_houses_keys)-1:
                    if len(set(pre_out))<mine: out.append(list(set(pre_out)))
                    for j in range(len(i)): pre_out.pop()
                else:
                    c+=1
                    total_guess(likely_houses_keys, likely_houses_values, mine, out, pre_out, c)
                    c-=1
                    for j in range(len(i)): pre_out.pop()
            return out
        change_to_100, change_to_0, out_100, out_0, guesses = list (), list (), list (), list (), total_guess(list(likely_houses.keys()), list(likely_houses.values()), mines)
        for i in guesses:
            new_inp, identify_check=inp.copy(), True
            for j in i: new_inp[j]='*'
            try:
                for j in new_inp: identify100and0(new_inp, j); identify100and0_v2(new_inp, j)
                total_mine(new_inp)
            except: identify_check=False
            if identify_check and checker(new_inp):
                pre_change_to_0, pre_change_to_100=list(), list()
                for i in inp:
                    if new_inp[i]=='*' and new_inp[i]!=inp[i]: pre_change_to_100.append(i)
                change_to_100.append(pre_change_to_100)
                for i in inp:
                    if new_inp [i] == '.' and new_inp [i] != inp [i]: pre_change_to_0.append (i)
                change_to_0.append (pre_change_to_0)
        for i in change_to_100 [0]:
            x = True
            for j in range (1, len (change_to_100)):
                if not (i in change_to_100 [j]): x = False; break
            if x: out_100.append (i)
        for i in change_to_0 [0]:
            x = True
            for j in range (1, len (change_to_0)):
                if not (i in change_to_0 [j]): x = False; break
            if x: out_0.append (i)
        for i in out_100:
            if inp [i] != '*':
                inp [i] = '*'
                for j in neighbor (i): inp = identify100and0 (inp, j)
        for i in out_0:
            if inp [i] != '.':
                inp [i] = '.'
                for j in neighbor (i): inp = identify100and0 (inp, j)
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
total_mine(inp)
while inp!=inp_saver:
    inp_saver=total_mine(inp).copy()

for i in inp:
    if inp[i]=='.': inp[i]=' '
    if inp[i]=='0': inp[i]=' '
    if inp[i]=='-': inp[i]='?'
print(f'''
╔═══╤═══╤═══╤═══╤═══╤═══╤═══╗
║ {inp[(0, 0)]} │ {inp[(0, 1)]} │ {inp[(0, 2)]} │ {inp[(0, 3)]} │ {inp[(0, 4)]} │ {inp[(0, 5)]} │ {inp[(0, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(1, 0)]} │ {inp[(1, 1)]} │ {inp[(1, 2)]} │ {inp[(1, 3)]} │ {inp[(1, 4)]} │ {inp[(1, 5)]} │ {inp[(1, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(2, 0)]} │ {inp[(2, 1)]} │ {inp[(2, 2)]} │ {inp[(2, 3)]} │ {inp[(2, 4)]} │ {inp[(2, 5)]} │ {inp[(2, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(3, 0)]} │ {inp[(3, 1)]} │ {inp[(3, 2)]} │ {inp[(3, 3)]} │ {inp[(3, 4)]} │ {inp[(3, 5)]} │ {inp[(3, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(4, 0)]} │ {inp[(4, 1)]} │ {inp[(4, 2)]} │ {inp[(4, 3)]} │ {inp[(4, 4)]} │ {inp[(4, 5)]} │ {inp[(4, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(5, 0)]} │ {inp[(5, 1)]} │ {inp[(5, 2)]} │ {inp[(5, 3)]} │ {inp[(5, 4)]} │ {inp[(5, 5)]} │ {inp[(5, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(6, 0)]} │ {inp[(6, 1)]} │ {inp[(6, 2)]} │ {inp[(6, 3)]} │ {inp[(6, 4)]} │ {inp[(6, 5)]} │ {inp[(6, 6)]} ║
╟───┼───┼───┼───┼───┼───┼───╢
║ {inp[(7, 0)]} │ {inp[(7, 1)]} │ {inp[(7, 2)]} │ {inp[(7, 3)]} │ {inp[(7, 4)]} │ {inp[(7, 5)]} │ {inp[(7, 6)]} ║
╚═══╧═══╧═══╧═══╧═══╧═══╧═══╝''')