from AMLib.Core.Scorers import AbstractVMScorer
from AMLib.Core.VM import VM


class DistanceScorer(AbstractVMScorer):
  def __init__(self):
    self.result = 0.

  def calc(self, vm: VM, end) -> None:
    if not end:
      for idx in range(len(vm.sample.expected)):
        self.result += abs(vm.sample.expected[idx] - vm.heap[idx])

  def get_name(self) -> str:
    return "Distance"

  def get_direction(self) -> bool:
    return False

  def get_result(self) -> float:
    return self.result

  def reset(self):
    self.result = 0.
