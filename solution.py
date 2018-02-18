assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
 
    # Naked Twins stratety identifies two equal pair of digits in the boxes of a unit
    # E.g. '56' and '56' that means that for sure 5 and 6 are in these two boxes
    # Hence, we can eliminate 5 and 6 from all other boxes of the unit
    
    for unit in unitlist:
                
        buffer = {}
        # Run through unit and collect all pairs of digis to the dictionary:
        # Key of the dictionary is the pair of digits
        # Value of the dictionary is list of all boxes with this pair of digits 
        for box in unit:
            if len(values[box]) == 2:
                if not values[box] in buffer:
                    buffer[values[box]] = [] 
                buffer[values[box]].append(box)
                
        # Now we search for twins and eliminate digits in twins
        # from all other boxes in the unit 
        for digits, boxes in buffer.items():
            if len(boxes) == 2: # if twins...
                for box in unit:
                    if not box in boxes: # ...then from all other boxes...
                        values[box] = values[box].replace(digits[0], '')
                        values[box] = values[box].replace(digits[1], '')

    return values


def cross(a, b):
    "Cross product of elements in a and elements in b."
    return [s+t for s in a for t in b]

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    output = {}
    for i in range(len(boxes)):
        if grid[i] != '.':
            output[boxes[i]] = grid[i]
        else:
            output[boxes[i]] = '123456789'
    return output

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # Find solved boxes
    solved_index = []
    for i, v in values.items():
        if len(v) == 1:
            solved_index.append(i)
            
    # For each solved box, remove its value from all its peers' possible values                 
    for i in solved_index:
        for p in peers[i]:
            values[p] = values[p].replace(values[i], '')

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    
    for unit in unitlist:
        unit_values = {key:values[key] for key in unit}
        for n in '123456789':
            match = [] # We will collect here all boxes within unit that contain digit n
            for k, v in unit_values.items():
                if n in v: # Is the digit is in the box k           
                    match.append(k)
            if len(match) == 1: # If the digit n is found in ounly one box within unit...
                values[match[0]] = n # ...we assign the digit to the box

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminate(values)
        # Use the Only Choice Strategy
        only_choice(values)
        # Naked Twins Strategy
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values.
        # This situation may occur during DFS when we force 
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def is_solved(values):
     return max([len(values[box]) for box in values]) == 1
 
def search(values):
    "Using DFS and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if is_solved(values):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    lengths = [(len(values[box]), box) for box in values if len(values[box]) > 1]
    digg = min(lengths)[1] # Getting fist (left to right) smallest tuple from lengths
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for d in values[digg]:
        hope = values.copy() # Important to create a copy, as dicrioany is mutable
        hope[digg] = d
        solution = search(hope)
        if solution:
            break # Exit the loop here 

    return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    solution = search(grid_values(grid))
    return(solution)

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.

column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.

# The following unit is specific to the "Diagonal Sudoku" problem only!
diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))],
                  [rows[i]+cols[len(cols)-i-1] for i in range(len(rows))]]

diagonal_sudoku = True # Set to False for ormal (non-diagonal Sudoku solution)
unitlist = row_units + column_units + square_units + (diagonal_units if diagonal_sudoku else [])

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')