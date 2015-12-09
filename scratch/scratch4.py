#!/usr/bin/env python
import yaml

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


a = {'key': 'I love you'}

with open('test.yaml', 'w') as f:
    f.write(yaml.dump(a, default_flow_style=False))
