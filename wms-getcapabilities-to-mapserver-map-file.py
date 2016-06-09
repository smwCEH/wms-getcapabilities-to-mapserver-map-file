#!/usr/bin/python


import os
import sys
import datetime
import time
import shutil
import types


import lxml.etree as ET


def hms_string(sec_elapsed):
    """Function to display elapsed time

    Keyword arguments:
    sec_elapsed -- elapsed time in seconds
    """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# Capture start_time
start_time = time.time()


# Define WMS GetCapabilities document
# wms_getcapabilities = r'http://lasigpublic.nerc-lancaster.ac.uk/arcgis/services/LandCoverMap/LCM2007_GB_25m_V2/MapServer/WMSServer?request=getCapabilities&service=WMS'
wms_getcapabilities = r'E:\MapServer\Python\lcm2007-gb-25m-v2.xml'
# wms_getcapabilities = r'E:\MapServer\Python\junk-01.xml'
print('\n\nwms_getcapabilites:\t{}'.format(wms_getcapabilities))


# Define default projection
DEFAULT_PROJECTION = 'EPSG:27700'


# Define MapServer URL and maps folder for WMS Service OnlineResource
MAPSERVER_URL = 'http:/localhost:8080/cgi-bin/mapserv?map='
MAPSERVER_MAPS_FOLDER = r'/vagrant/maps/'


# Define XML Parser
xml_parser = ET.XMLParser()


# Parse WMS GetCapabilities document
xml_doc = ET.parse(wms_getcapabilities, xml_parser)
# Print parser error log
# print(len(xml_parser.error_log))


# Define root element for the xml document
root = xml_doc.getroot()


# Define schema/XSD
schema_url = r'http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xsd'
# print('\n\nschema_url:\t{}'.format(schema_url))


# Validate schema/XSD
validate_schema = False
if validate_schema:
    print('\tValidating schema...')
    schema_doc = ET.parse(schema_url)
    try:
        schema = ET.XMLSchema(schema_doc)
    except ET.XMLSchemaParseError as e:
        print e
        exit(1)
    print('\tSchema OK.')


# Validate XML against schema/XSD
validate_document = False
if validate_document:
    print('\n\nxml_file:\t{}'.format(wms_getcapabilities))
    print('\tTesting for well-formedness...')
    try:
        xml_doc = ET.parse(wms_getcapabilities)
    except ET.XMLSyntaxError as e:
        print('\tDocument not well-formed!')
        print('\t\t{}'.format(e))
    else:
        print('\tDocument is well-formed.')
        print('\tValidating document...')
        # xml_doc = etree.parse(xml_file)
        try:
            print('\t\tschema.validate(xml_doc):\t{}'.format(schema.validate(xml_doc)))
            schema.assertValid(xml_doc)
        except ET.DocumentInvalid as e:
            print('\tDocument not valid!')
            # print('\t\t{0}'.format(e))
            print('\t\tErrors found:\t{:>3}'.format(len(schema.error_log)))
            error_count = 0
            for error in schema.error_log:
                error_count += 1
                print('\t\t\tError:\t{:>3}'.format(error_count))
                print('\t\t\terror:\t{}'.format(error))
                print('\t\t\t\tMessage:\t{}'.format(error.message))
                print('\t\t\t\tDomain:\t{}'.format(error.domain))
                print('\t\t\t\tType:\t{}'.format(error.type))
                print('\t\t\t\tLevel:\t{}'.format(error.level))
                print('\t\t\t\tLine number:\t{}'.format(error.line))
                print('\t\t\t\tColumn:\t{}'.format(error.column))
                print('\t\t\t\tFilename:\t{}'.format(error.filename))
                print('\t\t\t\tDomain name:\t{}'.format(error.domain_name))
                print('\t\t\t\tType name:\t{}'.format(error.type_name))
                print('\t\t\t\tLevel name:\t{}'.format(error.level_name))
                # exit(1)
        else:
            print('\tDocument is valid.')


# Iterate through XML document elements
# for i, element in enumerate(xml_doc.getiterator()):
#     print(element.tag)


# Get namespaces as a dictionary
nsdict = root.nsmap
# Copy the default un-named namespace item (identified with the [None] key) in the namespace dictionary
# to a named default namespace (identified with the key ['default'])
nsdict['default'] = nsdict[None]
# Delete the default un-named namespace item (identified with the [None] key) in the namespace dictionary
del nsdict[None]
nsdict['xlink'] = r'http://www.w3.org/1999/xlink'
print('\n\nnsdict:\t{}\n\n'.format(nsdict))


# def get_xml_element(elementxpath):
#     """"Return element from XML document
#
#     Keyword arguments:
#     elementxpath -- xpath, with namespaces, to element in XML document
#     """
#     print('\n\n\tGetting XML element...\n\txpath:\t\t{}'.format(elementxpath))
#     element = root.xpath(elementxpath,
#                          namespaces=nsdict)
#     # print element, type(element)
#     if len(element) == 0:
#         sys.exit('No element selected!\n\n')
#     elif len(element) > 1:
#         sys.exit('Multiple elements selected!\n\n')
#     else:
#         # print element[0].tag, element[0].text
#         return element[0]


# Define tab size and spacing between parameters and values in the MapServer .map file
tab_size = 4
tab_gap = tab_size * 17


# def write_line_to_file(tabs, parameter, value='', quotes=False, comment=''):
#     """Write parameter and value to MapServer .map file
#
#     Keyword arguments:
#     tabs -- indent for parameter
#     parameter -- parameter name
#     value -- parameter value
#     quotes -- Boolean to print parameter value in double quotes
#     comment -- Comment to add to line
#     """
#     # Determine tabs gap
#     if value != '':
#         if ((tab_gap - len(parameter))) % tab_size > 0:
#             extra_tab = 1
#         else:
#             extra_tab = 0
#         gap_tabs = ((tab_gap - len(parameter)) // tab_size) - tabs
#     else:
#         extra_tab = gap_tabs = 0
#     # Set output_value to write to map file based upon input value type and quotes
#     if value is None:
#         output_value = ''
#     elif type(value) == types.BooleanType:
#         if value == True:
#             output_value = 'true'
#         else:
#             output_value = 'false'
#     elif type(value) == int:
#         output_value = str(value)
#     elif type(value) == str:
#         output_value = value
#     if quotes:
#         output_value = '\"' + output_value +'\"'
#     # Write formatted line to MapServer .map file
#     map_file.write('{}{}{}{}{}{}\n'.format('\t' * tabs,
#                                        parameter,
#                                        '\t' * (extra_tab + gap_tabs),
#                                        output_value,
#                                        '\t' * (extra_tab + gap_tabs),
#                                        '#' + ' ' + comment))


def write_line_to_list(list, tabs, parameter, value='', quotes=False, comment=''):
    """Write parameter and value to MapServer .map list

    Keyword arguments:
    tabs -- indent for parameter
    parameter -- parameter name
    value -- parameter value
    quotes -- Boolean to print parameter value in double quotes
    comment -- Comment to add to line
    """
    # Set output_value to write to map file based upon input value type and quotes
    if value is None:
        output_value = ''
    elif type(value) == types.BooleanType:
        if value == True:
            output_value = 'true'
        else:
            output_value = 'false'
    elif type(value) == int:
        output_value = str(value)
    elif type(value) == str:
        output_value = value.replace('&', '&amp;')
    if quotes:
        output_value = '\"' + output_value +'\"'

    ignore_comments = False

    # Write line elements to MapServer .map file list
    if ignore_comments:
        list.append([tabs,
                     parameter,
                     output_value,
                     ''])
    else:
        list.append([tabs,
                     parameter,
                     output_value,
                     '# ' + comment])


# Define MapServer .map file to be written to
map_file_filename = r'E:\MapServer\Python\maps\test-01.map'


map_file_list = []


DATASET_METADATA_FILE_ID = 'a1f88807-4826-44bc-994d-a902da5119c2'
SERVICE_METADATA_FILE_ID = '987544e0-22d8-11e4-8c21-0800200c9a66'


# Write parameters and values for an WMS INSPIRE View Service to the MapServer .map file
# Map object
write_line_to_list(map_file_list,
                   tabs=0,
                   parameter='MAP',
                   comment='Start of Map Object')
#
# Map name
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='NAME',
                   value='Layer',
                   quotes=True,
                   comment='Prefix attached to map created using this mapfile')
#
# Map status
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='STATUS',
                   value='ON',
                   comment='Status of the map (on|off)')
#
# Map image type
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='IMAGETYPE',
                   value='PNG',
                   comment='Output format to generate')
#
# Map size
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='SIZE',
                   value='350 650',
                   comment='Size in pixels of the output image (map)')
#
# Map extent
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:BoundingBox[@CRS="{}"]'.format(DEFAULT_PROJECTION)
bounding_box = root.xpath(xpath, namespaces=nsdict)[0]
bounding_box = bounding_box.get('minx') + ' ' + bounding_box.get('miny') + ' ' +bounding_box.get('maxx') + ' ' +bounding_box.get('maxy')
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='EXTENT',
                   value=bounding_box,
                   comment='Spatial extent of the map')
#
# Map units
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='UNITS',
                   value='METERS',
                   comment='Units of the map coordinates')
#
# Map shapepath
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='SHAPEPATH',
                   value='//vagrant//data//smw',
                   quotes=True,
                   comment='Path to the directory holding the shapefiles or tiles')
#
# Fontset
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='FONTSET',
                   value='//vagrant//maps//fonts//fonts.list',
                   quotes=True,
                   comment='Filename of the fontset file to use')
#
# Map web metadata
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='WEB',
                   comment='Start of a Web object')
#
#  MapServer Imapgepath
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='IMAGEPATH',
                   value='/ms4w/tmp/ms_tmp/',
                   quotes=True,
                   comment='Path to the temporary directory for writing temporary files and images')
#
#  MapServer ImageURL
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='IMAGEURL',
                   value='/ms_tmp/',
                   quotes=True,
                   comment='Base URL for the IMAGEPATH')
#
#  WMS Service
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='METADATA',
                   comment='Start of METADATA section')
#
#  INSPIRE View Service support
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_inspire_capabilities\"',
                   value='url',
                   quotes=True,
                   comment='Activate INSPIRE support using a reference to an external service metadata (scenario 1)')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_languages\"',
                   value='eng',
                   quotes=True,
                   comment='Supported languages; first specified is the default')
catalogue_url = r'https://catalogue.ceh.ac.uk/'
metadataurl_href = catalogue_url + 'id/' + SERVICE_METADATA_FILE_ID + '?format=gemini&'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_inspire_metadataurl_href\"',
                   value=metadataurl_href,
                   quotes=True,
                   comment='URL to INSPIRE external metadata')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_inspire_metadataurl_format\"',
                   value='application/vnd.iso.19139+xml',
                   quotes=True,
                   comment='Format of INSPIRE external metadata')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_keywordlist_ISO_vocabulary\"',
                   value='infoMapAccessService',
                   quotes=True,
                   comment='INSPIRE classification of spatial data services')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_keywordlist_vocabulary\"',
                   value='ISO',
                   quotes=True,
                   comment='Vocabulary for INSPIRE classification of spatial data services')
#
#  WMS Title
xpath = r'/default:WMS_Capabilities/default:Service/default:Title'
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_title\"',
                   value=wms_title.text,
                   quotes=True,
                   comment='WMS title')
#
#  WMS Abstract
xpath = r'/default:WMS_Capabilities/default:Service/default:Abstract'
wms_abstract = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_abstract\"',
                   value=wms_abstract.text,
                   quotes=True,
                   comment='WMS abstract')
#
#  WMS KeywordList
xpath = r'/default:WMS_Capabilities/default:Service/default:KeywordList/default:Keyword'
wms_keywords = root.xpath(xpath, namespaces=nsdict)
wms_keywords_list = []
wms_keywords_vocab_list= []
for wms_keyword in wms_keywords:
    if wms_keyword.get('vocabulary'):
        vocabulary = wms_keyword.get('vocabulary')
        if vocabulary == 'GEMET - INSPIRE themes, version 1.0':
            vocabulary = 'GEMET'
        if vocabulary == 'ISO':
            continue
        write_line_to_list(map_file_list,
                           tabs=3,
                           parameter='\"wms_keywordlist_{}_items\"'.format(vocabulary),
                           value=wms_keyword.text,
                           quotes=True,
                           comment='Keywords')
        write_line_to_list(map_file_list,
                           tabs=3,
                           parameter='\"wms_keywordlist_vocabulary\"',
                           value=vocabulary,
                           quotes=True,
                           comment='Keywords vocabulary')
    else:
        wms_keywords_list.append(wms_keyword.text)
wms_keyword_string = ','.join(wms_keywords_list)
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_keywordlist\"',
                   value=wms_keyword_string,
                   quotes=True,
                   comment='Keywords list')
#
#  TODO - Need to ensure GEMET vocabulary and GEMET "Land Cover" keyword are included in WMS keywords section.  May appear (?) when add in INSPIRE service requirements
#
#  WMS OnlineResource
wms_onlineresource = MAPSERVER_URL + MAPSERVER_MAPS_FOLDER + os.path.basename(map_file_filename) + '&'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_onlineresource\"',
                   value=wms_onlineresource,
                   quotes=True,
                   comment='WMS OnlineResource')
#
#  WMS ContactInformation
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPersonPrimary/default:ContactPerson'
# wms_contactperson = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactperson = wms_contactperson.text
wms_contactperson = r''
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactperson\"',
                   value=wms_contactperson,
                   quotes=True,
                   comment='WMS ContactPerson')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPersonPrimary/default:ContactOrganization'
# wms_contactorganization = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactorganization = wms_contactorganization.text
wms_contactorganization = r'Centre for Ecology & Ecology'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactorganization\"',
                   value=wms_contactorganization,
                   quotes=True,
                   comment='WMS ContactOrganization')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactPosition'
# wms_contactposition = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactposition = wms_contactposition.text
wms_contactposition = r'pointOfContact'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactposition\"',
                   value=wms_contactposition,
                   quotes=True,
                   comment='WMS ContactPosition')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:AddressType'
# wms_addresstype = root.xpath(xpath, namespaces=nsdict)[0]
# wms_addresstype = wms_addresstype.text
wms_addresstype = r'Postal'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_addresstype\"',
                   value=wms_addresstype,
                   quotes=True,
                   comment='WMS Contact AddressType')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:Address'
# wms_address = root.xpath(xpath, namespaces=nsdict)[0]
# wms_address = wms_address.text
wms_address = r'Lancaster Environment Centre, Library Avenue, Bailrigg'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_address\"',
                   value=wms_address,
                   quotes=True,
                   comment='WMS Address')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:City'
# wms_city = root.xpath(xpath, namespaces=nsdict)[0]
# wms_city = wms_city.text
wms_city = r'Lancaster'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_city\"',
                   value=wms_city,
                   quotes=True,
                   comment='WMS City')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:StateOrProvince'
# wms_stateorprovince = root.xpath(xpath, namespaces=nsdict)[0]
# wms_stateorprovince = wms_stateorprovince.text
wms_stateorprovince = r'Lancashire'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_stateorprovince\"',
                   value=wms_stateorprovince,
                   quotes=True,
                   comment='WMS StateOrProvince')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:PostCode'
# wms_postcode = root.xpath(xpath, namespaces=nsdict)[0]
# wms_postcode = wms_postcode.text
wms_postcode = r'LA1 4AP'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_postcode\"',
                   value=wms_postcode,
                   quotes=True,
                   comment='WMS PostCode')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactAddress/default:Country'
# wms_country = root.xpath(xpath, namespaces=nsdict)[0]
# wms_country = wms_country.text
wms_country = r'UK'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_country\"',
                   value=wms_country,
                   quotes=True,
                   comment='WMS Country')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactVoiceTelephone'
# wms_contactvoicetelephone = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactvoicetelephone = wms_contactvoicetelephone.text
wms_contactvoicetelephone = r''
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactvoicetelephone\"',
                   value=wms_contactvoicetelephone,
                   quotes=True,
                   comment='WMS ContactVoiceTelephone')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactFacsimileTelephone'
# wms_contactfacsimiletelephone = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactfacsimiletelephone = wms_contactfacsimiletelephone.text
wms_contactfacsimiletelephone = r''
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactfacsimiletelephone\"',
                   value=wms_contactfacsimiletelephone,
                   quotes=True,
                   comment='WMS ContactFacsimileTelephone')
# xpath = r'/default:WMS_Capabilities/default:Service/default:ContactInformation/default:ContactElectronicMailAddress'
# wms_contactelectronicmailaddress = root.xpath(xpath, namespaces=nsdict)[0]
# wms_contactelectronicmailaddress = wms_contactelectronicmailaddress.text
wms_contactelectronicmailaddress = r'enquiries@ceh.ac.uk'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_contactelectronicmailaddress\"',
                   value=wms_contactelectronicmailaddress,
                   quotes=True,
                   comment='WMS ContactElectronicMailAddress')
#
#  WMS Fees
xpath = r'/default:WMS_Capabilities/default:Service/default:Fees'
wms_fees = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_fees\"',
                   value=wms_fees.text,
                   quotes=True,
                   comment='WMS Fees')
#
#  WMS Access Constraints
# xpath = r'/default:WMS_Capabilities/default:Service/default:AccessConstraints'
# wms_accessconstraints = root.xpath(xpath, namespaces=nsdict)[0]
# wms_accessconstraints = wms_accessconstraints.text
wms_accessconstraints = r'license'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_accessconstraints\"',
                   value=wms_accessconstraints,
                   quotes=True,
                   comment='WMS AccessConstraints')
#
#  MapServer WMS Requests
# xpath = r'/default:WMS_Capabilities/default:Capability/default:Request'
# requests = root.xpath(xpath, namespaces=nsdict)[0]
# wms_enable_requests = []
# for request in requests:
#     # Only select OGC WMS requests
#     if nsdict['default'] in request.tag:
#         # Limit which OGC WMS to specify:
#         allowed_requests = ['GetCapabilities', 'GetMap']
#         if any(x in request.tag for x in allowed_requests):
#             # Remove namespace from request element
#             i = request.tag.find('}')
#             if i > 0:
#                 request.tag = request.tag[i+1:]
#             wms_enable_requests.append(request.tag)
# wms_enable_request = ' '.join(wms_enable_requests)
wms_enable_request = r'GetCapabilities GetMap'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_enable_request\"',
                   value=wms_enable_request,
                   quotes=True,
                   comment='Space separated list of WMS requests to enable')
#
# WMS GetMap Formats
# xpath = r'//default:Format'
# # xpath = xpath.replace(r'//', r'//default:')
# print('xpath:\t\t{}'.format(xpath))
# all_format_nodes = root.xpath(xpath, namespaces=nsdict)
# # print('all_format_nodes:\t{}'.format(all_format_nodes))
# wms_getmap_formatlist = []
# for format in all_format_nodes:
#     # print '\t', format.tag, '\t', format.text, '\t', format.getparent().tag
#     if format.getparent().tag == 'GetMap':
#         wms_getmap_formatlist.append(format.text)
# wms_getmap_formatlist = ','.join(wms_getmap_formatlist[1:])
# print('wms_getmap_formatlist:\t{}'.format(wms_getmap_formatlist))
wms_getmap_formatlist = r'image/jpeg,image/tiff,image/png'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_getmap_formatlist\"',
                   value=wms_getmap_formatlist,
                   quotes=True,
                   comment='Valid image formats for a WMS GetMap request')
#
#  Root Layer CRS
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:CRS'
coordinate_reference_systems = root.xpath(xpath, namespaces=nsdict)
wms_srs = []
for coordinate_reference_system in coordinate_reference_systems:
    wms_srs.append(coordinate_reference_system.text)
wms_srs = ' '.join(wms_srs)
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_srs\"',
                   value=wms_srs,
                   quotes=True,
                   comment='WMS supported EPSG projection codes')
#
#  Extended BoundingBox support (If set to True bounding boxes for all supported projections are reported)
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_bbox_extended\"',
                   value=True,
                   quotes=True,
                   comment='true|false. If true, bounding boxes are reported for all supported SRS/CRS in the GetCapabilities document')
#
# Set style for the root layer
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_name\"',
                   value='inspire_common:DEFAULT',
                   quotes=True,
                   comment='Style name')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_title\"',
                   value='inspire_common:DEFAULT',
                   quotes=True,
                   comment='Style title')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_legendurl_width\"',
                   value=226,
                   quotes=True,
                   comment='Override style legendURL width')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_legendurl_height\"',
                   value=431,
                   quotes=True,
                   comment='Override style legendURL height')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_legendurl_format\"',
                   value='image/png',
                   quotes=True,
                   comment='Override style legendURL format')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_style_legendurl_href\"',
                   value=r'http://eidc.ceh.ac.uk/administration-folder/tools/wms/987544e0-22d8-11e4-8c21-0800200c9a66/legends/LCM2007_DomTar.png',
                   quotes=True,
                   comment='Override style legendURL href')
#
#  SLD support
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_sld_enabled\"',
                   value=False,
                   quotes=True,
                   comment='true|false. If false, SLD and SLD_BODY parameters ignored to disable remote styling of WMS layers')
#
# End of Web Metadata section
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='END',
                   comment='End of Web Metadata')
#
# End of Web section
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='END',
                   comment='End of Web')
#
#  MapServer Map Projection
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='PROJECTION',
                   comment='Start of output projection definition')
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower(),
                   comment='')
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='END',
                   comment='End of output projection definition')
#
#  WMS Layer
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='LAYER',
                   comment='Start of Layer definition')
#
#  Name
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Name'
name = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='NAME',
                   value=name.text,
                   quotes=True,
                   comment='Short name for the Layer')
#
#  WMS Layer Metadata
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='METADATA',
                   comment='Start of Layer Metadata')
#
#  WMS Layer Title
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:Title'
wms_title = root.xpath(xpath, namespaces=nsdict)[0]
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_title\"',
                   value=wms_title.text,
                   quotes=True,
                   comment='WMS layer title')
#
#  WMS CRS
xpath = r'/default:WMS_Capabilities/default:Capability/default:Layer/default:Layer/default:CRS'
coordinate_reference_systems = root.xpath(xpath, namespaces=nsdict)
wms_srs = []
for coordinate_reference_system in coordinate_reference_systems:
    wms_srs.append(coordinate_reference_system.text)
wms_srs = ' '.join(wms_srs)
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_srs\"',
                   value=wms_srs,
                   quotes=True,
                   comment='WMS human-readable name for the layer')
#
#  Layer WMS MetadataURL Type, Format, and OnlineResource
# xpath = r'/WMS_Capabilities/Capability/Layer/Layer/MetadataURL'
# xpath = xpath.replace('/', '/default:')
# wms_metadataurl_type = root.xpath(xpath, namespaces=nsdict)[0]
# wms_metadataurl_type = wms_metadataurl_type.attrib['type']
wms_metadataurl_type = r'ISO10115:2003'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_metadataurl_type\"',
                   value=wms_metadataurl_type,
                   quotes=True,
                   comment='Standard to which the metadata complies')
# xpath = r'/WMS_Capabilities/Capability/Layer/Layer/MetadataURL/Format'
# xpath = xpath.replace('/', '/default:')
# wms_metadataurl_format = root.xpath(xpath, namespaces=nsdict)[0]
# wms_metadataurl_format = wms_metadataurl_format.text
wms_metadataurl_format = r'text/xml'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_metadataurl_format\"',
                   value=wms_metadataurl_format,
                   quotes=True,
                   comment='The file format MIME type for the metadata record')
# xpath = r'/WMS_Capabilities/Capability/Layer/Layer/MetadataURL/OnlineResource'
# xpath = xpath.replace('/', '/default:')
# wms_metadataurl_href = root.xpath(xpath, namespaces=nsdict)[0]
# wms_metadataurl_href = wms_metadataurl_href.attrib['{'+nsdict['xlink']+'}href']
wms_metadataurl_href = catalogue_url + 'id/' + DATASET_METADATA_FILE_ID + '?'
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"wms_metadataurl_href\"',
                   value=wms_metadataurl_href,
                   quotes=True,
                   comment='URL to the layer\'s metadata')
#
#  Layer Style
# xpath = r'/WMS_Capabilities/Capability/Layer/Layer/Style'
# xpath = xpath.replace('/', '/default:')
# styles = root.xpath(xpath, namespaces=nsdict)
# for style in styles:
#     style_name = style.xpath('default:Name', namespaces=nsdict)[0].text
#     write_line_to_list(map_file_list,
#                        tabs=3,
#                        parameter='\"wms_style\"',
#                        value=style_name,
#                        quotes=True,
#                        comment='The LegendURL style name')
#     style_width = style.xpath('default:LegendURL', namespaces=nsdict)[0].attrib['width']
#     write_line_to_list(map_file_list,
#                        tabs=3,
#                        parameter='\"wms_style_{}_legendurl_width\"'.format(style_name),
#                        value=style_width,
#                        quotes=True,
#                        comment='The width of the legend image in pixels')
#     style_height = style.xpath('default:LegendURL', namespaces=nsdict)[0].attrib['height']
#     write_line_to_list(map_file_list,
#                        tabs=3,
#                        parameter='\"wms_style_{}_legendurl_height\"'.format(style_name),
#                        value=style_height,
#                        quotes=True,
#                        comment='The height of the legend image in pixels')
#     style_format = style.xpath('default:LegendURL/default:Format', namespaces=nsdict)[0].text
#     write_line_to_list(map_file_list,
#                        tabs=3,
#                        parameter='\"wms_style_{}_legendurl_format\"'.format(style_name),
#                        value=style_format,
#                        quotes=True,
#                        comment='The file format MIME type of the legend image')
#     style_onlineresource = style.xpath('default:LegendURL/default:OnlineResource', namespaces=nsdict)[0].attrib['{'+nsdict['xlink']+'}href']
#     write_line_to_list(map_file_list,
#                        tabs=3,
#                        parameter='\"wms_style_{}_legendurl_href\"'.format(style_name),
#                        value=style_onlineresource,
#                        quotes=True,
#                        comment='The URL to the layer\'s legend')
#
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='END',
                   comment='End of layer metadata')
#
# Layer data type
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='TYPE',
                   value='RASTER',
                   comment='Layer data type')
#
# Layer status
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='STATUS',
                   value='OFF',
                   comment='Layer status')
#
# Layer data
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='DATA',
                   value='LCM2007_GB_25M_V2.tif',
                   quotes=True,
                   comment='Layer data')
#
# Layer projection
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='PROJECTION',
                   comment='Layer projection')
write_line_to_list(map_file_list,
                   tabs=3,
                   parameter='\"init={}\"'.format(DEFAULT_PROJECTION).lower(),
                   comment='')
write_line_to_list(map_file_list,
                   tabs=2,
                   parameter='END',
                   comment='End of Layer projection')
#
write_line_to_list(map_file_list,
                   tabs=1,
                   parameter='END',
                   comment='End of Layer object')
#
write_line_to_list(map_file_list,
                   tabs=0,
                   parameter='END',
                   comment='End of Map Object')


# print('{}{}'.format('\n' * 5, map_file_list))


widths = [max(map(len, col)) for col in zip(*map_file_list)[1:]]
if widths[1] > 100:
    widths[1] = 120
    print('\n\nwidths:\t{}'.format(widths))


max_tab = max([i[0] for i in map_file_list])


# Open MapServer .map file to be written to
map_file = open(map_file_filename, mode='w')


print('\n')
for row in map_file_list:
    line = '\t' * row[0] + \
           row[1].ljust(widths[0] + ((max_tab - row[0]) * tab_size)) + \
           '\t' + \
           row[2].ljust(widths[1]) + \
           '\t' + \
           row[3].strip() + \
           '\n'
    map_file.write(line)


# Close MapServer .map file
map_file.close()


# Copy map file into Vagrant MapServer machine maps folder (to test WMS GetCapabilities created by MapServer in Vagrant VM)
vagrant_maps_folder = r'E:\vmachines\mapserver-vagrant\maps'
shutil.copy2(map_file_filename, vagrant_maps_folder)


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {} to exceute this.'.format(hms_string(end_time - start_time)))
print('\n\nDone.\n')
