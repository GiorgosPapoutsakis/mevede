from vrp_model import Model
from initial_solution import *

m = Model()
m.build_model()
s = Solver(m)
s.solve()