from mutator import GenericMutator


class FutureTimeMutator(GenericMutator):
  def __init__(self, seconds=100):
      self.seconds = seconds


  def mutate_syscalls(self, syscalls):
    for k, v in enumerate(syscalls):
      if v.name == 'time':
        syscalls[k].ret = (syscalls[k].ret[0] + self.seconds, '')


  def identify_lines(self, syscalls, lines):
    for k, v in enumerate(syscalls):
      if v.name == 'time':
        lines.append(k)

  def error_message(self, args):
    print('{} did not recognize that the system clock moved
    forward'.format(args[0]['test_name']))

  def explain_message(self, args):
    print('This report was made because CrashSimulator identified the following
    issues:')
    for i in range(len(args)):
      print('(At event {}): {} did not recognize that the system clock moved
      forward'.format(args[i]['event'], args[i]['test_name']))
