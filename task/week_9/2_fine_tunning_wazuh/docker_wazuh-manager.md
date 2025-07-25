# wazuh-manager
## setup
```bash
docker run -d --name wazuh-manager \
  -p 1514:1514/udp \
  -p 1515:1515 \
  -v wazuh_data:/var/ossec \
  wazuh/wazuh-manager:4.7.3

docker exec -it wazuh-manager bash
```

## configuration
```bash
apt install nano

# create file
echo > /var/ossec/ruleset/decoders/0585-openstack-nova.xml 
echo > /var/ossec/ruleset/rules/1001-openstack-nova-rules.xml

# permission (alternatif karena di docker gak perlu permission)
chown -R root:wazuh /var/ossec/ruleset/decoders/0585-openstack-nova.xml
chown -R root:wazuh /var/ossec/ruleset/rules/1001-openstack-nova-rules.xml
```

## config ruels
```bash
# shorcut biar copy paste nya sekali click
echo > /var/ossec/ruleset/decoders/0585-openstack-nova.xml && nano /var/ossec/ruleset/decoders/0585-openstack-nova.xml
echo > /var/ossec/ruleset/rules/1001-openstack-nova-rules.xml && nano /var/ossec/ruleset/rules/1001-openstack-nova-rules.xml
```

> untuk confignya bisa di cek di (https://notes.ariaf.my.id/#/ruleset_idn_test#0585-openstack-nova.xml) untuk decoder, dan ruleset (https://notes.ariaf.my.id/#/ruleset_idn_test#1001-openstack-nova-rules.xml)

## restart (opsional kareana ganti rules gka perlu di reload (kecuali jika ada erorr cant connect gitu))
```bash
# alternatif gak bisa aystemctl di docker
pkill wazuh-analysisd ; /var/ossec/bin/wazuh-analysisd &
pkill wazuh-remoted ; /var/ossec/bin/wazuh-remoted &

# untuk liat error jika ketika di restart gak bisa kehubung ke anaylsis
cat /var/ossec/logs/ossec.log | grep -i error | tail -n 50
```

## testing
```bash
echo 'nova-compute.log.1.2017-05-16_13:55:31 2017-05-16 03:19:50.385 2931 INFO nova.virt.libvirt.imagecache [req-addc1839-2ed5-4778-b57e-5854eb7b8b09 - - - - -] Removable base files: /var/lib/nova/instances/_base/a489c868f0c37da93b76227c91bb03908ac0e742' | /var/ossec/bin/wazuh-logtest
```