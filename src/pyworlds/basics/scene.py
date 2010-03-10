import soya
import pyworlds.basics.body

class Scene(soya.World,pyworlds.basics.body.Body):

	round_duration=.04
        # Commented because it does nothing and it uses a 6% of CPU
	"""def begin_round(self):
		soya.World.begin_round(self)
		# TODO: place master callback here!
        """
        # Commented because it does nothing and it uses a 6% of CPU
	"""def advance_time(self, proportion):
		soya.World.advance_time(self, proportion)
		# TODO: place master callback here!
        """
        # Commented because it does nothing and it uses a 6% of CPU
	"""def end_round(self):
		soya.World.end_round(self)
		# TODO: place master callback here!
        """
scene = None


scene = Scene()

