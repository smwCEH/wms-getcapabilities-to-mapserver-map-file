#!/usr/bin/python


import os
import sys
import datetime
import time


import lxml.etree as ET


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


start_time = time.time()


wms_getcapabilities = r'http://lasigpublic.nerc-lancaster.ac.uk/arcgis/services/LandCoverMap/LCM2007_GB_25m_V2/MapServer/WMSServer?request=getCapabilities&service=WMS'
# xml_file = r'E:\MapServer\Python\lcm2007-gb-25m-v2.xml'
# xml_file = r'E:\MapServer\Python\junk-01.xml'


print('\n\nwms_getcapabilites:\t{}'.format(wms_getcapabilities))


# Parse WMS GetCapabilities document
xml_doc = ET.parse(wms_getcapabilities)


# Define root element for the xml document
root = xml_doc.getroot()


# Get namespaces as a dictionary
nsdict = root.nsmap
# print('nsDict:\t{}'.format(nsdict))
# Copy the default un-named namespace item (identified with the [None] key) in the namespace dictionary
# to a named default namespace (identified with the key ['default'])
nsdict['default'] = nsdict[None]
# print('nsDict:\t{}'.format(nsdict))
# Delete the default un-named namespace item (identified with the [None] key) in the namespace dictionary
del nsdict[None]
# print('\n\nnsdict:\t{}'.format(nsdict))
nsdict['xlink'] = r'http://www.w3.org/1999/xlink'
print('\n\nnsdict:\t{}'.format(nsdict))



def get_xml_element(elementxpath):
    """"Return element from XML document

    Keyword arguments:
    elementxpath -- xpath, with namespaces, to element in XML document
    """
    print('\n\n\tGetting XML element...\n\txpath:\t\t{}'.format(elementxpath))
    element = root.xpath(elementxpath,
                         namespaces=nsdict)
    # print element, type(element)
    if len(element) == 0:
        sys.exit('No element selected!\n\n')
    elif len(element) > 1:
        sys.exit('Multiple elements selected!\n\n')
    else:
        # print element[0].tag, element[0].text
        return element[0]


tab_size = 4
tab_gap = tab_size * 12


def write_line_to_file(tabs=0, parameter='', value='', quotes=False):
    if value != '':
        if ((tab_gap - len(parameter))) % tab_size > 0:
            extra_tab = 1
        else:
            extra_tab = 0
        gap_tabs = ((tab_gap - len(parameter)) // tab_size) - tabs
    else:
        extra_tab = gap_tabs = 0
    # print (tab_gap - len(parameter)), extra_tab, gap_tabs
    if quotes:
        value = '\"' + value +'\"'
    map_file.write('{}{}{}{}\n'.format('\t' * tabs,
                                       parameter,
                                       '\t' * (extra_tab + gap_tabs),
                                       value))


DEFAULT_PROJECTION = 'EPSG:27700'


map_file_filename = r'E:\MapServer\Python\maps\test-01.map'
map_file = open(map_file_filename, mode='w')


MAPSERVER_URL = 'http:/localhost:8080/cgi-bin/mapserv?map='
MAPSERVER_MAPS_FOLDER = r'/vagrant/maps/'


write_line_to_file(tabs=0, parameter='MAP')
#
write_line_to_file(tabs=1, parameter='NAME', value='test-wms-01-name')
#
write_line_to_file(tabs=1, parameter='IMAGETYPE', value='PNG')
#
# xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:BoundingBox'
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:BoundingBox[@CRS="{}"]'.format(DEFAULT_PROJECTION)
bounding_box = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=1, parameter='EXTENT', value=bounding_box.get('minx') + ' ' + bounding_box.get('miny') + ' ' +bounding_box.get('maxx') + ' ' +bounding_box.get('maxy'))
#
write_line_to_file(tabs=1, parameter='SIZE', value='350 650')
#
write_line_to_file(tabs=1, parameter='SHAPEPATH', value='/vagrant/data/smw', quotes=True)
#
write_line_to_file(tabs=1, parameter='FONTSET', value='/vagrant/maps/fonts/fonts.list', quotes=True)
#
write_line_to_file(tabs=1, parameter='PROJECTION')
write_line_to_file(tabs=2, parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower())
write_line_to_file(tabs=1, parameter='END')
#
write_line_to_file(tabs=1, parameter='WEB')
#
write_line_to_file(tabs=2, parameter='IMAGEPATH', value='/ms4w/tmp/ms_tmp/', quotes=True)
#
write_line_to_file(tabs=2, parameter='IMAGEURL', value='/ms_tmp/', quotes=True)
#
write_line_to_file(tabs=3, parameter='METADATA')
xpath = r'/default:WMS_Capabilities/default:Service/default:Title'
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_title\"', value=wms_title.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:Abstract'
wms_abstract = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_abstract\"', value=wms_abstract.text, quotes=True)
# xpath = r'/default:WMS_Capabilities/default:Service/default:OnlineResource/@xlink:href'
# wms_onlineresource = root.xpath(xpath, namespaces=nsdict)[0]
wms_onlineresource = MAPSERVER_URL + MAPSERVER_MAPS_FOLDER + os.path.basename(map_file_filename) + r'&'
write_line_to_file(tabs=4, parameter='\"wms_onlineresource\"', value=wms_onlineresource, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Capability/default:Request'
requests = root.xpath(xpath, namespaces=nsdict)[0]
wms_enable_requests = []
for request in requests:
    # Only select OGC WMS requests
    if nsdict['default'] in request.tag:
        # Limit which OGC WMS to specify:
        allowed_requests = ['GetCapabilities', 'GetMap']
        if any(x in request.tag for x in allowed_requests):
            # Remove namespace from request element
            i = request.tag.find('}')
            if i > 0:
                request.tag = request.tag[i+1:]
            wms_enable_requests.append(request.tag)
wms_enable_request = ' '.join(wms_enable_requests)
write_line_to_file(tabs=4, parameter='\"wms_enable_request\"', value=wms_enable_request, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:CRS'
coordinate_reference_systems = root.xpath(xpath, namespaces=nsdict)
wms_srs = []
for coordinate_reference_system in coordinate_reference_systems:
    wms_srs.append(coordinate_reference_system.text)
wms_srs = ' '.join(wms_srs)
write_line_to_file(tabs=4, parameter='\"wms_srs\"', value=wms_srs, quotes=True)
write_line_to_file(tabs=3, parameter='END')
#
write_line_to_file(tabs=1, parameter='END')
#
write_line_to_file(tabs=1, parameter='LAYER')
#
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Name'
name = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=2, parameter='NAME', value=name.text, quotes=True)
#
write_line_to_file(tabs=2, parameter='DATA', value='LCM2007_GB_25M_V2.tif', quotes=True)
#
write_line_to_file(tabs=2, parameter='STATUS', value='OFF')
#
write_line_to_file(tabs=2, parameter='TYPE', value='RASTER')
#
write_line_to_file(tabs=2, parameter='PROJECTION')
write_line_to_file(tabs=3, parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower())
write_line_to_file(tabs=2, parameter='END')
#
write_line_to_file(tabs=2, parameter='METADATA')
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Title'
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=3, parameter='\"wms_title\"', value=wms_title.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:CRS'
coordinate_reference_systems = root.xpath(xpath, namespaces=nsdict)
wms_srs = []
for coordinate_reference_system in coordinate_reference_systems:
    wms_srs.append(coordinate_reference_system.text)
wms_srs = ' '.join(wms_srs)
write_line_to_file(tabs=3, parameter='\"wms_srs\"', value=wms_srs, quotes=True)
write_line_to_file(tabs=2, parameter='END')
#
write_line_to_file(tabs=1, parameter='END')
#
write_line_to_file(tabs=0, parameter='END')


map_file.close()


end_time = time.time()


# elapsed_time = end_time - start_time
print('\n\nIt took {} to exceute this.\n'.format(hms_string(end_time - start_time)))
print('Done.\n')
