# 
#
# (C) Copyright IBM 2024.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Defines the methods that an evaluator should have."""

from abc import ABC, abstractmethod

from typing import Dict, Optional


class BaseEvaluator(ABC):
    """Defines the interface for the evaluators.

    This makes the evaluators pluggable in parameter trainers. This base class
    is designed to be as light-weight as possible to (i) not constrain development
    and (ii) base classes are notoriously hard to remove from code.
    """

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> float:
        """Evaluate the energy for the given arguments.

        Returns:
            This function returns the energy as a real value.
        """

    def get_results_from_last_iteration(self) -> Dict:
        """Function to access results of the simulation at the last iteration

        This function (which should be overriden by derived class) should be used
        to retrieve results from the last call of the evaluator that are different
        from the energy.
        For instance, if there is an approximate simulator, it would be useful to
        know the accuracy of the energy estimate at the last simulation step.
        This function enables to access these data.

        By default, an empty dictionary is returned (if the method is not defined
        in the derived class)

        Returns:
            Dict: dictionary with results from the last optimizer iteration
        """
        return {}

    def to_config(self) -> dict:
        """Json serializable config to keep track of how results are generated."""
        return {"name": self.__class__.__name__}

    @classmethod
    def parse_init_kwargs(cls, init_kwargs: Optional[str] = None) -> dict:
        """A hook that sub-classes can implement to parse initialization kwargs."""
        return dict()
