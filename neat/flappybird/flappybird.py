import pygame
from random import randint

class environment():
	def __init__(self, mode='ai'):
		self.H = 500
		self.W = 700
		# tubes
		self.tubes = []
		self.voidSize = 100
		self.tubeWidth = 70
		self.tubeSpeedInitial = 5.0
		self.tubeAcc = 0.00005
		# bird
		self.a = 0.04
		self.jump = -1.3
		self.x = 100
		self.birdSize = 10
		self.action_space = 2
		self.mode = mode
		self.green = (0,255,0)
		self.yellow = (250,250,20)
		self.sky = (135,206,235)
		if self.mode == 'human':
			pygame.init()
			self.gameDisplay = pygame.display.set_mode((self.W,self.H))

	def sample(self):
		return randint(0,1)

	def reset(self):
		self.y = int(self.H/2)
		self.v = 0
		self.tubeSpeed = self.tubeSpeedInitial
		self.tubes = []
		self.addTube()
		return [self.tubeSpeed, self.tubes[0][0]-(self.x+self.birdSize), self.tubes[0][1], self.x, self.y, self.v]

	def addTube(self):
		self.tubes.append([self.W,randint(int(self.H*0.4),int(self.H*0.9))])

	def step(self, action):
		# tubes
		for i in self.tubes:
			i[0] -= self.tubeSpeed
		for i in self.tubes:
			if i[0]<0:
				self.tubes = self.tubes[1:]
				self.addTube()
		self.tubeSpeed += self.tubeAcc
		# bird
		if action == 0:
			self.v += self.a
		if action == 1:
			self.v = self.jump
		self.y += self.v
		# dead
		result = [self.tubeSpeed, self.tubes[0][0]-(self.x+self.birdSize), self.tubes[0][1], self.x, self.y, self.v]
		if self.y<0 or self.y>self.H:
			return result, -1, 1, ""
		for i in self.tubes:
			if (i[0]<=self.x+self.birdSize and self.x-self.birdSize<=i[0]+self.tubeWidth) and \
				not(i[1]>=self.y+self.birdSize and self.y-self.birdSize>=i[1]-self.voidSize):
				return result, -1, 1, ""
		# alive
		return result, 1, 0, ""

	def render(self):
		if self.mode == 'human':
			self.gameDisplay.fill(self.sky)
			pygame.draw.circle(self.gameDisplay, self.yellow, (self.x,int(self.y)), self.birdSize)
			for i in self.tubes:
				pygame.draw.rect(self.gameDisplay, self.green,(int(i[0]),int(i[1]),self.tubeWidth,int(self.H-i[1])))
				pygame.draw.rect(self.gameDisplay, self.green,(int(i[0]),0,self.tubeWidth,int(i[1]-self.voidSize)))
			pygame.display.update()


"""
env = environment('human')
env.reset()
while True:
	v = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				v = 1
	if(env.step(v)[1]==-1):
		env.reset()
		print("ouch")
	#env.render()
"""