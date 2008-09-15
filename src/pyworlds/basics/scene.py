import soya
import pyworlds.basics.body

class Scene(soya.World,pyworlds.basics.body.Body):

	round_duration=.04
	def begin_round(self):
		soya.World.begin_round(self)

	def advance_time(self, proportion):
		soya.World.advance_time(self, proportion)


scene = None


scene = Scene()

