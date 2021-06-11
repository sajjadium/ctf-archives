import urllib
import sys
import urlparse
import os
import time
import types
import shutil

from string import joinfields, split, lower
from xml.dom import minidom
domimpl = minidom.getDOMImplementation()

BUFFER_SIZE = 128 * 1000

class Resource(object):
    # XXX this class is ugly
    def __init__(self, fp, file_size):
        self.__fp = fp
        self.__file_size = file_size

    def __len__(self):
        return self.__file_size

    def __iter__(self):
        while 1:
            data = self.__fp.read(BUFFER_SIZE)
            if not data:
                break
            yield data
            time.sleep(0.005)
        self.__fp.close()

    def read(self, length = 0):
        if length == 0:
            length = self.__file_size

        data = self.__fp.read(length)
        return data


class FilesystemHandler():

    def __init__(self, directory, uri, verbose=False):
        self.setDirectory(directory)
        self.setBaseURI(uri)
        self.verbose = verbose

    def setDirectory(self, path):

        if not os.path.isdir(path):
            raise Exception, '%s must be a directory!' % path

        self.directory = os.path.normpath(path)

    def setBaseURI(self, uri):

        if uri:
            self.baseuri = uri
        else:
            self.baseuri = '/'

    def uri2local(self,uri):

        path = os.path.normpath(uri) + '/'
        if path.startswith(self.baseuri):
            path = path[len(self.baseuri):]
        filepath = os.path.join(self.directory, path)
        filepath = os.path.normpath(filepath)
        return filepath

    def local2uri(self,filepath):
        """ map local path to file to self.baseuri """
        filepath = os.path.normpath(filepath)
        if filepath.startswith(self.directory):
            uri = filepath[len(self.directory):]
        uri = os.path.normpath(self.baseuri + uri)
        #print('local2uri: %s -> %s' % (filepath, uri))
        return uri

    def get_children(self, uri, filter=None):
        """ return the child objects as self.baseuris for the given URI """

        fileloc=self.uri2local(uri)
        filelist=[]

        if os.path.exists(fileloc):
            if os.path.isdir(fileloc):
                try:
                    files=os.listdir(fileloc)
                except Exception:
                    raise ValueError

                for file in files:
                    newloc=os.path.join(fileloc,file)
                    filelist.append(self.local2uri(newloc))
        return filelist

    def get_data(self,uri, range = None):
        """ return the content of an object """

        path=self.uri2local(uri)
        if os.path.exists(path):
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                if range == None:
                    fp=open(path,"r")
                    return Resource(fp, file_size)
                else:
                    if range[1] == '':
                        range[1] = file_size
                    else:
                        range[1] = int(range[1])

                    if range[0] == '':
                        range[0] = file_size - range[1]
                    else:
                        range[0] = int(range[0])

                    if range[0] > file_size:
                        return 416

                    if range[1] > file_size:
                        range[1] = file_size

                    fp = open(path, "r")
                    fp.seek(range[0])
                    return Resource(fp, range[1] - range[0])
            elif os.path.isdir(path):
                # GET for collections is defined as 'return s/th meaningful' :-)
                from StringIO import StringIO
                stio = StringIO('Directory at %s' % uri)
                return Resource(StringIO('Directory at %s' % uri), stio.len)
            else:
                pass
                # also raise an error for collections
                # don't know what should happen then..

        return 404


    def put(self, uri, data, content_type=None):
        """ put the object into the filesystem """
        path=self.uri2local(uri)
        try:
            fp=open(path, "w+")
            if isinstance(data, types.GeneratorType):
                for d in data:
                    fp.write(d)
            else:
                if data:
                    fp.write(data)
            fp.close()
            status = 201
        except:
            status = 424

        return status

    def mkcol(self,uri):
        """ create a new collection """
        path=self.uri2local(uri)

        # remove trailing slash
        if path[-1]=="/": path=path[:-1]

        # test if file already exists
        if os.path.exists(path):
            return 405

        # test if parent exists
        h,t=os.path.split(path)
        if not os.path.exists(h):
            return 409

        # test, if we are allowed to create it
        try:
            os.mkdir(path)
            return 201
        # No space left
        except IOError:
            return 507
        except:
            return 403

def parse_propfind(xml_doc):
    """
    Parse an propfind xml file and return a list of props
    """

    doc = minidom.parseString(xml_doc)

    request_type=None
    props={}
    namespaces=[]

    if doc.getElementsByTagNameNS("DAV:", "allprop"):
        request_type = "RT_ALLPROP"
    elif doc.getElementsByTagNameNS("DAV:", "propname"):
        request_type = "RT_PROPNAME"
    else:
        request_type = "RT_PROP"
        for i in doc.getElementsByTagNameNS("DAV:", "prop"):
            for e in i.childNodes:
                if e.nodeType != minidom.Node.ELEMENT_NODE:
                    continue
                ns = e.namespaceURI
                ename = e.localName
                if props.has_key(ns):
                    props[ns].append(ename)
                else:
                    props[ns]=[ename]
                    namespaces.append(ns)

    return request_type, props, namespaces

class PropfindProcessor:
    """ parse a propfind xml element and extract props

    It will set the following instance vars:

    request_class   : ALLPROP | PROPNAME | PROP
    proplist    : list of properties
    nsmap       : map of namespaces

    The list of properties will contain tuples of the form
    (element name, ns_prefix, ns_uri)

    """

    def __init__(self, uri, dataclass, depth, body):
        self.request_type = None
        self.nsmap = {}
        self.proplist = {}
        self.default_ns = None
        self._depth = str(depth)

        self._uri = uri.rstrip('/')

        self._has_body = None   # did we parse a body?
        self._dataclass = dataclass

        if body:
            self.request_type, self.proplist, self.namespaces = \
                parse_propfind(body)
            self._has_body = True

    def create_response(self):
        """ Create the multistatus response

        This will be delegated to the specific method
        depending on which request (allprop, propname, prop)
        was found.

        If we get a PROPNAME then we simply return the list with empty
        values which we get from the interface class

        If we get an ALLPROP we first get the list of properties and then
        we do the same as with a PROP method.

        """

        # check if resource exists
        localpath = self._dataclass.uri2local(self._uri)

        if not os.path.exists(localpath):
            raise IOError

        if self.request_type == 2: # propname
            df = self.create_propname()

        elif self.request_type == 3: # prop
            df = self.create_prop()

        else: # allprop
            df = self.create_allprop()

        return df

    def get_propnames(self):
        """ return the property names allowed """

        # defined properties ; format is namespace: [list of properties]
        return { "DAV:" : ('creationdate',
                           #'displayname',
                           #'getcontentlanguage',
                           'getcontentlength',
                           #'getcontenttype',
                           #'getetag',
                           'getlastmodified',
                           #'lockdiscovery',
                           'resourcetype',
                           #'source',
                           #'supportedlock'
                          )
                 }

    def get_prop(self, path, ns, propname):
        """ return the value of a given property

        uri        -- uri of the object to get the property of
        ns        -- namespace of the property
        pname        -- name of the property
        """

        info = os.stat(path)

        if propname == 'creationdate':
            response = info[9]
        elif propname == 'getlastmodified':
            response = info[8]
        elif propname == 'getcontentlength':
            response = '0' if not os.path.isfile(path) else str(info[6])
        elif propname == 'resourcetype':
            response = int(os.path.isfile(path))

        return str(response)

    def create_propname(self):
        """ create a multistatus response for the prop names """

        dc = self._dataclass
        # create the document generator
        doc = domimpl.createDocument(None, "multistatus", None)
        ms = doc.documentElement
        ms.setAttribute("xmlns:D", "DAV:")
        ms.tagName = 'D:multistatus'

        if self._depth == "0":
            pnames = self.get_propnames()
            re = self.mk_propname_response(self._uri, pnames, doc)
            ms.appendChild(re)

        elif self._depth == "1":
            pnames = self.get_propnames()
            re = self.mk_propname_response(self._uri, pnames, doc)
            ms.appendChild(re)

            for newuri in dc.get_children(self._uri):
                pnames = self.get_propnames()
                re = self.mk_propname_response(newuri, pnames, doc)
                ms.appendChild(re)

        else:
            uri_list = [self._uri]
            while uri_list:
                uri = uri_list.pop()
                pnames = self.get_propnames()
                re = self.mk_propname_response(uri, pnames, doc)
                ms.appendChild(re)
                uri_childs = self._dataclass.get_children(uri)
                if uri_childs:
                    uri_list.extend(uri_childs)

        return doc.toxml(encoding="utf-8")

    def create_allprop(self):
        """ return a list of all properties """
        self.proplist = {}
        self.namespaces = []
        for ns, plist in self.get_propnames().items():
            self.proplist[ns] = plist
            self.namespaces.append(ns)

        return self.create_prop()

    def create_prop(self):
        """ handle a <prop> request

        This will

        1. set up the <multistatus>-Framework

        2. read the property values for each URI
           (which is dependant on the Depth header)
           This is done by the get_propvalues() method.

        3. For each URI call the append_result() method
           to append the actual <result>-Tag to the result
           document.

        We differ between "good" properties, which have been
        assigned a value by the interface class and "bad"
        properties, which resulted in an error, either 404
        (Not Found) or 403 (Forbidden).

        """
        # create the document generator
        doc = domimpl.createDocument(None, "multistatus", None)
        ms = doc.documentElement
        ms.setAttribute("xmlns:D", "DAV:")
        ms.tagName = 'D:multistatus'

        if self._depth == "0":
            gp, bp = self.get_propvalues(self._uri)
            res = self.mk_prop_response(self._uri, gp, bp, doc)
            ms.appendChild(res)

        elif self._depth == "1":
            gp, bp = self.get_propvalues(self._uri)
            res = self.mk_prop_response(self._uri, gp, bp, doc)
            ms.appendChild(res)

            for newuri in self._dataclass.get_children(self._uri):
                gp, bp = self.get_propvalues(newuri)
                res = self.mk_prop_response(newuri, gp, bp, doc)
                ms.appendChild(res)
        elif self._depth == 'infinity':
            uri_list = [self._uri]
            while uri_list:
                uri = uri_list.pop()
                gp, bp = self.get_propvalues(uri)
                res = self.mk_prop_response(uri, gp, bp, doc)
                ms.appendChild(res)
                uri_childs = self._dataclass.get_children(uri)
                if uri_childs:
                    uri_list.extend(uri_childs)

        return doc.toxml(encoding="utf-8")

    def mk_propname_response(self, uri, propnames, doc):
        """ make a new <prop> result element for a PROPNAME request

        This will simply format the propnames list.
        propnames should have the format {NS1 : [prop1, prop2, ...], NS2: ...}

        """
        re = doc.createElement("D:response")

        if self._dataclass.baseuri:
            uri = self._dataclass.baseuri + '/' + '/'.join(uri.split('/')[3:])

        # write href information
        uparts = urlparse.urlparse(uri)
        fileloc = uparts[2]
        href = doc.createElement("D:href")

        huri = doc.createTextNode(uparts[0] + '://' +
                                  '/'.join(uparts[1:2]) +
                                  urllib.quote(fileloc))
        href.appendChild(huri)
        re.appendChild(href)

        ps = doc.createElement("D:propstat")
        nsnum = 0

        for ns, plist in propnames.items():
            # write prop element
            pr = doc.createElement("D:prop")
            nsp = "ns" + str(nsnum)
            pr.setAttribute("xmlns:" + nsp, ns)
            nsnum += 1

            # write propertynames
            for p in plist:
                pe = doc.createElement(nsp + ":" + p)
                pr.appendChild(pe)

            ps.appendChild(pr)
        re.appendChild(ps)

        return re

    def mk_prop_response(self, uri, good_props, bad_props, doc):
        """ make a new <prop> result element

        We differ between the good props and the bad ones for
        each generating an extra <propstat>-Node (for each error
        one, that means).

        """
        re = doc.createElement("D:response")
        # append namespaces to response
        nsnum = 0
        for nsname in self.namespaces:
            if nsname != 'DAV:':
                re.setAttribute("xmlns:ns" + str(nsnum), nsname)
            nsnum += 1

        if self._dataclass.baseuri:
            uri = urlparse.urljoin(self._dataclass.baseuri, uri)
        # write href information
        uparts = urlparse.urlparse(uri)
        fileloc = uparts[2]
        href = doc.createElement("D:href")

        huri = doc.createTextNode(uparts[0] + '://' +
                                  '/'.join(uparts[1:2]) +
                                  urllib.quote(fileloc))
        href.appendChild(huri)
        re.appendChild(href)

        # write good properties
        ps = doc.createElement("D:propstat")
        if good_props:
            re.appendChild(ps)

        gp = doc.createElement("D:prop")
        for ns in good_props.keys():
            if ns != 'DAV:':
                ns_prefix = "ns" + str(self.namespaces.index(ns)) + ":"
            else:
                ns_prefix = 'D:'
            for p, v in good_props[ns].items():

                pe = doc.createElement(ns_prefix + str(p))
                if isinstance(v, minidom.Element):
                    pe.appendChild(v)
                elif isinstance(v, list):
                    for val in v:
                        pe.appendChild(val)
                else:
                    if p == "resourcetype":
                        if v == 1:
                            ve = doc.createElement("D:collection")
                            pe.appendChild(ve)
                    else:
                        ve = doc.createTextNode(v)
                        pe.appendChild(ve)

                gp.appendChild(pe)

        ps.appendChild(gp)
        s = doc.createElement("D:status")
        t = doc.createTextNode("HTTP/1.1 200 OK")
        s.appendChild(t)
        ps.appendChild(s)
        re.appendChild(ps)

        # now write the errors!
        if len(bad_props.items()):

            # write a propstat for each error code
            for ecode in bad_props.keys():
                ps = doc.createElement("D:propstat")
                re.appendChild(ps)
                bp = doc.createElement("D:prop")
                ps.appendChild(bp)

                for ns in bad_props[ecode].keys():
                    if ns != 'DAV:':
                        ns_prefix = "ns" + str(self.namespaces.index(ns)) + ":"
                    else:
                        ns_prefix = 'D:'

                    for p in bad_props[ecode][ns]:
                        pe = doc.createElement(ns_prefix + str(p))
                        bp.appendChild(pe)

                s = doc.createElement("D:status")
                t = doc.createTextNode("HTTP/1.1 %s" % (ecode))
                s.appendChild(t)
                ps.appendChild(s)
                re.appendChild(ps)

        # return the new response element
        return re

    def get_propvalues(self, uri):
        """ create lists of property values for an URI

        We create two lists for an URI: the properties for
        which we found a value and the ones for which we
        only got an error, either because they haven't been
        found or the user is not allowed to read them.

        """
        good_props = {}
        bad_props = {}

        path = self._dataclass.uri2local(uri)
        ddc = self._dataclass
        for ns, plist in self.proplist.items():
            good_props[ns] = {}
            for prop in plist:
                ec = 0
                try:
                    r = self.get_prop(path, ns, prop)
                    good_props[ns][prop] = r
                except UnboundLocalError, error_code:
                    ec = error_code[0]

                # ignore props with error_code if 0 (invisible)
                if ec == 0:
                    continue

                if ec in bad_props:
                    if ns in bad_props[ec]:
                        bad_props[ec][ns].append(prop)
                    else:
                        bad_props[ec][ns] = [prop]
                else:
                    bad_props[ec] = {ns: [prop]}

        return good_props, bad_props

