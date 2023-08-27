# Student Information
# Name: David Dobrin
# Student ID: 501165841

import random

                ############## Description ##############
"""
The problem this program solves is how to make a battleship game.

                    Grid creation and ship placement:
This program takes user input on grid size, then creates and places in this grid
a number of ships of random sizes, in random locations, random directions. 
The ships cannot touch directly (although diagonals are allowed).

                                Firing:
The user can fire at various locations throughout the grid, either missing
or hitting battleships. The programs constantly updates the grid with the effects
of the torpedo firings. 

                                Abilites:
The user has two special abilites that reveal ships and empty tiles. 
The radar reveals all tiles around a torpedo hit in the grid. 
The spotting plane reveals all tiles in a straight line, horizontally or vertically. 

                                Gameplay:
The user must sink all the battleships as fast as possible.
The program ends when all the ships are sunk. 

As the user is charge of the navy, attempting to leave before clearing 
the sea of all hostiles results in a court martial. 
To prevent such shame, there is no option to leave the program aside from closing the program itself!
"""

# Grid
grid = [] # 2D list. Every element in grid represents a y-value.Each element is also a list, containing x-values.

gridSize = None # gridSize is from 5 to 9 (input from the user)
letters = "ABCDEFGHI" # First 9 letters of the alphabet. Amount used is based on gridSize

# Ships
shipList = [] # A list of a random amount of ships (depending on gridSize), each a random size of 2 or 3
minSize = 2
maxSize = 3

unAvailableCoordinates = set() # All coordinates that are not possible for ship locations. Updated for every ship that is placed

# These two dictionaries are direct opposites, as it's needed to go from coords to ship and vice versa. 
# As dictionaries are only fast from key to element, and not the other way around, two dictionaries are needed. 
shipPositions = {} # Dictionary containing coords for all the ships as keys, in order.
coordPositions = {} # Dictionary containing all the coords as keys, pointing to their respective ship. 

directions = ["Up", "Down", "Left", "Right"] # Possible direction
possible = True # Whether possible for placing down a ship

# Tile Types
emptyTile = '.'
shipTile = '.' # This variable is used for test purposes
revealedShip = "0"
revealedEmpty = "_"
hitTile = "x" 
missTile = "*" 

# Firing
num_of_shots = 1 

# The following variables are the x, y code input from the user, firing somewhere on the board
# These are used to compare with ship and coord positions
fire_x = None 
fire_y = None
fire_coord = ()

hit_coords = set() # Set containing all locations already fired at. Used to prevent firing at same location, and for first ability

# Ability
num_of_planes = 1 # Default number of abilities (increases with gridSize)
num_of_radar = 1


def getGridSize():
    """
    Gets the gridSize from user input. This gridSize affects many variables, such as 
    number of abilites
    """
    global gridSize # All global variables, as their values given here will affect other functions
    global rows, cols
    global num_of_planes
    global num_of_radar
    print("Hello there commander! We need you help in this time of great need! The enemy have taken control of the sea, and we must wipe them out!")
    print("Before we begin commander, what is the size of the sea (5-9)? ", end = "")
    while True:
        value = input() # Collects user input about the grid size
        try: # Try-except used to validate correct user input
            gridSize = int(value)
            if gridSize >= 5 and gridSize <= 9: # If statement checks whether input is within bounds
                break
            else:
                print("Value out of bounds. Try again")                
        except:
            print("Invalid input. Try again")
    print("Very good commander! Now let's take remove these hostiles from our territory!")
    # Number of abilities hanges with gridSize, with a default of always at least 1
    num_of_planes += gridSize - 7 
    num_of_radar += gridSize - 6
    if num_of_planes < 1:
        num_of_planes = 1
    if num_of_radar < 1:
        num_of_radar = 1
    
     
def createShipList():
    """
    Creates the shipList based on gridSize. 
    """
    global shipList
    num_of_ships = gridSize - 2 # Getting the number of ships
    for i in range(num_of_ships):
        shipList.append(random.randint(minSize, maxSize)) # Each ship is assigned a random value of 2 or 3, which represents their size
    
    if shipList.count(3) == len(shipList): # If all the ships are of length 3
        shipList[0] = 2 # First two are changed to length 2
        shipList[1] = 2
    # The above condition is done as if every ship is length 3, there are some possibilities
    # for impossible situations, due to a no touching system implement later on in the code. 
    # This insures that all the ships can be placed in the grid. 
        
def createGrid():
    """
    Creates the grid, which is a 2D list. At first, every tile in the grid is 'empty' as
    ship locations are not known
    """
    global grid
    global gridSize
    global emptyTile
    
    for i in range(gridSize):
        row = []
        for q in range(gridSize):
            row.append(emptyTile)
        grid.append(row)
        
    
def printGrid():
    """
    Function used to go through every element in the grid 2D list [row][column]
    and print it. In addition, prints the letters and numbers on the left and top of the 
    board to represent rows and columns respectively.
    """
    # Grid numbers
    print("\n   ", end = "")
    for z in range(gridSize): # Prints every single number 1 -> gridSize, to represent columns
        print(z+1, end = "   ") # To be noted that the number representing every column is 1 more than the index of the column in the grid list. 
    print("\n") 
    
    # Grid and letters
    for i in range(gridSize): # Letters and tiles printed at the same time (same row)
        print(letters[i], end = "  ") # The index i is used to take the respective value from the strin alphabet
        for q in range(gridSize):
            print(grid[i][q], end = "   ") # Prints the row
        print("\n")

def antiTouching(shipNum):
    """
    When ships are placed (in another function), this function goes through each coordinate
    of that ship one at a time, placing all the squares adjacent (exluding diagonals) 
    in the unAvailableCoordinates set. This is to prevent ships touching directly, and
    making them spread out more around the grid
    """
    global unAvailableCoordinates
    
    for i in shipPositions[shipNum]: # Each ship is a key representing a list of tuples. Each tupes is a coordinate
        # i is the list element (tuple)
        letter = i[0] # First element of tuple is the letter, as in 'A' from 'A1'
        number = i[1] # Second element of tuple is the number, as in 1 from 'A1'
        
        y_coor = letters.index(letter) # The letter and number is transformed into x and y coordinates
        x_coor = int(number) - 1
        
        # Whatever coordinates give, the coordinates up, down, left and right are added to the set (if they exist)
        if x_coor - 1 >= 0:
            unAvailableCoordinates.add((x_coor-1, y_coor))
        if x_coor + 1 < gridSize:
            unAvailableCoordinates.add((x_coor+1, y_coor))
        if y_coor - 1 >= 0:
            unAvailableCoordinates.add((x_coor, y_coor-1))
        if y_coor + 1 < gridSize:
            unAvailableCoordinates.add((x_coor, y_coor+1)) # Diagonals not included
        
def placeShipsRandomly():
    """
    This function goes through every ship (or element) in the shipList. 
    It gives the ship a random (x, y) coordinate. If the coordinate has not yet been added to 
    the unAvailableCoordinates set, it is tested for all 4 directions as the ship will have a size of 2 or 3. 
    If one of the directions work, place the ship, and add all respective coordinates to the unAvailable set. 
    (including the the noTouching system). If not possible, add the coordinate as unavailable, and try for another coordinate
    """
    global grid
    global shipList
    global shipPositions  
    global directions
    global possible
    global unAvailableCoordinates
    global direction
    
    index = 0
    for i in shipList: # For every ship
        
        shipSize = i # Get ship Size
        repeat = True # Continuously repeat until a break (ship placed)
        while repeat:
            x_coor = random.randint(0, gridSize-1) # Get random coords
            y_coor = random.randint(0, gridSize-1)
            coords = (x_coor, y_coor, shipSize)            
            
            if coords in unAvailableCoordinates: # If already unAvailable/tested, go back and get another set of random coords
                continue
            directions = ["Up", "Down", "Left", "Right"]
            for q in range(4):                 
                direction = directions[random.randint(0, len(directions)-1)] # Going through all 4 directions in a random order
                checkAvailability(shipSize, x_coor, y_coor, direction) # Checks if the ship is possible to place            
            
                if possible == True: # If possible to place
                    placeShip(shipSize, x_coor, y_coor, direction, index) # Place ship
                    antiTouching(index) # Add all adjacent coordinates to unAvailable set to prevent touching
                    repeat = False # Stop the while loop
                    break
                directions.remove(direction) # If direction tested and doesn't work, remove it and repeat
                    
            # If none of the directions work, add coordinate as unAvailable. 
            unAvailableCoordinates.add((x_coor, y_coor))
                
        index += 1    
def checkAvailability(shipSize, x_coor, y_coor, direction):
      """
      Goes through all the coordinates of the ship, one by one. Based on direction, 
      the coordinates change a shipSize number of times. Each coordinate is checked if it works
      """
      global grid
      global possible
      possible = True
      for i in range(shipSize):
          
          try: # Tests if coordinates exist in the grid system (using try, checks for indexes above gridSize - 1)
              if grid[y_coor][x_coor] != emptyTile or x_coor <0 or y_coor < 0: # can have negative indexes in lists, which doens't work logically in the program
                  possible = False # If coordinate doesn't exist (out of bounds), not possible 
                  break
          except:
            possible = False # coordinate out of bounds (greater than gridSize - 1)
            break # This check is done by grid[y_coor][x_coor], where if y or x are too large, the except runs
         
          # If the coordinates are unAvaiable, not possible 
          if (x_coor, y_coor) in unAvailableCoordinates:
              possible = False
              break
          # If the coordinate passes all conditions, change the coordinate based on direction
          x_coor, y_coor = directionEffect(x_coor, y_coor, direction)
          
def placeShip(shipSize, x_coor, y_coor, direction, shipNum):
      """
      Similar to checkAvailability without checking the conditions, 
      this fucntion goes through every single coordinate, changing with direction, 
      and placing it in the grid. In addition, it adds/creates new key-element pairs
      to the two dictionaires, which are used later on in the firing section
      
      Note: When calling the grid function, grod[y][x], important to note that the grid
            is a list of lists, where every single list represents all the x_coords to one
            y_coord
      """
      global grid
      global possible
      global shipTile
      global shipPositions
      possible = True
      for i in range(shipSize):
          grid[y_coor][x_coor] = shipTile # While not needed as shipTile = emptyTile, this is used for testing purposes 
          # Add ship position to ship key of ship. If key doesn't exist, add key, then position 
          shipPositionDictionaries(shipNum, (getShipPositions(x_coor, y_coor))) # Calls a function to create the key-element pars of ship number and coordinates 
          unAvailableCoordinates.add((x_coor, y_coor))
          x_coor, y_coor = directionEffect(x_coor, y_coor, direction) # Coordinates change with direction
          
          
def getShipPositions(x_coor, y_coor):
    """
    Function used many times by many different functions. Converts the x and y 
    coordinates to letters and numbers. Ex: (0, 0) becomes A1. 
    This is done so that user input from the user when firing can be quickly tested 
    for misses, hits, sinking of ships, etc. 
    """
    letter = letters[y_coor] # Takes the respective letter using the y_coord as an index for the alphabet
    return letter, x_coor+1 # returns these values

def shipPositionDictionaries(shipNum, coords):
    """
    Creates two dictionaries, direct opposites of each other (key <-> element) 
    """
    # Dictionary of ships
    if shipNum in shipPositions:
        shipPositions[shipNum].append(coords)
    else:
        shipPositions[shipNum] = [coords]
    # Dictionary of coords (every coord is unique, so no needed to test if key already in dictionary)
    coordPositions[coords] = shipNum
        
def directionEffect(x_coor, y_coor, direction):
    """
    Based on the coords and direction given, returns the new coordinates
    """
    
    if direction == "Up":
        y_coor -= 1
    elif direction == "Down":
        y_coor += 1
    elif direction == "Left":
        x_coor -= 1
    elif direction == "Right":
        x_coor += 1
    return x_coor, y_coor
        
def fire():
    while len(shipPositions) != 0: # While there are ships left to sink
        if len(shipPositions) > 1:
            print(f"Shot number {num_of_shots}: ({len(shipPositions)} ships remaining)")
        else: # Literally only use of if-else is to change the word ships to ship. Very important :)
            print(f"Shot number {num_of_shots}: ({len(shipPositions)} ship remaining)")
        getTorpedoCoordinates()# Get input from user 
        printGrid() # Re-print the grid
    # Once exiting the while loop, all ships are sunk, so print respective message
    print(f"You sunk all their battleships in {num_of_shots} shots! Good job!")

def getTorpedoCoordinates():
    """
    Get user input in the form A1. If input passes all conditions 
    (such as length and in bounds of grid) Checks, if the coordinate is a repeat
    of a previous user input. If not, then the coordinate is transformed into (x, y)
    and the respective effect of the shot (hit/miss) is tested and outputted. 
    
    Note: For special ability, once activated, cannot go back to normal firing until 
          used. Two abilites. Do not count as shots, and reveal ships and empty tiles
    
    """
    global hit_coords
    print("Please enter coordinates (form 'A1') to fire. To use special ability, enter s1 or s2 respectively:")
    print(f"s1: Radar. Use on torpedo locations {hitTile}, {missTile}, reveal all ships around it. Uses left: {num_of_radar}")
    print(f"s2: Plane. Use on row or column, revealing all ships in a straight line. Uses left: {num_of_planes}")
    torpedo_coords = input().upper() # Done so that a1 --> A1
    while True:
        if len(torpedo_coords) != 2: # Checking for valid length
            print("Invalid input (length). Try again:", end = " ")
            torpedo_coords = input().upper()
            continue
        
        # Testing for special ability (input of s1 or s2)
        if torpedo_coords[0] == "S":
            if torpedo_coords[1] == "1":
                if len(hit_coords) == 0: # At least one shot must be fired to use
                    print("Invalid input (minimum 1 shot fired to use). Try again:", end = " ")
                    torpedo_coords = input().upper()
                    continue
                if num_of_radar == 0:
                    print("Invalid input (no uses left). Try again:", end = " ")
                    torpedo_coords = input().upper()
                    continue
                specialAbilityRadar()
                break
            elif torpedo_coords[1] == "2":
                if num_of_planes == 0:
                    print("Invalid input (no uses left). Try again:", end = " ")
                    torpedo_coords = input().upper()
                    continue
                specialAbilityPlane()
                break
                
        
        # Testing ASCII (letter within bounds)
        if torpedo_coords[0] < letters[0] or torpedo_coords[0] > letters[gridSize - 1]:
            print("Invalid input (first character). Try again:", end = " ")
            torpedo_coords = input().upper()
            continue
        
        # Testing number (Is number and number within bounds)
        try:
            if int(torpedo_coords[1]) > gridSize or int(torpedo_coords[1]) < 1:
                print("Invalid input (second character). Try again:", end = " ")
                torpedo_coords = input().upper()
                continue
        except:
            print("Invalid input (second character). Try again:", end = " ")
            torpedo_coords = input().upper()
            continue 
            
        
        # Tests if shot already fired at location
        if torpedo_coords in hit_coords:
            print("Invalid input (torpedo already launched at location). Try again:", end = " ")
            torpedo_coords = input().upper()
            continue
        
        # If all conditions passed, coordinates transformed into (x, y), and tested
        # whether it was a hit or a miss
        getTorpedoPositions(torpedo_coords[0], torpedo_coords[1])
        hit_coords.add(torpedo_coords)
        hitOrMiss()        
        break
        
def getTorpedoPositions(letter, number):
    """
    Takes board coordinates, in the form 'A1' and transforms them into 
    (x, y) coordinates in the grid. Ex: 'A1' --> (0, 0). 
    
    Note: grid is called using [y][x], not [x][y]
    """
    global fire_x, fire_y, fire_coord
    fire_y = letters.index(letter)
    fire_x = int(number) - 1
    fire_coord = (letter, int(number))


def hitOrMiss():
    """
    Tests if the shot is a hit or a miss by checking if the coordinate exists
    in the dictionary of coordPositions, all of them coordinates of ships.     
    """
    global num_of_shots    
    num_of_shots += 1 # Increases number of shots taken, whether hit or miss
    shipNum = None
    
    if fire_coord in coordPositions: # If in dictionary, its a hit
        shipNum = coordPositions[fire_coord]
        hit(shipNum)        
    else:
        miss() # If not in dictionary, it's a miss
    
    
def miss():
    """
    If miss, transform respective grid coordinate into a miss tile. 
    """
    print("That's a miss!")
    grid[fire_y][fire_x] = missTile

def hit(shipNum):
    """
    If a hit, changes respective tile to a hit tile. 
    Finally, the use of 2 dictionaries: 
    CoordPositions is used to quicly check if the coordinate is part of a ship,
    as well as which ship (element of key). This key-pair is then deleted.
    
    However, using the ship number, by going to the shipPositions dictionary, we
    can find all the coordinates of said ship. The coordinate that was struct by a 
    torpedo is removed from the list of tuples of said ship (key - element pair). 
    If the ship (key) contains a list (element) of 0 elements (no tuples 
    representing coordinates), that means that the ship sunk. 
    """
    print("That's a hit!")
    grid[fire_y][fire_x] = hitTile
    
    
    del(coordPositions[fire_coord]) # Delete key-element pair of coordinate - shipNum
    for i in shipPositions[shipNum]:
        if i == fire_coord:
            shipPositions[shipNum].remove(i) # Remove tuple element from list of shipNum - coordinates dictionary
            break
    if len(shipPositions[shipNum]) == 0: # If list is length 0, ship is sunk
        del(shipPositions[shipNum]) # Ship removed from dictionary
        print("You sunk a battleship!")

def revealShipOrSea(x, y):
    """
    For abilities, reveals whether the coordinate revealed is a ship or empty
    """
    if getShipPositions(x, y) in coordPositions: # If in dictionary of ship coordinates, it's a ship
        grid[y][x] = revealedShip
    elif grid[y][x] == emptyTile: # If not in dictionary, not in ship 
            grid[y][x] = revealedEmpty
    # Note, the above code does nothing with hit or miss tiles, as it should
    # Miss tiles are not emptyTiles, and hit tiles are no longer in coordPositions
    

def revealRadar(coords):
    """
    Given a respective coordinate, looks at all 8 squares surrounding it (if
    there are 8) and reveals whether it is a ship or empty. 
    """
    global num_of_radar
    y = letters.index(coords[0])
    x = int(coords[1]) - 1 # Converts input of the form 'A1' into (x,y) coords
    
    #Chekcs for Non-diagonals    
    if x - 1 >= 0:
        revealShipOrSea(x-1, y)
    if x + 1 < gridSize:
        revealShipOrSea(x+1, y)
    if y - 1 >= 0:
        revealShipOrSea(x, y-1)
    if y + 1 < gridSize:
        revealShipOrSea(x, y+1)
    
    # Checks for Diagonals
    if x - 1 >= 0 and y - 1 >= 0:
        revealShipOrSea(x-1, y-1)
    if x - 1 >= 0 and y+1 < gridSize:
        revealShipOrSea(x-1, y+1)
    if x + 1 < gridSize and y - 1 >= 0:
        revealShipOrSea( x+1, y-1)
    if x + 1 < gridSize and y+1 < gridSize:
        revealShipOrSea(x+1, y+1)
    num_of_radar -= 1
    
def specialAbilityRadar(): 
    """
    Once s1 is inputted in getTorpedoCoordinates(), this code activates. 
    At first, checks for valid input, (correct length, at previous torpedo location, etc.)
    Once input is confirmed to be correct, revealRadar() revealing tiles. 
    """
    # Check if radar allowed to be used (no available spots or no uses left)
    # Get coordinates from player
    # Look at all 8 coordinates (if there are 8) surrounding the chosen coord
    # Find ships in 8 coords
    # Reveal these ships
    print(f"Plese enter either a coordinate (form 'A1') of already hit positions ({missTile} or {hitTile}):")
    radar_coords = input().upper()
    while True:
        if len(radar_coords) != 2: # Testing length
            print("Invalid input (length). Try again:", end = " ")
            radar_coords = input().upper()
            continue
        
        # Testing ASCII
        if radar_coords[0] < letters[0] or radar_coords[0] > letters[gridSize - 1]:
            print("Invalid input (first character). Try again:", end = " ")
            radar_coords = input().upper()
            continue
        
        # Testing number
        try:
            if int(radar_coords[1]) > gridSize or int(radar_coords[1]) < 1:
                print("Invalid input (second character). Try again:", end = " ")
                radar_coords = input().upper()
                continue
        except:
            print("Invalid input (second character). Try again:", end = " ")
            radar_coords = input().upper()
            continue
              
        # Radar coordinates must be in hit_coords to work.         
        if radar_coords not in hit_coords:
            print("Invalid input (torpedo not already launched at location). Try again:", end = " ")
            radar_coords = input().upper()
            continue
        
        revealRadar(radar_coords)        
        break

def getPlanePath():
    """    
    Checks for valid one length input (letter or number). Checks for letter first
    then number. Returns value. If invalid input, try again until valid. 
    """
    print("Plese enter either a letter or number, representing a row or column respectively")
    path = input().upper()
    while True:
        if len(path) != 1:
            print("Invalid input (length). Try again:", end = " ")
            path = input().upper()
            continue
        
        # Testing ASCII
        if path >= letters[0] and path <= letters[gridSize - 1]:
            return path
            
        
        # Testing number
        try:
            if int(path) <= gridSize and int(path) >= 1:
                return int(path)
        except:
            pass        
        print("Invalid input. Try again: ", end = " ")
        
        
            
def revealColumn(number):
    """
    Goes through every single row (same x-value, different y-value)
    and reveals whether they are a ship or empty
    """
    column = number - 1
    
    for i in range(gridSize): # For every list element in grid (y-values). X-value is same throughout
        if (letters[i], number) in coordPositions:  # Checks if in dictionary of coords that are parts of ships
            grid[i][column] = revealedShip # Reveal ship
        else:
            grid[i][column] = revealedEmpty # Reveal empty
        

def revealRow(letter):
    """
    Goes through every single column (same y-value, different x-value)
    and reveals whether they are a ship or empty
    """
    row = letters.index(letter)
    element = 0
    for i in grid[row]: # For every element in the list y of the list of lists grid
        if (letter, element+1) in coordPositions: # Checks if in dictionary of coordinates that are parts of ships
            grid[row][element] = revealedShip # Reveal ship
        else:
            grid[row][element] = revealedEmpty # Reveal empty
        element += 1
        
    
    
def specialAbilityPlane():
    """
    Once s2 is inputted in getTorpedoCoordinates(), this code activates. 
    getPlanePath() is called to check whether correct input. 
    If input is a letter, revealRow, else its a number, revealColumn
    """
    global num_of_planes
    value = getPlanePath()
    if type(value) == int:
        revealColumn(value)
    else:
        revealRow(value)
    num_of_planes -= 1

if (__name__ == "__main__"):
    getGridSize()
    createShipList() 
    createGrid()   
    placeShipsRandomly()
    printGrid()
    fire()
    
    
    
