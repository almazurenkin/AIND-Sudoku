# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We introduce Naked Twins strategy in addition to Elimination and Only Choice.

The Naked Twins strategy "looks" for two boxes within a unit that both have the
same two possible digits, e.g. "12" and "12". Existance of such a pair means that
digits "1" and "2" are surely in these two "twin" boxes and can be safelt
eliminated from all other boxes in the unit.

Each of these strategies performs a transformation that reduces solution search
space (and so the complexity of the problem) while enforcing satisfaction of the
problem's constraints (Sudoku rules).

One round of the reduction strateges applied in sequence might not solve the puzzle completely,
but it reduces number of possible solutions (i.e. number of possble values in
the boxes) and reveals new constraints in a form of solved boxed, "Only Choice" combinations, or twins.

For example, a removal of Naked Twins digits from their peers may reveal another
Naked Twins in the unit, or even solve some boxes, that can be used in next
reduction round.

This process applied repeatdly is the Constraint Propagation we use to reduce
search space for DFS.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: Diagonal is a normal Sudoku extended with a condition, that within the two
main diagonals, the numbers 1 to 9 should all appear exactly once.

This sets an additional constraint that is taken into account by our solution
search space reduction strategies, when applied.

To implememnt this logic, we use same approach and strategies as for the
"non-diagonal" sudoku, but introduce two new units (two main diagonals), so that
each box that lays on a diagonal, gets 6 more diagonal peers (note, that box E5
in the center of the board gets 12 peers from both diagonal units).


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

