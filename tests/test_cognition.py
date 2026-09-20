import unittest

from core.cognition import CognitiveSubstrate, MnemonicRegistry


class CognitionTests(unittest.TestCase):
    def test_vector_weights_are_normalized(self):
        substrate = CognitiveSubstrate()
        state = substrate.analyze("entropy and memory", ["information", "recall"])
        self.assertAlmostEqual(sum(state["weights"].values()), 1.0, places=5)
        self.assertGreaterEqual(state["entropy"], 0.0)
        self.assertLessEqual(state["entropy"], 1.0)
        self.assertTrue(state["dream"]["novel_direction"] in substrate.dimensions)

    def test_mnemonic_encodings(self):
        registry = MnemonicRegistry()
        self.assertEqual(registry.encode(42, "major"), "R N")
        self.assertEqual(registry.encode(12, "dominic"), "AB")
        self.assertEqual(registry.encode(2, "number_shape"), "swan")

    def test_workflow_has_methodical_gate(self):
        substrate = CognitiveSubstrate()
        state = substrate.analyze("a query", [])
        self.assertIn(state["workflow"]["phase"], {"observe", "compress", "simulate", "verify", "commit"})
        self.assertIn("next_action", state["workflow"])


if __name__ == "__main__":
    unittest.main()