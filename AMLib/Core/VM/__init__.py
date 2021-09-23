from typing import List


class VM:
  """
  Virtual machine for commands execution.
  Used to 'play' selected gene.
  """
  __slots__ = [
    'gene', 'samples', 'scorers', 'exception_handlers',  # External things
    'stack', 'registers', 'heap',  # VM Hardware
    'register_count', 'heap_size',  # VM Hardware params
    'stackLimit', 'tickLimit',  # Limits
    'pointer', 'counter', 'registers_usage',  # Counters
    'sample', 'sample_idx',  # Actual sample
    'step_complete'  # Flags

  ]

  def __init__(self):
    self.gene = []
    self.scorers = []
    self.exception_handlers = {}
    self.register_count = 4
    self.heap_size = 10
    self.stackLimit = 10
    self.tickLimit = 1000

    self.samples = []

    self.registers = None
    self.heap = None
    self.stack = None
    self.counter = None
    self.pointer = None
    self.registers_usage = None
    self.sample = None
    self.step_complete = False
    self.sample_idx = None

  def set_samples(self, samples) -> None:
    """ Override samples data in VM """
    self.samples = samples

  def set_gene(self, gene) -> None:
    """ Override gene data in VM """
    self.gene = gene

  def reset_partial(self) -> None:
    """ Reset state for next sample in dataset calculation """
    self.registers = [0. for _ in range(self.register_count)]
    self.registers_usage = [0. for _ in range(self.register_count)]
    self.heap = [0. for _ in range(max(self.heap_size, len(self.sample.expected)))]
    self.stack = []
    self.counter = 0
    self.pointer = 0
    self.step_complete = False
    self.sample_idx = 0

  def reset_full(self) -> None:
    """ Reset state for next dataset calculation """
    self.sample = self.samples[0]
    self.reset_partial()
    for idx in range(len(self.scorers)):
      self.scorers[idx].reset()

  def step(self, sample) -> bool:
    """
     Calculate one sample.
    """
    # Prepare
    self.sample = sample
    self.reset_partial()

    # Calc
    try:
      while True:
        # Early exit conditions (with zero len gene possibility)
        if (self.pointer >= len(self.gene)) or self.pointer < 0:
          break

        if self.counter >= self.tickLimit:
          break

        # Calculate gene
        self.gene[self.pointer].calc(self)

        # Update counters
        self.counter += 1
        self.pointer += 1

    except Exception as exc:
      if not exc.args[0] in self.exception_handlers:
        raise exc
      else:
        self.exception_handlers[exc.args[0]](self)

    else:
      self.step_complete = True

    # Post calc
    for scorer in self.scorers:
      scorer.calc(self, end=False)

    # Return result
    return self.step_complete

  def calc(self) -> List[bool]:
    """ Calculate all dataset in VM """
    self.reset_full()

    result = []
    for idx, sample in enumerate(self.samples):
      self.sample_idx = idx
      result.append(self.step(sample))

    for scorer in self.scorers:
      scorer.calc(self, end=True)

    return result
