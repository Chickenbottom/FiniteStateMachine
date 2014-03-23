FiniteStateMachine
==================

finite state machine built in python


#The structure used in this program is as follows
#the base of the structure is a dict which is keyed 
#by the states of the finite state machine
# The state dict holds a tuple which contains a list 
# and another dict. 
# the list holds code associated with the state key
# the second dict is keyed by the events of the 
# finite state machine
# the second dict holds a tuple which contains two
# lists. the first list simply holds the next state 
# which the even leads to, though this list will only
# hold a single string a list was chosen so if the 
# programmer of the finite state machine made a mistake
# or the next state needed to be changed it is not
# held by an immutiable string.
# the second list holds all code that is associated with
# the event. 
#though the structure is rather complex it allows 
#navigation through the finite state machine without
#the need of keeping track of which events are tied
#to which states etc.

# The program will generate C++ output which compiles and runs 
# an example of the code required to make the finite state machine 
# work properly is provieded 
