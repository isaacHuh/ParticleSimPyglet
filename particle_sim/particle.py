import random as rnd
import pyglet

def particle_at(x, y, particle_list):		
	for i in range(len(particle_list)):
		if(particle_list[i].x == x and particle_list[i].y == y and particle_list[i].type != "smoke"):
			return particle_list[i]
	return None

def out_of_range(pos, window_width, window_height):
	if(pos[0] > window_width or pos[0] < 0 or pos[1] > window_height or pos[1] < 0):
		return True
	return False

def swap_particle_pos(particle1, particle2, particles, width, height):
	temp = (particle1.x, particle1.y)

	particle1.x = particle2.x
	particle1.y = particle2.y

	particle2.x = temp[0]
	particle2.y = temp[1]

	particle1.moving = True
	particle2.moving = True
	particle1.move(particles, width, height)
	#particle2.move(particles, width, height)

def swap_particle_up(particle1, particles):
	particle2 = particle_at(particle1.x, particle1.y + particle1.size, particles)
	if(particle2 == None):
		particle1.y += particle1.size
		particle1.moving = True
		return

	particle1.x = particle2.x
	particle1.y = particle2.y

	particle1.moving = True
	particle2.moving = True

	swap_particle_up(particle2, particles)

class Particle:
	def __init__(self, particle_type, particle_size, x_pos, y_pos):
		self.size = particle_size
		self.x = x_pos
		self.y = y_pos
		self.moving = True
		self.type = particle_type

		self.color = (255, 255, 255)

		if(self.type == "sand"):
			self.color = (66, 245, 132)
		elif(self.type == "water"):
			self.color = (66, 145, 245)
		elif(self.type == "lava"):
			self.color = (235, 64, 52)
		elif(self.type == "smoke"):
			self.color = (115, 115, 115)



	#set surrounding particles ot moving
	def set_to_move(self, particles):

		particles_to_move =	(particle_at(self.x,self.y - self.size, particles),
							particle_at(self.x - self.size,self.y, particles),
							particle_at(self.x + self.size,self.y, particles))

		for i in particles_to_move:
			if(i == None):
				continue
			else:
				i.moving = True

	def move(self, particle_list, window_width, window_height):

		if(self.type == "smoke"):
			if(self.y > window_height):
				particle_list.remove(self)
				return
			
			self.y += self.size#*rnd.random()

			if(rnd.random() < 0.5):
				self.x += self.size#*rnd.random()
			else:
				self.x -= self.size#*rnd.random()

			return

		moves = [(self.x, self.y - self.size), 
				(self.x - self.size, self.y - self.size), 
				(self.x + self.size, self.y - self.size)]

		if(self.type == "water" or self.type == "lava"):
			if(rnd.random() < 0.5):
				moves.append((self.x - self.size, self.y))
				moves.append((self.x + self.size, self.y))
			else:
				moves.append((self.x + self.size, self.y))
				moves.append((self.x - self.size, self.y))
		
		#movement
		for new_pos in moves:
			particle_collide = particle_at(new_pos[0], new_pos[1], particle_list)

			valid = False

			if(particle_collide == None):
				valid = True
			elif(particle_collide.type == "smoke"):
				valid = True

			if(valid):
				if(out_of_range(new_pos, window_width, window_height)):
					continue

				self.set_to_move(particle_list)

				self.x = new_pos[0]
				self.y = new_pos[1]
				return
			elif((particle_collide.type == "water" or particle_collide.type == "lava") and self.type == "sand"):
				swap_particle_pos(particle_collide, self, particle_list, window_width, window_height)
				return
			elif((particle_collide.type == "lava" and self.type == "water") or (particle_collide.type == "water" and self.type == "lava")):
				particle_list.append(Particle("smoke", self.size, self.x, self.y))
				
				particle_collide.set_to_move(particle_list)
				self.set_to_move(particle_list)

				particle_list.remove(particle_collide)
				particle_list.remove(self)
				return
		
		self.moving = False


class SpawnPoint:
	def __init__(self, particle_size, x_pos, y_pos):
		self.size = particle_size
		self.x = x_pos
		self.y = y_pos

	def move_to(self, new_pos, width, height):
		if(out_of_range(new_pos, width, height)):
			return
		else:
			self.x = new_pos[0]
			self.y = new_pos[1]

	def draw(self):

		pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
								[0,1,2,1,2,3],
								('v2i', (self.x, self.y,
										self.x, self.y + self.size,
										self.x + self.size, self.y,
										self.x + self.size, self.y + self.size)),

                                ('c3B', (255,255,255) * 4))


