import os
import random
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
class generate(object):
	def position_on_current(self, current_player, player, position):
		if position == 0 or position >= 52:
			return position
		player = (player + 4 - current_player) % 4
		return (13 * player + position - 1) % 52 + 1
	def load_image(self,filepath):
		return Image.open(filepath).convert("RGBA")

	def __init__(self):
		self.path = [
			[[(160, 1040), (160, 880), (320, 880), (320, 1040)], (522, 1080), (522, 1001), (522, 921), (522, 841),
			 (522, 762), (439, 678), (359, 678), (280, 678), (200, 678), (121, 678), (41, 678), (41, 604),
			 (41, 526), (121, 526), (200, 526), (280, 526), (359, 526), (439, 526), (521, 442), (521, 363),
			 (521, 286), (521, 203), (521, 124), (521, 45), (599, 45), (676, 45), (676, 124), (676, 203),
			 (676, 286), (676, 363), (676, 442), (757, 527), (836, 527), (916, 527), (996, 527), (1076, 527),
			 (1156, 527), (1156, 603), (1156, 678), (1076, 678), (996, 678), (916, 678), (836, 678), (757, 678),
			 (677, 762), (677, 841), (677, 921), (677, 1001), (677, 1081), (677, 1158), (600, 1158), (600, 1080),
			 (600, 1000), (600, 921), (600, 841), (600, 762), (599, 678)],
			[[(160, 325), (160, 165), (320, 165), (320, 325)], (121, 526), (200, 526), (280, 526), (359, 526),
			 (439, 526), (521, 442), (521, 363), (521, 286), (521, 203), (521, 124), (521, 45), (599, 45),
			 (676, 45), (676, 124), (676, 203), (676, 286), (676, 363), (676, 442), (757, 527), (836, 527),
			 (916, 527), (996, 527), (1076, 527), (1156, 527), (1156, 603), (1156, 678), (1076, 678), (996, 678),
			 (916, 678), (836, 678), (757, 678), (677, 762), (677, 841), (677, 921), (677, 1001), (677, 1081),
			 (677, 1158), (600, 1158), (522, 1158), (522, 1080), (522, 1001), (522, 921), (522, 841), (522, 762),
			 (439, 678), (359, 678), (280, 678), (200, 678), (121, 678), (41, 678), (41, 604), (121, 604),
			 (200, 604), (280, 604), (360, 604), (440, 604), (522, 604)],
			[[(876, 325), (876, 165), (1036, 165), (1036, 325)], (676, 124), (676, 203), (676, 286), (676, 363),
			 (676, 442), (757, 527), (836, 527), (916, 527), (996, 527), (1076, 527), (1156, 527), (1156, 603),
			 (1156, 678), (1076, 678), (996, 678), (916, 678), (836, 678), (757, 678), (677, 762), (677, 841),
			 (677, 921), (677, 1001), (677, 1081), (677, 1158), (600, 1158), (522, 1158), (522, 1080), (522, 1001),
			 (522, 921), (522, 841), (522, 762), (439, 678), (359, 678), (280, 678), (200, 678), (121, 678),
			 (41, 678), (41, 604), (41, 526), (121, 526), (200, 526), (280, 526), (359, 526), (439, 526),
			 (521, 442), (521, 363), (521, 286), (521, 203), (521, 124), (521, 45), (599, 45), (599, 124),
			 (599, 203), (599, 286), (599, 363), (599, 442), (599, 527)],
			[[(876, 1040), (876, 880), (1036, 880), (1036, 1040)], (1076, 678), (996, 678), (916, 678), (836, 678),
			 (757, 678), (677, 762), (677, 841), (677, 921), (677, 1001), (677, 1081), (677, 1158), (600, 1158),
			 (522, 1158), (522, 1080), (522, 1001), (522, 921), (522, 841), (522, 762), (439, 678), (359, 678),
			 (280, 678), (200, 678), (121, 678), (41, 678), (41, 604), (41, 526), (121, 526), (200, 526),
			 (280, 526), (359, 526), (439, 526), (521, 442), (521, 363), (521, 286), (521, 203), (521, 124),
			 (521, 45), (599, 45), (676, 45), (676, 124), (676, 203), (676, 286), (676, 363), (676, 442),
			 (757, 527), (836, 527), (916, 527), (996, 527), (1076, 527), (1156, 527), (1156, 603), (1075, 604),
			 (996, 604), (916, 604), (836, 604), (757, 604), (674, 603)]
		]
		self.colors = ["board/blue", "board/red", "board/green", "board/yellow"]
		self.cached_images = {
			"bord": {},
			"colors": {}
		}

		
	def generate2(self, positions, players):
		file_list = []
		with ThreadPoolExecutor() as executor:
			# Preload all necessary images
			futures = {}
			for color in self.colors:
				futures[f"{color}.png"] = executor.submit(self.load_image, f"{color}.png")
				for i in range(1, 5):
					futures[f"{color}{i}.png"] = executor.submit(self.load_image, f"{color}{i}.png")
			for at in players:
				futures[f"board/bord{at}.png"] = executor.submit(self.load_image, f"board/bord{at}.png")

			for key, future in futures.items():
				self.cached_images["colors" if key.startswith(tuple(self.colors)) else "bord"][key] = future.result()

		def process_player_image(at):
			img1 = self.cached_images["bord"][f"board/bord{at}.png"].convert("RGB")

			for i in range(4):
				if i == at:
					continue

				for j in range(4):
					img2 = self.cached_images["colors"][f"{self.colors[i]}.png"]
					if positions[i][j] != 0:
						count = sum(1 for k in range(j + 1, 4) if positions[i][j] == positions[i][k])

						if positions[i][j] < 52:
							count += sum(
								1 for k in range(i + 1, 4) if k != at for l in positions[k] if l < 52 and self.position_on_current(i, k, l) == positions[i][j]
							)
							count += sum(1 for l in positions[at] if self.position_on_current(i, at, l) == positions[i][j])

						pos = self.path[(i - at) % 4][positions[i][j]]
						img1.paste(img2, (pos[0] - 28 - 6 * count, pos[1] - 40), mask=img2)
					else:
						pos = self.path[(i - at) % 4][0][j]
						img1.paste(img2, pos, mask=img2)

			for i in range(4):
				img2 = self.cached_images["colors"][f"{self.colors[at]}{i + 1}.png"]
				count = sum(1 for j in range(i + 1, 4) if positions[at][i] == positions[at][j])

				if positions[at][i] != 0:
					pos = self.path[0][positions[at][i]]
					img1.paste(img2, (pos[0] - 28 - 6 * count, pos[1] - 40), mask=img2)
				else:
					pos = self.path[0][0][i]
					img1.paste(img2, pos, mask=img2)

			img1 = img1.convert('RGB')

			if not os.path.exists("gena"):
				os.makedirs("gena")

			random_number = str(random.randint(1000000000, 9999999999))
			img1.save(f"gena/{random_number}.jpg", optimize=True, quality=50)
			return f"{random_number}.jpg"

		with ThreadPoolExecutor() as executor:
			results = list(executor.map(process_player_image, players))

		file_list.extend(results)
		return file_list

#import hashlib
#import shutil
#count = 0
#dat = [[random.randint(0, 57), random.randint(0, 57), random.randint(0, 57), random.randint(0, 57)], [random.randint(0, 57), random.randint(0, 57), random.randint(0, 57), random.randint(0, 57)], [random.randint(0, 57), random.randint(0, 57), random.randint(0, 57), random.randint(0, 57)], [random.randint(0, 57), random.randint(0, 57), random.randint(0, 57), random.randint(0, 57)]]
#import time
#p = generate()
#st = time.time()
#p.generate2(dat, [1,3])
#p.generate2(dat, [0,2])
#print(time.time()-st)