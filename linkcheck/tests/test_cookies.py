# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Test cookie routines.
"""

import unittest
import linkcheck.cookies


class TestCookies (unittest.TestCase):
    """
    Test list dictionary routines.
    """

    def test_netscape_cookie1 (self):
        data = (
            ("Foo", "Bar"),
            ("Comment", "justatest"),
            ("Max-Age", "1000"),
            ("Path", "/"),
            ("Version", "1"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.NetscapeCookie(value, scheme, host, path)
        self.assert_(cookie.check_expired())
        self.assert_(cookie.is_valid_for("http", host, 80, "/"))
        self.assert_(cookie.is_valid_for("https", host, 443, "/a"))

    def test_netscape_cookie2 (self):
        data = (
            ("Foo", "Bar"),
            ("Comment", "justatest"),
            ("Max-Age", "0"),
            ("Path", "/"),
            ("Version", "1"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.NetscapeCookie(value, scheme, host, path)
        self.assert_(cookie.is_expired())

    def test_netscape_cookie3 (self):
        data = (
            ("Foo", "Bar\""),
            ("Port", "hul,la"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        self.assertRaises(linkcheck.cookies.CookieError,
                 linkcheck.cookies.NetscapeCookie, value, scheme, host, path)

    def test_netscape_cookie4 (self):
        data = (
            ("Foo", "Bar\""),
            ("Domain", "localhost"),
            ("Port", "100,555,76"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.NetscapeCookie(value, scheme, host, path)

    def test_netscape_cookie5 (self):
        data = (
            ("Foo", "Bar"),
            ("Domain", "example.org"),
            ("Expires", "Wed, 12-Dec-2001 19:27:57 GMT"),
            ("Path", "/"),
        )
        # note: values are without quotes
        parts = ['%s=%s' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "example.org"
        path = "/"
        cookie = linkcheck.cookies.NetscapeCookie(value, scheme, host, path)
        self.assert_(cookie.is_expired())

    def test_rfc_cookie1 (self):
        data = (
            ("Foo", "Bar"),
            ("Comment", "justatest"),
            ("Max-Age", "1000"),
            ("Path", "/"),
            ("Version", "1"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.Rfc2965Cookie(value, scheme, host, path)
        self.assert_(cookie.check_expired())
        self.assert_(cookie.is_valid_for("http", host, 80, "/"))
        self.assert_(cookie.is_valid_for("https", host, 443, "/a"))

    def test_rfc_cookie2 (self):
        data = (
            ("Foo", "Bar"),
            ("Comment", "justatest"),
            ("Max-Age", "0"),
            ("Path", "/"),
            ("Version", "1"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.Rfc2965Cookie(value, scheme, host, path)
        self.assert_(cookie.is_expired())

    def test_rfc_cookie3 (self):
        data = (
            ("Foo", "Bar\""),
            ("Port", "hul,la"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        self.assertRaises(linkcheck.cookies.CookieError,
                 linkcheck.cookies.Rfc2965Cookie, value, scheme, host, path)

    def test_rfc_cookie4 (self):
        data = (
            ("Foo", "Bar\""),
            ("Port", "100,555,76"),
        )
        parts = ['%s="%s"' % (key, value) for key, value in data]
        value = "; ".join(parts)
        scheme = "http"
        host = "localhost"
        path = "/"
        cookie = linkcheck.cookies.Rfc2965Cookie(value, scheme, host, path)

    def test_cookie_parse1 (self):
        lines = [
            'Host: example.org',
            'Path: /hello',
            'Set-cookie: ID="smee"',
            'Set-cookie: spam="egg"',
        ]
        from_headers = linkcheck.cookies.from_headers
        headers, scheme, host, path = from_headers("\r\n".join(lines))

    def test_cookie_parse2 (self):
        lines = [
            'Scheme: https',
            'Host: imaweevil.org',
            'Set-cookie: baggage="elitist"; comment="hologram"',
        ]
        from_headers = linkcheck.cookies.from_headers
        headers, scheme, host, path = from_headers("\r\n".join(lines))

    def test_cookie_parse3 (self):
        lines = [
            'Scheme: https',
        ]
        from_headers = linkcheck.cookies.from_headers
        self.assertRaises(ValueError, from_headers, "\r\n".join(lines))

    def test_cookie_parse4 (self):
        lines = [
            ' Host: imaweevil.org',
            'Set-cookie: baggage="elitist"; comment="hologram"',
        ]
        from_headers = linkcheck.cookies.from_headers
        self.assertRaises(ValueError, from_headers, "\r\n".join(lines))


def test_suite ():
    """
    Build and return a TestSuite.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCookies))
    return suite


if __name__ == '__main__':
    unittest.main()
