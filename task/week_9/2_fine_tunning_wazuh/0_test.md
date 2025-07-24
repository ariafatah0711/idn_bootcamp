```
nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server [req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829
```

# testa
```bash
^nova-[\w\-]+\.log
nova-api.log

\.\d+\.\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}
.1.2017-05-16_13:53:08

^(nova-[\w\-]+\.log)\.(\d+\.\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})
nova-api.log
1.2017-05-16_13:53:08
```

# testb
```bash
\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL)

.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO 
```