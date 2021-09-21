from AMLib.Core.VM import VMScorer, VM


class DistanceScorer(VMScorer):
  @staticmethod
  def calc(vm: VM) -> float:
    result = 0.
    for idx in range(vm.params.output_size):
      result -= abs(vm.outputs[idx] - vm.samples[vm.sample_idx][1][idx])
    return result
