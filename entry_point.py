from vrp_model import *
from initial_solution import *
from improve_solution import *

m = Model()
m.build_model()
s = Solver(m)
initial_solution = s.solve()
imp = Improver(initial_solution,m)
imp.improve()