# Copyright 2018 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cstar.job
import cstar.jobreader
import os
import shutil

from cstar.output import msg


def cleanup(max_days, listdir=os.listdir, jobread=cstar.jobreader.read, delete=shutil.rmtree):
    job_dir = os.path.expanduser('~/.cstar/jobs')
    for job_id in listdir(job_dir):
        try:
            jobread(cstar.job.Job(), job_id, stop_after=None, max_days=max_days, endpoint_mapper=lambda x: None)
        except Exception:
            msg("Removing job", job_id)
            full_name = os.path.join(job_dir, job_id)
            delete(full_name)


def execute_cleanup(args):
    msg('Cleaning up old jobs')
    cleanup(args.max_job_age)


def add_cleanup_subparser(subparsers, add_common_arguments, add_cstar_arguments_without_command):
    cleanup_parser = subparsers.add_parser('cleanup-jobs', help='Cleanup old finished jobs and exit (*)')
    cleanup_parser.set_defaults(func=execute_cleanup)
    add_common_arguments(cleanup_parser)
    add_cstar_arguments_without_command(cleanup_parser)
