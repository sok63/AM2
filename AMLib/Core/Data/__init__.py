from typing import List, Dict, Any


class VMSample:
  def __init__(self, initial: List[float] = None, expected: List[float] = None, additional: Dict[str, Any] = None):
    self.initial = initial
    self.expected = expected
    self.additional = additional


class VMDataset(List):
  """
  Describe compatible dataset format for VMs
  """

  def __init__(self, samples: List[VMSample]):
    super().__init__(samples)
