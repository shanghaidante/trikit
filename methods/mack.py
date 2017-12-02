from .chain_ladder import BaseMethod



class Mack(BaseMethod):
    """
    Mack method.
    """
    def __init__(self, triangle, selection='all-weighted', tail_factor=1.0):
        BaseMethod.__init__(self, triangle, selection, tail_factor)
        pass





