#
#
# (C) Copyright IBM 2024.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Statevector-based QAOA evaluator tests."""

from unittest import TestCase

from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

from qaoa_training_pipeline.evaluation.statevector_evaluator import StatevectorEvaluator
from qaoa_training_pipeline.training.scipy_trainer import ScipyTrainer


class TestStatevectorEvaluator(TestCase):
    """Test that the state vector evaluator works."""

    def setUp(self):
        """Setup the variables."""
        self.cost_op = SparsePauliOp.from_list([("II", 1.0), ("IZ", 1.0), ("ZZ", 1.0)])
        self.evaluator = StatevectorEvaluator()

    def qiskit_circuit_simulation(self, cost_op, params):
        """This is the baseline simulation based on Qiskit."""

        ansatz = QAOAAnsatz(cost_op, reps=len(params) // 2)
        estimator = StatevectorEstimator()
        ansatz.assign_parameters(params, inplace=True)
        result = estimator.run([(ansatz, cost_op, [])]).result()
        return float(result[0].data.evs)

    def test_evaluate(self):
        """Basic test of the evaluator."""
        self.assertAlmostEqual(
            self.evaluator.evaluate(self.cost_op, params=[0.2, 0.3]),
            self.qiskit_circuit_simulation(self.cost_op, [0.2, 0.3]),
        )

    def test_optimize(self):
        """Test that we can use this in a scipy optimization."""
        trainer = ScipyTrainer(self.evaluator, {"options": {"maxiter": 3, "rhobeg": 0.2}})
        result = trainer.train(cost_op=self.cost_op, params0=[0.2, 0.3])

        self.assertGreaterEqual(len(result["energy_history"]), 3)
