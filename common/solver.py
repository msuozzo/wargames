"""Base solver for automating wargames.
"""
from common import pexpect_utils


class Solver(object):
  def __init__(self, hostname, initial_password, first_level=1,
      check_host_key=True):
    self.hostname = hostname
    self._initial_password = initial_password
    self._first_level = first_level
    self._check_host_key = check_host_key

  def get_password_path(self, level_num):
    raise NotImplementedError

  def get_username(self, level_num):
    raise NotImplementedError

  def get_level_solution(self, level_num):
    raise NotImplementedError

  def run_level(self, level_num, password):
    return pexpect_utils.ssh_session(self.get_username(level_num),
        self.hostname, password, self._check_host_key)

  def solve_until(self, max_level):
    if max_level < self._first_level:
      raise Exception
    passwords = [self._initial_password]
    for level in xrange(self._first_level, max_level + 1):
      with self.run_level(level, passwords[-1]) as proc:
        password = self.get_level_solution(level)(proc)
        if password is None:
          password_path = self.get_password_path(level + 1)
          password = proc.get_password_from_shell(password_path)
        passwords.append(password)
    return dict(zip(xrange(self._first_level, max_level + 1),
      passwords))
