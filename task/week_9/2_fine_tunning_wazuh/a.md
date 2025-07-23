# /var/ossec/ruleset/decoders/0585-openstack-nova.xml
## 1
```xml
<decoder name="nova-api-log">
  <prematch>nova\.osapi_compute\.wsgi\.server</prematch>
  <regex>^[^ ]+ (\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\.\\d+) \\d+ INFO ([\\w\\.\\-_]+)</regex>
  <order>timestamp,program_name</order>
</decoder>
```

## 2
```xml
<decoder name="nova-api-log">
  <prematch>nova\.osapi_compute\.wsgi\.server</prematch>
  <regex>^[^\s]+ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.\d{3}) (\d+) ([A-Z]+) ([\w\.]+)</regex>
  <order>timestamp, pid, level, program</order>
</decoder>
```

## 3
```xml

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
cat > 0585-openstack-nova.xml << EOF
<decoder name="nova-api-log">
  <prematch>nova\.osapi_compute\.wsgi\.server</prematch>
  <regex><![CDATA[
^[^ ]+ (?<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3,6})?) (?<pid>[^ ]*) (?<level>[A-Z]+) (?<program>[\w\.]+)(?: \[(?<context>[^\]]*)\])? (?<ip>[\d\.]+) "(?<method>[^ ]+) (?<path>[^"]+)" status: (?<status>\d+) len: (?<len>\d+) time: (?<time>[0-9.]+)
  ]]></regex>
  <order>timestamp,pid,level,program,context,ip,method,path,status,len,time</order>
</decoder>
EOF
systemctl restart wazuh-manager
```