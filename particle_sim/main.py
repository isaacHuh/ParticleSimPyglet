import pyglet
import particle
from pyglet.window import key

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_location(400,100)
		self.size = (800,600)
		self.frame_rate = 1/60.0
		self.particles = []
		self.particle_size = 15
		self.spawning = False
		self.type = "sand"

		self.move_right = False
		self.move_left = False
		self.move_up = False
		self.move_down = False

		self.spawn_point = particle.SpawnPoint(self.particle_size, 300, 300)

		self.text = pyglet.text.Label('Particle Simulation',
                          font_name='Arial',
                          font_size=12,
                          x=10, y=self.size[1]-10,
                          anchor_y="top",
                          multiline=True,
                          width=500,
                          bold=True,
                          italic=True,
                          color=(255, 255, 0, 255))


	def on_draw(self):
		main_batch = pyglet.graphics.Batch()

		self.clear()

		for i in self.particles:
			main_batch.add(6, pyglet.gl.GL_TRIANGLES, None,
								#[0,1,2,1,2,3],
								('v2i', (i.x, i.y,
										i.x, i.y + i.size,
										i.x + i.size, i.y,

										i.x, i.y + i.size,
										i.x + i.size, i.y,
										i.x + i.size, i.y + i.size)),

                                ('c3B', i.color * 6)
                                )
		
		spawn_point = self.spawn_point
		main_batch.add(6, pyglet.gl.GL_TRIANGLES, None,
								#[0,1,2,1,2,3],
								('v2i', (spawn_point.x, spawn_point.y,
										spawn_point.x, spawn_point.y + spawn_point.size,
										spawn_point.x + spawn_point.size, spawn_point.y,

										spawn_point.x, spawn_point.y + spawn_point.size,
										spawn_point.x + spawn_point.size, spawn_point.y,
										spawn_point.x + spawn_point.size, spawn_point.y + spawn_point.size)),

                                ('c3B', (255,255,255) * 6))
		
		self.text.batch = main_batch

		main_batch.draw()

		#self.spawn_point.draw()
		#self.text.draw()



	def update(self, dt):
		if(self.move_right):
			self.spawn_point.move_to((self.spawn_point.x + self.spawn_point.size, self.spawn_point.y), 
										self.size[0], self.size[1])
		if(self.move_left):
			self.spawn_point.move_to((self.spawn_point.x - self.spawn_point.size, self.spawn_point.y), 
										self.size[0], self.size[1])
		if(self.move_up):
			self.spawn_point.move_to((self.spawn_point.x, self.spawn_point.y + self.spawn_point.size), 
										self.size[0], self.size[1])
		if(self.move_down):
			self.spawn_point.move_to((self.spawn_point.x, self.spawn_point.y - self.spawn_point.size), 
										self.size[0], self.size[1])

		if(self.spawning):
			x_pos = self.spawn_point.x
			y_pos = self.spawn_point.y

			if(particle.particle_at(x_pos, y_pos, self.particles) == None):
				self.particles.append(particle.Particle(self.type, self.particle_size, x_pos, y_pos))

		particles = [0,0,0,0]
		for i in self.particles:
			'''
			if(i.type == "sand"):
				particles[0] += 1
			if(i.type == "water"):
				particles[1] += 1
			if(i.type == "lava"):
				particles[2] += 1
			if(i.type == "smoke"):
				particles[3] += 1
			'''
			if(i.moving):
				i.move(self.particles, self.size[0], self.size[1])

		self.text.text = "Particle Simulation\n\n" + \
							"Total Particles: {}\n".format(len(self.particles)) + \
							"Land Particles: {}\n".format(particles[0]) + \
							"Water Particles: {}\n".format(particles[1]) + \
							"Lava Particles {}\n".format(particles[2]) + \
							"Smoke Particles {}\n".format(particles[3])

	'''
	def on_mouse_press(self, x, y, button, modifiers):
		if(button == pyglet.window.mouse.LEFT):
			self.mouse_pos[0] = x
			self.mouse_pos[1] = y
			#self.mouse_hold = True

			x_pos = int(self.mouse_pos[0]/self.particle_size) * self.particle_size
			y_pos = int(self.mouse_pos[1]/self.particle_size) * self.particle_size

			if(particle.particle_at(x_pos, y_pos, self.particles) == None):
				self.particles.append(particle.Particle(self.type, self.particle_size, x_pos, y_pos))


	def on_mouse_release(self, x, y, button, modifiers):
		if(button == pyglet.window.mouse.LEFT):
			self.mouse_hold = False

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.mouse_pos[0] = x
		self.mouse_pos[1] = y
		x_pos = int(self.mouse_pos[0]/self.particle_size) * self.particle_size
		y_pos = int(self.mouse_pos[1]/self.particle_size) * self.particle_size

		if(particle.particle_at(x_pos, y_pos, self.particles) == None):
			self.particles.append(particle.Particle(self.type, self.particle_size, x_pos, y_pos))
	'''
	def on_key_press(self, symbol, modifiers):
		if(symbol == key.UP):
			self.move_up = True
		if(symbol == key.DOWN):
			self.move_down = True
		if(symbol == key.RIGHT):
			self.move_right = True
		if(symbol == key.LEFT):
			self.move_left = True


		if(symbol == key.R):
			self.particles.clear()
		if(symbol == key._1):
			self.type = "sand"
		if(symbol == key._2):
			self.type = "water"
		if(symbol == key._3):
			self.type = "lava"	
		if(symbol == key.SPACE):
			self.spawning = True

	def on_key_release(self, symbol, modifiers):
		if(symbol == key.UP):
			self.move_up = False
		if(symbol == key.DOWN):
			self.move_down = False
		if(symbol == key.RIGHT):
			self.move_right = False
		if(symbol == key.LEFT):
			self.move_left = False

		if(symbol == key.SPACE):
			self.spawning = False


if __name__ == "__main__":
	window = GameWindow(800,600,"Particle Simulation", resizable = False)
	cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
	window.set_mouse_cursor(cursor)

	pyglet.clock.schedule_interval(window.update, window.frame_rate)
	pyglet.app.run()


