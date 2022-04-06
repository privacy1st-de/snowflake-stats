#!/usr/bin/env python3
from __future__ import annotations
from typing import List
from datetime import datetime
import sys

import exec


def main():
    if len(sys.argv) > 1:
        log = get_docker_log()
    else:
        log = sys.stdin.read()

    filtered: List[str] = [line for line in log.splitlines()
                           if Throughput.PATTERN in line]
    # filtered = filtered_example()

    tps = [Throughput.from_str(line) for line in filtered]
    print(f'From {tps[0].dt} until {tps[-1].dt}:')

    grouped_by_day = {}
    for tp in tps:
        if tp.dt.date() in grouped_by_day.keys():
            grouped_by_day[tp.dt.date()].append(tp)
        else:
            grouped_by_day[tp.dt.date()] = [tp]

    for day, tp_list in grouped_by_day.items():
        tps_sum = sum(tp_list, Throughput.zero())
        print(f'{day}: {tps_sum}')


def filtered_example() -> List[str]:
    return [
       '2022/04/04 15:08:10 Traffic throughput (up|down): 4 MB|259 KB -- (691 OnMessages, 3886 Sends, over 269 seconds)',
       '2022/04/04 16:00:06 Traffic throughput (up|down): 13 MB|15 MB -- (46326 OnMessages, 32325 Sends, over 36634 seconds)',
       '2022/04/04 15:57:04 Traffic throughput (up|down): 61 KB|8 KB -- (69 OnMessages, 91 Sends, over 157 seconds)',
    ]


def get_docker_log() -> str:
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <docker-container-name> [<ssh-hostname>]', file=sys.stderr)
        exit(1)

    container_name = sys.argv[1]

    ssh_hostname = None
    if len(sys.argv) > 2:
        ssh_hostname = sys.argv[2]

    return docker_logs(container_name, ssh_hostname)


def docker_logs(container_name: str, ssh_host: str = None) -> str:
    return exec.execute_and_capture(['docker', 'logs', container_name], ssh_host, 'stderr')


class Throughput:
    FORMAT_EXAMPLE = '2022/04/06 10:37:42'
    FORMAT_STR = '%Y/%m/%d %H:%M:%S'
    FORMAT_LENGTH = len(FORMAT_EXAMPLE)

    PATTERN = ' Traffic throughput (up|down): '

    _unit_dict = {
        'B': 1,
        'KB': 10 ** 3,
        'MB': 10 ** 6,
        'GB': 10 ** 9,
        'TB': 10 ** 12,
    }

    @classmethod
    def from_str(cls, line: str) -> Throughput:
        dt_str = line[0:Throughput.FORMAT_LENGTH]
        dt = datetime.strptime(dt_str, Throughput.FORMAT_STR)

        _, tail = line.split(Throughput.PATTERN)
        up, tail = tail.split('|')
        down, tail = tail.split(' -- (')
        on_messages, tail = tail.split(', ', maxsplit=1)
        sends, tail = tail.split(', ')
        seconds, tail = tail.split(')')

        bytes_up = cls._split_to_bytes(up)
        bytes_down = cls._split_to_bytes(down)
        on_messages = int(on_messages.split(' ')[0])
        sends = int(sends.split(' ')[0])
        seconds = int(seconds.split(' ')[1])

        return cls(dt, bytes_up, bytes_down, on_messages, sends, seconds)

    @classmethod
    def from_args(cls, dt, bytes_up, bytes_down, on_messages, sends, seconds) -> Throughput:
        return cls(dt, bytes_up, bytes_down, on_messages, sends, seconds)

    @classmethod
    def zero(cls) -> Throughput:
        return cls(None, 0, 0, 0, 0, 0)

    def __init__(self, dt, bytes_up, bytes_down, on_messages, sends, seconds):
        self.dt = dt
        self.bytes_up = bytes_up
        self.bytes_down = bytes_down
        self.on_messages = on_messages
        self.sends = sends
        self.seconds = seconds

    def __add__(self, other):
        if not isinstance(other, Throughput):
            raise ValueError('invalid argument')
        return Throughput.from_args(
            self.dt,
            self.bytes_up + other.bytes_up,
            self.bytes_down + other.bytes_down,
            self.on_messages + other.on_messages,
            self.sends + other.sends,
            self.seconds + other.seconds,
        )

    def __str__(self) -> str:
        return f'{Throughput._to_gb(self.bytes_up)} GB up, {Throughput._to_gb(self.bytes_down)} GB down ({self.on_messages} OnMessages, {self.sends} sends, {self.seconds} seconds)'

    @classmethod
    def _split_to_bytes(cls, num_unit: str) -> int:
        num, unit = num_unit.split(' ')
        num = int(num)
        return cls._to_bytes(num, unit)

    @classmethod
    def _to_bytes(cls, num: int, unit: str) -> int:
        return num * cls._unit_dict[unit]

    @classmethod
    def _to_gb(cls, num_bytes: int) -> int:
        return round(num_bytes / cls._unit_dict['GB'], 1)


if __name__ == '__main__':
    main()
