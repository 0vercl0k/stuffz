# Axel '0vercl0k' Souchet - 3 January 2019
# SVGs files exported by Microsoft Visio 2018 do not preserve white-spaces.

import xml.dom.minidom as minidom
import codecs
import sys
import os

def fix_file(filein):
    dom = minidom.parse(filein)
    style = dom.getElementsByTagName('style')[0]
    cdata = filter(
        lambda p: p.nodeType == style.CDATA_SECTION_NODE,
        style.childNodes
    )
    assert(len(cdata) == 1)
    cdata = cdata[0]
    if 'text { white-space: pre}' in cdata.data:
        return False

    cdata.data = 'text { white-space: pre}\n' + cdata.data
    with codecs.open(filein, 'w', 'utf-8') as out:
        dom.writexml(out)
    return True

def main(argc, argv):
    if argc != 2:
        print './fix_visio_svgs.py <file | directory>'
        return 0

    assert(os.path.isfile(argv[1]) or os.path.isdir(argv[1]))

    filepaths = [argv[1]]
    if os.path.isdir(argv[1]):
        filepaths = map(
            lambda p: os.path.join(argv[1], p),
            os.listdir(argv[1])
        )

    for filepath in filepaths:
        if not filepath.endswith('.svg'):
            continue

        if fix_file(filepath):
            print 'Updated', filepath

    print 'Done'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
