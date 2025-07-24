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

# fixed
```bash
\.([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}) ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}) ([0-9]{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[req-([a-f0-9\-]+)(?: [^\]]*)?\](?: ([0-9\.,]+))?

---

nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server [req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829

nova-api.log.1.2017-05-16_13:53:08 2017-05-16 06:24:34.596 25786 INFO nova.metadata.wsgi.server [req-62f52759-163e-469d-9823-a6562fed14d7 - - - - -] 10.11.23.165,10.11.10.1 "GET /openstack/2013-10-17/vendor_data.json HTTP/1.1" status: 200 len: 124 time: 0.2370501

nova-api.log.1.2017-05-16_13:53:08 2017-05-16 06:25:02.867 25746 ERROR keystonemiddleware.auth_token [req-1cc7d50c-25a2-46b0-a668-9c00f589160c 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] Bad response code while validating token: 503

nova-api.log.1.2017-05-16_13:53:08 2017-05-16 06:25:02.868 25746 WARNING keystonemiddleware.auth_token [req-1cc7d50c-25a2-46b0-a668-9c00f589160c 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] Identity response: <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">

nova-api.log.2017-05-14_21:27:04 2017-05-14 19:39:01.445 25746 INFO nova.osapi_compute.wsgi.server [req-5a2050e7-b381-4ae9-92d2-8b08e9f9f4c0 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1,10.1.10.12 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1583 time: 0.1919448

nova-compute.log.1.2017-05-16_13:55:31 2017-05-16 00:00:04.500 2931 INFO nova.compute.manager [req-3ea4052c-895d-4b64-9e2d-04d64c4d94ab - - - - -] [instance: b9000564-fe1a-409b-b8cc-1e88b294cd1d] VM Started (Lifecycle Event)
```

\.([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}) ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}) ([0-9]{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[req-([a-f0-9\-]+)(?: [^\]]*)?\](?: ([0-9\.,]+))? "(GET|POST|PUT|DELETE) ([^ ]+) HTTP\/([0-9.]+)" status: (\d{3}) len: (\d+) time: ([0-9\.]+)