---
layout: plain
---

Introduction to LibVMI
======================


About LibVMI
------------
LibVMI is an introspection library focused on reading and writing
memory from virtual machines (VMs). For convienence, LibVMI also
provides functions for accessing CPU registers, pausing and unpausing
a VM, printing binary data, and more. LibVMI is designed to work
across multiple virtualization platforms. LibVMI currently supports
VMs running in either Xen or KVM. LibVMI also supports reading
physical memory snapshots when saved as a file.

Features
--------

* Works with Xen (v3.x through 4.1) and KVM (with patch against QEMU-KVM 0.14)

* Works with physical memory snapshots saved in a file (e.g., VMWare snapshots)

* Native API in C (LibVMI) and a feature complete wrapper API in Python (PyVMI)

* [Volatility][1] address space plugin enabled running Volatility on a live VM

* Works with 32-bit and 64-bit Windows and Linux guests (64-bit support
  in version 0.8 and newer)

* Read and write arbitrary data from and to memory

* Access memory using physical addresses, virtual addresses, or kernel symbols

* Parse kernel symbols dynamically from running Windows kernel while also
  providing access to symbols from the KPCR table

* Load Linux kernel symbols from system map file

* Expose useful address translation functions through API functions to
  resolve kernel symbols to a virtual address or translate a kernel or
  user virtual address into a physical address

* Pause/unpause the VM through an API function

* Write your introspection code once and have it work across multiple
  virtualization platforms

Brief Technical Details
-----------------------
Memory introspection is useful because it allows you to monitor (read
memory values) and control (write (present tense) memory values) an
operating system from a protected location. But this is a difficult task.

Essentially, memory introspection is the process of viewing the memory
of one virtual machine from a different virtual machine. On the surface,
this sounds rather simple. In fact, Xen even provides a function to
facilitate this type of memory access (although KVM does not).

What makes memory introspection difficult, and where LibVMI comes in, is
the semantic gap between the two virtual machines. For example, to look
up virtual addresses, LibVMI must walk the page tables inside the user
virtual machine; however, in order to walk these page tables, LibVMI
must first know where the page directory is located. And this location
depends on the process address space you are viewing.

The more you think about the process of memory introspection, the clearer
the complexities become. One must know a lot of details about the user
operating system in order to build these higher levels of abstraction.
LibVMI fills this knowledge gap.

Previous research has shown that introspection can be used for a wide
variety of security applications, but more ideas are coming out all the
time. Using LibVMI, you can quickly experiment with your new ideas and
help advance this new and exciting research direction.

![Introspection Detail](/assets/images/intro-detail.png)

History
-------
LibVMI grew out of the XenAccess Project. While XenAccess was focused exclusively on Xen, LibVMI aims to be extensible to a wide variety of
virtualization platforms. Furthermore, LibVMI provides a more intuitive
API by transparently handling reads and writes across memory page
boundaries. You can read more details about XenAccess in our research
paper from ACSAC 2007 titled
[Secure and Flexible Monitoring of Virtual Machines][2].


[1]: http://www.volatilityfoundation.org/
[2]: http://www.acsac.org/2007/abstracts/138.html
