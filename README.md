## varyaml

Ever wanted to reference environment arguments inside your config file?

```yaml
db:
    host: database.internal.dns
    port: $DBPORT
    username: $DBUSER
    password: rosebud
    # todo: make password an env arg for security? nah
```

When you load this file with varyaml, DBPORT and DBUSER will be read from your environment and the loader will **crash** (yes) if they're missing.

Why is this important? Orchestration frameworks prefer to pass args in as env vars, but programs are easier to understand if they have config files. This tool lets you have both.

### Usage

```python
import varyaml
varyaml.load('{}')
# or
varyaml.load(open('config.yml'))
```

### Installation

```bash
pip install varyaml
# or
pip install git+git://github.com/abe-winter/varyaml
```

### Reading vars from disk (secrets)

Some orchestration frameworks put secrets on disk. You can get at them like this:

```yaml
db:
    password: $DB_PASS
varyaml:
    path: /run/secrets
```

In this example, varyaml will check first for an environment var named DB_PASS, then it will read the contents /run/secrets/DB_PASS if the file exists, then it will go to defaults (not provided in this sample), then crash if not found.

### Default values

You can specify defaults (i.e. make the environment var optional).

(todo: what if the top-level object isn't a dictionary?)

The special string value `__omit__` says to pop the key if not found.

```yaml
db:
    port: $DBPORT
    username: $DBUSER
    database: $DBNAME
varyaml:
    defaults:
        DBPORT: 5432
        DBNAME: __omit__
    path: /run/secrets
```

### Environment overrides & merging

The parser takes an `overrides` section which can be used to set different defaults for different environments where your code runs. The order of precedence is:

* env vars take highest priority
* then on-disk in varyaml.path
* then check for overrides in the current env
* then look in the defaults section

Overrides are controlled with environment vars. Example (controlled with `APP_ENV`):

```yaml
db:
    host: $DBHOST
varyaml:
    overrides:
    - __filter__: {APP_ENV: prod}
      DBHOST: managed-db.cloudhost.com
    # note: these are 'or' conditions. (env=staging or env=test)
    - __filter__: {APP_ENV: staging, APP_ENV: test}
      DBHOST: db.local
```

There's a working example in [`test_overrides` in the test suite](https://github.com/abe-winter/varyaml/search?q=test_overrides).

Design guidance for overrides:

* Put per-environment overrides in your checked-in config file
* Except anything that needs to be changed a lot, which you should make an env var or fetch from a live config system
* And except secrets, which you should pass as environment vars or on disk

### Python versions & release status

This is in beta release as of June 2017. The test suite is limited and not informed by any real-world snafus.

I think pyyaml doesn't support yaml aliases, but if it does is there a possibility of circular references? If that happens `varyaml.process` (called by `load`) will hang.

Tested on py3.5. Probably works on anything recent that supports pyyaml.

### Contributions

* Blog posts on using this in the wild (a) will be appreciated and (b) may be linked to from this spot if they're good.
* I'm not sure if I need env var redirection (i.e. `DEFAULT_HOST=localhost DBHOST='$DEFAULT_HOST'`). If you have a use case and you want to add the feature (disabled by default), send a pull request with tests.
* Escaping for dollar signs in config values (currently they're always converted to environment vars)
* Is there a need for integer casting (i.e. for ports)? I assume not but if you need it, send a pull request.
