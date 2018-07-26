# coding: utf-8
# flake8: noqa
from __future__ import absolute_import
from __future__ import unicode_literals

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_influxdb_repo_is_installed(host):
    influxdb_repo = host.file('/etc/yum.repos.d/influxdb.repo')

    expected_content = '''[influxdb]
baseurl = https://repos.influxdata.com/rhel/$releasever/$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
name = influxdb-rhel

'''

    assert influxdb_repo.exists
    assert influxdb_repo.is_file
    assert influxdb_repo.user == 'root'
    assert influxdb_repo.group == 'root'
    assert influxdb_repo.mode == 0o0644
    assert influxdb_repo.content_string.strip() == expected_content.strip()


def test_influxdb_is_installed(host):
    influxdb = host.package('influxdb')

    assert influxdb.is_installed
    assert influxdb.version == '1.6.0'


def test_influxdb_service_is_running_and_enabled(host):
    influxdb = host.service('influxdb')

    assert influxdb.is_running
    assert influxdb.is_enabled


def test_etc_influxdb_config_exists(host):
    influxdb = host.file('/etc/influxdb/influxdb.conf')
    expected_content = '''# This config file is managed by Ansible

# GLOBAL configuration options
bind-address = "127.0.0.1:8088"
reporting-disabled = true

###
### [meta]
###
### Controls the parameters for the Raft consensus group that stores metadata
### about the InfluxDB cluster.
###
[meta]
dir = "/var/lib/influxdb/meta"
logging-enabled = true
retention-autocreate = true

###
### [data]
###
### Controls where the actual shard data for InfluxDB lives and how it is
### flushed from the WAL. "dir" may need to be changed to a suitable place
### for your system, but the WAL settings are an advanced configuration. The
### defaults should work for most systems.
###
[data]
cache-max-memory-size = "1g"
cache-snapshot-memory-size = "25m"
cache-snapshot-write-cold-duration = "10m"
compact-full-write-cold-duration = "4h"
dir = "/var/lib/influxdb/data"
index-version = "inmem"
max-concurrent-compactions = 0
max-index-log-file-size = "1m"
max-series-per-database = 1000000
max-values-per-tag = 100000
query-log-enabled = true
trace-logging-enabled = false
wal-dir = "/var/lib/influxdb/wal"
wal-fsync-delay = "0s"

###
### [coordinator]
###
### Controls the clustering service configuration.
###
[coordinator]
log-queries-after = "0s"
max-concurrent-queries = 0
max-select-buckets = 0
max-select-point = 0
max-select-series = 0
query-timeout = "0s"
write-timeout = "10s"

###
### [retention]
###
### Controls the enforcement of retention policies for evicting old data.
###
[retention]
check-interval = "30m"
enabled = true

###
### [shard-precreation]
###
### Controls the precreation of shards, so they are available before data arrives.
### Only shards that, after creation, will have both a start- and end-time in the
### future, will ever be created. Shards are never precreated that would be wholly
### or partially in the past.
[shard-precreation]
advance-period = "30m"
check-interval = "10m"
enabled = true

###
### Controls the system self-monitoring, statistics and diagnostics.
###
### The internal database for monitoring data is created automatically if
### if it does not already exist. The target retention within this database
### is called 'monitor' and is also created with a retention period of 7 days
### and a replication factor of 1, if it does not exist. In all cases the
### this retention policy is configured as the default for the database.
[monitor]
store-database = "_internal"
store-enabled = true
store-interval = "10s"

###
### [http]
###
### Controls how the HTTP endpoints are configured. These are the primary
### mechanism for getting data into and out of InfluxDB.
###
[http]
access-log-path = ""
auth-enabled = false
bind-address = ":8086"
bind-socket = "/var/run/influxdb.sock"
debug-pprof-enabled = false
enabled = true
enqueued-write-timeout = 0
https-certificate = "/etc/ssl/influxdb.pem"
https-enabled = false
https-private-key = ""
log-enabled = true
max-body-size = 25000000
max-concurrent-write-limit = 0
max-connection-limit = 0
max-enqueued-write-limit = 0
max-row-limit = 0
pprof-enabled = true
realm = "InfluxDB"
shared-secret = ""
suppress-write-log = false
unix-socket-enabled = false
write-tracing = false

###
### [ifql]
###
### Configures the ifql RPC API.
###
[ifql]
bind-address = ":8082"
enabled = true
log-enabled = true

###
### [logging]
###
### Controls how the logger emits logs to the output.
###
[logging]
format = "auto"
level = "info"
suppress-logo = false

###
### [subscriber]
###
### Controls the subscriptions, which can be used to fork a copy of all data
### received by the InfluxDB host.
###
[subscriber]
ca-certs = ""
enabled = true
http-timeout = "30s"
insecure-skip-verify = false
write-buffer-size = 1000
write-concurrency = 40

###
### [[graphite]]
###
### Controls one or many listeners for Graphite data.
###
[[graphite]]
batch-pending = 10
batch-size = 5000
batch-timeout = "1s"
bind-address = ":2003"
consistency-level = "one"
database = "graphite"
enabled = false
protocol = "tcp"
retention-policy = ""
separator = "."
tags = []
templates = []
udp-read-buffer = 0

###
### [collectd]
###
### Controls one or many listeners for collectd data.
###
[[collectd]]
auth-file = "/etc/collectd/auth_file"
batch-pending = 10
batch-size = 5000
batch-timeout = "10s"
bind-address = ":25826"
database = "collectd"
enabled = false
parse-multivalue-plugin = "split"
read-buffer = 0
retention-policy = ""
security-level = "none"
typesdb = "/usr/local/share/collectd"

###
### [opentsdb]
###
### Controls one or many listeners for OpenTSDB data.
###
[[opentsdb]]
batch-pending = 5
batch-size = 1000
batch-timeout = "1s"
bind-address = ":4242"
certificate = "/etc/ssl/influxdb.pem"
consistency-level = "one"
database = "opentsdb"
enabled = false
log-point-errors = true
retention-policy = ""
tls-enabled = false

###
### [[udp]]
###
### Controls the listeners for InfluxDB line protocol data via UDP.
###
[[udp]]
batch-pending = 10
batch-size = 5000
batch-timeout = "1s"
bind-address = ":8089"
database = "udp"
enabled = false
read-buffer = 0
retention-policy = ""

###
### [continuous_queries]
###
### Controls how continuous queries are run within InfluxDB.
###
[continuous_queries]
enabled = true
log-enabled = true
query-stats-enabled = false
run-interval = "1s"'''

    assert influxdb.exists
    assert influxdb.is_file
    assert influxdb.user == 'root'
    assert influxdb.group == 'root'
    assert influxdb.mode == 0o0644
    assert influxdb.content_string.strip() == expected_content


def test_etc_default_influxdb_exists(host):
    config = host.file('/etc/default/influxdb')
    expected_content = '''STDERR="/var/log/influxdb/influxd-error.log"
STDOUT="/var/log/influxdb/influxd-stdout.log"
'''

    assert config.exists
    assert config.is_file
    assert config.user == 'root'
    assert config.group == 'root'
    assert config.content_string.strip() == expected_content.strip()


def test_var_log_influxdb_is_a_directory(host):
    influxdb_dir = host.file('/var/log/influxdb')

    assert influxdb_dir.exists
    assert influxdb_dir.is_directory
    assert influxdb_dir.user == 'influxdb'
    assert influxdb_dir.group == 'influxdb'
    assert influxdb_dir.mode == 0o0755


def test_var_log_influxdb_influxd_error_dot_log_exists(host):
    log_file = host.file('/var/log/influxdb/influxd-error.log')

    assert log_file.exists
    assert log_file.is_file
    assert log_file.user == 'influxdb'
    assert log_file.group == 'influxdb'
    assert log_file.mode == 0o0644


def test_var_log_influxdb_influxd_stdout_dot_log_exists(host):
    log_file = host.file('/var/log/influxdb/influxd-stdout.log')

    assert log_file.exists
    assert log_file.is_file
    assert log_file.user == 'influxdb'
    assert log_file.group == 'influxdb'
    assert log_file.mode == 0o0644
