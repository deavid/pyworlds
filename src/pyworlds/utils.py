import soya,math

def xy_toangle(x1,y1):
	h_xz=math.sqrt(x1*x1+y1*y1)
	x=x1/h_xz
	z=y1/h_xz
	angle=math.asin(z)*180/math.pi
	if x<0:
		angle+=90  # place 0 degrees up
		angle=-angle # mirror the result
		angle-=90  # restore it.
		
	if angle<0: angle+=360
	
	return angle



def Box(x,y,z,parent = None, material = None, insert_into = None, texcoord_size=1, origin=(0,0,0)):
	"""Box(parent = None, material = None, insert_into = None) -> World

Creates and returns a World in PARENT, containing a box(x,y,z) length centered
on the origin, with material MATERIAL.

If INSERT_INTO is not None, the cube's faces are inserted into it, instead of
creating a new world."""
	ox=origin[0]
	oy=origin[1]
	oz=origin[2]
	
	cube = insert_into or soya.World(parent)
	s = texcoord_size
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									], material)

	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									], material)
	

	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									], material)
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									], material)
	
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									], material)
	soya.Face(cube, [soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									], material)
	
	return cube

	


def Sphere(parent = None, material = None, quality = (10,10), smooth_lit = 1, insert_into = None, 
					texcoords=[(0,1),(0,1)], size=(1,1,1),position=(0,0,0)):
	"""Sphere(parent = None, material = None, slices = 20, stacks = 20, insert_into = None, min_tex_x = 0.0, max_tex_x = 1.0, min_tex_y = 0.0, max_tex_y = 1.0) -> World

Creates and returns a World in PARENT, containing a sphere of 1 radius centered
on the origin, with material MATERIAL.

SLICES and STACKS can be used to control the quality of the sphere.

If INSERT_INTO is not None, the sphere's faces are inserted into it, instead of
creating a new world.

MIN/MAX_TEX_X/Y can be used to limit the range of the texture coordinates to the given
values."""
	from math import sin, cos
	slices = quality[0]
	stacks = quality[1]
	
	min_tex_x = texcoords[0][0] 
	max_tex_x = texcoords[0][1]
	min_tex_y = texcoords[1][0]
	max_tex_y = texcoords[1][1]

	px=position[0]
	py=position[1]
	pz=position[2]
	
	sx=size[0]
	sy=size[1]
	sz=size[2]
	
	
	sphere = insert_into or World(parent)
	
	step1 = 6.28322 / slices
	step2 = 3.14161 / stacks
	
	angle1 = 0.0
	for i in xrange(slices):
		angle2 = 0.0
		j = 0
		
		face = soya.Face(sphere, [
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1 + step1) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			], material)
		face.smooth_lit = smooth_lit
		angle2 += step2
		
		for j in range(1, stacks - 1):
			face = soya.Face(sphere, [
				soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
				soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1 + step1) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
				soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1 + step1) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
				soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
				], material)
			face.smooth_lit = smooth_lit
			angle2 += step2

		j = stacks - 1
		
		face = soya.Face(sphere, [
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1 + step1) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			], material)
		face.smooth_lit = smooth_lit
		
		angle1 += step1
		
	return sphere














def look_at_elastic(self,p2,vector=None, factor=0.5, sqrt_from=15):
	if p2 == None: raise Exception, "lookat_elastic: You must give at least the p2 parameter"
	if vector == None:
		vector = soya.Vector(self,0,0,-1000)

	q=vector % self.parent # I mean an upper container.
	
	v1 = (self >> q)
	v2 = (self >> p2)
	
	angle = v1.angle_to(v2)
	
	v12 = v1.cross_product(v2)
	a12 = v1.dot_product(v2)
	if a12<0: angle = -angle
	if abs(angle)>90: angle=-angle
	v12.normalize()
	if abs(angle) < 0.1: 
		return
	if abs(angle) == 180.0: angle=180.1;

	original_angle=angle
	
	if angle>sqrt_from:
		angle/=sqrt_from
		angle=math.sqrt(angle)
		angle*=sqrt_from	
	
	angle*=factor
	
	self.rotate_axis(angle, v12)

