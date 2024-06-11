import numpy as np
class game(object):
	def rand(self):
		return np.random.randint(low = 1,high=6)
	def next_player(self, player):
		return (self.player_shift + player)%4
	def is_safe(self, position):
		if ((position-1)%14 == 0): return 1
		elif ((position-9)%14 == 0): return 1
		elif (position>=52 and position<=57): return 1
		else: return 0
	def position_on_current(self, player, position):
		if (position == 0 or position >= 52): return position
		else:
			player = (player+4-self.current_player)%4
			return (13*player+position-1)%52+1
	def __init__(self, players):
		self.count_dice = 0

		self.dice_pending_moves = 1
		self.dice_got = []
		self.last_got_dice = 0

		self.dice_move = 0
		self.guti_move = 1
		self.no_move = 2

		self.position = [0]
		self.position_self = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		
		if (players != 2 and players != 4): players = 4
		self.players = players
		if (players == 2): self.player_shift = 2
		elif (players == 4): self.player_shift = 1
		self.current_player = 0
		self.count_six = 0
		self.current_condition = self.dice_move

		self.guti_can_be_moved = []

	def status(self):
		current_player = self.current_player
		players = [current_player]
		current_player = self.next_player(current_player)
		while current_player != players[0]:
			players.append(current_player)
			current_player = self.next_player(current_player)
		players.sort()
		return [players, self.current_player, self.current_condition, self.position_self]
	def dice(self, value):
		if(self.dice_pending_moves and self.current_condition == self.dice_move):
			if (value == 0): value = self.rand()
			self.last_got_dice = value
			if (value>=1 and value<=5):
				self.dice_got += [6]*self.count_six
				self.dice_got.append(value)
				self.dice_pending_moves -= 1
				if self.position_self[self.current_player] == [0, 0, 0, 0] and self.dice_pending_moves == 0 and 6 not in self.dice_got:
					self.dice_got = []
				#if self.position_self[self.current_player] == [0, 0, 0, 0] and self.dice_pending_moves == 0 and 6 not in self.dice_got:
				#No move when almost finish need to be handled
				self.count_six = 0
			elif (value== 6):
				self.count_six += 1
				if (self.count_six == 3):
					self.dice_pending_moves -= 1
					self.count_six = 0
				else:
					self.current_condition = self.dice_move
			else: return
			
			self.count_dice += 1
			if (self.dice_pending_moves == 0):
				if(len(self.dice_got) == 0):
					self.current_player = self.next_player(self.current_player)
					self.dice_pending_moves = 1
					self.current_condition = self.dice_move
				else:
					self.current_condition = self.guti_move
			
			return self.dice_got

	def can_move_by_dice(self, value):
		self.guti_can_be_moved = []
		if value in self.dice_got:
			for i in range(4):
				if (self.position_self[self.current_player][i] == 0 and value == 6): self.guti_can_be_moved.append(i) #max 57
				elif (self.position_self[self.current_player][i] != 0 and self.position_self[self.current_player][i] + value <= 57): self.guti_can_be_moved.append(i)
		return self.guti_can_be_moved
	def make_move(self, value, at):
		if (self.dice_pending_moves == 0):
			print("////", self.guti_can_be_moved, self.dice_got)
			if (at in self.guti_can_be_moved and value in self.dice_got):
				self.dice_got.remove(value)
				
				if (value == 6 and self.position_self[self.current_player][at] == 0): #move out from home
					self.position_self[self.current_player][at] = 1
				
				elif (self.position_self[self.current_player][at] + value <= 57): #O/W
					self.position_self[self.current_player][at] += value
					if (self.is_safe(self.position_self[self.current_player][at]) == 0):
						player = self.current_player
						player = self.next_player(player)
						cut_count = 0
						who = 0
						which = 0
						while player != self.current_player:
							for guti in self.position_self[player]:
								position = self.position_on_current(player, guti)
								if (position == self.position_self[self.current_player][at]):
									cut_count +=1
									who = player
									which = guti
							player = self.next_player(player)
						if (cut_count == 1):
							self.position_self[who][which] = 0
							self.current_condition = self.dice_move
							self.dice_pending_moves += 1
				if (self.dice_pending_moves == 0 and len(self.dice_got) == 0):
					self.current_player = self.next_player(self.current_player)
					self.dice_pending_moves = 1
					self.current_condition = self.dice_move
		return
	def can_move_by_guti(self, value):
		self.dice_can_be_moved = []
		for dice_value in self.dice_got:
			if self.position_self[self.current_player][value] == 0 and dice_value == 6:
				self.dice_can_be_moved.append(dice_value)
			elif self.position_self[self.current_player][value] != 0 and self.position_self[self.current_player][value] <= 57:
				self.dice_can_be_moved.append(dice_value)
		return self.dice_can_be_moved
	def avail_guti(self):
		available = []
		for guti in range(4):
			available.append(self.can_move_by_guti(guti))
		return available

"""a = game(2)
#print(a.status())
a.dice(5)
a.avail_guti()
a.dice(6)
a.dice(5)
a.avail_guti()
a.can_move_by_dice(6)
a.make_move(6,0)
print(a.status())
#print(a.status(),a.avail_guti())
#a.dice(2)
#print(a.status())
#print(a.status(),a.last_got_dice, a.dice_got, a.can_move_by_dice(2), a.can_move_by_dice(6),a.make_move(6,0),a.status())"""