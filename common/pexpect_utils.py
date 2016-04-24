import contextlib

import pexpect


class BetterProc(object):
  _PROMPT_REGEX = r'\$ '

  def __init__(self, proc):
    self._proc = proc

  def expect_prompt(self):
    self._proc.expect(self._PROMPT_REGEX)

  def get_password_from_shell(self, password_path):
    # Use the shell prompt to get the next password
    self.expect_prompt()
    self._proc.sendline('cat ' + password_path)
    self.expect_prompt()
    password = self._proc.before.splitlines()[1]

    # Exit the shell
    self._proc.sendeof()

    return password

  def __hasattribute__(self, attr):
    return super(BetterProc, self).__hasattribute__(attr)

  def __getattribute__(self, attr):
    # Try to find attribute on the underlying proc first, then try
    # this object
    proc = super(BetterProc, self).__getattribute__('_proc')
    if hasattr(proc, attr):
      return getattr(proc, attr)
    else:
      return super(BetterProc, self).__getattribute__(attr)


@contextlib.contextmanager
def ssh_session(username, hostname, password=None, check_host_key=True):
  host_key_str = '-o StrictHostKeyChecking=' + (
      'yes' if check_host_key else 'no')
  cmd = 'ssh %s %s@%s' % (host_key_str, username, hostname)

  proc = BetterProc(pexpect.spawn(cmd))
  # Only expect a password prompt if a password was provided
  if password is not None:
    proc.expect('password: ')
    proc.sendline(password)
  proc.expect_prompt()
  yield proc

  proc.sendeof()
  proc.terminate()
