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