from mutator import GenericMutator
from MutationError import MutationError


class UnusualFiletypeMutator(GenericMutator):
  def __init__(self, filetype='S_IFREG', name=None, file_descriptor=None):
    if name is not None and file_descriptor is not None:
      raise MutationError('Cannot specify both a name and a file_descriptor')
    self.filetype = filetype
    self.name = name
    self.file_descriptor = file_descriptor


  def mutate_syscalls(self, syscalls):
    index = self._find_index(syscalls)
    # TODO: posix-omni-parser does not parse stat-like calls correctly.
    # This means we cannot be sure the st_mode member will always be in the same place.
    # As a result, we must iterate through all of the arguments to find it.
    for i in syscalls[index].args:
      if 'st_mode' in i:
        # TODO: we only support replacing S_IFREG right now
        syscalls[index].args[i].replace('S_IFREG', self.filetype)


  def _find_index(self, syscalls):
    for k, v in enumerate(syscalls):
      # fstat takes a file descriptor
      if v.name.startswith('fstat'):
        if self.file_descriptor:
          if self.file_descriptor != v.args[0].value:
            continue
        return k
      # stat and lstat take a name rather than a file descriptor
      if v.name.startswith('stat') or v.name.startswith('lstat'):
        if self.name:
          if self.name != v.args[0].value:
            continue
        return k

  def identify_lines(self, syscalls, lines):
    for k, v in enumerate(syscalls):
      # fstat takes a file descriptor
      if v.name.startswith('fstat'):
        if self.file_descriptor:
          if self.file_descriptor != v.args[0].value:
            continue
        lines.append(k)
      # stat and lstat take a name rather than a file descriptor
      if v.name.startswith('stat') or v.name.startswith('lstat'):
        if self.name:
          if self.name != v.args[0].value:
            continue
        lines.append(k)

  def error_message(self, args):
    print('{} may behave unexpectedly when running in Linux environments
    where {} is not a regular file.'.format(args[0]['test_name'],
        args[0]['filename'])

  def explain_message(self, args):
    print('Message: "{} may encounter problems in Linux environments where
    {} is not a regular file."

    CrashSimulator has identified that {} does not recognize situations
    where it has been simulated
    that {} is not a regular file.  This is problematic in Linux
    environments where {}
    is supplied by (or may be manipulated by) {}\'s user.  {} should be
    modified to use a call from the
    "stat" family to gather information about {} before processing
    it.  Failure to do so could
    result in {} crashing, hanging, or exhausing system
    resources.'.format(args[0]['test_name'], args[0]['filename'],
        args[0]['test_name'], args[0]['filename'], args[0]['filename'],
        args[0]['test_name'], args[0]['test_name'], args[0]['filename'],
        args[0]['test_name']) 
    print('This report was made because CrashSimulator identified the following
    issues:')
    for i in range(len(args)):
      print('(At event {}): {} doesn\'t recognize when {} is
      a {}'.format(args[i]['event'], args[i]['test_name'],
          args[i]['file_type'])
    print('These issues were found by: "Unusual Filetype Mutator"')
