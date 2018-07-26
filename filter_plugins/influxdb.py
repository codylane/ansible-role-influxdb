#!/usr/bin/env python
# flake8: noqa
# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals
from ansible.module_utils import six

import re


def parse_influxdb_config_value(v):
    if isinstance(v, six.string_types) and re.match(r'^[\d]+$', v):
        return v

    if isinstance(v, bool):
        return str(v).lower()

    if isinstance(v, (int, float, list)):
        return v

    # if we get here just return a string
    return '{!s}'.format(v)


def build_influxdb_config_section(config, section, show_header=True):
    result = []

    if config:
        if show_header:
            result.append("[{section}]".format(section=section))

        keys = sorted(config.keys())

        for key in keys:
            value = config[key]
            val = parse_influxdb_config_value(value)
            result.append("{key} = {val}".format(key=key, val=val))

    if not result:
        return ''

    return '\n'.join(result)


def build_influxdb_sub_config_section(config, section):
    result = []

    if config:
        result.append("[[{section}]]".format(section=section))
        result.append(build_influxdb_config_section(config, section=section, show_header=False))

    if not result:
        return ''

    return '\n'.join(result)


class FilterModule(object):
    """Ansible influxdb influxdb.conf filters

    """

    def filters(self):
        return {
            'parse_influxdb_config_value': parse_influxdb_config_value,
            'build_influxdb_config_section': build_influxdb_config_section,
            'build_influxdb_sub_config_section': build_influxdb_sub_config_section,
        }
