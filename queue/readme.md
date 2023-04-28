## start rabbit mq

```shell
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
```

## publish to queue

Usage:
```shell
python3 publish.py <start_range> <end_range>
```

Example:
```shell
python3 publish.py 0.0.0.0 0.0.0.10
```

## worker

```shell
python3 worker.py <workers>
```

Example: 

```shell
python3 worker.py 10
```