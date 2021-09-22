from random import randint

from AMLib.Core.Scorers.SimpleScorers import DistanceScorer
from AMLib.Core.VM import VM, VMParams, VMSample, VMDataset


class Dummy:
  pass


class TestDistanceScorer:
  def test_dummy(self):
    # Prepare
    smpl = Dummy()
    smpl.output = [1., 2., 3.]
    d = Dummy()
    d.sample = smpl
    d.heap = [2., 3., 4]

    # Act
    result = -1. * sum([abs(smpl.output[x] - d.heap[x]) for x in range(len(smpl.output))])

    # Assert
    assert result == DistanceScorer.calc(d)

  def test_VMSample_and_one_step(self):
    # Prepare
    vm = VM()
    smpl = VMSample(input=[1., 2., 3.], output=[2., 3., 4])
    vm.step(smpl)

    # Act
    result = -1. * sum([abs(smpl.output[x] - vm.heap[x]) for x in range(len(smpl.output))])

    # Assert
    assert result == DistanceScorer.calc(vm)

  def test_VMDataset_and_full_calc(self):
    # Prepare
    vm = VM()
    smpl = VMSample(input=[1., 2., 3.], output=[2., 3., 4])
    ds = VMDataset([smpl])
    vm.samples = ds
    vm.calc()

    # Act
    result = -1. * sum([abs(vm.sample.output[x] - vm.heap[x]) for x in range(len(vm.sample.output))])

    # Assert
    assert result == DistanceScorer.calc(vm)
