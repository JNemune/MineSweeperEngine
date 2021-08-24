# MineSweeperEngine
Play two-player mine sweeper with engine. The winner of which is the one who finds and disposes more mines.
For more information visit this robot: T.me/minroobot. This engine is going to play the game as a human (maybe better).

map road:
   1) algorithm
       ✅1.1) inputs
       1.2) identify certain houses
           ✅1.2.1) identify with one neighbor
           ✅1.2.2) identify whit more than one neighbor
           1.2.3) use numbers of all mines in the filed
        1.3) probability calculation
        1.4) prepare a checker(generate map and solve it)
            1.4.1) prepare performance reports
        1.5) choice between same-chance houses
            1.5.1) using p (the chance of finding mine) and p' (the opponent's chance if finding mine failed)
                1.5.1.1) max(p-p')
                1.5.1.2) max(p/p')
                1.5.1.3) min(p'/p)
                1.5.1.4) the all methods with checker
            1.5.2) probability of whole and prevent it
                1.5.2.1) identify the whole size
        1.6) negative the algorithm (classic mine sweeper solver)
        1.7) in-vain move for escaping of bad chance
            1.7.1) best play with in-vain move and let the bad chance for opponent
            1.7.2) help to prove the bad chance for opponent and escape the main move(is tha true? check it with checker)
        1.8) Optimization
            1.8.1) prize and turn algorithm
        1.9) prove exiting and performance
            1.9.1) lose and wins of each version
            1.9.2) time and sources of each version
    2) connect to the server
        2.1) connection
            2.1.1) the program and account connection
            2.1.2) the account and telegram connection
        2.2) working with bot
            2.2.1) translate data from bot to program
                2.2.1.1) lose algorithm for advertising
            2.2.2) start a new game automatically
            2.2.3) messages handling
                2.2.3.1) block manager
            2.2.4) request for play again
            2.2.5) get free coin
        2.3) play more than 1 game at the same time and define maximum of same-time games
            2.3.1) duplicate games
            2.3.2) time sleep for movements
            2.3.3) try all fields
                2.3.3.1) improve performance report
                2.3.3.2) use the best way to win(best field and algorithm about time and sources)
        2.4) advertising
            2.4.1) auto answering
            2.4.2) duplicate persons
