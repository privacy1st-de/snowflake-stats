#!/usr/bin/env python3
from typing import List
import sys
import subprocess
import shlex


class NonZeroExitCode(Exception):
    def __init__(self, exit_code, stdout, stderr):
        super(NonZeroExitCode, self).__init__(f'exit_code: {exit_code}, stdout: {stdout}, stderr: {stderr}')


def wrap_command_with_ssh(command: List[str], ssh_host: str) -> List[str]:
    return ['ssh', ssh_host, ' '.join([shlex.quote(arg) for arg in command])]


def execute(command: List[str], ssh_host: str = None) -> None:
    """
    https://docs.python.org/3.10/library/subprocess.html#frequently-used-arguments

    Executes the given command using stdin, stdout, stderr of the parent process.

    The output is not captured.

    :raises subprocess.CalledProcessError: In case of non-zero exit code.
    """
    if ssh_host is not None:
        command = wrap_command_with_ssh(command, ssh_host)

    print(f'[DEBUG] execute: {command}')

    subprocess.run(
        command,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )


def execute_and_capture(command: List[str], ssh_host: str = None, file='stdout') -> str:
    """
    Executes the given command and captures it stdout.

    :return: Stdout of subprocess.
    :raises NonZeroExitCode: In case of non-zero exit code. This exception includes the exit_code, stdout and stderr in it's message.
    """
    if ssh_host is not None:
        command = wrap_command_with_ssh(command, ssh_host)

    print(f'[DEBUG] execute_and_capture: {command}')

    completed: subprocess.CompletedProcess = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise NonZeroExitCode(completed.returncode, completed.stdout, completed.stderr)

    if file == 'stdout':
        return completed.stdout
    if file == 'stderr':
        return completed.stderr
    raise ValueError('invalid argument')
