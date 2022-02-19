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

A command below from the project directory (where `Vagrantfile` is located) creates a virtual machine and installs some dependencies, which may be better to be installed on system. If you want to configure it, see `bootstrap.sh`.

```sh
vagrant up
```

Next, you should install main `dd-klee`. This proedure is done with `provision`, the subcommand of `vagrant`. Provisioning with `klee_deps` builds some dependencies (e.g. STP) from source. This is done by the script `install_deps.sh`. Provisioning with `klee` builds our extension of KLEE. The script `install_klee.sh` is used and it includes `cmake` usage described in the section [From Source](#From-Source).

```sh
vagrant provision --with-provision klee_deps,klee
```

Now you can `ssh` the Ubuntu 18.04 VirtualBox machine and use our tool. It's easy to halt the machine after exitting ssh session.

```sh
vagrant ssh

# halt the machine after exitting ssh
vagrant halt
```

If you've done `vagrant up` once, it is not necessary to update and install dependent softwares (by `bootstrap.sh`) every time you run the machine. Then, the option  `--no-provision` is useful to power on the machine quickly.

```sh
vagrant up --no-provision
```





### Installing Datalog Engine

Running Doop Framework requires Datalog engine that computes new facts from initial facts and inference rules given by Doop framework. Please execute the following command in your terminal to make sure your system has one of them.

```
$ bloxbatch -help
```

If you need to install Datalog engine, please visit [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html). The page provides a deb package of an academic version of LogicBlox v3 engine. (We recommend `.deb` package installation)

### Verifying Installation

Verifying installation is very easy. First, move to 'doop/' folder. Then, you can check the installation by running the following command:

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

The analyses can be found in 'doop/logic' folder. For example, you can analyze a program `foo.jar` with 2-object-sensitivity with the following command:

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

