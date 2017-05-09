# Sudoku Solver
Multiprocessing Brute-Force Sudoku Solver, written in Python

The code is fairly self explanitory. str_to_puzle converts a puzzle string input to a puzzle list format, where variables are [None] and values are integers. Running solve_puzzle will then convert a puzzle into a solution. 

Running as a program will ask for 9 lines of input, then feed those strings to str_to_puzzle. str_to_puzzle can accept delimeters as ' ', ',' or no delimeter. Variables can be either 'x' or '0'. Examples of puzzles are:

003020600

900305001

001806400

008102900

700000008

006708200

002609500

800203009

005010300

or

2 x x x 8 x 3 x x

x 6 x x 7 x x 8 4

x 3 x 5 x x 2 x 9

x x x 1 x 5 4 x 8

x x x x x x x x x

4 x 2 7 x 6 x x x

3 x 1 x x 7 x 4 x

7 2 x x 4 x x 6 x

x x 4 x 1 x x x 3
