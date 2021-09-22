from AMLib.Core.VM import VMScorer, VM


class DistanceScorer(VMScorer):
  @staticmethod
  def calc(vm: VM) -> float:
    result = 0.
    for idx in range(len(vm.sample.output)):
      result -= abs(vm.heap[idx] - vm.sample.output[idx])
    return result
