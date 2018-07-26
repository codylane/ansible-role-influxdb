influxdb
=========

Installs and configures open source InfluxDB.

Requirements
------------

None

Role Variables
--------------

# Defaults

* See the [defaults](../defaults/main.yml)

#### `influxdb_version`

 * The version of InfluxDB to install.  Default: `1.6.0`

#### `influxdb_config_file`

 * The full path to the influxdb.conf. Default: `/etc/influxdb/influxdb.conf`

#### `influxdb_error_log_file`

* The full path to the stderr log file. Default: `/var/log/influxdb/influxd-error.log`

#### `influxdb_stdout_log_file`

* The full path to the stdout log file. Default: `/var/log/influxdb/influxd-stdout.log`

#### `influxdb_service`

* The service name for influxdb. Default: `influxdb`

#### `influxdb_startup_config_file`

* The full path to the startup config file. Default: `/etc/default/influxdb`

#### `influxdb_log_owner`

* The default user that has write access to the stdout and stderr logs. Default. `influxdb`

#### `influxdb_log_group`

* The default group that has write access to the stdout and stderr logs. Default: `influxdb`

#### `influxdb_conf`

* A dictionary hash for influxdb.conf settings, where a section is a dictionary key.

```
influxdb_config:
  global:
    'bind-address': '"127.0.0.1:8088"'
```

* That would create a section called `global` with the value `"127.0.0.1:8088"`.
* NOTE: Any value that requires quotes like above should always look like this.
* You can find the rest of the settings and what they mean on the [InfluxDBdocs](https://docs.influxdata.com/influxdb/v1.6/administration/config/#configuration-file-settings)

#### `influxdb_yum_repo`

* A hash of keys for configuring the internal/external yum repo for installing InfluxDB via a yum
* The default is:

```
influxdb_yum_repo:
  state: present
  enabled: true
  baseurl: 'https://repos.influxdata.com/rhel/$releasever/$basearch/stable'
  gpgcheck: true
  gpgkey: 'https://repos.influxdata.com/influxdb.key'
```

#### `manage_install`

* When `true` Ansible will attempt to install InfluxDB via the configured package manager. Default: `true`

#### `manage_repos`

* When `true` Ansible will attempt to install/configure the InfluxDB repository for the supported OS. Default: `true`

#### `manage_service`

* When `true` Ansible will attempt to manage/configure the InfluxDB service. Default: `true`

Example Playbook
----------------

* Installs, configures, and starts the influxdb service using all the defaults.

```
    - hosts: servers
      roles:
         - role: codylane.influxdb
```

Example playbook with customized defaults (RHEL) only.

```
    - hosts: servers
      roles:
         - role: codylane.influxdb
           influxdb_yum_repo:
             state: present
             enabled: true
             baseurl: 'https://myspecial.snowflake.repo/influxdb/$releasever/$basearch/stable'
             gpgcheck: false
             gpgkey: 'https://repos.influxdata.com/influxdb.key'
```


License
-------

MIT

Author Information
------------------

* Cody Lane
