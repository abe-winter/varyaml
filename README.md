## varyaml

This is a straight-up wrapper of pyyamml **but** it can also do this:

```
db:
    host: database.internal.dns
    port: $DBPORT
    username: $DBUSER
    password: rosebud
    # todo: make password an env arg for security? nah
```

When you load this file with varyaml, DBPORT and DBUSER will be read from your environment and the loader will **crash** (yes) if they're missing.

Why is this important? Orchestration frameworks prefer to pass args in as env vars, but programs are easier to understand if they have config files. This tool lets you have both.

### Defaults

If there's a top-level varyaml key, you can specify defaults (i.e. make the environment var optional).

(todo: what if the top-level object isn't a dictionary?)

The special string value '__omit__' says to pop the key if there's no env arg.

```
db:
    port: $DBPORT
    username: $DBUSER
    database: $DBNAME
varyaml:
    defaults:
        DBPORT: 5432
        DBNAME: __omit__
```

### Python versions & release status

This is in beta release as of June 2017. The test suite is limited and not informed by any real-world snafus.

I think pyyaml doesn't support yaml aliases, but if it does is there a possibility of circular references? If that happens `varyaml.process` (called by `load`) will hang.

Tested on py3.5. Probably works on anything recent that supports pyyaml.

### Contributions

High-quality technical blogposts on using this in the wild (a) will be appreciated and (b) may be linked to from this spot if they're really good.

I'm not sure if I need env var redirection (i.e. `DEFAULT_HOST=localhost DBHOST='$DEFAULT_HOST'`). If you have a use case and you want to add the feature (disabled by default), send a pull request with tests.

Is there a need for integer casting (i.e. for ports)? I assume not but if you need it, send a pull request.
