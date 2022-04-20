# pushpy-start

# Description

This is a template project for creating new [PushPy](https://github.com/briangu/pushpy) Raft-based Python application server deployments.  Each deployment is different will likely have different boot and configuration setups.  Base Docker images are provided to simplify customization.

# Layout

The key components are the 

* boot - the boot python module that initializes pushpy
* conf - the config setups for different pushpy nodes

The docker image scripts are setup to use these two directories when populating the image.

## Deploy

The deploy directory has two examples of deployment

* bare
* simple-cluster

The bare example shows how to deploy pushpy without containers which can be useful on small machines (e.g. Graviton).
The simple-cluster shows how to deploy using containers and emphasizes the bootstrapping style where there is a primary node and secondary nodes are launched from it.

## Docker

The docker directory shows how to create custom pushpy images that are derived from the base pushpy image.  There are two example images

* python3.8
* tensorflow

These are obviously just different deployments, with the tensorflow image being optimized for machine-learning.

# Quickstart

Quickstart examples to bring up a pushpy cluster using two different strategies.

## Deploy Docker

```bash
# terminal 1
$ source setenv.sh
$ cd deploy/simple-cluster
$ ./primary.sh python3.8 up 

# terminal 2
$ source setenv.sh
$ cd deploy/simple-cluster
$ ./secondary.sh python3.8 up

# terminal 3
$ source setenv.sh
$ cd deploy/simple-cluster
$ ./secondary-2.sh python3.8 up
```

## Deploy bare

```bash
$ source setenv.sh
$ python3 -m venv venv

# terminal 1
$ source venv/bin/activate
$ cd deploy/bare
$ ./run_primary.sh

# terminal 2+
$ source venv/bin/activate
$ cd deploy/bare
$ ./run_secondary.sh

```