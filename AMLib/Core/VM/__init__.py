from typing import List, Dict, Any


class VMSample(List):
  def __init__(self, input: List[float] = None, output: List[float] = None, other: Dict[str, Any] = None):
    super().__init__([input, output, other])

  def __getattribute__(self, item):
    if item == "input":
      return self[0]
    elif item == "output":
      return self[1]
    elif item == "other":
      return self[2]


class VMDataset(List):
  """
  Describe compatible dataset format for VMs
  """

  def __init__(self, samples: List[VMSample]):
    super().__init__(samples)


class VMScorer:
  """
  Calculate score for VM.
  """
  @staticmethod
  def calc(vm) -> float:
    pass

  @staticmethod
  def get_name() -> str:
    """
    Return name of scorer.
    """
    raise TypeError()

  @staticmethod
  def get_direction() -> bool:
    """
    Return direction of optimization, where:
    False - negative is better
    True - positive is better
    """
    raise TypeError()


class VMParams:
  """
  Contains constants VM settings.
  """
  def __init__(self, scorers: List[VMScorer]):
    self.register_count = 4
    self.heap_size = 10
    self.stackLimit = 10
    self.tickLimit = 1000
    self.scorers = {"step": [], "result": []}
    if scorers is not None:
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
    'registers_usage', 'sample', 'scores',
    'step_complete', 'sample_idx', 'input_size'
  ]

  def __init__(self, params: VMParams = VMParams(), gene: List = None):
    self.params = params
    self.gene = []
    if gene is not None:
      self.gene = gene

    self.samples = []

    self.registers = None
    self.heap = None
    self.stack = None
    self.command_counter = None
    self.command_pointer = None
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

  def reset_scores(self) -> None:
    """ Reset all scores for VM """
    self.scores = {}

  def reset(self) -> None:
    """ Reset state for next sample calculation """
    self.registers = [0. for _ in range(self.params.register_count)]
    self.registers_usage = [0. for _ in range(self.params.register_count)]
    self.heap = [0. for _ in range(max(self.params.heap_size, len(self.sample.output)))]
    self.stack = []
    self.command_counter = 0
    self.command_pointer = 0
    self.step_complete = False
    self.sample_idx = 0

  def step(self, sample) -> bool:
    """
     Calculate one sample.
    """
    # Prepare
    self.sample = sample
    self.reset()

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
    for scorer in self.params.scorers["step"]:
      self.scores[scorer.__str__] = scorer.calc(self)

    # Return result
    return self.step_complete

  def calc(self) -> List[bool]:
    """ Calculate all samples in VM """
    result = []
    for idx, sample in enumerate(self.samples):
      self.sample_idx = idx
      result.append(self.step(sample))

    for scorer in self.params.scorers["result"]:
      self.scores[scorer.__str__] = scorer.calc(self)

    return result
