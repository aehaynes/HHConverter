#Extract the following information, and store in dictionary:
# Table name
# Blinds
# Date/time
# Hand ID
# Table type (6max, etc.)
# Players at each seat (e.g. seat['1'] = 'player1')
# Player stacks
# Known hole cards,
# Hero (if he exists)
# Preflop actions for each seat
# Flop actions for each seat
# Turn actions for each seat
# Board at flop
# Board at turn
# Board at river
# Showdown hands for each seat
# Showdown hand strength for each seat
# Winners, and winnings
# Rake
# Misc?


##Get list of all HH files in dir

import os
import re as re

file_list = []
path = '' #path = os.getcwd()

for root,dirs,files in os.walk(path):
    for file in files:
       if file.endswith(".txt"):
       	f = os.path.join(root, file)
       	file_list.append(str(f) + os.linesep)

##Read individual HH files
for hh in file_list[0:1]:
	with open(hh.strip('\n'), "r") as myfile:
		data = myfile.read()

#Find start and end points of all hands in hh
hand_loc = [d.start() for d in re.finditer(r'Hand #', data)] + [len(data)]
# for i in range(len(hand_loc) -1):
#	hand = data[ hand_loc[i]:hand_loc[i+1] ]
hand = data[ hand_loc[0]:hand_loc[1] ].split('\n')

#regex for table name
#idx_table = [i for i,l in enumerate(hand) if l.startswith('Table:') ] 
#idx_seat = [i for i,l in enumerate(hand) if l.startswith('Seat ') ] 

#it may be slow to enumerate list multiple times...worry about this later

#Player name and chips regex
#re.search(r'(Seat [0-9]): ([a-zA-Z0-9_-]+) \((\d+.\d+)\)', line)

def parseHH(hand):

	field_idx = {}
	field_dict = {}
	field_idx['table'] = []
	field_idx['seats'] = []
	field_idx['sb'] = []
	field_idx['bb'] = []
	field_idx['dealer'] = []
	field_idx['preflop'] = []
	field_idx['flop'] = []
	field_idx['turn'] = []
	field_idx['river'] = []
	field_idx['showdown'] = []
	regex_table = re.compile(r'Table: (.*)')
	regex_seat = re.compile(r'(Seat [0-9]): ([a-zA-Z0-9_-]+)')#\((\d+.\d+)\)')
	regex_dealer = re.compile(r'([a-zA-Z0-9-_]+) has the dealer button')
	regex_sb = re.compile(r'([a-zA-Z0-9-_]+) posts small blind+')
	regex_bb = re.compile(r'([a-zA-Z0-9-_]+) posts big blind+')
	regex_preflop = re.compile(r'\*\* Hole Cards+')
	regex_flop = re.compile(r'\*\* Flop \*\* \[(.*)\]')
	regex_turn = re.compile(r'\*\* Turn \*\* \[(.*)\]')
	regex_turn = re.compile(r'\*\* Turn \*\* \[(.*)\]')
	regex_river = re.compile(r'\*\* River \*\* \[(.*)\]')
	regex_showdown = re.compile(r'\*\* Pot Show Down \*\* \[(.*)\]')
	#regex_oopblind
	for i in range(len(hand)):
		if field_idx['table'] == []:
			table = re.search(regex_table, hand[i])
			if table is not None:
				field_dict['table'] = table.group(1)
		seat = re.search(regex_seat, hand[i])
		if seat is not None:
			field_dict[seat.group(1)] = [seat.group(2)]#, seat.group(3)]
			if field_idx['seats'] == []:
				field_idx['seats'] = [i]
			else:
				field_idx['seats'].append(i)
		if field_idx['dealer'] == []:
			dealer = re.search(regex_dealer, hand[i])
			if dealer is not None:
				field_idx['dealer'] = [i]
				field_dict['dealer'] = dealer.group(1)
		if field_idx['sb'] == []:
			sb = re.search(regex_sb, hand[i])
			if sb is not None:
				field_idx['sb'] = [i]
				field_dict['sb'] = sb.group(1)
		if field_idx['bb'] == []:
			bb = re.search(regex_sb, hand[i])
			if bb is not None:
				field_idx['bb'] = [i]
				field_dict['bb'] = bb.group(1)
		if field_idx['preflop'] == []:
			preflop = re.search(regex_preflop, hand[i])
			if preflop is not None:
				field_idx['preflop'] = [i]
		if field_idx['flop'] == []:
			flop = re.search(regex_flop, hand[i])
			if flop is not None:
				field_idx['flop'] = [i]
				field_dict['flop'] = flop.group(1)
		if field_idx['turn'] == []:
			turn = re.search(regex_turn, hand[i])
			if turn is not None:
				field_idx['turn'] = [i]
				field_dict['turn'] = turn.group(1)
		if field_idx['river'] == []:
			river = re.search(regex_river, hand[i])
			if river is not None:
				field_idx['river'] = [i]
				field_dict['river'] = river.group(1)
		if field_idx['showdown'] == []:
			showdown = re.search(regex_showdown, hand[i])
			if showdown is not None:
				field_idx['showdown'] = [i]
				field_dict['showdown'] = showdown.group(1)
	return [field_idx, field_dict]
	# Now parse bet actions from preflop to showdown:


	#Index lines for: seat information, preflop, flop, turn, river
