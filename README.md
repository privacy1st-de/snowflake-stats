# snowflake-stats

## Usage

```bash
(venv-310) [user@linux snoflake-stats]$ ./main.py
```

## Example output

```
[DEBUG] execute_and_capture: ['ssh', 'root_at_my_server', 'docker logs snowflake-proxy']
From 2022-03-28 11:58:25 until 2022-04-06 12:31:40:
2022-03-28: 1.8 GB up, 0.1 GB down (335199 OnMessages, 1799508 sends, 151390 seconds)
2022-03-29: 3.2 GB up, 0.2 GB down (509488 OnMessages, 2925767 sends, 117434 seconds)
2022-03-30: 3.5 GB up, 0.2 GB down (815323 OnMessages, 3441369 sends, 907236 seconds)
2022-03-31: 1.7 GB up, 0.1 GB down (350893 OnMessages, 1801615 sends, 222564 seconds)
2022-04-01: 7.0 GB up, 0.4 GB down (1358655 OnMessages, 6719817 sends, 239774 seconds)
2022-04-02: 1.8 GB up, 0.1 GB down (340389 OnMessages, 1702678 sends, 92243 seconds)
2022-04-03: 4.9 GB up, 0.3 GB down (972402 OnMessages, 4976213 sends, 1249335 seconds)
2022-04-04: 4.8 GB up, 0.3 GB down (824929 OnMessages, 5106120 sends, 265337 seconds)
2022-04-05: 2.1 GB up, 0.2 GB down (475139 OnMessages, 2322166 sends, 298093 seconds)
2022-04-06: 0.5 GB up, 0.2 GB down (553513 OnMessages, 894773 sends, 206981 seconds)
```
