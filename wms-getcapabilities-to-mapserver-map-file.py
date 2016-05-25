#!/usr/bin/python


import os
import sys
import datetime
import time
import shutil


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
tab_gap = tab_size * 20


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
    if value is None:
        value = ''
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


# MapServer Map
write_line_to_file(tabs=0, parameter='MAP')
#
# MapServer Map Name
write_line_to_file(tabs=1, parameter='NAME', value='test-wms-01-name')
#
# MapServer Map ImageType
write_line_to_file(tabs=1, parameter='IMAGETYPE', value='PNG')
#
# MapServer Map Extent
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:BoundingBox[@CRS="{}"]'.format(DEFAULT_PROJECTION)
bounding_box = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=1, parameter='EXTENT', value=bounding_box.get('minx') + ' ' + bounding_box.get('miny') + ' ' +bounding_box.get('maxx') + ' ' +bounding_box.get('maxy'))
#
# MapServer Map Size
write_line_to_file(tabs=1, parameter='SIZE', value='350 650')
#
# MapServer Map Shapepath
write_line_to_file(tabs=1, parameter='SHAPEPATH', value='/vagrant/data/smw', quotes=True)
#
# MapServer Fontset
write_line_to_file(tabs=1, parameter='FONTSET', value='/vagrant/maps/fonts/fonts.list', quotes=True)
#
# MapServer Map Projection
write_line_to_file(tabs=1, parameter='PROJECTION')
write_line_to_file(tabs=2, parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower())
write_line_to_file(tabs=1, parameter='END')
#
write_line_to_file(tabs=1, parameter='WEB')
#
# MapServer Imapgepath
write_line_to_file(tabs=2, parameter='IMAGEPATH', value='/ms4w/tmp/ms_tmp/', quotes=True)
#
# MapServer ImageURL
write_line_to_file(tabs=2, parameter='IMAGEURL', value='/ms_tmp/', quotes=True)
#
# WMS Service
write_line_to_file(tabs=3, parameter='METADATA')
xpath = r'/default:WMS_Capabilities/default:Service/default:Title'
#
#  WMS Title
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_title\"', value=wms_title.text, quotes=True)
#
#  WMS Abstract
xpath = r'/default:WMS_Capabilities/default:Service/default:Abstract'
wms_abstract = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_abstract\"', value=wms_abstract.text, quotes=True)
#
#  WMS KeywordList
xpath = r'/default:WMS_Capabilities/default:Service/default:KeywordList/default:Keyword'
wms_keywords = root.xpath(xpath, namespaces=nsdict)
print wms_keywords
wms_keywords_list = []
wms_keywords_vocab_list= []
for wms_keyword in wms_keywords:
    print wms_keyword.tag, wms_keyword.text
    if wms_keyword.get('vocabulary'):
        vocabulary = wms_keyword.get('vocabulary')
        if vocabulary == 'GEMET - INSPIRE themes, version 1.0':
            vocabulary = 'GEMET'
        print vocabulary
        # if vocabulary == 'ISO':
        #     continue
        write_line_to_file(tabs=4, parameter='\"wms_keywordlist_vocabulary\"', value=vocabulary, quotes=True)
        write_line_to_file(tabs=4, parameter='\"wms_keywordlist_{}_items\"'.format(vocabulary), value=wms_keyword.text, quotes=True)
    else:
        wms_keywords_list.append(wms_keyword.text)
wms_keyword_string = ','.join(wms_keywords_list)
write_line_to_file(tabs=4, parameter='\"wms_keywordlist\"', value=wms_keyword_string, quotes=True)


#
#  TODO - Need to ensure GEMET vocabulary and GEMET "Land Cover" keyword are included in WMS keywords section.  May appear (?) when add in INSPIRE service requirements
#


#
#  WMS OnlineResource
wms_onlineresource = MAPSERVER_URL + MAPSERVER_MAPS_FOLDER + os.path.basename(map_file_filename) + r'&'
write_line_to_file(tabs=4, parameter='\"wms_onlineresource\"', value=wms_onlineresource, quotes=True)
#
#  ContactInformation
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPersonPrimary/default:ContactPerson'
wms_contactperson = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_contactperson\"', value=wms_contactperson.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPersonPrimary/default:ContactOrganization'
wms_contactorganization = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_contactorganization\"', value=wms_contactorganization.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPosition'
wms_contactposition = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_contactposition\"', value=wms_contactposition.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:AddressType'
wms_addresstype = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_addresstype\"', value=wms_addresstype.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:Address'
wms_address = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_address\"', value=wms_address.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:City'
wms_city = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_city\"', value=wms_city.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:StateOrProvince'
wms_stateorprovince = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_stateorprovince\"', value=wms_stateorprovince.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:PostCode'
wms_postcode = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_postcode\"', value=wms_postcode.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:Country'
wms_country = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_country\"', value=wms_country.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactVoiceTelephone'
wms_contactvoicetelephone = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_contactvoicetelephone\"', value=wms_contactvoicetelephone.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactFacsimileTelephone'
wms_contactfacsimiletelephone = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=4, parameter='\"wms_contactfacsimiletelephone\"', value=wms_contactfacsimiletelephone.text, quotes=True)
xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactElectronicMailAddress'
wms_contactelectronicmailaddress = root.xpath(xpath, namespaces=nsdict)[0]
print wms_contactelectronicmailaddress.tag, wms_contactelectronicmailaddress.text
write_line_to_file(tabs=4, parameter='\"wms_contactelectronicmailaddress\"', value=wms_contactelectronicmailaddress.text, quotes=True)
#
#  MapServer WMS Requests
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
#
#  CRS
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:CRS'
coordinate_reference_systems = root.xpath(xpath, namespaces=nsdict)
wms_srs = []
for coordinate_reference_system in coordinate_reference_systems:
    wms_srs.append(coordinate_reference_system.text)
wms_srs = ' '.join(wms_srs)
write_line_to_file(tabs=4, parameter='\"wms_srs\"', value=wms_srs, quotes=True)
#
write_line_to_file(tabs=3, parameter='END')
#
write_line_to_file(tabs=1, parameter='END')
#
# WMS Layer
write_line_to_file(tabs=1, parameter='LAYER')
#
# Name
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Name'
name = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=2, parameter='NAME', value=name.text, quotes=True)
#
# MapServer dataset
write_line_to_file(tabs=2, parameter='DATA', value='LCM2007_GB_25M_V2.tif', quotes=True)
#
# MapServer Status
write_line_to_file(tabs=2, parameter='STATUS', value='OFF')
#
# MapServer Data Type
write_line_to_file(tabs=2, parameter='TYPE', value='RASTER')
#
# MapServer Projection
write_line_to_file(tabs=2, parameter='PROJECTION')
write_line_to_file(tabs=3, parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower())
write_line_to_file(tabs=2, parameter='END')
#
# WMS Layer Title
write_line_to_file(tabs=2, parameter='METADATA')
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Title'
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_file(tabs=3, parameter='\"wms_title\"', value=wms_title.text, quotes=True)
# WMS CRS
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


# Copy map file into Vagrant MapServer machine maps folder
vagrant_maps_folder = r'E:\vmachines\mapserver-vagrant\maps'
shutil.copy2(map_file_filename, vagrant_maps_folder)


end_time = time.time()


# elapsed_time = end_time - start_time
print('\n\nIt took {} to exceute this.\n'.format(hms_string(end_time - start_time)))
print('Done.\n')
