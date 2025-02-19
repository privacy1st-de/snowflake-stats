#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime
import sys


def test() -> None:
    log = example_log().splitlines()
    parse_log(log)

    log = example_systemd_log().splitlines()
    log = [remove_systemd_prefix(line) for line in log]
    parse_log(log)


def main() -> None:
    systemd = parse_args()
    log = sys.stdin.read().splitlines()
    if systemd:
        log = [remove_systemd_prefix(line) for line in log]
    parse_log(log)


def parse_args() -> bool:
    usage = (f'usage: {sys.argv[0]} -p|-s\n'
             f'  -p: parse plain Snowflake output\n'
             f'  -p: parse Snowflake output logged by systemd\n')

    if len(sys.argv) != 2 or sys.argv[0] in ['--help', '-h']:
        print(usage, file=sys.stderr)
        exit(1)

    arg1 = sys.argv[1]
    if arg1 == '-p':
        return False
    elif arg1 == '-s':
        return True
    else:
        raise Exception(usage)


def remove_systemd_prefix(line: str) -> str:
    pattern_str = r'[A-Z][a-z]+ [0-9]+ [0-9][0-9]:[0-9][0-9]:[0-9][0-9] \S+ \S+\[[0-9]+\]: (.+)'
    pattern = re.compile(pattern_str)
    match = pattern.match(line)

    if not match:
        raise Exception(match)

    return match.group(1)


def parse_log(log: list[str]) -> None:
    tps = [Throughput.from_str(line) for line in log]
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
            '2025/02/19 18:24:29 In the last 1h0m0s, there were 31 completed connections. Traffic Relayed ↓ 46719 KB, ↑ 3229 KB.'
            'sctp ERROR: 2022/09/29 23:00:53 [0xc00006e000] stream 1 not found)',
        ]
    )


def example_systemd_log() -> str:
    return 'Feb 19 19:24:29 yodaNas proxy[1318]: 2025/02/19 18:24:29 In the last 1h0m0s, there were 3 completed connections. Traffic Relayed ↓ 46719 KB, ↑ 3229 KB.\n'


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
                      r' In the last 1h0m0s, there were (\d+) completed connections\. ' \
                      r'Traffic Relayed ↓ (\d+ [A-Z]+), ↑ (\d+ [A-Z]+)\.'
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
        bytes_down = cls._split_to_bytes(match.group(3))
        bytes_up = cls._split_to_bytes(match.group(4))

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
