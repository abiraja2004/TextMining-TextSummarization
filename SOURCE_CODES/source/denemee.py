import xml.etree.ElementTree
from xml.parsers import expat
tree = ElementTree()
root = tree.parse(xml_file, parser=expat.ParserCreate('UTF-8') )
root = tree.parse(xml_file, parser=expat.ParserCreate('UTF-16') )
root = tree.parse(xml_file, parser=expat.ParserCreate('ISO-8859-1') )
root = tree.parse(xml_file, parser=expat.ParserCreate('ASCII') )

try:
    file = '../sumdata/data/d062j/WSJ891019-0086.S'
    root = xml.etree.ElementTree.parse(file).getroot()
except Exception as e:
    print e
    if(str(e).__contains__('not well-formed (invalid token)')):
        print file
        os.system("iconv -t utf-8 "+file+">"+"/opt/file")
