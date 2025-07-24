# log
## log normal
```bash
nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server [req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829
nova-compute.log.1.2017-05-16_13:55:31 2017-05-16 00:00:04.500 2931 INFO nova.compute.manager [req-3ea4052c-895d-4b64-9e2d-04d64c4d94ab - - - - -] [instance: b9000564-fe1a-409b-b8cc-1e88b294cd1d] VM Started (Lifecycle Event)
```

# /var/ossec/ruleset/decoders/0585-openstack-nova.xml
## 1 test nova api
```xml
<decoder name="nova-api">
  <prematch type="pcre2">^nova\-api\.log</prematch>
</decoder>

<decoder name="nova-api-logfile">
  <parent>nova-api</parent>
  <regex type="pcre2" offset="after_parent">\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})</regex>
  <order>log_index, log_timestamp</order>
</decoder>
```

## 2 nova log
```xml
<decoder name="nova-log">
  <prematch type="pcre2">^nova\-[^ ]+\.log</prematch>
</decoder>

<decoder name="nova-log_1">
  <parent>nova-log</parent>
  <regex type="pcre2" offset="after_parent">\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})</regex>
  <order>log_index, log_timestamp</order>
</decoder>
```

## 3 focuesd regex
### log_index - event timestamp
```xml
<decoder name="nova-log_combined">
  <parent>nova-log</parent>
  <regex type="pcre2" offset="after_parent">\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})</regex>
  <order>log_index, log_timestamp, event_timestamp</order>
</decoder>
```

### log_index - log_level
```xml
<decoder name="nova-log_combined">
  <parent>nova-log</parent>
  <regex type="pcre2" offset="after_parent">\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL)</regex>
  <order>log_index, log_timestamp, event_timestamp, pid, log_level</order>
</decoder>
```

### log_index - request id
```xml
<decoder name="nova-log_combined">
  <parent>nova-log</parent>
  <regex type="pcre2" offset="after_parent">\.(\d+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[req-([a-f0-9\-]+)</regex>
  <order>log_index, log_timestamp, event_timestamp, pid, log_level, module, request_id</order>
</decoder>
```

## 4 dipisah
### parent
```xml
<decoder name="nova-api-log">
  <prematch type="pcre2">^nova-api\.log</prematch>
</decoder>

<decoder name="nova-computed-log">
  <prematch type="pcre2">^nova-compute\.log</prematch>
</decoder>
```

### 1
```xml
<!-- Decoder gabungan untuk nova-api -->
<decoder name="nova-api-log-detail">
  <parent>nova-api-log</parent>
  <regex type="pcre2" offset="after_parent">\.([0-9]+)\.([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}) ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}) ([0-9]{4,6}) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[req-([a-f0-9\-]+) [a-f0-9]+ [a-f0-9]+ - - -\] ([0-9\.]+) "(GET|POST|PUT|DELETE) ([^"]+)" status: (\d{3}) len: (\d+) time: ([0-9\.]+)</regex>
  <order>log_index, log_timestamp, event_timestamp, pid, log_level, module, request_id, ip, http_method, http_path, http_status, http_len, http_time</order>
</decoder>
```

### 2
```xml
<!-- Decoder gabungan untuk nova-compute -->
<decoder name="nova-compute-log-detail">
  <parent>nova-computed-log</parent>
  <regex type="pcre2">\.([0-9]+)\.(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d+) (INFO|DEBUG|ERROR|WARNING|CRITICAL) ([\w\.]+) \[([^\]]+)\](?: \[instance: ([a-f0-9\-]+)\])?(?: (.+))?</regex>
  <order>log_index, log_timestamp, pid, pid_num, log_level, module, request_id, instance_id, message</order>
</decoder>
```

# /var/ossec/etc/rules/local_rules.xml
## 1
```xml
<group name="nova,">
  <rule id="100020" level="3">
    <decoded_as>nova-api-log</decoded_as>
    <description>Test match for nova-api-log decoder</description>
  </rule>
</group>
```

# a
```bash
cd /var/ossec/ruleset/decoders
# xmllint --noout 0585-openstack-nova.xml

systemctl restart wazuh-manager
systemctl status wazuh-manager | cat

echo 'nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server [req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829' | /var/ossec/bin/wazuh-logtest
echo 'nova-compute.log.1.2017-05-16_13:55:31 2017-05-16 00:00:04.500 2931 INFO nova.compute.manager [req-3ea4052c-895d-4b64-9e2d-04d64c4d94ab - - - - -] [instance: b9000564-fe1a-409b-b8cc-1e88b294cd1d] VM Started (Lifecycle Event)' | /var/ossec/bin/wazuh-logtest

# echo 'nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server' | /var/ossec/bin/wazuh-logtest

# echo 'nova-api.log.1.2017-05-16_13:53:08' | /var/ossec/bin/wazuh-logtest
```