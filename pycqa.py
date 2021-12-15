#!/usr/bin/env python3
"""Run Python Code Quality Authority (pycqa) tests."""

import argparse
import os
import subprocess

PY_VERSION = os.getenv('PY_VERSION', '3.8')
BLACK_PYTHON_VERSION = f'py{PY_VERSION.replace(".", "")}'


def _run_cmd(cmd: list, files: list) -> bool:
    """Run a subprocess command and capture the output."""
    passed = False
    cmd.extend(files)
    print(f'\nRunning "{" ".join(cmd)}":\n')
    result = subprocess.run(cmd)
    if result.returncode:
        print(f'\nFailed test (Code {result.returncode}):\nOutput: {result.stdout}\nErrors: {result.stderr}')
    else:
        print('\nPassed test!\n')
        passed = True
    return passed


def get_user_args() -> argparse.ArgumentParser:
    """Get user arguments for test configuration."""
    parser = argparse.ArgumentParser()
    parser.add_argument('files', help='The files or directories to run tests against.', nargs='*')
    parser.add_argument('-b', '--bandit', action='store_true', help='Run Bandit security tests.')
    parser.add_argument('-f', '--flake8', action='store_true', help='Run Flake8 code style tests.')
    parser.add_argument('-c', '--pycodestyle', action='store_true', help='Run PyCodeStyle tests.')
    parser.add_argument('-d', '--pydocstyle', action='store_true', help='Run PyDocStyle documentation tests.')
    parser.add_argument('-l', '--pylint', action='store_true', help='Run Pylint code style tests.')
    parser.add_argument('-m', '--mypy', action='store_true', help='Run MyPy type-hint tests.')
    parser.add_argument('-p', '--pytest', action='store_true', help='Run pytest unit tests tests.')
    parser.add_argument('-C', '--pytest-cov', action='store_true', help='Include code coverage with pytest.')
    parser.add_argument('-P', '--pytest-perf', action='store_true', help='Include performance tests with pytest.')
    parser.add_argument('-M', '--pytest-mem', action='store_true', help='Include memory tests with pytest.')
    parser.add_argument('-B', '--black', action='store_true', help='Run "Black" to automatically apply changes.')
    parser.add_argument('--fast-fail', action='store_true', help='Stop on the first failure.')
    return parser


def main() -> None:
    """Run pycqa tests."""
    parser = get_user_args()
    args = parser.parse_args()
    commands = []
    if args.bandit:
        commands.append(['bandit', '-r', '-lll'])
    if args.flake8:
        commands.append(['flake8', '--ignore=E501'])
    if args.mypy:
        commands.append(
            [
                'mypy',
                '--python-version',
                PY_VERSION,
                '--ignore-missing-imports',
                '--follow-imports',
                'skip',
                '--exclude=conftest.py',
            ]
        )
    if args.pycodestyle:
        commands.append(['pycodestyle', '--ignore=E501'])
    if args.pydocstyle:
        commands.append(['pydocstyle'])
    if args.pylint:
        commands.append(['pylint', '--disable=line-too-long,logging-fstring-interpolation,fixme,R0801'])
    if args.pytest:
        command = ['pytest', '-vv', '--cache-clear', ]
        if args.pytest_cov:
            # This requires specifying which files/directories to show coverage for.
            for filename in args.files:
                command.append(f'--cov={filename}')
        if args.pytest_perf:
            command.append('--benchmark-compare')
        if args.pytest_mem:
            mem_link = 'https://pypi.org/project/memory-profiler/'
            print(f'\nNote: The @profile decorator must be applied to show memory details.\nSee {mem_link}\n')
            command = ['python', '-m', 'memory_profiler'] + command
        commands.append(command)
    if args.black:
        commands.append(['black', '-v', '-l', '120', '-t', BLACK_PYTHON_VERSION])

    # Run all of the specified tests.
    failed_tests = []
    for cmd in commands:
        passed = _run_cmd(cmd, args.files)
        if not passed:
            if args.fast_fail:
                raise ValueError('Test failed. Exiting.')
            else:
                failed_tests.append(cmd)
    if failed_tests:
        raise ValueError('One or more tests failed.')


if __name__ == '__main__':
    main()
