# snowflake-stats

## Usage

Redirect your Snowflake logs to this python script. 

Add argument `-p` if they are "plain" Snowflake logs or `-s` if Snowflakes output was logged by systemd.

Examples:

```shell
ssh root@snowflake-host 'docker logs snowflake-proxy' 2>&1 | ./main.py -p
```

```shell
ssh user@snowflake-host 'journalctl -u snowflake-proxy.service' | ./main.py -s
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
