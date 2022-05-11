# snowflake-stats

## Usage

Usage: `<write-log-to-stdout> | ./main.py`

- Example: Pipe docker log from remote computer into `main.py`

   ```bash
   (venv-310) [user@linux snoflake-stats]$ ssh root_at_my_server 'docker logs snowflake-proxy' 2>&1 | ./main.py
   ```

- Example: Pipe logfile into `main.py`

   ```bash
   (venv-310) [user@linux snoflake-stats]$ cat snowflake.log | ./main.py
   ```

Usage: `./main.py <docker-container-name> [<ssh-hostname>]`

- Example: Specify name of local docker container

   ```bash
   (venv-310) [user@linux snoflake-stats]$ ./main.py snowflake-proxy
   ```

- Example: Docker container name and ssh hostname

   ```bash
   (venv-310) [user@linux snoflake-stats]$ ./main.py snowflake-proxy root_at_my_server
   ```

## Example output

```
From 2022-03-28 11:58:25 until 2022-05-11 17:45:10:
2022-03-28: 1.8 GB up, 0.1 GB down (335199 OnMessages, 1799508 sends, 151390 seconds)
2022-03-29: 3.2 GB up, 0.2 GB down (509488 OnMessages, 2925767 sends, 117434 seconds)
2022-03-30: 3.5 GB up, 0.2 GB down (815323 OnMessages, 3441369 sends, 907236 seconds)
2022-03-31: 1.7 GB up, 0.1 GB down (350893 OnMessages, 1801615 sends, 222564 seconds)
2022-04-01: 7.0 GB up, 0.4 GB down (1358655 OnMessages, 6719817 sends, 239774 seconds)
2022-04-02: 1.8 GB up, 0.1 GB down (340389 OnMessages, 1702678 sends, 92243 seconds)
2022-04-03: 4.9 GB up, 0.3 GB down (972402 OnMessages, 4976213 sends, 1249335 seconds)
2022-04-04: 4.8 GB up, 0.3 GB down (824929 OnMessages, 5106120 sends, 265337 seconds)
2022-04-05: 2.1 GB up, 0.2 GB down (475139 OnMessages, 2322166 sends, 298093 seconds)
2022-04-06: 1.3 GB up, 0.3 GB down (681647 OnMessages, 1634764 sends, 243176 seconds)
2022-04-07: 2.1 GB up, 0.4 GB down (780276 OnMessages, 2250390 sends, 1058689 seconds)
2022-04-08: 2.6 GB up, 0.2 GB down (529734 OnMessages, 2523616 sends, 229954 seconds)
2022-04-09: 3.4 GB up, 0.4 GB down (1005909 OnMessages, 4061421 sends, 405517 seconds)
2022-04-10: 2.8 GB up, 0.2 GB down (519923 OnMessages, 3031888 sends, 190182 seconds)
2022-04-11: 4.1 GB up, 0.4 GB down (1190807 OnMessages, 4422564 sends, 433816 seconds)
2022-04-12: 2.6 GB up, 0.2 GB down (465997 OnMessages, 2444356 sends, 410940 seconds)
2022-04-13: 0.9 GB up, 0.1 GB down (190105 OnMessages, 851693 sends, 61943 seconds)
2022-04-14: 0.9 GB up, 0.0 GB down (161528 OnMessages, 882392 sends, 97842 seconds)
2022-04-15: 1.1 GB up, 0.1 GB down (204203 OnMessages, 1009753 sends, 67307 seconds)
2022-04-16: 1.0 GB up, 0.1 GB down (247984 OnMessages, 1058909 sends, 193348 seconds)
2022-04-17: 2.5 GB up, 0.1 GB down (510571 OnMessages, 2325162 sends, 322398 seconds)
2022-04-18: 4.8 GB up, 0.3 GB down (930634 OnMessages, 4648450 sends, 262240 seconds)
2022-04-19: 3.4 GB up, 0.3 GB down (764165 OnMessages, 3137377 sends, 451375 seconds)
2022-04-20: 2.2 GB up, 0.1 GB down (420295 OnMessages, 2261495 sends, 124751 seconds)
2022-04-21: 2.9 GB up, 0.2 GB down (692373 OnMessages, 3385141 sends, 214505 seconds)
2022-04-22: 3.7 GB up, 0.3 GB down (786635 OnMessages, 3812077 sends, 552288 seconds)
2022-04-23: 1.0 GB up, 0.1 GB down (252780 OnMessages, 1062040 sends, 239023 seconds)
2022-04-24: 2.4 GB up, 0.3 GB down (588342 OnMessages, 2356137 sends, 713742 seconds)
2022-04-25: 3.6 GB up, 0.3 GB down (812840 OnMessages, 3343832 sends, 387011 seconds)
2022-04-26: 1.8 GB up, 0.3 GB down (571760 OnMessages, 1826338 sends, 313410 seconds)
2022-04-27: 3.8 GB up, 0.2 GB down (683827 OnMessages, 3389844 sends, 162686 seconds)
2022-04-28: 4.3 GB up, 0.2 GB down (652429 OnMessages, 4288312 sends, 103591 seconds)
2022-04-29: 1.7 GB up, 0.1 GB down (285062 OnMessages, 1583714 sends, 121755 seconds)
2022-04-30: 1.5 GB up, 0.1 GB down (267516 OnMessages, 1381774 sends, 94873 seconds)
2022-05-01: 1.0 GB up, 0.1 GB down (209293 OnMessages, 990016 sends, 91807 seconds)
2022-05-02: 2.3 GB up, 0.2 GB down (544654 OnMessages, 2599260 sends, 223918 seconds)
2022-05-03: 1.9 GB up, 0.1 GB down (360980 OnMessages, 1749322 sends, 120365 seconds)
2022-05-04: 1.5 GB up, 0.1 GB down (316361 OnMessages, 1419125 sends, 126368 seconds)
2022-05-05: 1.3 GB up, 0.1 GB down (313311 OnMessages, 1274478 sends, 187806 seconds)
2022-05-06: 1.9 GB up, 0.1 GB down (344031 OnMessages, 1832855 sends, 201665 seconds)
2022-05-07: 0.7 GB up, 0.1 GB down (223631 OnMessages, 770158 sends, 150485 seconds)
2022-05-08: 0.9 GB up, 0.1 GB down (233068 OnMessages, 928026 sends, 135007 seconds)
2022-05-09: 1.3 GB up, 0.1 GB down (217657 OnMessages, 1263314 sends, 143293 seconds)
2022-05-10: 1.6 GB up, 0.1 GB down (249023 OnMessages, 1432468 sends, 118368 seconds)
2022-05-11: 0.9 GB up, 0.1 GB down (252949 OnMessages, 888759 sends, 156176 seconds)
Total:
108.1 GB up, 8.2 GB down (23444717 OnMessages, 108916473 sends, 12655026 seconds)
```
