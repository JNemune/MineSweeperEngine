from itertools import combinations
from random import randint
from os import system, name
def clear():
    if name=='posix': system('clear')
    if name=='nt': system ('cls')
    print ('''
    ╔═══════════════════════════╗
    ║    minesweeper1.2.3.2     ║
    ╠═══════════════════════════╣
    ║    Powered by JNemune     ║
    ╚═══════════════════════════╝''')
    system(f"color {['A', 'B', 'C', 'D', 'E', 'F'][randint(0, 5)]}")
def whole_checker (x, y):
    try:
        if int(x)<0 or int(x)>y: print ('Invalid input!'); return whole_checker(input('Please send an whole number: '), y)
        return int(x)
    except: print('Invalid input!'); return whole_checker (input ('Please send an whole number: '), y)
def input_(inp):
    pre_inp, fucking_inp=dict(), input('inp= ')
    if fucking_inp=='exit': return 'exit'
    if fucking_inp=='new': return 'new'
    while len(fucking_inp)!=3 or not fucking_inp[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '*']: print('invalid input!'); fucking_inp=input('inp= ')
    column, line, x=7-whole_checker(fucking_inp[0], 7), whole_checker(fucking_inp[1], 8)-1, fucking_inp[2]
    while line!=-1 and column!=7:
        pre_inp[(line, column)], fucking_inp=x, input('inp= ')
        while len(fucking_inp)!=3 or not fucking_inp[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '*']: print('invalid input!'); fucking_inp=input('inp= ')
        column, line, x=7-whole_checker(fucking_inp[0], 7), whole_checker(fucking_inp[1], 8)-1, fucking_inp[2]
    for i in pre_inp: inp[i]=pre_inp[i]
    return inp
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
        if inp[i]=='-': free_houses.append(i)
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
    if len(likely_houses)!=0:
        def total_guess(likely_houses_keys, likely_houses_values, out=list (), pre_out=list (), c=0):
            for i in combinations(likely_houses_keys[c], likely_houses_values[c]):
                for j in i: pre_out.append(j)
                if c==len(likely_houses_keys)-1:
                    out.append(list(set(pre_out)))
                    for j in range(len(i)): pre_out.pop()
                else:
                    c+=1
                    total_guess(likely_houses_keys, likely_houses_values, out, pre_out, c)
                    c-=1
                    for j in range(len(i)): pre_out.pop()
            return out
        change_to_100, change_to_0, out_100, out_0, guesses = list (), list (), list (), list (), total_guess(list(likely_houses.keys()), list(likely_houses.values()))
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

clear()
beginning_inp={(0, 0): '-', (0, 1): '-', (0, 2): '-', (0, 3): '-', (0, 4): '-', (0, 5): '-', (0, 6): '-', (1, 0): '-', (1, 1): '-', (1, 2): '-', (1, 3): '-', (1, 4): '-', (1, 5): '-', (1, 6): '-', (2, 0): '-', (2, 1): '-', (2, 2): '-', (2, 3): '-', (2, 4): '-', (2, 5): '-', (2, 6): '-', (3, 0): '-', (3, 1): '-', (3, 2): '-', (3, 3): '-', (3, 4): '-', (3, 5): '-', (3, 6): '-', (4, 0): '-', (4, 1): '-', (4, 2): '-', (4, 3): '-', (4, 4): '-', (4, 5): '-', (4, 6): '-', (5, 0): '-', (5, 1): '-', (5, 2): '-', (5, 3): '-', (5, 4): '-', (5, 5): '-', (5, 6): '-', (6, 0): '-', (6, 1): '-', (6, 2): '-', (6, 3): '-', (6, 4): '-', (6, 5): '-', (6, 6): '-', (7, 0): '-', (7, 1): '-', (7, 2): '-', (7, 3): '-', (7, 4): '-', (7, 5): '-', (7, 6): '-'}
inp=input_(beginning_inp.copy())
clear()
while inp!='exit':
    while not inp in ['new', 'exit']:
        inp_saver = inp.copy ()
        while True:
            for item in inp: inp=identify100and0 (inp, item)
            if inp == inp_saver: break
            inp_saver=inp.copy()
        while True:    
            if '-' in inp.values():
                for item in inp: inp=identify100and0_v2(inp, item)
            if inp==inp_saver: break
            inp_saver=inp.copy()
        total_mine(inp)
        while inp!=inp_saver:
            inp_saver=total_mine(inp).copy()

        inp_print=inp.copy()
        for i in inp_print:
            if inp_print[i]=='.':
                neighbors=list()
                for j in neighbor(i): neighbors.append(inp_print[j])
                if not '-' in neighbors: inp_print[i]=neighbors.count('*')
        for i in inp_print:
            if inp_print[i]=='-': inp_print[i]=' '
        print('''
    ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╗
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╟───┼───┼───┼───┼───┼───┼───╢
    ║ {} │ {} │ {} │ {} │ {} │ {} │ {} ║
    ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╝'''.format(*list(inp_print.values())))
        inp=input_(inp)
        clear()
    inp=input_(beginning_inp.copy())
    clear()