import yaml

YAMLF = '/mnt/sda1/opt/usr/tmp/test.yaml'
with open(YAMLF) as f:
    YAMLDATA=yaml.load(f)
LOGPATH = YAMLDATA.get('logpath','')
