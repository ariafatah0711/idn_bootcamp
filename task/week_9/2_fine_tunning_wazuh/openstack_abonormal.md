# log openstack abonormal
## log
```bash
nova-api.log.2017-05-14_21:27:04 2017-05-14 19:39:01.445 25746 INFO nova.osapi_compute.wsgi.server [req-5a2050e7-b381-4ae9-92d2-8b08e9f9f4c0 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1583 time: 0.1919448
nova-compute.log.2017-05-14_21:27:09 2017-05-14 19:39:02.007 2931 INFO nova.virt.libvirt.driver [req-e285b551-587f-4c1d-8eba-dceb2673637f 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] [instance: 3edec1e4-9678-4a3a-a21b-a145a4ee5e61] Creating image
```

yang membedakana hanya di bagian awal ```^([\w\-\.]+)\.log\.``` kalo yang normal ada ini ```^([\w\-\.]+)\.log\.\d+\```

# # /var/ossec/ruleset/decoders/0585-openstack-nova.xml
## 1
```xml
<decoder name="nova-api-log">
  <prematch type="pcre2">^nova-api\.log</prematch>
</decoder>

<decoder name="nova-computed-log">
  <prematch type="pcre2">^nova-compute\.log</prematch>
</decoder>

<!-- Decoder gabungan untuk nova-api -->
<decoder name="nova-api-log-detail">
  <parent>nova-api-log</parent>
  <regex type="pcre2" offset="after_parent">\.([0-9]+)\.([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}) ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}) ([0-9]{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[req-([a-f0-9\-]+) [a-f0-9]+ [a-f0-9]+ - - -\] ([0-9\.]+) "(GET|POST|PUT|DELETE) ([^"]+)" status: (\d{3}) len: (\d+) time: ([0-9\.]+)</regex>
  <order>log_index, log_timestamp, event_timestamp, pid, log_level, module, request_id, ip, http_method, http_path, http_status, http_len, http_time</order>
</decoder>

<!-- Decoder gabungan untuk nova-compute -->
<decoder name="nova-compute-log-detail">
  <parent>nova-computed-log</parent>
  <regex type="pcre2">\.([0-9]+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d+) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[([^\]]+)\](?: \[instance: ([a-f0-9\-]+)\])?(?: (.+))?</regex>
  <order>log_index, log_timestamp, pid, pid_num, log_level, module, request_id, instance_id, message</order>
</decoder>
```

# run
```bash
echo 'nova-api.log.2017-05-14_21:27:04 2017-05-14 19:39:01.445 25746 INFO nova.osapi_compute.wsgi.server [req-5a2050e7-b381-4ae9-92d2-8b08e9f9f4c0 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1583 time: 0.1919448' | /var/ossec/bin/wazuh-logtest
echo 'nova-compute.log.2017-05-14_21:27:09 2017-05-14 19:39:02.007 2931 INFO nova.virt.libvirt.driver [req-e285b551-587f-4c1d-8eba-dceb2673637f 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] [instance: 3edec1e4-9678-4a3a-a21b-a145a4ee5e61] Creating image' | /var/ossec/bin/wazuh-logtest
```