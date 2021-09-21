from random import randint

from AMLib.Core.Scorers.SimpleScorers import DistanceScorer
from AMLib.Core.VM import VM, VMParams


class TestDistanceScorer:
  def test_naive(self):
    n_results = 2

    vm = VM(VMParams())
    vm.params.output_size = n_results
    vm.outputs = [randint(-10000, 10000) for _ in range(n_results)]
    vm.samples.append([[None, None], [randint(-10000, 10000) for _ in range(n_results)]])
    assert -1. * sum([abs(vm.samples[0][1][x] - vm.outputs[x]) for x in range(n_results)]) == DistanceScorer.calc(vm)
