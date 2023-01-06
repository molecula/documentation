# Local build

Two methods are available to run a local build of the featurebase-docs site.

* Docker
* Virtual Machine

WARNING: We **do not** recommend local installation of system files because of version conflicts with pre-existing application dependencies.

## Before you begin

* Setup Git (including user name and password)
* Add SSH keys to your GitHub account
* Request Read/Write access to `featurebase/featurebase-docs` if you do not already have it
* Clone repository

## Docker

### Before you begin

* Install [Docker Desktop](https://www.docker.com/get-started/)
* [Learn about Docker build](https://docs.docker.com/engine/reference/commandline/build/){:target="_blank"}

### Load Docker container from Dockerfile

Perform this action once.

`Dockerfile` and `docker-compose.yml` can be found in the root directory.

NOTE: This process can take some time if starting from scratch or after executing `docker system prune -a`

1. Use the Dockerfile to load the container

| OS | CLI | Command
|---|---|
| Windows | Powershell | `Get-Content Dockerfile | docker build -` |
| Linux | Bash | `$ docker build - < Dockerfile` |
| Mac | Terminal | `$ docker build - < Dockerfile` |

### Serve the container

```
docker compose up serve
```

### View local site

To view the local site on port `4000` head to:

http://localhost:4000/ or
http://<local-ip>:4000

## Editing files

You an edit the files in the repo and refresh the page to view changes immediately.

## Virtual Machine

The repository has been tested on Ubuntu and Linux Mint but will most likely work on other Linux variants.

### Before you begin

The VM requires:
* Minimum 16GB memory
* Network connection
* Git setup as above
* SSH keys setup as above
* Read/Write access to featurebase-docs

### Install Ruby, Bundler and Jekyll

Minimum versions are found in `gemfile` and `gemfile.lock`

TIP: In my experience you can use the [standard jekyll setup instructions for your OS](https://jekyllrb.com/docs/installation/#requirements)

### Installing dependencies for the first time

Run bundler on the command line to install dependencies

```

uername@virtualmachine
$ bundle

```

### Serving the site

This method allows you to make changes to site files and view changes.

NOTE: Changes to `_config.yml` requires a restart.

Run this command:

```
bundle exec jekyll serve
```
