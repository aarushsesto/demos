# Copyright 2016 Open Source Robotics Foundation, Inc.
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

import os
import sys

from launch.legacy import LaunchDescriptor
from launch.legacy.launcher import DefaultLauncher
from ros2run.api import get_executable_path


def add_process_to_descriptor(launch_descriptor, size, depth):
    name = '{0}_depth_{1}'.format(size, depth)
    payload = 0 if size == 'small' else 100000
    package = 'topic_monitor'
    executable = get_executable_path(package_name=package, executable_name='data_publisher')
    launch_descriptor.add_process(
        cmd=[executable, name, '--depth', str(depth), '--payload-size', str(payload)],
        name=name,
    )


def main():
    launcher = DefaultLauncher()
    launch_descriptor = LaunchDescriptor()

    os.environ['PYTHONUNBUFFERED'] = '1'  # force unbuffered output to get prints to sync correctly

    add_process_to_descriptor(launch_descriptor, 'small', 1)
    add_process_to_descriptor(launch_descriptor, 'small', 50)
    add_process_to_descriptor(launch_descriptor, 'large', 1)
    add_process_to_descriptor(launch_descriptor, 'large', 50)
    launcher.add_launch_descriptor(launch_descriptor)

    rc = launcher.launch()
    if rc != 0:
        print('Something went wrong. Return code: ' + str(rc), file=sys.stderr)
        exit(rc)


if __name__ == '__main__':
    main()
