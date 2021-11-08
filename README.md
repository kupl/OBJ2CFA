# OBJ2CFA
This is the implementation of our POPL'22 paper "Return of CFA: Call-Site Sensitivity Can Be Superior to Object Sensitivity Even for Object-Oriented Programs". It challenges the commonly-accepted wisdom in static analysis that object sensitivity is superior to call-site sensitivity for object-oriented programs. Our paper claims that call-site sensitivity is generally a superior context abstraction because it is practically possible to transform object sensitivity into more precise call-site sensitivity. To support this claim, we present a technique, called OBJ2CFA, for transforming given object sensitivity into more precise, call-site-sensitivity. We implemented OBJ2CFA in Doop and used it to derive a new call-site-sensitive analysis from a state-of-the-art object-sensitive pointer analysis.

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

### Verifying Installation

Verifying installation is very easy. First, move to "OBJ2CFA/doop/". Then, you can check the installation by running the following command:

```
$ ./run -jre1.6 1-tunneled-call-site-sensitive+heap jars/dacapo/luindex.jar
```

You will see the results as follows:

```
running dacapo benchmark: luindex
...
Pointer analysis START
analysis time: 51.32s
Pointer analysis FINISH
...
var points-to                        250,012 (insens) / 2,930,383 (sens)
reachable casts that may fail        357
call graph edges                     36,578 (insens) / 363,253 (sens)
reachable methods                    7,710 (insens) / 80,760 (sens)
polymorphic virtual call sites       908

```

The results say that

- The program to be analyzed is luindex
- The analysis 51.32 seconds
- The results for the clients (VarPtsTo, #may-fail casts, #call-graph-edges, #reachable-methods, #polymorphic-calls)

