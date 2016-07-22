---
layout: plain
---

LibVMI Installation Instructions
================================


Introduction
------------
LibVMI is designed for looking at 32-bit or 64-bit x86 virtual machines
running on Xen or KVM. It also works with physical memory snapshots saved
to a file. LibVMI should work with all recent Xen versions (3.x through
4.1), with KVM using a patched version of QEMU-KVM or the GDB interface,
and with any physical memory snapshot. Please report your success and
problems using the contact information for the VMI Tools project so that
we can continue to make this a better tool for everyone. You can get the
latest released version of LibVMI from the download section of this website.

Building LibVMI
---------------
For detailed instructions, please see the README file included with your
LibVMI release. The instructions below provide a general overview of the
LibVMI installation process. Before compiling LibVMI, make sure that you
have a standard development environment installed including gcc, make,
autoconf, etc. You will also need the follow dependencies (note, you can
build LibVMI without support for one of its virtualization platforms if
you would rather not install all of the dependencies for that platform):

* (Xen only) libxc

* (Xen only) libxenstore

* (KVM only) libvirt

* yacc or bison

* lex or flex

* glib version 2.16 or newer

LibVMI uses the standard GNU build system. To compile the library, follow
the steps shown below:

```
./autogen.sh
./configure
make
```

Note that you can specify options to the configure script to specify,
for example, the installation location. Of note is the "--disable-xen"
and "--disable-kvm" options, which allow you to build LibVMI without
support for Xen or KVM, respectively. If the configure script doesn’t
find a library that is required for only one virtualization platform,
then it will automatically disable the associated virtualization platform.
The results of configure are displayed to stdout so you can verify that
everything is as you intended before proceeding with the compilation.
For a complete list of configure options, run:

```
./configure --help
```

Installing LibVMI
-----------------
Installation is optional. This is useful if you will be developing code
to use the LibVMI library. However, if you are just running the examples,
then there is no need to do an installation. If you choose to install
LibVMI, you can do it using the steps shown below:

```
su -
make install
ldconfig
exit
```

Configuring LibVMI
------------------
In order to work properly, LibVMI requires that you install a configuration
file into either $HOME/etc/libvmi.conf or /etc/libvmi.conf. This file has
a set of entries for each virtual machine or memory image that LibVMI will
access. These entries specify things such as the OS type (e.g., Linux or
Windows), the location of symbolic information, and offsets used to access
data within the virtual machine or memory image. The file format is
relatively straightforward. The generic format is shown below:

```
<VM Name or Filename> {
    <key> = <value>;
    <key> = <value>;
}
```

The VM name is what appears when you use the "xm list," "xl list,"
or "virsh list" commands. The filename is the filename of the memory
image without the entire path. There are 9 different keys available
for use. The ostype is used by both Linux and Windows targets. The
sysmap is only used for Linux targets. The others specify offsets such
that the linux\_\* values are required for Linux and the win\_\* values
are required for Windows. The available keys are listed below:

* ostype Linux or Windows guests are supported.

* sysmap The path to the System.map file for the VM.  Note that this
  file must be copied into the dom0 or host VM from the domU or guest
  VM so that LibVMI can access it.

* linux\_tasks The number of bytes (offset) from the start of the struct
  until task\_struct->tasks from linux/sched.h in the target’s kernel.

* linux\_mm Offset to task\_struct->mm.

* linux\_pid Offset to task\_struct->pid.

* linux\_pgd Offset to mm\_struct->pgd.

* win\_tasks Offset to EPROCESS->ActiveProcessLinks.

* win\_pdbase Offset to EPROCESS->Pcb->DirectoryTableBase.

* win\_pid Offset to EPROCESS->UniqueProcessId.

Instructions and scripts helpful for determining these offsets for a
specific guest can be found in the libvmi package. The tools for Linux
guests are in libvmi/tools/linux-offset-finder and Windows guests are
in libvmi/tools/windows-offset-finder.

All of the offsets can be specified in either hex or decimal. For hex,
the number should be preceded with a "0x". An example configuration
file is shown below:

```
Fedora-HVM {
    sysmap      = "/boot/System.map-2.6.18-1.2798.fc6";
    ostype      = "Linux";
    linux_tasks = 268;
    linux_mm    = 276;
    linux_pid   = 312;
    linux_pgd   = 40;
}

WinXPSP2 {
    ostype      = "Windows";
    win_tasks   = 0x88;
    win_pdbase  = 0x18;
    win_pid     = 0x84;
}
```

You can specify as many targets as you wish in this configuration
file. When you are done creating this file, it must be saved to either
$HOME/etc/libvmi.conf or /etc/libvmi.conf. With the configuration file
in place, you are now ready to start using LibVMI.

Debugging
---------
LibVMI includes the ability to show debugging output. This output is
very verbose, but may be useful when tracking down bugs in your
application or in LibVMI itself. To enable the debug output, uncomment
the VMI\_DEBUG variable near the top of the `libvmi/debug.h` file. After
uncommenting this variable, you will need to recompile LibVMI (and,
optionally, reinstall LibVMI). With the debug output enabled, you will
see lots of information on stdout about LibVMI’s operation.

If you are requesting help from the developers, please send the debug
output -- preferably a full debug trace attached to your email or issue
ticket -- along with your question as it will be easier to diagnose your
problem this way.

When troubleshooting your application, it is best to be able to see what
is going on. If you think that the problem is within LibVMI, you can try
enabling the debug output to identify the problem. If you think that you
have found a bug in LibVMI, please send an email with this debug output
and a description of the bug to the mailing list.

If you want to see the memory maping by your application, consider using
the vmi\_print\_hex function. This function allows you to easily print the
hex and ascii values from a region of memory to stdout, which can often
simplify debugging.
