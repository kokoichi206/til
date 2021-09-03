import xml.etree.ElementTree as ET


root = ET.Element('root')
tree = ET.ElementTree(element=root)

employee = ET.SubElement(root, 'employee')

employ = ET.SubElement(employee, 'employ')
employ_id = ET.SubElement(employ, 'id')
employ_id.text = '111'
employ_id = ET.SubElement(employ, 'name')
employ_id.text = 'Mike'

employ = ET.SubElement(employee, 'employ')
employ_id = ET.SubElement(employ, 'id')
employ_id.text = '222'
employ_id = ET.SubElement(employ, 'name')
employ_id.text = 'Nancy'

tree.write('test.xml', encoding='utf-8', xml_declaration=True)

tree = ET.ElementTree(file='test.xml')
root = tree.getroot()

for employee in root:
    for employ in employee:
        for person in employ:
            print(person.tag)
