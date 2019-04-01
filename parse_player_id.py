import pickle

player_name_id_dict = {}
with open('playerId.txt', 'r') as f:
	lines = f.readlines()
	for line in lines:
		id_name = line.strip().split('/')
		id_num = int(id_name[0])
		name = id_name[1].split(',')
		if len(name) != 1:
			firstname = name[1].strip()
			lastname = name[0].strip()
			name = firstname + ' ' + lastname
		elif len(name) == 1:
			name = name[0].strip()
		player_name_id_dict[name] = id_num

filename = 'player_name_id_dict'
outfile = open(filename,'wb')
pickle.dump(player_name_id_dict, outfile)
outfile.close()