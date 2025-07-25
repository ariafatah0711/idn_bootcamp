# yara ke wazuh
- [documentation.wazuh.com/current/proof-of-concept-guide/detect-malware-yara-integration.html](https://documentation.wazuh.com/current/proof-of-concept-guide/detect-malware-yara-integration.html)

## buat sebuah module yara di agent (msh gagal)
```bash
sudo apt update
sudo apt install yara
```

## testing
```bash
mkdir -p /opt/test
echo "virus detected" > /opt/test/sampe.txt

cat << 'EOF' > /opt/local.yar
rule detect_virus
{
    strings:
        $a = "virus detected"
    condition:
        $a
}
EOF
```

```sudo nano /var/ossec/etc/ossec.conf```
```xml
<wodle name="yara">
    <disabled>no</disabled>
    <scan_on_start>yes</scan_on_start>
    <interval>5m</interval>
    <paths>/opt/test</paths>
    <rules_path>/opt/local.yar</rules_path>
</wodle>
```

restart wazuh
```bash
sudo systemctl restart wazuh-agent
```

## cek log
```bash
yara /opt/local.yar /opt/test

# manager
sudo tail -f /var/ossec/logs/alerts/alerts.json | grep yara

# agent
sudo tail -f /var/ossec/logs/ossec.log | grep -i yara
```