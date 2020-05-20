# LibVMI Website

Available under [libvmi.com](http://libvmi.com).

## Repository structure

* `source` - default branch with the source code, pull requests/changes should be submitted to this branch;
* `master` - the actual content of the web page; this branch contains static HTML which is automatically generated from `source` and shouldn't be edited directly, see [.github/workflows/main.yml](https://github.com/libvmi/libvmi.github.io/blob/source/.github/workflows/main.yml) for reference.

## Generated API docs

The API documentation at [libvmi.com/api/](http://libvmi.com/api/) is generated automatically in such way:

1. Latest version of `libvmi/libvmi` branch `master` is fetched.
2. Doxygen is ran in `libvmi/` directory (the one which contains `libvmi.h` and other exported headers).
3. Doxygen's XML output file `libvmi_8h.xml` is parsed by [parse-doxygen-xml.py](https://github.com/libvmi/libvmi.github.io/blob/source/parse-doxygen-xml.py) script from this repository.
4. The output of the above script is saved under `api/index.html` file.
