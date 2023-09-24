# -*- coding: utf-8 -*-

# Copyright (c) 2022, Håkon Lerring
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


def get_consul_url(configuration):
    return '%s://%s:%s/v1' % (configuration.scheme,
                              configuration.host, configuration.port)


def get_auth_headers(configuration):
    if configuration.token is None:
        return {}
    else:
        return {'X-Consul-Token': configuration.token}


class RequestError(Exception):
    pass


def handle_consul_response_error(response):
    if 400 <= response.status_code < 600:
        raise RequestError('%d %s' % (response.status_code, response.content))


class ConsulVersion:
    def __init__(self, version_string):
        split = version_string.split('.')
        self.major = split[0]
        self.minor = split[1]
        self.patch = split[2]

    def __ge__(self, other):
        return int(self.major + self.minor +
                   self.patch) >= int(other.major + other.minor + other.patch)

    def __le__(self, other):
        return int(self.major + self.minor +
                   self.patch) <= int(other.major + other.minor + other.patch)

class ServiceIdentity:
    def __init__(self, input):
        if not isinstance(input, dict) or 'name' not in input:
            raise ValueError(
                "Each element of service_identities must be a dict with the keys name and optionally datacenters")
        self.name = input["name"]
        self.datacenters = input["datacenters"] if "datacenters" in input else None

    def to_dict(self):
        return {
            "ServiceName": self.name,
            "Datacenters": self.datacenters
        }


class NodeIdentity:
    def __init__(self, input):
        if not isinstance(input, dict) or 'name' not in input:
            raise ValueError(
                "Each element of node_identities must be a dict with the keys name and optionally datacenter")
        self.name = input["name"]
        self.datacenter = input["datacenter"] if "datacenter" in input else None

    def to_dict(self):
        return {
            "NodeName": self.name,
            "Datacenter": self.datacenter
        }


class RoleLink:
    def __init__(self, dict):
        self.id = dict.get("id", None)
        self.name = dict.get("name", None)

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name
        }


class PolicyLink:
    def __init__(self, dict):
        self.id = dict.get("id", None)
        self.name = dict.get("name", None)

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name
        }
