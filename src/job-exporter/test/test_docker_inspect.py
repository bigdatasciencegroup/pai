# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import unittest

import base

sys.path.append(os.path.abspath("../src/"))

from docker_inspect import parse_docker_inspect

class TestDockerInspect(base.TestBase):
    """
    Test docker_inspect.py
    """

    def test_parse_docker_inspect(self):
        sample_path = "data/docker_inspect_sample.json"
        with open(sample_path, "r") as f:
            docker_inspect = f.read()
        inspect_info = parse_docker_inspect(docker_inspect)
        target_inspect_info = {"labels": {"container_label_PAI_USER_NAME": "openmindstudio", "container_label_GPU_ID": "0,1,", "container_label_PAI_HOSTNAME": "paigcr-a-gpu-1058", "container_label_PAI_JOB_NAME": "trialslot_nnimain_d65bc5ac", "container_label_PAI_CURRENT_TASK_ROLE_NAME": "tuner"}, "env": {"container_env_PAI_TASK_INDEX": "0"}, "pid": 95539}
        self.assertEqual(target_inspect_info, inspect_info)

if __name__ == '__main__':
    unittest.main()
