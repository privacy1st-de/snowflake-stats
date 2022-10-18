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
From 2022-09-25 22:14:50 until 2022-09-29 11:02:26:
2022-09-25: 2000 KB up  1000 KB down    4 Connections
2022-09-26: 1152 MB up  395 MB down     199 Connections
2022-09-27: 1608 MB up  548 MB down     278 Connections
2022-09-28: 774 MB up   423 MB down     281 Connections
2022-09-29: 760 MB up   314 MB down     136 Connections

Total:
4297 MB up      1682 MB down    898 Connections
```
