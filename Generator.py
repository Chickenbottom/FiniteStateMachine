#! usr/bin/python
#Chad Hickenbottom
#CSS 390 Scripting
#Winter 2014
#FINITE STATE MACHINE

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

import sys
#structures used throughout program
#code for the beginning of program up to swtich statement
cppbegin_code = [] 	
#code from switch statement to end of file/input
cppend_code = []
#header of the main structure which holds switch statment info
state = {}
#holds machine name
machine={}
#used as a temp place holder of information
dictvalues = []
#holds all lines of user input or of the file
commands = []
#used to navigate commands globally 
index = 0
#create cpp file to run generated code
output_file = open("generated_code.cpp", "w")


#prints cppbegin array and everything up to the 
#switch statment
def print_cppbegin_code() : 
	for line in cppbegin_code :
		output_file.write(line)
	output_file.write("#include <iostream>\n")
	output_file.write("using namespace std; \n")
	output_file.write("enum State {\n")
	
	#used to print the states in alphebetical order
	temp_states = state.keys()
	temp_states.sort()
	
	for key in temp_states :
		output_file.write("\t" + key + "_STATE,\n")
	output_file.write("};\n\n")

	output_file.write("enum Event {\n")
	output_file.write("\tINVALID_EVENT,\n")
	# used to print the events in alphebetical order
	temp_events = []
	for _ in xrange(0,len(temp_states)) :
		ev = state[temp_states[_]][1].keys()
 		for e in ev :
 		 	temp_events.append(e)
 	temp_events.sort()

	for event in temp_events :
		output_file.write("\t" + event + "_EVENT,\n")
	output_file.write("};\n\n")

	func_header = cppend_code[0]
	func_header = func_header.lstrip()
	output_file.write(func_header.replace(" {", ";")+"\n")

	output_file.write("Event string_to_event(string event_string){\n")

	for event in temp_events :
		output_file.write("\tif (event_string == \"" + event + "\"){\n")
		output_file.write("\t   return " + event + "_EVENT;\n")
		output_file.write("\t}\n" )
	output_file.write("\treturn INVALID_EVENT;\n")
	output_file.write("}\n")
	output_file.write("\n\n\nint "+machine["machine"]+"(State initial_state){\n")
	output_file.write("\nState state = initial_state;\n")
	output_file.write("Event event;\n")
	
#print out the contents of the switch statment
def print_switch_code() :
	temp_states = state.keys()
	output_file.write( "while (true){\n")
 	output_file.write( "  switch(state){\n")

 	for i in xrange(0,len(temp_states)) :
		output_file.write( "\tcase "+ temp_states[i] +"_STATE:\n")
		for x in xrange(0,len(state[temp_states[i]][0])) :		
			output_file.write("\t" + state[temp_states[i]][0][x]	+"\n")
		output_file.write( "\t\tevent = GetNextEvent();\n\n")	
		output_file.write( "\t\tswitch(event){\n\n")	

		case_events = state[temp_states[i]][1].keys()
		case_events.sort()
		if case_events and state[temp_states[i]][1] :
			for y in xrange(0,len(case_events)) :
 				output_file.write( "\t\tcase " + case_events[y] + "_EVENT:\n")
				for k in xrange(0,len(state[temp_states[i]][1][case_events[y]][1])) :
					output_file.write( "\t\t  " + state[temp_states[i]][1][case_events[y]][1][k] + "\n")
				output_file.write( "\t\t\tstate = " + str(state[temp_states[i]][1][case_events[y]][0][0]) +"_STATE;\n")
				output_file.write( "\t\t\tbreak;\n")
		output_file.write( "\t\tdefault:\n")
		output_file.write( "\t\t  cerr << \"invalid event in state "+ temp_states[i] +": \" << event << endl;\n")
		output_file.write( "\t\t  return -1;\n")
		output_file.write( "\t  }\n")
		output_file.write( "\t  break;\n\n\n")

	output_file.write( "\tdefault:\n")
	output_file.write( "\t\tcerr << \"INVALID STATE \" << state << endl;\n")
	output_file.write( "\t\treturn -1;\n")
	output_file.write( "    }\n")
	output_file.write( "  }\n")
	output_file.write( "}\n\n")
	return

#prints the "end" of the program everything after the
# switch statment
def print_cppend_code():
	for index in cppend_code:	
		output_file.write(index)

def populate_cppend_code(index) :
	index += 1 #ignore %end_machine line
	for line in range(index, len(commands)) :
		cppend_code.append(commands[index])
		index += 1



def populate_state(index) :
	dictvalues = commands[index].split()
	dictvalues[0] = dictvalues[0].strip("%")
	cur_state = dictvalues[1]
	state[cur_state] = ([],{})
	index += 1	
	for _ in xrange(index, len(commands)) :
		if not "%" in commands[index] :
		# next_line(cur_state, index)
			state[cur_state][0].append(commands[index])
			index += 1 
		else:
			return cur_state



def populate_event(cur_state, index) :
	values = commands[index].split()
	state[cur_state][1][values[1]] = ([],[]) 
	state[cur_state][1][values[1]][0].append(values[2])
	unknown_state = state[cur_state][1][values[1]][0]
	if not any(values[2] in s for s in state) :
		state[values[2]] = ([],{})
	index += 1 
	for _ in xrange(index, len(commands)) :
		if not "%" in commands[index] :
			state[cur_state][1][values[1]][1].append(commands[index])
			index += 1
		else :
			return


#capture all lines input from standard in
#populates commands array for easier processing
for line in sys.stdin:
	emptyline = line.split()
	if not emptyline :
		continue #ignor blank lines
	else : 
		commands.append(line)

for line in commands :
	if not "%machine" in line :
		cppbegin_code.append(commands[index])
		index += 1
		continue
	else : 
		dictvalues = line.split()
		dictvalues[0] = dictvalues[0].strip("%")
		machine[dictvalues[0]] = dictvalues[1]
		index += 1 
		break

for index in xrange(0,len(commands)):
	if "%state" in commands[index] :
		cur_state = populate_state(index)
	elif "%event" in commands[index] :
		populate_event(cur_state, index)
	elif "%end_machine" in commands[index] :
		populate_cppend_code(index)


print_cppbegin_code()
print_switch_code()
print_cppend_code()

output_file.close()
