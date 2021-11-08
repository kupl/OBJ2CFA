# OBJ2CFA


#### Table of Contents

* [Getting-Started Guide](#Getting-Started-Guide)
  * [Requirements](#Requirements)
  * [Setup Instruction](#Setup-Instruction)
  * [Verifying Installation](#Verifying-Installation)
* [Artifact](#Artfact)

## Getting-Started Guide

## Requirements

- A 64-bit Ubuntu system
- A Java 8 distribution
- A Python 2.x interpreter

Please set your `JAVA_HOME` environment variable to point to your Java installation directory.

### Setup Instruction

### Installing Datalog Engine

Running Doop Framework requires Datalog engine that computes new facts from initial facts and inference rules given by Doop framework. Please execute the following command in your terminal to make sure your system has one of them.

```
$ bloxbatch -help
```

If you need to install Datalog engine, please visit [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html). The page provides a deb package of an academic version of LogicBlox v3 engine. (We recommend `.deb` package installation)
