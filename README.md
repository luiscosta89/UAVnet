# UAVnet
UAV networks simulations with the WSNET simulator and the use of Q-Learning for routing scheme.

# Instructions

To install WSNET and perfom the simulations, follow the instructions:

- Downloading the WSNet source code from the SVN repository by typing the following command:
```
$ svn checkout svn://scm.gforge.inria.fr/svn/wsnet
```
- Compiling the source code by typing the following commands within the WSNet archive directory:
```
$ ./bootstrap && ./configure && make
```
- Installing WSNet by typing the following command (with root privileges) within the WSNet archive
directory:
```
$ sudo make install
```
- You can add the WSNet install directory in the search path by adding the following entries in ~/.bashrc:
```
$ PATH=$PATH:/usr/local/wsnet-2.0/bin
$ export PATH
```
Then, first create and move to the working directory by typing the following commands:
```
$ mkdir $HOME/wsnet-module/
$ cd $HOME/wsnet-module/
```
Second, move the user_models folder to your HOME directory. 
Finally, we have to setup the WSNET_MODDIR environment variable by adding the following lines in
$HOME/.bashrc file:
```
$ export WSNET_MODDIR=$HOME/wsnet-module/lib
```
You must copy qlearningplus.c within the $HOME/wsnet-module/user_modules/ directory.

To compile qlearningplus.c type the following commands:
```
$ ./bootstrap
$ ./configure --prefix=$HOME/wsnet-module --with-wsnet-dir=/usr/local/wsnet-2.0
$ make
```
To install the compiled module, type the following command:
```
$ make install
```
This command will install the module within the directory defined by the configure --prefix option.
In our case, the module is installed within the $HOME/wsnet-module/lib/ directory:
```
$ ls $HOME/wsnet-module/lib/
```
To run the simulation, type the following command:
```
$ wsnet -c qlearningplus.xml
```
