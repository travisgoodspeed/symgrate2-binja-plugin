

# httplib was renamed for Python3.
import http.client as httplib
import urllib.parse

class Symgrate2:
    """HTTP client for the Symgrate web API."""

    LEN=18

    def queryfn(raw):
        """Queries the server for the first bytes of ASCII armored machine language."""
        data=Symgrate2.queryfns("raw=%s"%raw);
        if data!=None and len(data)>2:
            return data.split(" ")[1].strip()
        return None;

    def queryfns(q):
        """Queries the server for the first bytes of ASCII armored machine language."""
        conn = httplib.HTTPConnection("symgrate.com",80)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        params=q
        try:
            params = urllib.parse.urlencode(q)  # Breaks in Python 3.9
        except TypeError:
            pass;

        #print(q+"\n")
        # FIXME, we should be taking bytes as raw instead of a string.
        conn.request("POST", "/fns", params, headers)
        
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
    
