# Copyright (c) 2019 Toyota Research Institute.  All rights reserved.

import unittest
from monty.tempfile import ScratchDir
from taburu.channel import FileChannel
from taburu.command import TaburuCommandProcessor, AddMethodCommanded, \
    AddParameterCommanded


class CommandTest(unittest.TestCase):
    def test_command_processor(self):
        with ScratchDir('.'):
            command_channel = FileChannel("commands.txt")
            event_channel = FileChannel("events.txt")
            processor = TaburuCommandProcessor(command_channel, event_channel)

            # Dump some commands
            add_parameter_1 = AddParameterCommanded(
                table_name="agent",
                parameters=[
                    {
                        "@class": ["camd.agent.agents.QBCStabilityAgent"],
                        "n_query": [4, 6, 8],
                        "n_members": list(range(2, 5)),
                        "hull_distance": [0.1, 0.2],
                        "training_fraction": [0.4, 0.5, 0.6],
                    },
                ]
            )
            add_parameter_2 = AddParameterCommanded(
                table_name="chemsys",
                parameters=[
                    {
                        "element_1": ["Fe", "Mn"],
                        "element_2": ["O", "S"],
                    },
                ]
            )
            add_method_1 = AddMethodCommanded(
                name="CamdAgentSimulation",
                parameter_names=["agent", "chemsys"]
            )
            command_channel.publish(add_parameter_1)
            command_channel.publish(add_parameter_2)
            command_channel.publish(add_method_1)
            # Run for 6 seconds
            processor.run(iterations=2, poll_time=0.5)
            self.assertEqual(
                processor.state.methods['CamdAgentSimulation'], (0, 1))
            self.assertEqual(
                len(processor.state.parameters['agent']), 54)


if __name__ == '__main__':
    unittest.main()
