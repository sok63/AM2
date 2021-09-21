from typing import List


class VMScorer:
  """
  Calculate score for VM.
  """
  @staticmethod
  def calc(vm, sub_result: bool) -> List[float]:
    pass


class VMParams:
  """
  Contains core VM settings.
  """
  def __init__(self, scorers: List[VMScorer]):
    self.register_count = 4
    self.heap_size = 10
    self.stackLimit = 10
    self.tickLimit = 1000
    self.input_size = 0
    self.output_size = 0
    self.scorers = scorers
    self.exception_handlers = {}


class VM:
  """
  Virtual machine for commands execution.
  Used to 'play' selected gene.
  """
  __slots__ = [
    'params', 'gene', 'samples', 'registers', 'heap',
    'stack', 'command_counter', 'command_pointer',
    'registers_usage', 'inputs', 'outputs', 'scores',
    'step_complete'
  ]

  def __init__(self, params: VMParams, gene: List = None):
    self.params = params
    self.gene = gene
    self.samples = []
    self.scores = {}

    self.registers = None
    self.heap = None
    self.stack = None
    self.command_counter = None
    self.command_pointer = None
    self.registers_usage = None
    self.inputs = None
    self.outputs = None
    self.step_complete = False

    self.reset()

  def set_samples(self, samples) -> None:
    """ Override samples data in VM """
    self.samples = samples

  def set_gene(self, gene) -> None:
    """ Override gene data in VM """
    self.gene = gene

  def reset_scores(self) -> None:
    """ Reset all scores for VM """
    self.scores = {}

  def reset(self) -> None:
    """ Reset state for next sample calculation """
    self.registers = [0. for _ in range(self.params.register_count)]
    self.registers_usage = [0. for _ in range(self.params.register_count)]
    self.outputs = [None for _ in range(self.params.output_size)]
    self.heap = [0. for _ in range(self.params.heap_size)]
    self.stack = []
    self.command_counter = 0
    self.command_pointer = 0
    self.inputs = []
    self.outputs = []
    self.step_complete = False

  def step(self, sample) -> bool:
    """
     Calculate one sample.
     Do reset() automatically before calculation process
    """
    # Prepare
    self.reset()
    self.inputs = sample

    # Calc
    try:
      while True:
        # Early exit conditions (with zero len gene possibility)
        if (self.command_pointer >= len(self.gene)) or self.command_pointer < 0:
          break

        if self.command_counter >= self.params.tickLimit:
          break

        # Calculate gene
        self.gene[self.command_pointer].calc(self)

        # Update counters
        self.command_counter += 1
        self.command_pointer += 1

    except Exception as exc:
      if not exc.args[0] in self.params.exception_handlers:
        raise exc
      else:
        self.params.exception_handlers[exc.args[0]](self)

    else:
      self.step_complete = True

    # Post calc
    for scorer in self.params.scorers:
      scorer.calc(self, sub_result=True)

    # Return result
    return self.step_complete

  def calc(self) -> List[bool]:
    """ Calculate all samples in VM """
    result = []
    for sample in self.samples:
      result.append(self.step(sample))

    for scorer in self.params.scorers:
      self.scores[scorer.__str__] = scorer.calc(self, sub_result=False)

    return result
