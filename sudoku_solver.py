from multiprocessing.pool import Pool


def test_solution(puzzle, solution):
    # column index and row index
    ci = 0
    ri = 0

    # Create a copy of the puzzle to work in.
    # It is easier to create a copy, move the solution
    # into it, and check that. Otherwise I'd have to
    # keep track of where all the previous values lie
    # in the puzzle without putting them there.
    test_puzzle = [list(row) for row in puzzle]
    for sol_val in solution:
        # Find the next empty spot that this puzzle can lie in.
        while test_puzzle[ri][ci] is not None:
            ci += 1
            if ci >= 9:
                ci = 0
                ri += 1

                if ri >= 9:
                    break

        if ri >= 9:
            break

        # Is this value in the row? Leave.
        if sol_val in test_puzzle[ri]:
            return False

        # Is this value in the column? Leave.
        if sol_val in (x[ci] for x in test_puzzle):
            return False

        # Is this value in the box? Leave.
        for box_ri in range((ri // 3) * 3, (ri // 3) * 3 + 3):
            for box_ci in range((ci // 3) * 3, (ci // 3) * 3 + 3):
                if test_puzzle[box_ri][box_ci] == sol_val:
                    return False

        # This value is good, add it to the solution and continue.
        test_puzzle[ri][ci] = sol_val

    # All values added, this is an acceptable solution (or partial solution)
    return True


def solve_puzzle(x, process_count=5):
    """Takes in a sudoku puzzle and returns the solution

    Args:
        x (9x9 2D array with integer or Null values): The puzzle to solve.

    Return:
        A 9x9 2D array with integer values: The solution of the puzzle.
    """

    ### Check the input argument. ###
    # Be idiot proof.
    input_value_error = "The input array must be 9x9 with integer or Null elements!"
    if len(x) != 9:
        raise Exception(input_value_error)

    # Recreate the puzzle to work in.
    puzzle = [[None] * 9 for i in range(9)]
    # Also count the variable count, so we know when to kill this.
    var_count = 0
    for ri, row in enumerate(x):
        if len(row) != 9:
            raise Exception(input_value_error)

        for ci, element in enumerate(row):
            if element is None or element in ['x', '0']:
                var_count += 1
                continue

            puzzle[ri][ci] = int(element)

    if var_count == 0:
        return puzzle

    ### Brute force. ###
    # The puzzle has been checked and made. Solve it via brute force.
    # Create the seed solutions. Just put 1 through 9 in the first spot.
    possible_solutions = [[i+1] for i in range(9)]
    # Create a multiprocess pool to speed test computations. 
    with Pool(process_count) as p:
        while True:
            # Delete the solutions that are too long.
            for solution in possible_solutions:
                if len(solution) > var_count:
                    del solution

            # Leave if we've gone over.
            if len(possible_solutions) == 0:
                raise Exception("No solutions found!!")

            # Test all the possible solutions currently in the pool. Also, create a new pool.
            test_solutions = possible_solutions
            test_success = p.starmap(test_solution, ((puzzle, solution) for solution in test_solutions))
            possible_solutions = []

            for i, success in list(enumerate(test_success)):
                # Only if this solution is ok.
                if success:
                    # If we have a solution the size of the var count, then we have a final solution. Leave.
                    if len(test_solutions[i]) == var_count:
                        for ri, row in enumerate(puzzle):
                            for ci, element in enumerate(row):
                                if element is None:
                                    puzzle[ri][ci] = test_solutions[i][0]
                                    del test_solutions[i][0]

                        return puzzle

                    # else we need to keep solving. Enumerate all the possible solutions with length n+1 using this solution.
                    for j in range(9):
                        possible_solutions.append(test_solutions[i] + [j+1])


def str_to_puzzle(input_str):
    puzzle = [[None] * 9 for i in range(9)]

    for row_i, raw_row in enumerate(input_str.split('\n')):
        for column_i, value in enumerate([x for x in list(raw_row) if x not in [',', ' ']]):
            puzzle[row_i][column_i] = int(value) if value.lower() not in ['x', '0'] else None

    return puzzle


if __name__ == '__main__':
    print("Welcome to the sudoku solver!")
    print("Enter your puzzle (spaces between numbers, use 'x' for unknown values): ")

    # Allocate the puzzle, AVOID append AT ALL COSTS
    puzzle = ''

    # Gather input from the user.
    for row_i in range(9):
        raw_row = input("")
        puzzle += raw_row + '\n'

    puzzle = str_to_puzzle(puzzle[:-1])
    print(puzzle)

    print("\nSolving.....\n")

    solution = solve_puzzle(puzzle, process_count=8)

    print("Done! The solution is as follows: ")

    for row_i in range(9):
        print(" ".join(map(str, solution[row_i])))
