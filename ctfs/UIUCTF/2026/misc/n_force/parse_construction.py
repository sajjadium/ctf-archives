from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterator, Callable
import gmpy2

# Outcome of reading a construction. `status` is authoritative; `score` is only
# meaningful when status == "valid". Previously read_str returned -1 for a failed
# construction, which callers compared against False -- and -1 == False is False,
# so every invalid submission was silently treated as a success.
VALID = "valid"
INVALID = "invalid"
INCOMPLETE = "incomplete"


@dataclass(slots=True)
class ParseResult:
	status: str
	score: Optional[int] = None
	detail: str = ""

	@property
	def ok(self) -> bool:
		return self.status == VALID

PREC = 4096
# epsilon to compare two floating points
EPS = gmpy2.mpfr("1e-640")

# Floating point comparison with epsilon
def _close(a, b = 0):
    return abs( a - b ) < EPS


def _rel_close(a, b) -> bool:
	"""Scale-independent comparison for polygon invariants."""
	delta = abs(a - b)
	scale = max(abs(a), abs(b))
	return delta == 0 or (scale != 0 and delta <= EPS * scale)


def _finite(*values) -> bool:
	return all(gmpy2.is_finite(value) for value in values)

# Utility function for 3x3 determinant
def det_33(M: list):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return det


@dataclass(slots=True)
class Point:
    x: object
    y: object
    name: str

    def __post_init__(self):
        self.x = gmpy2.mpfr(self.x)
        self.y = gmpy2.mpfr(self.y)
        
    @staticmethod
    def distance_squared(pt1: Point, pt2: Point):
        dx = pt1.x - pt2.x
        dy = pt1.y - pt2.y
        return dx * dx + dy * dy

    def __repr__(self):
        return f"{self.name}: ({self.x}, {self.y})"

class Line:
	# Represent line as a x + b y + c = 0
	# See https://github.com/sympy/sympy/blob/16fa855354eb7bcabd3fe10993841e03b1382692/sympy/geometry/line.py#L1987
	def __init__(self, p1: Point, p2: Point, name: Optional[str] = None):
		if Point.distance_squared(p1, p2) == 0:
			raise ValueError("a line requires two distinct points")
		x1 = p1.x
		y1 = p1.y
		x2 = p2.x
		y2 = p2.y
		if _close( x1 , x2 ):  # Vertical line
			self.a, self.b, self.c = (gmpy2.mpfr(1), gmpy2.mpfr(0), -x1)
		elif _close( y1 , y2 ):  # Horizontal line
			self.a, self.b, self.c = (gmpy2.mpfr(0), gmpy2.mpfr(1), -y1)
		else:
			self.a, self.b, self.c = (y1 - y2, x2 - x1, x1 * y2 - y1 * x2)
		self.name = name if name is not None else f"Line({p1.name}, {p2.name})"

	@classmethod
	def from_coeffs(
		cls, a, b, c, name: str
	):
		line_out = cls.__new__(cls)
		line_out.a = a
		line_out.b = b
		line_out.c = c
		line_out.name = name
		return line_out

	def __iter__(self):
		# Return coefficients of equation representing line
		return iter([self.a, self.b, self.c])

	def __repr__(self):
		return self.name

class Circle:
	def __init__(self, center: Point, pt_on_circle: Point, name: Optional[str] = None):
		self.c = center
		self.r2 = Point.distance_squared(center, pt_on_circle)
		if self.r2 == 0:
			raise ValueError("a circle requires a non-zero radius")
		self.name = name

	def __repr__(self):
		return (
			self.name
			if self.name is not None
			else f"Circle(c={self.c.name}, r2={self.r2})"
		)

def _meets_line_line(L1: Line, L2: Line, name_out: str) -> Point:
	# Solve the system
	# A1 x + B1 y + C1 = 0
	# A2 x + B2 y + C2 = 0
	A1, B1, C1 = tuple(L1)
	A2, B2, C2 = tuple(L2)
	if _close( A1 * B2 - A2 * B1 ):
		raise ValueError(f"lines {L1} and {L2} are parallel!")
	px = (B2 * C1 - B1 * C2) / (A2 * B1 - A1 * B2)
	py = (A1 * C2 - A2 * C1) / (A2 * B1 - A1 * B2)
	return Point(x=px, y=py, name=name_out)

# Some utility methods to check whether list of points form a regular polygon
class Polygon:
	@staticmethod
	def check_concyclic(l: list[Point]):
		# Check if a list of points is concyclic
		# We do this by calculating the equation of the circle A(x^2+y^2)+Bx+Cy+d=0 for the first 3 points then verifying the equation holds for the rest
		if len(l) < 3:
			raise ValueError("cannot form polygon from less than 3 points")
		x1, y1 = l[0].x, l[0].y
		s1 = x1**2 + y1**2
		x2, y2 = l[1].x, l[1].y
		s2 = x2**2 + y2**2
		x3, y3 = l[2].x, l[2].y
		s3 = x3**2 + y3**2

		A = det_33([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]])
		area_scale = max(
			abs(x1 * (y2 - y3)), abs(x2 * (y3 - y1)),
			abs(x3 * (y1 - y2)))
		if A == 0 or (area_scale != 0 and abs(A) <= EPS * area_scale):
			return False  # the points are collinear
		B = -det_33([[s1, y1, 1], [s2, y2, 1], [s3, y3, 1]])
		C = det_33([[s1, x1, 1], [s2, x2, 1], [s3, x3, 1]])
		D = -det_33([[s1, x1, y1], [s2, x2, y2], [s3, x3, y3]])
		for i in range(3, len(l)):
			x, y = l[i].x, l[i].y
			terms = (A * (x**2 + y**2), B * x, C * y, D)
			residual = sum(terms)
			scale = max(abs(term) for term in terms)
			if not (residual == 0 or (scale != 0 and abs(residual) <= EPS * scale)):
				return False
		return True

	@staticmethod
	def check_regular(l: list[Point]):
		# Check if a list of points forms a regular polygon. Returns 0 if not and the number of vertices if so
		# We do this by checking if the points are concyclic and equidistant
		if len(l) < 3:
			raise ValueError("cannot form polygon from less than 3 points")
		if any(not _finite(point.x, point.y) for point in l):
			return False
		# Names are not geometry. Reconstructing the same point under thousands of
		# aliases must not turn a triangle into an n-gon.
		coordinates = {(point.x, point.y) for point in l}
		if len(coordinates) != len(l):
			return False
		d = Point.distance_squared(l[0], l[-1])
		if d <= 0 or not gmpy2.is_finite(d):
			return False
		for i in range(0, len(l) - 1):
			if not _rel_close(Point.distance_squared(l[i], l[i + 1]), d):
				return False
		if not Polygon.check_concyclic(l):
			return False
		return True

# Custom exceptions for when line and circle do not meet or are tangent
class TangentError(Exception):
	pass


class DoesNotIntersectError(Exception):
	pass

def _meets_line_circle(
	L1: Line, C1: Circle, name1: str, name2: str
) -> tuple[Point, Point]:
	# We want to return (P1, P2) such that P1.x < P2.x or P1.x = P2.x and P1.y < P2.y
	# See https://mathworld.wolfram.com/Circle-LineIntersection.html
	A, B, C = tuple(L1)
	cx = C1.c.x
	cy = C1.c.y
	r2 = C1.r2
	# Break into two cases
	# Case 1: line is vertical
	if _close( B ):
		line_x = -C / A
		# Solve the system
		# x = line_x
		# (x - cx)^2 + (y - cy)^2 = r^2
		# => (y - cy)^2 = r^2 - (line_x - cx)^2
		disc = r2 - (line_x - cx) ** 2
		if disc < 0:
			raise DoesNotIntersectError(f"Line {L1} and Circle {C1} do not intersect!")
		if disc == 0:
			raise TangentError(
				f"Line {L1} is tangent to Circle {C1} - this is not supported"
			)
		y1, y2 = cy - gmpy2.sqrt(disc), cy + gmpy2.sqrt(disc)
		return (Point(x=line_x, y=y1, name=name1), Point(x=line_x, y=y2, name=name2))
	# Case 2: line is not vertical
	else:
		# Solve the system
		# Ax + By + C = 0
		# (x - cx)^2 + (y - cy)^2 = r^2

		# Substitute: y = ( -C - Ax ) / B
		# (x - cx)^2 + ( (-C - Ax)/B - cy)^2 - r^2 = 0
		# The above is a quadratic in x: u x^2 + v x + w = 0
		u = 1 + (A / B) ** 2
		v = -2 * cx + 2 * A * cy / B + 2 * A * C / B**2
		w = cx**2 + cy**2 - r2 + 2 * C * cy / B + (C / B) ** 2
		disc = v**2 - 4 * u * w
		if disc < 0:
			raise DoesNotIntersectError(f"Line {L1} and Circle {C1} do not intersect!")
		if disc == 0:
			raise TangentError(
				f"Line {L1} is tangent to Circle {C1} - this is not supported"
			)
		x1, x2 = (-v - gmpy2.sqrt(disc)) / (2 * u), (-v + gmpy2.sqrt(disc)) / (2 * u)
		# assert x1 < x2
		y1 = (-C - A * x1) / B
		y2 = (-C - A * x2) / B
		return (Point(x=x1, y=y1, name=name1), Point(x=x2, y=y2, name=name2))

def _meets_circle_circle(
	C1: Circle, C2: Circle, name1: str, name2: str
) -> tuple[Point, Point]:
	# See https://mathworld.wolfram.com/Circle-CircleIntersection.html
	# We want to return (P1, P2) such that P1.x < P2.x or P1.x = P2.x and P1.y < P2.y
	px = C1.c.x
	py = C1.c.y
	qx = C2.c.x
	qy = C2.c.y
	r2 = C1.r2
	R2 = C2.r2
	# We want to solve the system
	# (x - px)^2 + (y - py)^2 = r^2  (I)
	# (x - qx)^2 + (y - qy)^2 = R^2 (II)
	# (II) - (I) => A*x + B*y + C = 0
	A = 2 * (px - qx)
	B = 2 * (py - qy)
	C = qx**2 + qy**2 - (px**2 + py**2) + r2 - R2
	if _close( A ) and _close( B ):
		raise DoesNotIntersectError(f"circles {C1} and {C2} are concentric")
	# Construct the radical axis through the two circles
	radical = Line.from_coeffs(A, B, C, "radical")
	try:
		return _meets_line_circle(radical, C1, name1, name2)
	except TangentError:
		raise TangentError(
			f"Circle {C1} and {C2} meet at only one point - this is not supported"
		)
	except DoesNotIntersectError:
		raise DoesNotIntersectError(f"Circle {C1} and {C2} do not intersect")

def is_ok_circle(geo_str: str) -> bool:
	"""Return True if the .geo file string contains only circles and no lines.

	Allowed commands: circle, meets_circle_circle, n_gon.
	Disallowed commands: line, meets_line_line, meets_line_circle.
	Comments (lines starting with '%') and blank lines are ignored.
	"""
	LINE_COMMANDS = {"line", "meets_line_line", "meets_line_circle"}
	for raw_line in geo_str.splitlines():
		stripped = raw_line.strip()
		if not stripped or stripped.startswith("%"):
			continue
		command = stripped.split()[0]
		if command in LINE_COMMANDS:
			return False
	return True


def is_ok_line(geo_str: str) -> bool:
	"""Return True if the .geo file starts with one circle then only uses lines.

	The first non-comment command must be 'circle'.
	All subsequent commands must be line-only: line, meets_line_line, n_gon.
	Disallowed after the first command: circle, meets_circle_circle, meets_line_circle.
	Comments (lines starting with '%') and blank lines are ignored.
	"""
	CIRCLE_COMMANDS = {"circle", "meets_circle_circle", "meets_line_circle"}
	found_first = False
	for raw_line in geo_str.splitlines():
		stripped = raw_line.strip()
		if not stripped or stripped.startswith("%"):
			continue
		command = stripped.split()[0]
		if not found_first:
			if command != "circle":
				return False
			found_first = True
		else:
			if command in CIRCLE_COMMANDS:
				return False
	return found_first


class Construction:
	def __init__(self, PREC = PREC, expected_n: Optional[int] = None):
		gmpy2.get_context().precision = PREC # Set gmpy precision
		# Number of vertices the n_gon command must produce. None disables the check.
		self.expected_n = expected_n
		O = Point(x=gmpy2.mpfr(0),  y=gmpy2.mpfr(0), name="O")
		P = Point(x=gmpy2.mpfr(1), y=gmpy2.mpfr(0), name="P")
		self.points = {"O": O, "P": P}
		self.lines = dict()
		self.circles = dict()

	@staticmethod
	def _require_distinct_outputs(*names: str) -> None:
		if len(set(names)) != len(names):
			raise ValueError("output names must be distinct")

	@staticmethod
	def _require_unused(name: str, existing: dict, kind: str) -> None:
		# Redefining a name would silently overwrite the dict entry, shrinking
		# len(points)/len(lines)/len(circles) below the number of commands that
		# actually ran -- which is exactly what score is computed from.
		if name in existing:
			raise ValueError(f"{kind} '{name}' is already defined")

	@staticmethod
	def _require_count(command: str, args: list[str], expected: int) -> None:
		if len(args) != expected:
			raise ValueError(f"invalid number of arguments for {command} command")

	def run_command(self, command: str, args: list[str]) -> Optional[bool]:
		match command:
			case "line":
				# Create line from two points
				# ex: line P Q L % creates line L between points P and Q
				self._require_count(command, args, 3)
				P1, P2, L_name = args
				if P1 not in self.points or P2 not in self.points:
					raise ValueError("line references an unknown point")
				self._require_unused(L_name, self.lines, "line")
				L = Line(p1=self.points[P1], p2=self.points[P2], name=L_name)
				self.lines[L_name] = L
				return None
			case "circle":
				# Create circle from center and point on circle
				# ex: circle A B C % creates circle C centered at A with point B on the circle
				self._require_count(command, args, 3)
				center, pt_on_circle, C_name = args
				if center not in self.points or pt_on_circle not in self.points:
					raise ValueError("circle references an unknown point")
				self._require_unused(C_name, self.circles, "circle")
				C = Circle(
					center=self.points[center],
					pt_on_circle=self.points[pt_on_circle],
					name=C_name,
				)
				self.circles[C_name] = C
				return None
			case "meets_line_line":
				# Create point at the intersection of two lines
				# ex: meets_line_line L1 L2 P % creates point P at the intersection of the lines L1 and L2
				self._require_count(command, args, 3)
				L1, L2, P_name = args
				if L1 not in self.lines or L2 not in self.lines:
					raise ValueError("meets_line_line references an unknown line")
				self._require_unused(P_name, self.points, "point")
				try:
					P = _meets_line_line(self.lines[L1], self.lines[L2], P_name)
					self.points[P_name] = P
					return None
				except Exception as e:
					raise ValueError(f"Error in meets_line_line: {e}")
			case "meets_line_circle":
				# Create two points at the intersection of a line and a circle
				# ex: meets_line_circle L1 C1 P Q % creates points P and Q at the intersection of line L1 and circle C1
				self._require_count(command, args, 4)
				L, C, P_name, Q_name = args
				if L not in self.lines or C not in self.circles:
					raise ValueError("meets_line_circle references an unknown object")
				self._require_distinct_outputs(P_name, Q_name)
				self._require_unused(P_name, self.points, "point")
				self._require_unused(Q_name, self.points, "point")
				try:
					P, Q = _meets_line_circle(
						self.lines[L], self.circles[C], P_name, Q_name
					)
					self.points[P_name] = P
					self.points[Q_name] = Q
					return None
				except Exception as e:
					raise ValueError(f"Error in meets_line_circle: {e}")
			case "meets_circle_circle":
				# Creates two points at the intersection of two circles
				# ex: meets_circle_circle C1 C2 P Q % creates points P and Q at the intersection of circles C1 and C2
				self._require_count(command, args, 4)
				C1, C2, P_name, Q_name = args
				if C1 not in self.circles or C2 not in self.circles:
					raise ValueError("meets_circle_circle references an unknown circle")
				self._require_distinct_outputs(P_name, Q_name)
				self._require_unused(P_name, self.points, "point")
				self._require_unused(Q_name, self.points, "point")
				try:
					P, Q = _meets_circle_circle(
						self.circles[C1], self.circles[C2], P_name, Q_name
					)
					self.points[P_name] = P
					self.points[Q_name] = Q
					return None
				except Exception as e:
					raise ValueError(f"Error in meets_circle_circle: {e}")
			case "n_gon":
				if len(args) < 3:
					raise ValueError("invalid number of arguments for n_gon")
				if args[0] != "P":
					raise ValueError("first point must be P")
				# The challenge fixes how many vertices the polygon must have. Without
				# this the regularity check alone is happy with any n >= 3, so a
				# six-line equilateral triangle satisfied the 65537-gon challenge.
				if self.expected_n is not None and len(args) != self.expected_n:
					raise ValueError(
						f"this challenge requires a {self.expected_n}-gon, "
						f"but n_gon was given {len(args)} vertices"
					)
				if len(set(args)) != len(args):
					raise ValueError("n_gon vertices must be distinct points")
				for pt_name in args:
					if pt_name not in self.points:
						raise ValueError(f"{pt_name} not a valid point name")
				return Polygon.check_regular([self.points[pt_name] for pt_name in args])
			case _:
				raise ValueError("unknown command!")

	def read_str(self, lines: list[str], progress_callback: Optional[Callable[[int, int], None]] = None) -> ParseResult:
		total = len(lines)
		for i, line in enumerate(lines):
			line = line.strip()
			if not line or line[0] == "%":
				if progress_callback:
					progress_callback(i + 1, total)
				continue
			tokens = line.split()
			if len(tokens) <= 1:
				raise ValueError(f"invalid line length on line {i + 1}")
			command, args = tokens[0], tokens[1:]
			out = self.run_command(command, args)
			if progress_callback:
				progress_callback(i + 1, total)
			if out is not None:
				for trailing in lines[i + 1:]:
					trailing = trailing.strip()
					if trailing and not trailing.startswith("%"):
						raise ValueError("n_gon must be the final command")
				if out is False:
					return ParseResult(INVALID, detail="the given points do not form a regular polygon")
				# score = |points| + |lines| + |circles|
				score = len(self.points) + len(self.lines) + len(self.circles)
				return ParseResult(VALID, score=score)
		return ParseResult(INCOMPLETE, detail="construction ended without an n_gon command")
