

# httplib was renamed for Python3.
import http.client as httplib
import urllib.parse

class Symgrate2:
    """HTTP client for the Symgrate web API."""

    LEN=18

    def queryfn(raw):
        """Queries the server for the first bytes of ASCII armored machine language."""

        conn = httplib.HTTPConnection("symgrate.com",80)
    
        conn.request("GET", "/fn?raw="+raw)
        
        r1 = conn.getresponse()
        #print r1.status, r1.reason
        # 200 OK ?
        toret=None
        if r1.status==200:
            data = r1.read()
            if len(data)>2:
                toret=data.split(b" ")[0].decode("utf-8")

        # TODO: This would go a little faster if we reused the socket.
        conn.close()
        return toret

    def queryfns(q):
        """Queries the server for the first bytes of ASCII armored machine language."""

        conn = httplib.HTTPConnection("symgrate.com",80)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        params = urllib.parse.urlencode(q)

        #print(q+"\n")
        conn.request("POST", "/fns", params, headers)  # FIXME, we should be taking bytes as raw instead of a string.
        
        r1 = conn.getresponse()
        #print r1.status, r1.reason
        # 200 OK ?
        toret=None
        if r1.status==200:
            data = r1.read()
            if len(data)>2:
                toret=data.decode("utf-8")

        # TODO: This would go a little faster if we reused the socket.
        conn.close()
        return toret

