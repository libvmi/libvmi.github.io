#!/usr/bin/env python
import cgi
import sys
import textwrap
import xmltodict

from collections import OrderedDict
from pprint import pprint


def small(text):
    return "<small>{}</small>".format(text)


def front_matter():
    output = textwrap.dedent("""
    ---
    layout: plain
    ---
    """)
    print output.strip()
    print


def _macros_active(memberdef):
    name = str(memberdef['name'])
    if 'param' in memberdef:
        value = ', '.join(x['defname'] for x in memberdef['param'])
        value = "(" + value + ")"
    else:
        try:
            value = str(memberdef['initializer'])
        except KeyError:
            value = ""
    return "{} {}".format(name, value)


def _macros_detail(memberdef):
    try:
        desc = memberdef['detaileddescription']['para']
        if type(desc) is OrderedDict:
            # this is a bit ugly, but the xml parser is
            # stripping out the ref and just leaving two
            # spaces as the only indication of where it
            # should be, so we work with that
            tmp = desc['#text']
            loc = tmp.find('  ') + 1
            desc = tmp[:loc] + desc['ref']['#text'] + tmp[loc:]
        desc = "<p>" + desc + "</p>"
    except (TypeError, KeyError):
        desc = ""

    if 'param' in memberdef:
        desc += "<p><strong>Value</strong><br />"
        value = memberdef['initializer']
        if type(value) is OrderedDict:
            if type(value['ref']) != list:
                values = [value['ref']['#text']]
            else:
                values = [x['#text'] for x in value['ref']]

            tmp = value['#text']
            if '\n' in tmp:
                tmp = "<br />".join(tmp.split('\n'))

            for replace in values:
                loc = tmp.find('= ;')
                if loc == -1:
                    loc = tmp.find('-> =')
                if loc == -1:
                    continue
                loc += 2
                tmp = tmp[:loc] + replace + tmp[loc:]
        else:
            tmp = cgi.escape(str(value))

        desc += small("<pre>{}</pre>".format(tmp))
        desc += "</p>"

    return desc


def macros(xml):
    navdata = OrderedDict()
    print "<h2 id='Macros'>Macros</h2>"
    print "<table class='table'>"
    for entry in xml['doxygen']['compounddef']['sectiondef']:
        for mem in entry['memberdef']:
            if mem['@kind'] == 'define':
                name = mem['name']
                navdata[name] = '#macro_{}'.format(name)

                content = """
                <ul class="list-group">
                <li class="list-group-item active" id="{}">#define {}</li>
                <li class="list-group-item">{}</li>
                </ul>
                """.format(navdata[name][1:],
                           _macros_active(mem),
                           _macros_detail(mem))
                print "<tr><td>{}</td></tr>".format(content)
    print "</table>"
    return navdata


def typedefs(xml):
    navdata = OrderedDict()
    print "<h2 id='Typedefs'>Typedefs</h2>"
    print "<table class='table'>"
    for entry in xml['doxygen']['compounddef']['sectiondef']:
        for mem in entry['memberdef']:
            if mem['@kind'] == 'typedef':
                definition = mem['definition']

                name = mem['name']
                navdata[name] = '#typedef_{}'.format(name)

                try:
                    desc = "<p>"
                    desc += mem['detaileddescription']['para']
                    desc += "</p>"
                except (TypeError, KeyError):
                    desc = ""

                content = """
                <ul class="list-group">
                <li class="list-group-item active" id="{}">{}</li>
                <li class="list-group-item">{}</li>
                </ul>
                """.format(navdata[name][1:], definition, desc)

                print "<tr><td>{}</td></tr>".format(content)
    print "</table>"
    return navdata


def enums(xml):
    navdata = OrderedDict()
    print "<h2 id='Enums'>Enums</h2>"
    print "<table class='table'>"
    for entry in xml['doxygen']['compounddef']['sectiondef']:
        for mem in entry['memberdef']:
            if mem['@kind'] == 'enum':
                name = mem['name']
                navdata[name] = '#enum_{}'.format(name)

                table = "<table class='table table-condensed table-striped'>"
                for value in mem['enumvalue']:
                    table += "<tr><td>"
                    table += value['name']
                    table += "</td><td>"
                    try:
                        table += value['detaileddescription']['para']
                    except (TypeError, KeyError):
                        pass
                    table += "</td></tr>"
                table += "</table>"

                content = """
                <ul class="list-group">
                <li class="list-group-item active" id="{}">enum {}</li>
                <li class="list-group-item">{}</li>
                </ul>
                """.format(navdata[name][1:], name, table)
                print "<tr><td>{}</td></tr>".format(content)
    print "</table>"
    return navdata


def _func_signature(memberdef):
    definition = memberdef['definition']
    args = memberdef['argsstring']
    return "{} {}".format(definition, args)


def _func_details(memberdef):
    details = memberdef['detaileddescription']
    output = ""

    if not details:
        return

    for para in details['para']:
        if type(para) != OrderedDict:
            output += "<p>" + str(para) + "</p>"

        elif '#text' in para and 'emphasis' in para:
            if type(para['emphasis']) is list:
                values = para['emphasis']
            else:
                values = [para['emphasis']]

            tmp = str(para['#text'])
            for value in values:
                value = "<em>" + str(value) + "</em>"
                loc = tmp.find('  ')
                if loc == -1:
                    loc = tmp.find(' .')
                if loc == -1:
                    value = "FAILED!!!!"
                loc += 1

                tmp = tmp[:loc] + value + tmp[loc:]

            output += "<p>" + tmp + "</p>"

        elif '#text' in para:
            #TODO fix this case
            #print >> sys.stderr, memberdef['name']
            #print >> sys.stderr, para
            pass

        elif 'parameterlist' in para:
            output += "<h5>Parameters</h5><ul>"
            if type(para['parameterlist']['parameteritem']) is list:
                items = para['parameterlist']['parameteritem']
            else:
                items = [para['parameterlist']['parameteritem']]

            for entry in items:
                dire = '<missing>'
                name = '<missing>'
                try:
                    if entry['parameternamelist']:
                        dire = entry['parameternamelist']['parametername']['@direction']
                        name = entry['parameternamelist']['parametername']['#text']
                    if entry['parameterdescription']:
                        desc = entry['parameterdescription']['para']
                except TypeError:
                    pass

                output += "<li>[{}] <em>{}</em> {}</li>".format(dire, name, desc)
            output += "</ul>"

            if 'simplesect' in para:
                output += "<h5>Returns</h5><ul>"
                output += "<li>{}</li></ul>".format(para['simplesect']['para'])

    return output


def functions(xml):
    navdata = OrderedDict()
    print "<h2 id='Functions'>Functions</h2>"
    print "<table class='table'>"
    for entry in xml['doxygen']['compounddef']['sectiondef']:
        for mem in entry['memberdef']:
            if mem['@kind'] == 'function':
                name = mem['name']
                navdata[name] = '#func_{}'.format(name)

                content = """
                <ul class="list-group">
                <li class="list-group-item active" id="{}">{}</li>
                <li class="list-group-item">{}</li>
                </ul>
                """.format(navdata[name][1:],
                           _func_signature(mem),
                           _func_details(mem))
                print "<tr><td>{}</td></tr>".format(content)
    print "</table>"
    return navdata


def nav(data):
    print """
    <ul class="nav nav-stacked">
    """
    for category in data.keys():
        print "<li>"
        print "<a href='#" + category + "'>" + category + "</a>"
        print "<ul class='nav nav-stacked'>"
        for item in data[category].keys():
            print "<li><a href='{}'>{}</a></li>".format(
                    data[category][item], item)
        print "</ul>"
        print "</li>"
    print """
    </ul>
    """


def main():
    with open(sys.argv[1], 'r') as f:
        xmldata = f.read()
    xml = xmltodict.parse(xmldata)

    sidenav = OrderedDict()

    front_matter()
    print "<div class='row'><div class='col-xs-9'>"
    sidenav['Macros'] = macros(xml)
    sidenav['Typedefs'] = typedefs(xml)
    sidenav['Enums'] = enums(xml)
    sidenav['Functions'] = functions(xml)
    print "</div>"
    print """
    <nav class="col-xs-3">
      <div class="bs-docs-sidebar">
    """
    nav(sidenav)
    print """
      </div>
    </nav>
    """
    print "</div>"


if __name__ == '__main__':
    main()
