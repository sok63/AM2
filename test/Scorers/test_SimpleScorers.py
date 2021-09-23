from AMLib.Core.Data import VMSample, VMDataset
from AMLib.Core.Scorers.SimpleScorers import DistanceScorer
from AMLib.Core.VM import VM


class TestDistanceScorer:
  def test_VMDataset_and_full_calc(self):
    # Prepare
    vm = VM()
    smpl = VMSample(initial=[1., 2., 3.], expected=[2., 3., 4])
    ds = VMDataset([smpl])
    vm.samples = ds
    vm.scorers.append(DistanceScorer())

    vm.calc()

    # Act
    result = sum([abs(vm.sample.expected[x] - vm.heap[x]) for x in range(len(vm.sample.expected))])

    # Assert
    assert result == vm.scorers[0].get_result()
