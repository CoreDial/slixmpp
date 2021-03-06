"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of Slixmpp.

    See the file LICENSE for copying permissio
"""

import datetime as dt

from slixmpp.jid import JID
from slixmpp.xmlstream import ElementBase, ET
from slixmpp.plugins import xep_0082


class MAM(ElementBase):
    name = 'query'
    namespace = 'urn:xmpp:mam:tmp'
    plugin_attrib = 'mam'
    interfaces = {'queryid', 'start', 'end', 'with', 'results'}
    sub_interfaces = {'start', 'end', 'with'}

    def setup(self, xml=None):
        ElementBase.setup(self, xml)
        self._results = []

    def get_start(self):
        timestamp = self._get_sub_text('start')
        return xep_0082.parse(timestamp)

    def set_start(self, value):
        if isinstance(value, dt.datetime):
            value = xep_0082.format_datetime(value)
        self._set_sub_text('start', value)

    def get_end(self):
        timestamp = self._get_sub_text('end')
        return xep_0082.parse(timestamp)

    def set_end(self, value):
        if isinstance(value, dt.datetime):
            value = xep_0082.format_datetime(value)
        self._set_sub_text('end', value)

    def get_with(self):
        return JID(self._get_sub_text('with'))

    def set_with(self, value):
        self._set_sub_text('with', str(value))

    # The results interface is meant only as an easy
    # way to access the set of collected message responses
    # from the query.

    def get_results(self):
        return self._results

    def set_results(self, values):
        self._results = values

    def del_results(self):
        self._results = []


class Preferences(ElementBase):
    name = 'prefs'
    namespace = 'urn:xmpp:mam:tmp'
    plugin_attrib = 'mam_prefs'
    interfaces = {'default', 'always', 'never'}
    sub_interfaces = {'always', 'never'}

    def get_always(self):
        results = set()

        jids = self.xml.findall('{%s}always/{%s}jid' % (
            self.namespace, self.namespace))

        for jid in jids:
            results.add(JID(jid.text))

        return results

    def set_always(self, value):
        self._set_sub_text('always', '', keep=True)
        always = self.xml.find('{%s}always' % self.namespace)
        always.clear()

        if not isinstance(value, (list, set)):
            value = [value]

        for jid in value:
            jid_xml = ET.Element('{%s}jid' % self.namespace)
            jid_xml.text = str(jid)
            always.append(jid_xml)

    def get_never(self):
        results = set()

        jids = self.xml.findall('{%s}never/{%s}jid' % (
            self.namespace, self.namespace))

        for jid in jids:
            results.add(JID(jid.text))

        return results

    def set_never(self, value):
        self._set_sub_text('never', '', keep=True)
        never = self.xml.find('{%s}never' % self.namespace)
        never.clear()

        if not isinstance(value, (list, set)):
            value = [value]

        for jid in value:
            jid_xml = ET.Element('{%s}jid' % self.namespace)
            jid_xml.text = str(jid)
            never.append(jid_xml)


class Result(ElementBase):
    name = 'result'
    namespace = 'urn:xmpp:mam:tmp'
    plugin_attrib = 'mam_result'
    interfaces = {'queryid', 'id'}


class Archived(ElementBase):
    name = 'archived'
    namespace = 'urn:xmpp:mam:tmp'
    plugin_attrib = 'mam_archived'
    plugin_multi_attrib = 'mam_archives'
    interfaces = {'by', 'id'}

    def get_by(self):
        return JID(self._get_attr('by'))

    def set_by(self, value):
        return self._set_attr('by', str(value))
