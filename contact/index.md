---
layout: plain
---

Community
---------
There are several ways to reach out to the LibVMI community. Please use
the appropriate option below, based on your needs, rather than contacting
one of the developers directly. This allows us to handle your inquiry 
more efficiently, while also allowing others to benefit from the 
information.

* [Mailing List][mailing_list]: Given that the LibVMI community spans the
  globe, this is the best place for technical discussion. Please use this
  as a place to learn more about LibVMI, ask questions, and help others.

* IRC: Many of the developers can be found on [Freenode][freenode] in
  the #libvmi channel. This is a great place for live discussions,
  simple questions, and collaborative development efforts.

* [Bug Reports][issues]: Any issues discovered with LibVMI should be
  reported through GitHub issues for the LibVMI project. _Security
  issues can be reported to the core team directly through encrypted
  email using [3045D1E5][gpgkey]_.


Core Developers
---------------
<div class="container-fluid">
{% for person in site.data.bios %}
<div class="row">
  <div class="col-md-2">
    <img src="/assets/images/{{ person.image }}" class="img-circle" />
  </div>
  <div class="col-md-10">
    {{ person.description }}
  </div>
</div>
<div class="spacer50"></div>
{% endfor %}
</div>


[mailing_list]: https://groups.google.com/group/vmitools
[freenode]: https://freenode.net/
[issues]: https://github.com/libvmi/libvmi/issues
[gpgkey]: https://pgp.mit.edu/pks/lookup?op=get&search=0x114D5DF83045D1E5
