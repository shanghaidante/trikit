from .chain_ladder import BaseMethod



class Bootstrap(BaseMethod):
    """
    Bootstrap method.
    """
    def __init__(self, triangle, selection='all-weighted', tail_factor=1.0):
        BaseMethod.__init__(self, triangle, selection, tail_factor)
        pass





