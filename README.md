# OBJ2CFA
This is the implementation of our POPL'22 paper "Return of CFA: Call-Site Sensitivity Can Be Superior to Object Sensitivity Even for Object-Oriented Programs". It challenges the commonly-accepted wisdom in static analysis that object sensitivity is superior to call-site sensitivity for object-oriented programs. Our paper claims that call-site sensitivity is generally a superior context abstraction because it is practically possible to transform object sensitivity into more precise call-site sensitivity. To support this claim, we present a technique, called OBJ2CFA, for transforming given object sensitivity into more precise, call-site-sensitivity. We implemented OBJ2CFA in Doop and used it to derive a new call-site-sensitive analysis from a state-of-the-art object-sensitive pointer analysis.

#### Table of Contents

* [Getting-Started Guide](#Getting-Started-Guide)
  * [Requirements](#Requirements)
  * [Vagrant Box](#Vagrant-Box)
  * [Setup Instruction](#Setup-Instruction)
  * [Verifying Installation](#Verifying-Installation)
* [Artifact](#Artfact)

## Getting-Started Guide

## Requirements

- A 64-bit Ubuntu system
- A Java 8 distribution

Please set your `JAVA_HOME` environment variable to point to your Java installation directory.

### Vagrant Box
We provide a Vagrant Box to easily setup environment for our tool. The Vagrantfile is supplied to build a box with Ubuntu 18.04 LTS running on VirtualBox machine. For installation and detailed manual of it, read [Vagrant](https://vagrantup.com).


You can customize virtual machine, depending on your system spec. The following part of `Vagrantfile` can be modified for such purpose

```ruby
Vagrant.configure("2") do |config|
  # ...
  config.vm.box = "ubuntu/bionic64"
  # ...
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"
  # ...
  end  
  # ...
end
```

A command below from the project directory (where `Vagrantfile` is located) creates a virtual machine and installs some dependencies, which may be better to be installed on system (e.g., java 8). If you want to configure it, see `bootstrap.sh`. 

```sh
vagrant up
```

Now you can `ssh` the Ubuntu 18.04 VirtualBox machine and use our tool. It's easy to halt the machine after exitting ssh session.

```sh
vagrant ssh

# halt the machine after exitting ssh
vagrant halt
```

For running doop, Datalog engine need to be additionally installed. Please visit [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html) and download `.deb` for Ubuntu 18.04 LTS (e.g., `pa-datalog_0.5-1bionic.deb`) and follow the instructions.

For example, install `.deb` package:

```sh
sudo dpkg -i pa-datalog_0.5-1bionic.deb
sudo apt-get install -f
```

Set `JAVA_HOME` to an appropriate path:
```sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```
Source `lb-env-bin.sh` script:
```sh
source /opt/lb/pa-datalog/lb-env-bin.sh
```

Now, you can run doop. Please follow the [Verifying Installation](#Verifying-Installation).


### Installing Datalog Engine

Running Doop Framework requires Datalog engine that computes new facts from initial facts and inference rules given by Doop framework. Please execute the following command in your terminal to make sure your system has one of them.

```
$ bloxbatch -help
```

If you need to install Datalog engine, please visit [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html). The page provides a deb package of an academic version of LogicBlox v3 engine. (We recommend `.deb` package installation)

### Verifying Installation

Verifying installation is very easy. First, move to `doop/` folder. Then, you can check the installation by running the following command:

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

### Running Doop
First, move to `doop/` foler. The command below runs Doop:

```
$ ./run -jre1.6 <analysis> <pgm.jar>
```

The analyses can be found in `doop/logic` folder. For example, you can analyze a program `foo.jar` with 2-object-sensitivity with the following command:

```
$ ./run -jre1.6 2-object-sensitive+heap foo.jar
```

 
### Running Doop with 1callH+SL
If you want to analyze a program with our state-of-the-art call-site sensitivity (e.g., 1callH+SL in our paper), use the following command:
 
```
$ ./run -jre1.6 1-tunneled-call-site-sensitive+heap <pgm.jar>
```

### Analyzing a Program with a Customized Tunneling Abstraction
You can also analyze a program with your own tunneling abstraction. To do so, you need to modify `TunnelingAbstraction.facts` file. The file includes a set of invocation sites that will be tunneled during the analysis. After the modification, type:

```
$ ./run -jre1.6 1-call-site-sensitive+heap+tunneling <pgm.jar>
```

For example, if you modify `TunnelingAbstraction.facts` to include empty set (e.g., `$ echo "" > TunnelingAbstraction.facts`), the program will be analyzed under conventional 1-call-site sensitivity without context tunneling. You can also run 1-object sensitivity with your tunneling abstraction by typing the following command:

```
$ ./run -jre1.6 1-object-sensitive+heap+tunneling <pgm.jar>
```


### Artifact (VirtualBox Image)
We've archived a ready-to-run version of our implementation in zenodo ([Link](https://zenodo.org/record/5652640#.YYjZq3UzYwY)).

