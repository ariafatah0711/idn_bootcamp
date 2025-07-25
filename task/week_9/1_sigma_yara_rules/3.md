# setup
```bash
pip install sigma-cli
```

or with
```bash
git clone https://github.com/SigmaHQ/sigma-cli.git
cd sigma-cli
apt install python3-poetry
poetry install && poetry shell
sigma version

# list plugin
sigma plugin list --plugin-type backend

# install plugin
sigma plugin install splunk
pip install pysigma-backend-elasticsearch
```

## Download rule Sigma
```bash
git clone https://github.com/SigmaHQ/sigma
cd sigma

cat << 'EOF' > rules/local.yml
title: Detect Hello in CommandLine
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    CommandLine|contains: "hello"
  condition: selection
EOF
```

## convert sigma
```bash
# convert
## sebelum itu kita harus tau target, dan pipelinenya dulu
sigma plugin list --plugin-type backend
sigma list pipelines <nama_plugin>

## splunk
sigma convert -t splunk rules/local.yml -p splunk_windows

## Elasticsearch
sigma convert -t lucene rules/local.yml
sigma convert -t eql rules/local.yml
sigma convert -t elastalert rules/local.yml

sigma convert -t lucene -p ecs_windows rules/local.yml
```