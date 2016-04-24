"""Base solver for automating OTW games.
"""
from common import solver


class OtwSolver(solver.Solver):
  def __init__(self, game_name):
    self._game_name = game_name

    super(OtwSolver, self).__init__(
      hostname='%s.labs.overthewire.org' % game_name,
      initial_password='%s0' % game_name,
      first_level=0,
      check_host_key=False)

  def get_username(self, level_num):
    return '%s%d' % (self._game_name, level_num)

  def get_password_path(self, level_num):
    return '/etc/%s_pass/%s%d' % (
        self._game_name, self._game_name, level_num)
