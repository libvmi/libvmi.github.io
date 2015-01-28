---
layout: plain
---

Stable Releases
---------------
LibVMI releases are shipped when a new set of features has reached
sufficient stability. Starting with the 0.12 release, we will begin
backporting bug fixes and providing maintenance releases, as needed.

Stable releases can be verfied using GnuPG and key [3045D1E5][gpgkey]
from the [MIT PGP public key server][keyserver].

<table class="table table-hover">
<tr>
  <th>Date</th>
  <th>Version</th>
  <th>Release</th>
  <th>Signature</th>
</tr>
{% for release in site.data.releases %}
<tr>
  <td>{{ release.date }}</td>
  <td>{{ release.version }}</td>
  <td><a href="https://github.com/libvmi/libvmi/archive/{{ release.filename   }}">libvmi-{{ release.version }}.tar.gz</a></td>
  <td><a href="/assets/sig/libvmi-{{ release.version }}.tar.gz.asc">libvmi-{{ release.version }}.tar.gz.asc</a></td>
</tr>
{% endfor %}
</table>

Development Code
----------------
Developers seeking the latest experimental features may want to work from the
development version available in the [LibVMI repository on Github][github].


[github]: https://github.com/libvmi/libvmi
[gpgkey]: https://pgp.mit.edu/pks/lookup?op=get&search=0x114D5DF83045D1E5
[keyserver]: https://pgp.mit.edu
