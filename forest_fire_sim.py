'''
Grey Goodwin
Forest Fire Simulator
'''

import tree
import button
import graphics
import random

# Global variables used for convenience in multiple functions.
TREE_SIZE = 29
WIDTH = TREE_SIZE * 24
HEIGHT = TREE_SIZE * 10

def create_forest(win):
# Creates forest and stores 1-D list of each graphic tree in forest.
    l_trees = []
    for i in range(10):
        l_col = []
        for j in range(15):
            point_x = ((2 * j + 1) * TREE_SIZE) / 2
            point_y = ((2 * i + 1) * TREE_SIZE) / 2
            arbor = tree.Tree(graphics.Point(point_x,point_y))
            arbor.draw(win)
            l_col.append(arbor)
        l_trees.append(l_col)

    return l_trees

def random_start(win,l_trees,f_prob):
# Based on randomized tree, fire will spread to neighboring trees based
# on the probability users entered.
    i_col = random.randint(0,14)
    i_row = random.randint(0,9)
    l_trees[i_row][i_col].burn_more(win)

# Will continue to burn neighbors as long as there is a tree on fire.
    i_step = 0
    while any_tree_on_fire(l_trees):
        l_burning_trees = trees_on_fire(l_trees)
        for arbor in l_burning_trees:
            if i_step > 0:
                l_trees[arbor[0]][arbor[1]].burn_more(win)
            burn_neighbors(win,f_prob,l_trees,arbor[0],arbor[1])                                        
        i_step += 1        
        any_tree_on_fire(l_trees)
        
# Once fire has subsided, message appears noting the number of steps
# for the fire to subside.
    subside_message = graphics.Text(
        graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                       HEIGHT / 2 - 50),
                        "Fire subsided in " + str(i_step) + " steps. Click to continue.")
    subside_message.setFill("red")
    subside_message.draw(win)
    click = win.getMouse()
    subside_message.undraw()

def click_start(win,click,l_trees,f_prob):
# Based on clicked tree, fire will spread to neighboring trees based
# on the probability users entered.
    for i in range(len(l_trees)):
        for j in range(len(l_trees[i])):
            if l_trees[i][j].point_is_inside(click):
                i_row = i
                i_col = j
                l_trees[i][j].burn_more(win)

# Will continue to burn neighbors as long as there is a tree on fire.
    i_step = 0
    while any_tree_on_fire(l_trees):
        l_burning_trees = trees_on_fire(l_trees)
        for arbor in l_burning_trees:
            if i_step > 0:
                l_trees[arbor[0]][arbor[1]].burn_more(win)
            burn_neighbors(win,f_prob,l_trees,arbor[0],arbor[1])                                        
        i_step += 1        
        any_tree_on_fire(l_trees)
        
# Once fire has subsided, message appears noting the number of steps
# for the fire to subside.
    subside_message = graphics.Text(
        graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                       HEIGHT / 2 - 50),
                        "Fire subsided in " + str(i_step) + " steps. Click to continue.")
    subside_message.setFill("red")
    subside_message.draw(win)
    click = win.getMouse()
    subside_message.undraw()

def reset_forest(win,lst_trees):   
# Undraws each tree in the forest
    for i in range(10):
        for j in range(15):
            lst_trees[i][j].undraw()

def should_burn(f_prob):   
# Decides whether or not neighboring tree should be set fire
# based on probability user entered.
    f_burn_prob = random.random()
    if f_burn_prob < f_prob:
        return True

def any_tree_on_fire(l_trees):   
# Tests if any tree at that step is on fire.
    for i in range(len(l_trees)):
        for j in range(len(l_trees[i])):
            if l_trees[i][j].is_on_fire():
                return True

def trees_on_fire(l_trees):   
# Creates 2-D list of location of trees that are on fire.
# Note the length of the list is equal to the total number
# of trees at the given step.
    l_burning_trees = []
    for i in range(len(l_trees)):
        for j in range(len(l_trees[i])):
            if l_trees[i][j].is_on_fire():
                i_row = i
                i_col = j
                l_burning_trees.append([i_row,i_col])
                
    return l_burning_trees

def burn_neighbors(win,f_prob,l_trees,i_row,i_col):   
# Based on location of the current burning tree in the step,
# fire will spread to any neighboring tree based on probability
# the user entered. If the neighboring tree is out of bounds,
# it is ignored.
    for i in range(3):
        for j in range(3):
            try:
                l_trees[1 + i_row - i][1 + i_col - j]
                if 1 + i_row - i >= 0 and 1 + i_col - j >= 0:
                    if (l_trees[1 + i_row - i][1 + i_col - j] !=
                        l_trees[i_row][i_col]
                        and should_burn(f_prob)):
                        l_trees[1 + i_row - i][1 + i_col - j].burn_more(win)
            except IndexError:
                pass    
    
def run_sim(win):  
# Creates and draws buttons at targetted locations
    bp_message = graphics.Text(
        graphics.Point(WIDTH - TREE_SIZE * 4.5,
                       HEIGHT / 2 - 25), "Burn Probability:")
    bp_message.setFill("blue")
    input_box = graphics.Entry(
        graphics.Point(WIDTH - TREE_SIZE * 4.5, HEIGHT / 2),
        20)
    random_start_button = button.Button(
        graphics.Point(WIDTH - TREE_SIZE * 6.5, HEIGHT / 2 + 50),
        graphics.Point(WIDTH - TREE_SIZE * 2.5, HEIGHT / 2 + 25),
        "Run (Random Start)")
    click_start_button = button.Button(
        graphics.Point(WIDTH - TREE_SIZE * 6.5, HEIGHT / 2 + 80),
        graphics.Point(WIDTH - TREE_SIZE * 2.5, HEIGHT / 2 + 55),
        "Run (Click to Start)")
    reset_button = button.Button(
        graphics.Point(WIDTH - TREE_SIZE * 6.5, HEIGHT / 2 + 110),
        graphics.Point(WIDTH - TREE_SIZE * 2.5, HEIGHT / 2 + 85),
        "Reset Simulation")
    exit_button = button.Button(
        graphics.Point(WIDTH - 15,15),
        graphics.Point(WIDTH,0),
        "X")
    exit_button.setFill("red")    
   
    bp_message.draw(win)
    input_box.draw(win)
    random_start_button.draw(win)
    click_start_button.draw(win)
    reset_button.draw(win)
    exit_button.draw(win)
    
    l_trees = create_forest(win)
    
# Gets click from user in window, based on click, runs selected options.
# If user has invalid input, user is informed and allowed to reclick their
# option until valid input is entered.
# Will continue to operate until user clicks designated exit button.
    click = win.getMouse()
    while not exit_button.point_is_inside(click):
        
        if random_start_button.point_is_inside(click):
            input_str = input_box.getText()
            try:
                f_prob = float(input_str)
                if 0 <= f_prob <= 1:
                    random_start(win,l_trees,f_prob)
                else:
                    invalid_message = graphics.Text(
                            graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                                           HEIGHT / 2 - 50),
                                            "Invalid input. Click anywhere to continue.")
                    invalid_message.setFill("red")
                    invalid_message.draw(win)
                    click = win.getMouse()
                    invalid_message.undraw()
            except ValueError:
                invalid_message = graphics.Text(
                        graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                                       HEIGHT / 2 - 50),
                                        "Invalid input. Click anywhere to continue.")
                invalid_message.setFill("red")
                invalid_message.draw(win)
                click = win.getMouse()
                invalid_message.undraw()           

        if click_start_button.point_is_inside(click):            
            input_str = input_box.getText()
            try:
                f_prob = float(input_str)
                if 0 <= f_prob <= 1:
                    click = win.getMouse()                  
                    click_start(win,click,l_trees,f_prob)
                else:
                    invalid_message = graphics.Text(
                            graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                                           HEIGHT / 2 - 50),
                                            "Invalid input. Click anywhere to continue.")
                    invalid_message.setFill("red")
                    invalid_message.draw(win)
                    click = win.getMouse()
                    invalid_message.undraw()
            except ValueError:
                invalid_message = graphics.Text(
                        graphics.Point(WIDTH - TREE_SIZE * 9 / 2,
                                       HEIGHT / 2 - 50),
                                        "Invalid input. Click anywhere to continue.")
                invalid_message.setFill("red")
                invalid_message.draw(win)
                click = win.getMouse()
                invalid_message.undraw()

        if reset_button.point_is_inside(click):
            reset_forest(win,l_trees)
            l_trees = create_forest(win)
        click = win.getMouse()

    win.close()

def main():  
# Opens graphic window
    win = graphics.GraphWin("Forest Fire Simulation", WIDTH, HEIGHT)
    
# Runs full simulation
    run_sim(win)

if __name__ == "__main__":
    main()
