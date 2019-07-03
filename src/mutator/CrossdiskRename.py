from mutator import GenericMutator


class CrossdiskRenameMutator(GenericMutator):
  def __init__(self, name=None):
      self.name = name


  def mutate_syscalls(self, syscalls):
    for k, v in enumerate(syscalls):
      if v.name == 'rename':
        if self.name:
          if v.args[0].value != self.name:
            continue
          syscalls[k].ret = (-1, 'EXDEV')


  def identify_lines(self, syscalls, lines):
    for k, v in enumerate(syscalls):
      if v.name == 'rename':
        if self.name:
          if v.args[0].value != self.name:
            continue
        lines.append(k)

  def error_message(self, args):
    print('{} does not prevent {} from being modified while
    copying it.'.format(args[0]['test_name'], args[0]['filename'])

  def explain_message(self, args):
    print('Message: "{} does not prevent {} from being
    modified while copying it."

    CrashSimulator has identified that {} does not prevent {}
    from being modified
    when copying a file from one disk to another.  When running under Linux,
    {} should store the
    inode number of a file before it begins copying and ensure this inode
    number does not change while
    copying the file.  Failure to do so means {} could be
    accidentally or maliciously
    replaced by another user or application resulting in unintended application
    behavior or security compromise.'.format(args[0]['test_name'],
        args[0]['filename'], args[0]['test_name'],
        args[0]['filename'], args[0]['test_name'],
        args[0]['filename']))
    print('This report was made because CrashSimulator identified the following
    issues:')
    for i in range(len(args)):
      print('(At event {}): {} does not check inode numbers to confirm that
      {} wasn\'t changed during copy'.format(args[i]['event'],
          args[i]['test_name'], args[i]['filename'])
    print('These issues were found by: "Crossdisk File Move"')
