#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime
import sys

import exec


def test() -> None:
    log = example_log()
    parse_log(log)


def main() -> None:
    if len(sys.argv) > 1:
        log = get_docker_log()
    else:
        log = sys.stdin.read()
    parse_log(log)


def parse_log(log: str) -> None:
    tps = [Throughput.from_str(line) for line in log.splitlines()]
    tps = [tp for tp in tps if tp]
    if len(tps) > 0:
        print()
        print(f'From {tps[0].dt} until {tps[-1].dt}:')

    grouped_by_day = {}
    for tp in tps:
        if tp.dt.date() in grouped_by_day.keys():
            grouped_by_day[tp.dt.date()].append(tp)
        else:
            grouped_by_day[tp.dt.date()] = [tp]

    tps_total = Throughput.zero()
    for day, tp_list in grouped_by_day.items():
        tps_sum = sum(tp_list, Throughput.zero())
        print(f'{day}: {tps_sum}')
        tps_total += tps_sum

    print()
    print(f'Total:\n{tps_total}')


def example_log() -> str:
    return '\n'.join(
        [
            '2022/09/13 15:08:36 Proxy starting',
            '2022/09/13 15:08:43 NAT type: unrestricted',
            '2022/09/27 02:02:26 In the last 1h0m0s, there were 1 connections. Traffic Relayed ↑ 708 KB, ↓ 328 KB.',
            '2022/09/28 02:02:26 In the last 1h0m0s, there were 0 connections. Traffic Relayed ↑ 0 B, ↓ 0 B.',
            '2022/09/29 05:02:26 In the last 1h0m0s, there were 5 connections. Traffic Relayed ↑ 6 MB, ↓ 787 KB.',
            '2022/09/29 11:02:26 In the last 1h0m0s, there were 26 connections. Traffic Relayed ↑ 16 MB, ↓ 10 MB.',
            'sctp ERROR: 2022/09/29 23:00:53 [0xc00006e000] stream 1 not found)',
        ]
    )


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
    # DATE_FORMAT_EXAMPLE = '2022/04/06 10:37:42'
    DATE_FORMAT_STR = '%Y/%m/%d %H:%M:%S'

    # Units sorted from small to large.
    _unit_dict = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024,
        'TB': 1024 * 1024 * 1024 * 1024,
    }

    @classmethod
    def from_str(cls, line: str) -> Throughput | None:
        pattern_str = r'(\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d)' \
                      r' In the last 1h0m0s, there were (\d+) connections\. ' \
                      r'Traffic Relayed ↑ (\d+ [A-Z]+), ↓ (\d+ [A-Z]+)\.'
        pattern = re.compile(pattern_str)
        match = pattern.match(line)

        if not match:
            if 'sctp ERROR' in line or \
                    'Proxy starting' in line or \
                    'NAT type: ' in line:
                return None

            print(f'No match for this line: {line}', file=sys.stderr)
            return None

        dt = datetime.strptime(match.group(1), Throughput.DATE_FORMAT_STR)
        connections = int(match.group(2))
        bytes_up = cls._split_to_bytes(match.group(3))
        bytes_down = cls._split_to_bytes(match.group(4))

        return cls(dt, bytes_up, bytes_down, connections)

    @classmethod
    def from_args(cls, dt, bytes_up, bytes_down, connections) -> Throughput:
        return cls(dt, bytes_up, bytes_down, connections)

    @classmethod
    def zero(cls) -> Throughput:
        return cls(None, 0, 0, 0)

    def __init__(self, dt, bytes_up, bytes_down, connections):
        self.dt = dt
        self.bytes_up = bytes_up
        self.bytes_down = bytes_down
        self.connections = connections

    def __add__(self, other):
        if not isinstance(other, Throughput):
            raise ValueError('invalid argument')
        return Throughput.from_args(
            self.dt,
            self.bytes_up + other.bytes_up,
            self.bytes_down + other.bytes_down,
            self.connections + other.connections,
        )

    def __str__(self) -> str:
        up, up_unit = Throughput._to_unit_auto(self.bytes_up)
        down, down_unit = Throughput._to_unit_auto(self.bytes_down)
        return f'{up} {up_unit} up\t{down} {down_unit} down\t{self.connections} Connections'

    @classmethod
    def _split_to_bytes(cls, num_unit: str) -> int:
        num, unit = num_unit.split(' ')
        num = int(num)
        return cls._to_bytes(num, unit)

    @classmethod
    def _to_bytes(cls, num: int, unit: str) -> int:
        return num * cls._unit_dict[unit]

    @classmethod
    def _to_unit(cls, num_bytes: int, unit: str = 'GB') -> int:
        return int(round(num_bytes / cls._unit_dict[unit], 1))

    @classmethod
    def _to_unit_auto(cls, num_bytes: int) -> (int, str):
        converted, unit = -1, 'ERROR'

        for unit, factor in cls._unit_dict.items():
            converted = cls._to_unit(num_bytes, unit)
            if converted < 9999:
                return converted, unit

        if unit == 'ERROR':
            raise ValueError('Invalid state')
        return converted, unit


if __name__ == '__main__':
    # test()
    main()
