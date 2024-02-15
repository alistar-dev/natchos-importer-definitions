import glob
from xml.dom import minidom
from datetime import datetime


infolder = "./FileDefinitions"
outfile = "index.html"
html_template = "template.html"

def string_value(el):
    if el is None:
        return ""
    return el

def int_value(el):
    if el is None:
        return ""
    return el

def bool_value(el):
    if el is None:
        return ""
    return "Yes" if el == "1" or el == "True" else ""

def get_valuelist(field, name):
    node = field.getElementsByTagName(name)
    if node is None:
        return ""
    if len(node) == 0:
        return ""
    l = []
    for c in node:
        for cc in c.childNodes:
            if (cc.nodeType == 1):
                # print(cc)
                # print(cc.nodeType)
                # print(cc.tagName)
                # print(cc.childNodes[0].data)
                if len(cc.childNodes) > 0:
                    l.append(cc.childNodes[0].data)
    return l

def get_value(field, name):
    node = field.getElementsByTagName(name)
    if node is None:
        return ""
    if len(node) == 0:
        return ""
    if len(node[0].childNodes) == 0:
        return ""
    return node[0].childNodes[0].data

def entity_from_filename(filename):
    # entity = filename[filename.index("/")+1:filename.index(".")]
    return filename.split("/")[-1].split(".")[0]

def generate_menu(filenames):
    html = "<p>"
    for filename in filenames:
        entity = entity_from_filename(filename)
        html += f"<a href='#{entity}' class='no-underline'><span class='ms-label ms-warning'>{entity}</span></a> "
    html += "</p>"
    html += "\r\n"
    return html

def generate(filename):
    print(filename)

    entity = entity_from_filename(filename)
    html = f"<div style='page-break-before: always;' id='{entity}' class='ms-alert ms-info'><h1>{entity}</h1></div>"
    html += "\r\n"

    html += "<table class='ms-table'>"
    html += "<tr><th class='ms-text-left'>Field Name</th><th class='ms-text-center'>Key Field</th><th class='ms-text-center'>Required</th><th class='ms-text-center'>Obsolete</th><th class='ms-text-center'>Type</th><th class='ms-text-center'>Max. Length </th></tr>"
    mydoc = minidom.parse(filename)
    fields = mydoc.getElementsByTagName('Field')

    for field in fields:
        name = get_value(field, "Name")
        isreq = get_value(field, "IsRequired")
        isobs = get_value(field, "IsObsolete")
        typee = get_value(field, "Type")
        prec = get_value(field, "Precision")
        scale = get_value(field, "Scale")
        maxl = get_value(field, "MaximumLength")
        iskey = field.getAttribute("iskey")
        builtin = field.getAttribute("builtintype")
        if builtin == "Action":
            name = "Action"
            typee = "char"
            maxl = "1"
            iskey = "0"
            isreq = "1"

        tr = "<tr>"
        tr += f"<td class='ms-text-left'>{string_value(name)}</td>"
        tr += f"<td class='ms-text-center'>{bool_value(iskey)}</td>"
        tr += f"<td class='ms-text-center'>{bool_value(isreq)}</td>"
        tr += f"<td class='ms-text-center'>{bool_value(isobs)}</td>"
        tr += f"<td class='ms-text-center'>{string_value(typee)}</td>"
        tr += f"<td class='ms-text-center'>{int_value(maxl)}</td>"
        tr += "</tr>"
        html += tr

    html += "</table>"
    html += "\r\n"

    for field in fields:
        name = get_value(field, "Name")
        default = get_value(field, "Default")
        descri = get_value(field, "Description")
        alts = get_valuelist(field, "AltHeaderNames")
        fixeds =get_valuelist(field, "FixedValueList")
        builtin = field.getAttribute("builtintype")

        if builtin == "Action":
            fixeds = ["I", "U", "D"]
            name = "Action"

        if len(descri) == 0 and len(alts) == 0 and len(fixeds) == 0:
            continue

        html += "<div class='ms-article'>"
        html += f"<div class='ms-article-title'><span class='ms-label ms-success'>Field</span><br/><h3>{name}</h3></div>"
        html += "<div class='ms-article-text'>"

        # html += f"<h4>{name}</h4>"

        if len(descri) > 0:
            descri = descri.strip()
            lines = descri.split("\n")
            html += "<div class='ms-blockquote ms-info'>"
            html += "<p class='ms-text-info'>"
            for line in lines:
                line = line.replace("  ", " ")
                line = line.strip()
                html += line
                html += "<br/>"
            html += "</p>"
            html += "</div>"

        if len(alts) > 0:
            html += "<p>"
            html += "<h6>Alternate Names</h6>"
            for ix, alt in enumerate(alts):
                #if ix != 0:
                #    html += ", "
                html += f"<span class='ms-label ms-medium'>{alt}</span> "
            html += "</p>"

        if len(fixeds) > 0:
            html += "<p>"
            html += "<h6>Allowed Values</h6>"
            for ix, alt in enumerate(fixeds):
                #if ix != 0:
                #    html += ", "
                html += f"<span class='ms-label ms-medium'>{alt}</span> "
            html += "</p>"

        if default is not None and len(default) > 0:
            html += "<p>"
            html += "<h6>Default</h6>"
            html += f"<span class='ms-label ms-medium'>{default}</span> "
            html += "</p>"

        html += "</div>"
        html += "</div>"
        html += "\r\n"


    html += "<hr/><hr/>"
    html += "\r\n"
    return html


if __name__ == "__main__":
    html = ""
    with open(html_template, "r") as ft:
        html = ft.read()

    body = ""
    filenames = sorted(glob.glob(infolder + "/*.xml"))

    body += generate_menu(filenames)

    for file in filenames:
        body += generate(file)

    html = html.replace("{body}", body)

# get current date and time
    current_date_and_time = datetime.now()
    html = html.replace("{generated_at}", current_date_and_time.strftime("%Y-%m-%d %H:%M"))

    with open(outfile, "w") as fo:
        fo.write(html)
