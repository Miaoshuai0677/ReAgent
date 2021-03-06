#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

import logging
import unittest

from reagent.models.dqn import FullyConnectedDQN
from reagent.test.models.test_utils import check_save_load


logger = logging.getLogger(__name__)


class TestFullyConnectedDQN(unittest.TestCase):
    def test_basic(self):
        state_dim = 8
        action_dim = 4
        model = FullyConnectedDQN(
            state_dim,
            action_dim,
            sizes=[8, 4],
            activations=["relu", "relu"],
            use_batch_norm=True,
        )
        input = model.input_prototype()
        self.assertEqual((1, state_dim), input.state.float_features.shape)
        # Using batch norm requires more than 1 example in training, avoid that
        model.eval()
        q_values = model(input)
        self.assertEqual((1, action_dim), q_values.q_values.shape)

    def test_save_load(self):
        state_dim = 8
        action_dim = 4
        model = FullyConnectedDQN(
            state_dim,
            action_dim,
            sizes=[8, 4],
            activations=["relu", "relu"],
            use_batch_norm=False,
        )
        expected_num_params, expected_num_inputs, expected_num_outputs = 6, 1, 1
        check_save_load(
            self, model, expected_num_params, expected_num_inputs, expected_num_outputs
        )

    def test_save_load_batch_norm(self):
        state_dim = 8
        action_dim = 4
        model = FullyConnectedDQN(
            state_dim,
            action_dim,
            sizes=[8, 4],
            activations=["relu", "relu"],
            use_batch_norm=True,
        )
        # Freezing batch_norm
        model.eval()
        expected_num_params, expected_num_inputs, expected_num_outputs = 21, 1, 1
        check_save_load(
            self, model, expected_num_params, expected_num_inputs, expected_num_outputs
        )
