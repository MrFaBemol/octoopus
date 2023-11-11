from urllib.parse import urlsplit, urlunsplit, quote
from odoo.addons.http_routing.models.ir_http import slug


def iri2uri(iri: str) -> str:
    """ Convert an IRI to a URI (Python 3) """
    uri = ''
    if isinstance(iri, str):
        (scheme, netloc, path, query, fragment) = urlsplit(iri)
        scheme = quote(scheme)
        netloc = netloc.encode('idna').decode('utf-8')
        path = quote(path)
        query = quote(query)
        fragment = quote(fragment)
        uri = urlunsplit((scheme, netloc, path, query, fragment))

    return uri


def slugged(value):
    res = slug(value).split('-')
    if len(res) > 1:
        res_id = res.pop()
        res.insert(0, res_id)

    return "-".join(res)

