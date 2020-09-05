import copy
import os
import tempfile

from dnslib import QTYPE, RCODE, RR, TXT
from dnslib.server import BaseResolver


class ZoneResolver(BaseResolver):
    """
    Simple fixed zone file resolver.
    """

    def __init__(self, zone, glob=False):
        """
        Initialise resolver from zone file.
        Stores RRs as a list of (label,type,rr) tuples
        If 'glob' is True use glob match against zone file
        """
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr) for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = "matchGlob" if glob else "__eq__"

    def resolve(self, request, handler):
        """
        Respond to DNS request - parameters are request packet & handler.
        Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        if qtype == "TXT":
            txtpath = os.path.join(tempfile.gettempdir(), str(qname).lower())
            if os.path.isfile(txtpath):
                reply.add_answer(
                    RR(qname, QTYPE.TXT, rdata=TXT(open(txtpath).read().strip()))
                )
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname, self.eq)(name) and (
                qtype == rtype or qtype == "ANY" or rtype == "CNAME"
            ):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ["CNAME", "NS", "MX", "PTR"]:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in ["A", "AAAA"]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply
