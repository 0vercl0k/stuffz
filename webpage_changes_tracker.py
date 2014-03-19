#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    webpage_changes_tracker.py - A simple script to track the modification of a web page
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import difflib
import urllib2
import time
import smtplib
import ConfigParser
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders
from urlparse import urlparse
from hashlib import sha1

class SMTPReportEmailer():
    """Send basic email through a SMTP SSL server"""
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.password = pwd

    def send(self, destination, subject, content, html_diff, new_file):
        """Send an email with 2 attached html files"""
        server = smtplib.SMTP_SSL(self.host, self.port)
        server.login(self.user, self.password)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = destination

        msg.attach(MIMEText(content))

        elems = {
            'diff.html' : html_diff,
            'new.html' : new_file
        }

        for name, content in elems.iteritems():
            m = MIMEBase('text', 'html')
            m.set_payload(content)
            Encoders.encode_base64(m)
            m.add_header('Content-Disposition', 'attachment; filename="%s"' % name)
            msg.attach(m)

        server.sendmail(self.user, destination, msg.as_string())
        server.quit()

class WebPageChangesTracker():
    """Track the changes of a webpage (if you have ads on it, forget this script :])"""
    def __init__(self, url, smtp_emailer = None, to = None, base_path = 'tracking'):
        self.url = url

        url_info = urlparse(url)
        self.page_name = url_info.path.replace('/', '_')

        # This is the path of the directory where we'll store the content of the pages
        # Pages from the same DNS will be stored in the same directory
        self.tracking_content_path = os.path.join(base_path, url_info.netloc)

        # This is the path of the page we are tracking
        self.tracking_page_path = os.path.join(self.tracking_content_path, self.page_name)

        # Now create the directories if they don't exist
        if os.path.isdir(base_path) == False:
            os.mkdir(base_path)

        if os.path.isdir(self.tracking_content_path) == False:
            os.mkdir(self.tracking_content_path)

        # Is it the first time we track this page ? Is a page content already exists ?
        if os.path.isfile(self.tracking_page_path) == False:
            # We need to grab the content of the page
            with open(self.tracking_page_path, 'w') as page:
                data = ''
                do_we_raise = False
                # If the website is not yet online, create a dumb file, this way you will be noticed
                # when it will be up!
                try:
                    data = urllib2.urlopen(self.url).read()
                except:
                    do_we_raise = True

                page.write(data)
                if do_we_raise:
                    raise Exception('Not online yet')

        # Now we need to have the SHA1 of the file, in order to find differences without diffing
        self.page_sha1 = self._get_page_sha1()

        self.to = to
        self.smtp_emailer = smtp_emailer

        # Is the report emailing activated ?
        if smtp_emailer != None:
            assert(isinstance(smtp_emailer, SMTPReportEmailer))
            assert(to != None)

    def _get_page_sha1(self):
        """Give the SHA1 of the file we are tracking"""
        page_sha1 = ''
        with open(self.tracking_page_path, 'r') as page:
            page_sha1 = sha1(page.read()).digest()
        return page_sha1

    def _diff_page_with_url(self, new_data):
        """Do the diffing between the content of the file we track and some data"""
        diff_content = None
        with open(self.tracking_page_path, 'r') as page:
            page_data = page.read().splitlines(1)
            new_data = new_data.splitlines(1)

            # Now we are going to diff the two contents
            # and generate a very nice html report \o/
            differ = difflib.HtmlDiff()

            diff_content = differ.make_file(
                page_data,
                new_data,
                '%s.old' % self.page_name,
                '%s.new' % self.page_name
            )

        return diff_content

    def check(self):
        """Check if the content has been changed"""
        # First step is to get the url
        req = urllib2.Request(
            self.url,
            None,
            { 'User-Agent' : 'Mozilla/5.0' }
        )
        new_data = urllib2.urlopen(req).read()

        # Now we compute its sha1
        data_sha1 = sha1(new_data).digest()

        # If the two sha1 are equal, it's good
        if data_sha1 == self.page_sha1:
            return

        # Else we need to see the difference
        diff_content = self._diff_page_with_url(new_data)

        # Now we got the diffing file, we are going to write it
        # But first, we have to generate a unique report name
        report_path = os.path.join(
            self.tracking_content_path,
            '%s-%s-diff.html' % (self.page_name, time.time())
        )

        # Write it
        with open(report_path, 'w') as report:
            report.write(diff_content)

        # OK now we can update the content we store
        with open(self.tracking_page_path, 'w') as page:
            page.write(new_data)

        if self.smtp_emailer == None:
            return

        # Send an email if we have configured an SMTP account
        mail_content = '''Hi,
A change in %s has been spotted.
You will find, attached to this email, the HTML report showing the differences between the old and the new version
and the new HTML file.
Have a nice day!''' % self.url
        
        self.smtp_emailer.send(
            self.to,
            '[WEBPAGE CHANGE in %s]' % self.url,
            mail_content,
            diff_content,
            new_data
        )


def main(argc, argv):
    # It works perfectly with a little crontab entry:
    # */5 * * * * /home/overclok/scripts/webpage_changes_tracker.py
    urls = map(
        lambda s: s.strip(),
        open('urls_to_track', 'r').readlines()
    )

    parser = ConfigParser.ConfigParser()
    if len(parser.read('email_account.cfg')) == 0:
        parser.add_section('smtp')
        parser.add_section('notified')
        parser.set('smtp', 'address', 'smtp.gmail.com')
        parser.set('smtp', 'port', 445)
        parser.set('smtp', 'username', 'testing@gmail.com')
        parser.set('smtp', 'password', 'el8')
        parser.set('notified', 'address', 'youraddress@gmail.com')
        parser.write(open('email_account.cfg', 'w'))
        print 'Fill your .cfg file now!'
        return 0

    emailer = SMTPReportEmailer(
        parser.get('smtp', 'address'),
        parser.getint('smtp', 'port'),
        parser.get('smtp', 'username'),
        parser.get('smtp', 'password')
    )

    for url in urls:
        if url.startswith('#') or url == '':
            continue

        print url
        try:
            WebPageChangesTracker(
                url,
                emailer,
                parser.get('notified', 'address')
            ).check()
        except Exception, e:
            print '%s is not yet online (%r).' % (url, e)

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))