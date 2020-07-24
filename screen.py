import pygame
import math
from random import randint  

class Screen():
	def __init__(self):
		#global variable
		#size
		self.width = 1280
		self.height = 720
		#colors
		self.white = pygame.Color(255, 255, 255)
		self.black = pygame.Color(0, 0, 0)
		self.red = pygame.Color(138, 14, 11)
		self.green = pygame.Color(13, 69, 50)
		self.orange = pygame.Color(255, 106, 0)
		#screen
		self.screen = pygame.display.set_mode((self.width, self.height))
		#font
		pygame.font.init() 
		self.fontSize = 35
		self.font = pygame.font.SysFont("Italic", self.fontSize)
		#traceList
		self.tracesList = []

	#draw background color with border
	def drawBackground(self):
		self.screen.fill(self.white)

		backgroudPoints = []
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.05)]);#left-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.05)]);#right-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.9)]);#right-bottom
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.9)]);#left-bottom

		pygame.draw.lines(self.screen, self.black, True, backgroudPoints, 5)

	#draw hero on heros position
	def drawHero(self, hero):
		pygame.draw.circle(self.screen, self.orange, hero, 7)

	#draw all houses. First and last have difrent color
	def drawHouses(self, houses):
		#first
		self.cDrawHouse(houses[0][0], houses[0][1], self.green, 0)
		
		#from second to one before last
		for i in range(1, len(houses) - 1):
			self.drawHouse(houses[i][0], houses[i][1], i)
		#last
		self.cDrawHouse(houses[len(houses) - 1][0], houses[len(houses) - 1][1], self.green, len(houses) - 1)

	def drawHouse(self, x, y, number):
		color = self.black
		#draw roof
		pygame.draw.rect(self.screen, color, (x - 30, y - 25, 60, 15))
		pygame.draw.polygon(self.screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
		pygame.draw.polygon(self.screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
		
		#draw house
		pygame.draw.rect(self.screen, color, (x - 30, y - 12, 60, 35))

		#render house number
		self.screen.blit(self.font.render(str(number), False, self.orange),(x - int(self.fontSize / 5),y - int(self.fontSize / 5)))

	def cDrawHouse(self, x, y, color, number):
		#draw roof
		pygame.draw.rect(self.screen, color, (x - 30, y - 25, 60, 15))
		pygame.draw.polygon(self.screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
		pygame.draw.polygon(self.screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
		
		#draw house
		pygame.draw.rect(self.screen, color, (x - 30, y - 12, 60, 35))

		#render house number
		self.screen.blit(self.font.render(str(number), False, self.orange),(x - int(self.fontSize / 5),y - int(self.fontSize / 5)))

	def drawAllTraces(self):
		for trace in self.tracesList:
			self.drawTrace(trace)

	def drawTrace(self, houses):
		#random color
		color = pygame.Color(randint(0,255), randint(0,255), randint(0,255));
		pygame.draw.lines(self.screen, color, False, houses, 3)
		if houses not in self.tracesList:
			self.tracesList.append(houses)

	def calcDistance(self, first, second):
		return math.sqrt(math.pow((first[0] - second[0]),2) + math.pow((first[1] - second[1]),2))

	def collcionTest(self, newHouse, houses):
		for house in houses:
			if house == None:
				continue
			if self.calcDistance(newHouse, house) < 150:
				return True
		return False

	def randomHouses(self, amount):
		minW = int(self.width * 0.05) + 50
		maxW = int(self.width * 0.9) - 50
		minH = int(self.height * 0.05)  + 50
		maxH = int(self.height * 0.9) - 50

		houses = [None] * amount
		distances = {}
		
		for i in range(amount):

			while True:
				x = randint(minW, maxW)
				y = randint(minH, maxH)
				if not self.collcionTest([x,y],houses):
					break

			#set random house to array[i]
			houses[i] = [x,y]
			
			#create distances set for house
			distances[str(i)] = {}
			if i > 1:
				#get 2 previous house distance to house[i]  
				distances[str(i-1)][str(i)] = self.calcDistance(houses[i-1], houses[i])
				self.drawTrace([houses[i-1], houses[i]])
				distances[str(i-2)][str(i)] = self.calcDistance(houses[i-2], houses[i])
				self.drawTrace([houses[i-2], houses[i]])
				#get distance from house[i] to 2 previous house
				distances[str(i)][str(i-2)] = self.calcDistance(houses[i], houses[i-2])
				distances[str(i)][str(i-1)] = self.calcDistance(houses[i], houses[i-1])

			if i == 1:
				#set distance to house[1] from house[0]
				distances["0"]["1"] = self.calcDistance(houses[0], houses[1])
				self.drawTrace([houses[0], houses[1]])
				#set distance to house[0] from house[1]
				distances["1"]["0"] = self.calcDistance(houses[1], houses[0])

		return [houses, distances]

	def updateScreen(self):
		pygame.display.update()

	def isExit(self):
		try:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					return True
		except pygame.error as error:
			return False
		return False