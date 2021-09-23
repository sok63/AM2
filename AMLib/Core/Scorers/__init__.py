class AbstractVMScorer:
  """
  Prototype for VM scorer.
  """

  def calc(self, vm, end: bool) -> None:
    """
    Called at end of every sample calculation and at the end of all samples calculations
    """
    pass

  def get_name(self) -> str:
    """
    Return name of scorer.
    """
    raise TypeError()

  def get_direction(self) -> bool:
    """
    Return direction of optimization, where:
    False - negative is better
    True - positive is better
    """
    raise TypeError()

  def get_result(self) -> float:
    """
    Return result score value.
    """
    pass

  def reset(self):
    """
    Reset internal state.
    """
    pass
