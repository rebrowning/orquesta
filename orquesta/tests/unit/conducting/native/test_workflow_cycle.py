# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orquesta import statuses
from orquesta.tests import mocks
from orquesta.tests.unit import base as test_base
from orquesta.tests.unit.conducting.native import base


class CyclicWorkflowConductorTest(
    base.OrchestraWorkflowConductorTest, test_base.WorkflowComposerTest
):
    def test_cycle(self):
        wf_name = "cycle"

        self.assert_spec_inspection(wf_name)

        expected_task_seq = [
            "prep",
            "task1",
            "task2",
            "task3",
            "task1",
            "task2",
            "task3",
            "task1",
            "task2",
            "task3",
        ]

        wf_def = self.get_wf_def(wf_name)
        wf_spec = self.spec_module.instantiate(wf_def)
        mock = mocks.WorkflowConductorMock(
            wf_spec,
            expected_task_seq,
        )
        mock.assert_conducting_sequences()

    def test_cycles(self):
        wf_name = "cycles"

        self.assert_spec_inspection(wf_name)

        expected_task_seq = [
            "prep",
            "task1",
            "task2",
            "task3",
            "task4",
            "task2",
            "task5",
            "task1",
            "task2",
            "task3",
            "task4",
            "task2",
            "task5",
            "task1",
            "task2",
            "task3",
            "task4",
            "task2",
            "task5",
        ]

        wf_def = self.get_wf_def(wf_name)
        wf_spec = self.spec_module.instantiate(wf_def)
        mock = mocks.WorkflowConductorMock(
            wf_spec,
            expected_task_seq,
        )
        mock.assert_conducting_sequences()

    def test_rollback_retry(self):
        wf_name = "rollback-retry"

        self.assert_spec_inspection(wf_name)

        expected_task_seq = ["init", "check", "create", "rollback", "check", "delete"]

        mock_statuses = [
            statuses.SUCCEEDED,  # init
            statuses.FAILED,  # check
            statuses.SUCCEEDED,  # create
            statuses.SUCCEEDED,  # rollback
            statuses.SUCCEEDED,  # check
            statuses.SUCCEEDED,  # delete
        ]
        wf_def = self.get_wf_def(wf_name)
        wf_spec = self.spec_module.instantiate(wf_def)
        mock = mocks.WorkflowConductorMock(wf_spec, expected_task_seq, mock_statuses=mock_statuses)
        mock.assert_conducting_sequences()

    def test_cycle_and_fork(self):
        wf_name = "cycle-fork"

        self.assert_spec_inspection(wf_name)

        expected_task_seq = [
            "init",
            "query",
            "decide_cheer",
            "decide_work",
            "cheer",
            "notify_work",
            "toil",
            "query",
            "decide_cheer",
            "decide_work",
        ]

        mock_results = [
            None,  # init
            True,  # query
            None,  # decide_cheer
            None,  # decide_work
            None,  # cheer
            None,  # notify_work
            None,  # toil
            False,  # query
            None,  # decide_cheer
            None,  # decide_work
        ]

        wf_def = self.get_wf_def(wf_name)
        wf_spec = self.spec_module.instantiate(wf_def)
        mock = mocks.WorkflowConductorMock(wf_spec, expected_task_seq, mock_results=mock_results)
        mock.assert_conducting_sequences()
