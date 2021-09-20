from typing import List


class VMScorer:
  """
  Calculate score for VM
  """
  @staticmethod
  def calc(vm) -> List[float]:
    pass


class VMParams:
  """
  Contains core VM settings.
  """
  def __init__(self, tickScorers: List[VMScorer], totalScorers: List[VMScorer]):
    self.register_count = 4
    self.heap_size = 10
    self.stackLimit = 10
    self.tickLimit = 1000
    self.input_size = 0
    self.output_size = 0
    self.tick_scorers = tickScorers
    self.total_scorers = totalScorers
    self.exception_handlers = {}


class VM:
  """
  Virtual machine for commands execution.
  Used to 'play' selected gene.
  """

  def __init__(self, params: VMParams, gene: List = None):
    self.params = params
    self.gene = gene
    self.samples = []

    self.registers = None
    self.heap = None
    self.stack = None
    self.command_counter = None
    self.command_pointer = None
    self.registers_usage = None
    self.inputs = None
    self.outputs = None

    self.reset()

  def setSamples(self, samples):
    """ Override samples data in VM """
    self.samples = samples

  def setNewGene(self, gene):
    """ Override gene data in VM """
    self.gene = gene

  def resetScores(self):
    """ Reset all scores for VM """
    self.scores = {}

  def reset(self):
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

  def calcStep(self, sample) -> List:
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

    # Post calc
    for scorer in self.params.tick_scorers:
      scorer.calc(self)

    # Return result
    return self.outputs

  def calcAll(self):
    """ Calculate all samples setted in VM """
    for sample in self.samples:
      self.calcStep(sample)
    for scorer in self.params.total_scorers:
      self.scores[scorer.__str__] = scorer.calc(self)
