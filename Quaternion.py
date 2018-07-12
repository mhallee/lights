class Quaternion:
	"""Represents the angle of a brick in quaternion format:
	where x,y,z define a vector of a brick axes and w is 
	the rotation around that axis"""	
	def __init__(self,w,x,y,z):
		self.w = w
		self.x = x
		self.y = y
		self.z = z