from smash_the_stack.io import solver as io_solver
from otw.leviathan import solver as leviathan_solver
from otw.narnia import solver as narnia_solver


def solve_game_until(game_name, level):
  if game_name == 'io':
    solver = io_solver.IoSolver()
  elif game_name == 'leviathan':
    solver = leviathan_solver.LeviathanSolver()
  elif game_name == 'narnia':
    solver = narnia_solver.NarniaSolver()
  else:
    raise Exception('Unknown game: %s' % game_name)

  for level, password in sorted(solver.solve_until(level).items()):
    print 'Level %d: "%s"' % (level, password)


if __name__ == '__main__':
  import sys

  game_name, level_str = sys.argv[1:3]
  try:
    level = int(level_str)
  except ValueError:
    print 'Unknown level number:', level_str
    print 'Usage:  ./solve.py <game_name> <level_num>'
  else:
    solve_game_until(game_name, level)
