'''
Created on Mar. 9, 2024

@author: Sebastian
'''
class BoundedQueue: 
    # Creates a new empty queue:
    def __init__(self, capacity): 
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity))) # throws an assertion error on not true
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.__items = [] # init the  list / queue as empty
        self.__capacity = capacity
 
    # Adds a new item to the back of the queue, and returns nothing:
    def enqueue(self, item): 
        '''
        Enqueue the element to the back of the queue
        :param item: the element to be enqueued
        :return: No returns
        '''
        if len(self.__items) >= self.__capacity:
            raise Exception("ERROR QUEUE FULL")
        '''
        Remember to check the conditions
        '''
        self.__items.append(item)
        
    # Removes and returns the front-most item in the queue.      
    # Returns nothing if the queue is empty.    
    def dequeue(self):        
        '''
        Dequeue the element from the front of the queue and return it
        :return: The object that was dequeued
        '''
        if len(self.__items) <= 0:
            raise Exception("ERROR QUEUE EMPTY")
        '''
        1. remember to check the conditions
        2. return the appropriate value
        '''
        return self.__items.pop(0)
    
    # Returns the front-most item in the queue, and DOES NOT change the queue.      
    def peek(self):        
        if len(self.__items) <= 0:            
            raise Exception('Error: Queue is empty')        
        return self.__items[0]
        
    # Returns True if the queue is empty, and False otherwise:    
    def isEmpty(self):
        return len(self.__items) == 0        
    
    # Returns True if the queue is full, and False otherwise:    
    def isFull(self):
        return len(self.__items) == self.__capacity
    
    # Returns the number of items in the queue:    
    def size(self):        
        return len(self.__items)        
    
    # Returns the capacity of the queue:    
    def capacity(self):        
        return self.__capacity
    
    # Removes all items from the queue, and sets the size to 0    
    # clear() should not change the capacity    
    def clear(self):        
        self.__items = []
    
    # Returns a string representation of the queue: 
    def __str__(self):               
        str_exp = ""        
        for item in self.__items:            
            str_exp += (str(item) + " ")                    
        return str_exp
        
    # Returns a string representation of the object bounded queue: 
    def __repr__(self):               
        return  str(self) + " Max=" + str(self.__capacity)      
    
class Stack:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity
    
    def push(self, item):
        if len(self.items) >= self.capacity:
            raise Exception("ERROR QUEUE FULL")
        
        self.items.append(item)
    
    # MODIFY: RAISE AN EXCEPTION IF THIS METHOD IS INVOKED ON AN EMPTY STACK
    def pop(self):       
        try:
            return self.items.pop()
        except IndexError:
            raise Exception("Stack is empty")
    
    # MODIFY: RAISE AN EXCEPTION IF THIS METHOD IS INVOKED ON AN EMPTY STACK
    def peek(self): 
        try:     
            return self.items[self.size()-1] 
        except IndexError:
            raise Exception("Stack is empty")
    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    def show(self):
        print(self.items)
    
    def __str__(self):
        stackAsString = ''
        for item in self.items:
            stackAsString += item + ' '
        return stackAsString
    
    def clear(self):
        if not self.isEmpty():
            self.items = []
            
    def capacity1(self):        
        return self.capacity
    
    def isFull(self):
        return len(self.items) == self.capacity
#
from time import sleep
import os
CHEM_QUANT = 3
ANSI = {
"AA": "\033[41m",
"CC": "\033[42m",
"BB": "\033[44m",
"EE": "\033[103m",
"FF": "\033[45m",
"DD": "\033[43m",
"UNDERLINE": "\033[4m",
"RESET": "\033[0m",
"CLEARLINE": "\033[0K"
}

ANSI2 = {
"1": "\033[41m",
"3": "\033[42m",
"2": "\033[44m",
"5": "\033[103m",
"6": "\033[45m",
"4": "\033[43m",
"UNDERLINE": "\033[4m",
"RESET": "\033[0m",
"CLEARLINE": "\033[0K"
}
os.system("")

def get_input_file():
    '''
    Asks the user to input the name of a text file and if the input ends with '.txt' returns the file name
    eg.
    inputting secretMessage1.txt would return 'secretMessage1.txt'
    while inputting secret would ask the user for a valid file name again
    '''
    user_input = input("Please provide a valid text file name: ")
    while not user_input.endswith(".txt"):
        user_input = input("Invalid filename extension. Please provide a valid text file name: ")
    return user_input

def distribute_chemicals(lines, flask_count):
    '''
    Takes a list of Strings with chemicals and codes to dequeue and enqueue and returns the corresponding list of flasks
    eg. AA
        BB
        2f1
        would return [{AA,BB}] where {} indicates a stack
    '''
    list_of_flasks = [""]*flask_count
    
    for i in range(flask_count):
        list_of_flasks[i] = Stack(4) #creates a flask in each position

    main_flask = BoundedQueue(4) 
    
    for line in lines[1:]:
        if line[0].isalpha(): #checks if it's a chemical or a dequeue order
            try:
                main_flask.enqueue(line) #adds chemical to main_flask
            except Exception:
                print(f"Bounded queue is full so {line} is discarded")
        else: #dequeues into flask
            try:
                f_index = line.find("F")
                to_dequeue = int(line[:f_index]) #gets the integer of all values before the F
                to_enqueue = int(line[f_index+1:]) #gets the integer of all values after
                
                for i in range(to_dequeue): #dequeus the amount specified chemicals and puts them in a flask
                    chemical = main_flask.dequeue()
                    list_of_flasks[to_enqueue-1].push(chemical)
                    
            except Exception:
                print(f"Bounded queue is empty so {line} nothing is dequeued")
    return(list_of_flasks)            

def display_flask(flask):  
    '''
    Returns a single flask formatted in the desired style
    '''
    capacity = flask.capacity1()
    replacement_flask = Stack(capacity)
    
    while not flask.isEmpty():
        replacement_flask.push(flask.pop())

    to_string = f"+--+"
    if seal_flask(replacement_flask): #if flask is sealed the string needs to account for the top 
        to_string = f"+--+\n|{ANSI[replacement_flask.peek()]}{replacement_flask.peek()}{ANSI['RESET']}|\n|{ANSI[replacement_flask.peek()]}{replacement_flask.peek()}{ANSI['RESET']}|\n|{ANSI[replacement_flask.peek()]}{replacement_flask.peek()}{ANSI['RESET']}|\n+--+"
        
        while not replacement_flask.isEmpty(): #puts all the chemicals into a fake flask that allows me to pop from and still have the original order by pushing the popped value
            flask.push(replacement_flask.pop())
        return to_string 

    for i in range(capacity): #goes over each entry in the stack, either a chemical or nothing      
        try:
            to_add = replacement_flask.pop() 
            to_string = f"|{ANSI[to_add]}{to_add}{ANSI['RESET']}|\n" + to_string
            flask.push(to_add)
        except Exception: #if the .pop() returns nothing then the exception adds an empty flask slot
            to_string = f"|  |\n" + to_string
               
    return to_string

def pour(flasks, take, give):
    '''
    Takes a list of flasks and two positions,
    provided the positions are within the range of flasks pours the top chemical to another flask
    '''
    if take > len(flasks) or take < 1 or give > len(flasks) or give < 1:
        display_error("Please provide an index in the range of flasks")
        return False
    elif seal_flask(flasks[take-1]) or flasks[take-1].isEmpty():
        display_error("Cannot take from that flask")
        return False
    elif seal_flask(flasks[give-1]) or flasks[give-1].isFull():
        display_error("Cannot pour into that flask")
        return False
    elif give == take:
        display_error("Cannot pour into itself")
        return False
    else:
        for i in range(flasks[take-1].size()):
            last_element = flasks[take-1].pop()
            if i != flasks[take-1].size():
                flasks[take-1].push(last_element)

        flasks[give-1].push(last_element)
        
    
def seal_flask(flask):
    '''
    Checks if flask should be sealed
    '''
    if flask.size() != CHEM_QUANT:
        return False
    
    capacity = flask.capacity1()
    replacement_flask = Stack(capacity)
    
    while not flask.isEmpty(): #puts all the chemicals into a fake flask that allows me to pop from and still have the original order by pushing the popped value
        replacement_flask.push(flask.pop())

    while not replacement_flask.isEmpty(): 
        try:
            to_enqueue = replacement_flask.pop()  
            flask.push(to_enqueue)
            if to_enqueue != replacement_flask.peek(): #after adding the top of the fake flask back to the real flask, checks if the next chemical matches
                while not replacement_flask.isEmpty(): #if the chemicals aren't the same pours the entire fake flask back into the real flask
                    flask.push(replacement_flask.pop())
                return False     
        except Exception:
            pass
          
    return True
    
def display_flasks(flasks):
    '''
    Displays all flasks formatted, takes a list of flasks
    '''
    num_flasks = len(flasks)
    flask_list = [""]*num_flasks
    
    for i in range(num_flasks):
        flask_list[i] = display_flask(flasks[i]) #puts the formatted individual flasks into a combined list
    
    for j in range(len(flask_list)):
        flask_list[j] = flask_list[j].split("\n") #splits the formatted flask by the new line character which separates each tier
    
    for k in range(flasks[0].capacity1()+1): #goes over each line of the formatted flasks + 1 for the base of the flask
        to_string =""
        for i in range(num_flasks): #goes over each individual flask and grabs the corresponding element from that flask
            to_string += flask_list[i][k] + " "
        print(to_string) #prints the row of all flasks
        
    num_list = [""] *num_flasks 
    num_str = ""
    for i in range(num_flasks): # prints the numerical indicators
        num_str += f"  {i+1}  "
        
    return num_str
    
def get_victorious(flasks):
    '''
    returns True iff all flasks are either sealed or empty
    '''
    win = True
    
    for flask in flasks:
        if not seal_flask(flask) and not flask.isEmpty():
            win = False
            
    return win

def print_location(x, y, text):
    '''
    Prints text at the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
        - text (str): text to print
    Returns: N/A
    '''
    print ("\033[{1};{0}H{2}".format(x, y, text))

def clear_screen():
    '''
    Clears the terminal screen for future contents.
    Input: N/A
    Returns: N/A
    '''
    if os.name == "nt":  # windows
        os.system("cls")
    else:
        os.system("clear")  # unix (mac, linux, etc.)
        
def print_header():
    '''
    Prints the Magical Flask Game header.
    Input: N/A
    Returns: N/A 
    '''
    print("{:^0}\033[0m".format("Magical Flask Game"))

def display_error(error):
    '''
    Displays an error message under the current site as specificed by "error".
    Input:
        - error (str): error message to display
    Returns: N/A
    '''
    move_cursor(0, 5)
    print("\033[6;31;40m{:^80}\033[0m".format(error))
    sleep(0.6)
    clear_screen()
    
def move_cursor(x, y):
    '''
    Moves the cursor to the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
    Returns: N/A
    '''
    print("\033[{1};{0}H".format(x, y), end='')

def main():

    file_name = get_input_file() 
    with open(file_name, "r") as file: 
        lines = file.readlines()
    
    for i in range(len(lines)): #removes all new line and whitespace characters that are at the ends of the file
        lines[i] = lines[i].strip()
        
    counts = lines[0].split(" ")
    num_flasks = int(counts[0])
    
    flasks = distribute_chemicals(lines, num_flasks)   
    print(display_flasks(flasks))

    seal_flask(flasks[0])
    stop = False
    while not stop:
        clear_screen()
        print_header()
        
       
        print_location(0, 3, "Please enter a flask to pour from: ")
        print_location(0, 4, "Please enter a flask to pour to: ")
        print()
        print_location(0, 11, display_flasks(flasks))
        move_cursor(36, 3)
        take = input()
        
        if take == "q" :
            stop = True
        else:
            move_cursor(34, 4)
            give = input()
            if give == "q":
                stop = True
            else:
                if not take.isnumeric() or not give.isnumeric():
                    display_error("Invalid input")
                else:
                    pour(flasks, int(take), int(give))
                    display_flasks(flasks)
            
        if get_victorious(flasks):
            stop = True
            print_location(0,12,"YOU WIN!")
        

if __name__ == "__main__":
    main()
