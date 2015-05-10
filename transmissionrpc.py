'''Taken from: https://bitbucket.org/blueluna/transmissionrpc/wiki/Home
Transformed the module in a single file to be more portable & easier to use'''
# -*- coding: utf-8 -*-
# Copyright (c) 2008-2013 Erik Svensson <erik.public@gmail.com>
# Licensed under the MIT license.

import re
import time
import operator
import warnings
import os
import socket
import datetime
import sys
import base64
import json
import logging

from six import iteritems, string_types, integer_types, PY3, text_type
from collections import namedtuple
from six import string_types, iteritems

if PY3:
    from urllib.parse import urlparse
    from urllib.request import urlopen
    from urllib.request import Request, build_opener, \
        HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, HTTPDigestAuthHandler
    from urllib.error import HTTPError, URLError
    from http.client import BadStatusLine
else:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib2 import Request, build_opener, \
        HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, HTTPDigestAuthHandler
    from urllib2 import HTTPError, URLError
    from httplib import BadStatusLine

LOGGER = logging.getLogger('transmissionrpc')
LOGGER.setLevel(logging.ERROR)

def mirror_dict(source):
    """
    Creates a dictionary with all values as keys and all keys as values.
    """
    source.update(dict((value, key) for key, value in iteritems(source)))
    return source

DEFAULT_PORT = 9091

DEFAULT_TIMEOUT = 30.0

TR_PRI_LOW    = -1
TR_PRI_NORMAL =  0
TR_PRI_HIGH   =  1

PRIORITY = mirror_dict({
    'low'    : TR_PRI_LOW,
    'normal' : TR_PRI_NORMAL,
    'high'   : TR_PRI_HIGH
})

TR_RATIOLIMIT_GLOBAL    = 0 # follow the global settings
TR_RATIOLIMIT_SINGLE    = 1 # override the global settings, seeding until a certain ratio
TR_RATIOLIMIT_UNLIMITED = 2 # override the global settings, seeding regardless of ratio

RATIO_LIMIT = mirror_dict({
    'global'    : TR_RATIOLIMIT_GLOBAL,
    'single'    : TR_RATIOLIMIT_SINGLE,
    'unlimited' : TR_RATIOLIMIT_UNLIMITED
})

TR_IDLELIMIT_GLOBAL     = 0 # follow the global settings
TR_IDLELIMIT_SINGLE     = 1 # override the global settings, seeding until a certain idle time
TR_IDLELIMIT_UNLIMITED  = 2 # override the global settings, seeding regardless of activity

IDLE_LIMIT = mirror_dict({
    'global'    : TR_RATIOLIMIT_GLOBAL,
    'single'    : TR_RATIOLIMIT_SINGLE,
    'unlimited' : TR_RATIOLIMIT_UNLIMITED
})

# A note on argument maps
# These maps are used to verify *-set methods. The information is structured in
# a tree.
# set +- <argument1> - [<type>, <added version>, <removed version>, <previous argument name>, <next argument name>, <description>]
#  |  +- <argument2> - [<type>, <added version>, <removed version>, <previous argument name>, <next argument name>, <description>]
#  |
# get +- <argument1> - [<type>, <added version>, <removed version>, <previous argument name>, <next argument name>, <description>]
#     +- <argument2> - [<type>, <added version>, <removed version>, <previous argument name>, <next argument name>, <description>]

# Arguments for torrent methods
TORRENT_ARGS = {
    'get' : {
        'activityDate':                 ('number', 1, None, None, None, 'Last time of upload or download activity.'),
        'addedDate':                    ('number', 1, None, None, None, 'The date when this torrent was first added.'),
        'announceResponse':             ('string', 1, 7, None, None, 'The announce message from the tracker.'),
        'announceURL':                  ('string', 1, 7, None, None, 'Current announce URL.'),
        'bandwidthPriority':            ('number', 5, None, None, None, 'Bandwidth priority. Low (-1), Normal (0) or High (1).'),
        'comment':                      ('string', 1, None, None, None, 'Torrent comment.'),
        'corruptEver':                  ('number', 1, None, None, None, 'Number of bytes of corrupt data downloaded.'),
        'creator':                      ('string', 1, None, None, None, 'Torrent creator.'),
        'dateCreated':                  ('number', 1, None, None, None, 'Torrent creation date.'),
        'desiredAvailable':             ('number', 1, None, None, None, 'Number of bytes avalable and left to be downloaded.'),
        'doneDate':                     ('number', 1, None, None, None, 'The date when the torrent finished downloading.'),
        'downloadDir':                  ('string', 4, None, None, None, 'The directory path where the torrent is downloaded to.'),
        'downloadedEver':               ('number', 1, None, None, None, 'Number of bytes of good data downloaded.'),
        'downloaders':                  ('number', 4, 7, None, None, 'Number of downloaders.'),
        'downloadLimit':                ('number', 1, None, None, None, 'Download limit in Kbps.'),
        'downloadLimited':              ('boolean', 5, None, None, None, 'Download limit is enabled'),
        'downloadLimitMode':            ('number', 1, 5, None, None, 'Download limit mode. 0 means global, 1 means signle, 2 unlimited.'),
        'error':                        ('number', 1, None, None, None, 'Kind of error. 0 means OK, 1 means tracker warning, 2 means tracker error, 3 means local error.'),
        'errorString':                  ('number', 1, None, None, None, 'Error message.'),
        'eta':                          ('number', 1, None, None, None, 'Estimated number of seconds left when downloading or seeding. -1 means not available and -2 means unknown.'),
        'etaIdle':                      ('number', 15, None, None, None, 'Estimated number of seconds left until the idle time limit is reached. -1 means not available and -2 means unknown.'),        
        'files':                        ('array', 1, None, None, None, 'Array of file object containing key, bytesCompleted, length and name.'),
        'fileStats':                    ('array', 5, None, None, None, 'Aray of file statistics containing bytesCompleted, wanted and priority.'),
        'hashString':                   ('string', 1, None, None, None, 'Hashstring unique for the torrent even between sessions.'),
        'haveUnchecked':                ('number', 1, None, None, None, 'Number of bytes of partial pieces.'),
        'haveValid':                    ('number', 1, None, None, None, 'Number of bytes of checksum verified data.'),
        'honorsSessionLimits':          ('boolean', 5, None, None, None, 'True if session upload limits are honored'),
        'id':                           ('number', 1, None, None, None, 'Session unique torrent id.'),
        'isFinished':                   ('boolean', 9, None, None, None, 'True if the torrent is finished. Downloaded and seeded.'),
        'isPrivate':                    ('boolean', 1, None, None, None, 'True if the torrent is private.'),
        'isStalled':                    ('boolean', 14, None, None, None, 'True if the torrent has stalled (been idle for a long time).'),
        'lastAnnounceTime':             ('number', 1, 7, None, None, 'The time of the last announcement.'),
        'lastScrapeTime':               ('number', 1, 7, None, None, 'The time af the last successful scrape.'),
        'leechers':                     ('number', 1, 7, None, None, 'Number of leechers.'),
        'leftUntilDone':                ('number', 1, None, None, None, 'Number of bytes left until the download is done.'),
        'magnetLink':                   ('string', 7, None, None, None, 'The magnet link for this torrent.'),
        'manualAnnounceTime':           ('number', 1, None, None, None, 'The time until you manually ask for more peers.'),
        'maxConnectedPeers':            ('number', 1, None, None, None, 'Maximum of connected peers.'),
        'metadataPercentComplete':      ('number', 7, None, None, None, 'Download progress of metadata. 0.0 to 1.0.'),
        'name':                         ('string', 1, None, None, None, 'Torrent name.'),
        'nextAnnounceTime':             ('number', 1, 7, None, None, 'Next announce time.'),
        'nextScrapeTime':               ('number', 1, 7, None, None, 'Next scrape time.'),
        'peer-limit':                   ('number', 5, None, None, None, 'Maximum number of peers.'),
        'peers':                        ('array', 2, None, None, None, 'Array of peer objects.'),
        'peersConnected':               ('number', 1, None, None, None, 'Number of peers we are connected to.'),
        'peersFrom':                    ('object', 1, None, None, None, 'Object containing download peers counts for different peer types.'),
        'peersGettingFromUs':           ('number', 1, None, None, None, 'Number of peers we are sending data to.'),
        'peersKnown':                   ('number', 1, 13, None, None, 'Number of peers that the tracker knows.'),
        'peersSendingToUs':             ('number', 1, None, None, None, 'Number of peers sending to us'),
        'percentDone':                  ('double', 5, None, None, None, 'Download progress of selected files. 0.0 to 1.0.'),
        'pieces':                       ('string', 5, None, None, None, 'String with base64 encoded bitfield indicating finished pieces.'),
        'pieceCount':                   ('number', 1, None, None, None, 'Number of pieces.'),
        'pieceSize':                    ('number', 1, None, None, None, 'Number of bytes in a piece.'),
        'priorities':                   ('array', 1, None, None, None, 'Array of file priorities.'),
        'queuePosition':                ('number', 14, None, None, None, 'The queue position.'),
        'rateDownload':                 ('number', 1, None, None, None, 'Download rate in bps.'),
        'rateUpload':                   ('number', 1, None, None, None, 'Upload rate in bps.'),
        'recheckProgress':              ('double', 1, None, None, None, 'Progress of recheck. 0.0 to 1.0.'),
        'secondsDownloading':           ('number', 15, None, None, None, ''),
        'secondsSeeding':               ('number', 15, None, None, None, ''),
        'scrapeResponse':               ('string', 1, 7, None, None, 'Scrape response message.'),
        'scrapeURL':                    ('string', 1, 7, None, None, 'Current scrape URL'),
        'seeders':                      ('number', 1, 7, None, None, 'Number of seeders reported by the tracker.'),
        'seedIdleLimit':                ('number', 10, None, None, None, 'Idle limit in minutes.'),
        'seedIdleMode':                 ('number', 10, None, None, None, 'Use global (0), torrent (1), or unlimited (2) limit.'),
        'seedRatioLimit':               ('double', 5, None, None, None, 'Seed ratio limit.'),
        'seedRatioMode':                ('number', 5, None, None, None, 'Use global (0), torrent (1), or unlimited (2) limit.'),
        'sizeWhenDone':                 ('number', 1, None, None, None, 'Size of the torrent download in bytes.'),
        'startDate':                    ('number', 1, None, None, None, 'The date when the torrent was last started.'),
        'status':                       ('number', 1, None, None, None, 'Current status, see source'),
        'swarmSpeed':                   ('number', 1, 7, None, None, 'Estimated speed in Kbps in the swarm.'),
        'timesCompleted':               ('number', 1, 7, None, None, 'Number of successful downloads reported by the tracker.'),
        'trackers':                     ('array', 1, None, None, None, 'Array of tracker objects.'),
        'trackerStats':                 ('object', 7, None, None, None, 'Array of object containing tracker statistics.'),
        'totalSize':                    ('number', 1, None, None, None, 'Total size of the torrent in bytes'),
        'torrentFile':                  ('string', 5, None, None, None, 'Path to .torrent file.'),
        'uploadedEver':                 ('number', 1, None, None, None, 'Number of bytes uploaded, ever.'),
        'uploadLimit':                  ('number', 1, None, None, None, 'Upload limit in Kbps'),
        'uploadLimitMode':              ('number', 1, 5, None, None, 'Upload limit mode. 0 means global, 1 means signle, 2 unlimited.'),
        'uploadLimited':                ('boolean', 5, None, None, None, 'Upload limit enabled.'),
        'uploadRatio':                  ('double', 1, None, None, None, 'Seed ratio.'),
        'wanted':                       ('array', 1, None, None, None, 'Array of booleans indicated wanted files.'),
        'webseeds':                     ('array', 1, None, None, None, 'Array of webseeds objects'),
        'webseedsSendingToUs':          ('number', 1, None, None, None, 'Number of webseeds seeding to us.'),
    },
    'set': {
        'bandwidthPriority':            ('number', 5, None, None, None, 'Priority for this transfer.'),
        'downloadLimit':                ('number', 5, None, 'speed-limit-down', None, 'Set the speed limit for download in Kib/s.'),
        'downloadLimited':              ('boolean', 5, None, 'speed-limit-down-enabled', None, 'Enable download speed limiter.'),
        'files-wanted':                 ('array', 1, None, None, None, "A list of file id's that should be downloaded."),
        'files-unwanted':               ('array', 1, None, None, None, "A list of file id's that shouldn't be downloaded."),
        'honorsSessionLimits':          ('boolean', 5, None, None, None, "Enables or disables the transfer to honour the upload limit set in the session."),
        'location':                     ('array', 1, None, None, None, 'Local download location.'),
        'peer-limit':                   ('number', 1, None, None, None, 'The peer limit for the torrents.'),
        'priority-high':                ('array', 1, None, None, None, "A list of file id's that should have high priority."),
        'priority-low':                 ('array', 1, None, None, None, "A list of file id's that should have normal priority."),
        'priority-normal':              ('array', 1, None, None, None, "A list of file id's that should have low priority."),
        'queuePosition':                ('number', 14, None, None, None, 'Position of this transfer in its queue.'),
        'seedIdleLimit':                ('number', 10, None, None, None, 'Seed inactivity limit in minutes.'),
        'seedIdleMode':                 ('number', 10, None, None, None, 'Seed inactivity mode. 0 = Use session limit, 1 = Use transfer limit, 2 = Disable limit.'),
        'seedRatioLimit':               ('double', 5, None, None, None, 'Seeding ratio.'),
        'seedRatioMode':                ('number', 5, None, None, None, 'Which ratio to use. 0 = Use session limit, 1 = Use transfer limit, 2 = Disable limit.'),
        'speed-limit-down':             ('number', 1, 5, None, 'downloadLimit', 'Set the speed limit for download in Kib/s.'),
        'speed-limit-down-enabled':     ('boolean', 1, 5, None, 'downloadLimited', 'Enable download speed limiter.'),
        'speed-limit-up':               ('number', 1, 5, None, 'uploadLimit', 'Set the speed limit for upload in Kib/s.'),
        'speed-limit-up-enabled':       ('boolean', 1, 5, None, 'uploadLimited', 'Enable upload speed limiter.'),
        'trackerAdd':                   ('array', 10, None, None, None, 'Array of string with announce URLs to add.'),
        'trackerRemove':                ('array', 10, None, None, None, 'Array of ids of trackers to remove.'),
        'trackerReplace':               ('array', 10, None, None, None, 'Array of (id, url) tuples where the announce URL should be replaced.'),
        'uploadLimit':                  ('number', 5, None, 'speed-limit-up', None, 'Set the speed limit for upload in Kib/s.'),
        'uploadLimited':                ('boolean', 5, None, 'speed-limit-up-enabled', None, 'Enable upload speed limiter.'),
    },
    'add': {
        'bandwidthPriority':            ('number', 8, None, None, None, 'Priority for this transfer.'),
        'download-dir':                 ('string', 1, None, None, None, 'The directory where the downloaded contents will be saved in.'),
        'cookies':                      ('string', 13, None, None, None, 'One or more HTTP cookie(s).'),
        'filename':                     ('string', 1, None, None, None, "A file path or URL to a torrent file or a magnet link."),
        'files-wanted':                 ('array', 1, None, None, None, "A list of file id's that should be downloaded."),
        'files-unwanted':               ('array', 1, None, None, None, "A list of file id's that shouldn't be downloaded."),
        'metainfo':                     ('string', 1, None, None, None, 'The content of a torrent file, base64 encoded.'),
        'paused':                       ('boolean', 1, None, None, None, 'If True, does not start the transfer when added.'),
        'peer-limit':                   ('number', 1, None, None, None, 'Maximum number of peers allowed.'),
        'priority-high':                ('array', 1, None, None, None, "A list of file id's that should have high priority."),
        'priority-low':                 ('array', 1, None, None, None, "A list of file id's that should have low priority."),
        'priority-normal':              ('array', 1, None, None, None, "A list of file id's that should have normal priority."),
    }
}

# Arguments for session methods
SESSION_ARGS = {
    'get': {
        "alt-speed-down":               ('number', 5, None, None, None, 'Alternate session download speed limit (in Kib/s).'),
        "alt-speed-enabled":            ('boolean', 5, None, None, None, 'True if alternate global download speed limiter is ebabled.'),
        "alt-speed-time-begin":         ('number', 5, None, None, None, 'Time when alternate speeds should be enabled. Minutes after midnight.'),
        "alt-speed-time-enabled":       ('boolean', 5, None, None, None, 'True if alternate speeds scheduling is enabled.'),
        "alt-speed-time-end":           ('number', 5, None, None, None, 'Time when alternate speeds should be disabled. Minutes after midnight.'),
        "alt-speed-time-day":           ('number', 5, None, None, None, 'Days alternate speeds scheduling is enabled.'),
        "alt-speed-up":                 ('number', 5, None, None, None, 'Alternate session upload speed limit (in Kib/s)'),
        "blocklist-enabled":            ('boolean', 5, None, None, None, 'True when blocklist is enabled.'),
        "blocklist-size":               ('number', 5, None, None, None, 'Number of rules in the blocklist'),
        "blocklist-url":                ('string', 11, None, None, None, 'Location of the block list. Updated with blocklist-update.'),
        "cache-size-mb":                ('number', 10, None, None, None, 'The maximum size of the disk cache in MB'),
        "config-dir":                   ('string', 8, None, None, None, 'location of transmissions configuration directory'),
        "dht-enabled":                  ('boolean', 6, None, None, None, 'True if DHT enabled.'),
        "download-dir":                 ('string', 1, None, None, None, 'The download directory.'),
        "download-dir-free-space":      ('number', 12, None, None, None, 'Free space in the download directory, in bytes'),
        "download-queue-size":          ('number', 14, None, None, None, 'Number of slots in the download queue.'),
        "download-queue-enabled":       ('boolean', 14, None, None, None, 'True if the download queue is enabled.'),
        "encryption":                   ('string', 1, None, None, None, 'Encryption mode, one of ``required``, ``preferred`` or ``tolerated``.'),
        "idle-seeding-limit":           ('number', 10, None, None, None, 'Seed inactivity limit in minutes.'),
        "idle-seeding-limit-enabled":   ('boolean', 10, None, None, None, 'True if the seed activity limit is enabled.'),
        "incomplete-dir":               ('string', 7, None, None, None, 'The path to the directory for incomplete torrent transfer data.'),
        "incomplete-dir-enabled":       ('boolean', 7, None, None, None, 'True if the incomplete dir is enabled.'),
        "lpd-enabled":                  ('boolean', 9, None, None, None, 'True if local peer discovery is enabled.'),
        "peer-limit":                   ('number', 1, 5, None, 'peer-limit-global', 'Maximum number of peers.'),
        "peer-limit-global":            ('number', 5, None, 'peer-limit', None, 'Maximum number of peers.'),
        "peer-limit-per-torrent":       ('number', 5, None, None, None, 'Maximum number of peers per transfer.'),
        "pex-allowed":                  ('boolean', 1, 5, None, 'pex-enabled', 'True if PEX is allowed.'),
        "pex-enabled":                  ('boolean', 5, None, 'pex-allowed', None, 'True if PEX is enabled.'),
        "port":                         ('number', 1, 5, None, 'peer-port', 'Peer port.'),
        "peer-port":                    ('number', 5, None, 'port', None, 'Peer port.'),
        "peer-port-random-on-start":    ('boolean', 5, None, None, None, 'Enables randomized peer port on start of Transmission.'),
        "port-forwarding-enabled":      ('boolean', 1, None, None, None, 'True if port forwarding is enabled.'),
        "queue-stalled-minutes":        ('number', 14, None, None, None, 'Number of minutes of idle that marks a transfer as stalled.'),
        "queue-stalled-enabled":        ('boolean', 14, None, None, None, 'True if stalled tracking of transfers is enabled.'),
        "rename-partial-files":         ('boolean', 8, None, None, None, 'True if ".part" is appended to incomplete files'),
        "rpc-version":                  ('number', 4, None, None, None, 'Transmission RPC API Version.'),
        "rpc-version-minimum":          ('number', 4, None, None, None, 'Minimum accepted RPC API Version.'),
        "script-torrent-done-enabled":  ('boolean', 9, None, None, None, 'True if the done script is enabled.'),
        "script-torrent-done-filename": ('string', 9, None, None, None, 'Filename of the script to run when the transfer is done.'),
        "seedRatioLimit":               ('double', 5, None, None, None, 'Seed ratio limit. 1.0 means 1:1 download and upload ratio.'),
        "seedRatioLimited":             ('boolean', 5, None, None, None, 'True if seed ration limit is enabled.'),
        "seed-queue-size":              ('number', 14, None, None, None, 'Number of slots in the upload queue.'),
        "seed-queue-enabled":           ('boolean', 14, None, None, None, 'True if upload queue is enabled.'),
        "speed-limit-down":             ('number', 1, None, None, None, 'Download speed limit (in Kib/s).'),
        "speed-limit-down-enabled":     ('boolean', 1, None, None, None, 'True if the download speed is limited.'),
        "speed-limit-up":               ('number', 1, None, None, None, 'Upload speed limit (in Kib/s).'),
        "speed-limit-up-enabled":       ('boolean', 1, None, None, None, 'True if the upload speed is limited.'),
        "start-added-torrents":         ('boolean', 9, None, None, None, 'When true uploaded torrents will start right away.'),
        "trash-original-torrent-files": ('boolean', 9, None, None, None, 'When true added .torrent files will be deleted.'),
        'units':                        ('object', 10, None, None, None, 'An object containing units for size and speed.'),
        'utp-enabled':                  ('boolean', 13, None, None, None, 'True if Micro Transport Protocol (UTP) is enabled.'),
        "version":                      ('string', 3, None, None, None, 'Transmission version.'),
    },
    'set': {
        "alt-speed-down":               ('number', 5, None, None, None, 'Alternate session download speed limit (in Kib/s).'),
        "alt-speed-enabled":            ('boolean', 5, None, None, None, 'Enables alternate global download speed limiter.'),
        "alt-speed-time-begin":         ('number', 5, None, None, None, 'Time when alternate speeds should be enabled. Minutes after midnight.'),
        "alt-speed-time-enabled":       ('boolean', 5, None, None, None, 'Enables alternate speeds scheduling.'),
        "alt-speed-time-end":           ('number', 5, None, None, None, 'Time when alternate speeds should be disabled. Minutes after midnight.'),
        "alt-speed-time-day":           ('number', 5, None, None, None, 'Enables alternate speeds scheduling these days.'),
        "alt-speed-up":                 ('number', 5, None, None, None, 'Alternate session upload speed limit (in Kib/s).'),
        "blocklist-enabled":            ('boolean', 5, None, None, None, 'Enables the block list'),
        "blocklist-url":                ('string', 11, None, None, None, 'Location of the block list. Updated with blocklist-update.'),
        "cache-size-mb":                ('number', 10, None, None, None, 'The maximum size of the disk cache in MB'),
        "dht-enabled":                  ('boolean', 6, None, None, None, 'Enables DHT.'),
        "download-dir":                 ('string', 1, None, None, None, 'Set the session download directory.'),
        "download-queue-size":          ('number', 14, None, None, None, 'Number of slots in the download queue.'),
        "download-queue-enabled":       ('boolean', 14, None, None, None, 'Enables download queue.'),
        "encryption":                   ('string', 1, None, None, None, 'Set the session encryption mode, one of ``required``, ``preferred`` or ``tolerated``.'),
        "idle-seeding-limit":           ('number', 10, None, None, None, 'The default seed inactivity limit in minutes.'),
        "idle-seeding-limit-enabled":   ('boolean', 10, None, None, None, 'Enables the default seed inactivity limit'),
        "incomplete-dir":               ('string', 7, None, None, None, 'The path to the directory of incomplete transfer data.'),
        "incomplete-dir-enabled":       ('boolean', 7, None, None, None, 'Enables the incomplete transfer data directory. Otherwise data for incomplete transfers are stored in the download target.'),
        "lpd-enabled":                  ('boolean', 9, None, None, None, 'Enables local peer discovery for public torrents.'),
        "peer-limit":                   ('number', 1, 5, None, 'peer-limit-global', 'Maximum number of peers.'),
        "peer-limit-global":            ('number', 5, None, 'peer-limit', None, 'Maximum number of peers.'),
        "peer-limit-per-torrent":       ('number', 5, None, None, None, 'Maximum number of peers per transfer.'),
        "pex-allowed":                  ('boolean', 1, 5, None, 'pex-enabled', 'Allowing PEX in public torrents.'),
        "pex-enabled":                  ('boolean', 5, None, 'pex-allowed', None, 'Allowing PEX in public torrents.'),
        "port":                         ('number', 1, 5, None, 'peer-port', 'Peer port.'),
        "peer-port":                    ('number', 5, None, 'port', None, 'Peer port.'),
        "peer-port-random-on-start":    ('boolean', 5, None, None, None, 'Enables randomized peer port on start of Transmission.'),
        "port-forwarding-enabled":      ('boolean', 1, None, None, None, 'Enables port forwarding.'),
        "rename-partial-files":         ('boolean', 8, None, None, None, 'Appends ".part" to incomplete files'),
        "queue-stalled-minutes":        ('number', 14, None, None, None, 'Number of minutes of idle that marks a transfer as stalled.'),
        "queue-stalled-enabled":        ('boolean', 14, None, None, None, 'Enable tracking of stalled transfers.'),
        "script-torrent-done-enabled":  ('boolean', 9, None, None, None, 'Whether or not to call the "done" script.'),
        "script-torrent-done-filename": ('string', 9, None, None, None, 'Filename of the script to run when the transfer is done.'),
        "seed-queue-size":              ('number', 14, None, None, None, 'Number of slots in the upload queue.'),
        "seed-queue-enabled":           ('boolean', 14, None, None, None, 'Enables upload queue.'),
        "seedRatioLimit":               ('double', 5, None, None, None, 'Seed ratio limit. 1.0 means 1:1 download and upload ratio.'),
        "seedRatioLimited":             ('boolean', 5, None, None, None, 'Enables seed ration limit.'),
        "speed-limit-down":             ('number', 1, None, None, None, 'Download speed limit (in Kib/s).'),
        "speed-limit-down-enabled":     ('boolean', 1, None, None, None, 'Enables download speed limiting.'),
        "speed-limit-up":               ('number', 1, None, None, None, 'Upload speed limit (in Kib/s).'),
        "speed-limit-up-enabled":       ('boolean', 1, None, None, None, 'Enables upload speed limiting.'),
        "start-added-torrents":         ('boolean', 9, None, None, None, 'Added torrents will be started right away.'),
        "trash-original-torrent-files": ('boolean', 9, None, None, None, 'The .torrent file of added torrents will be deleted.'),
        'utp-enabled':                  ('boolean', 13, None, None, None, 'Enables Micro Transport Protocol (UTP).'),
    },
}


class TransmissionError(Exception):
    """
    This exception is raised when there has occurred an error related to
    communication with Transmission. It is a subclass of Exception.
    """
    def __init__(self, message='', original=None):
        Exception.__init__(self)
        self.message = message
        self.original = original

    def __str__(self):
        if self.original:
            original_name = type(self.original).__name__
            return '%s Original exception: %s, "%s"' % (self.message, original_name, str(self.original))
        else:
            return self.message

class HTTPHandlerError(Exception):
    """
    This exception is raised when there has occurred an error related to
    the HTTP handler. It is a subclass of Exception.
    """
    def __init__(self, httpurl=None, httpcode=None, httpmsg=None, httpheaders=None, httpdata=None):
        Exception.__init__(self)
        self.url = ''
        self.code = 600
        self.message = ''
        self.headers = {}
        self.data = ''
        if isinstance(httpurl, string_types):
            self.url = httpurl
        if isinstance(httpcode, integer_types):
            self.code = httpcode
        if isinstance(httpmsg, string_types):
            self.message = httpmsg
        if isinstance(httpheaders, dict):
            self.headers = httpheaders
        if isinstance(httpdata, string_types):
            self.data = httpdata

    def __repr__(self):
        return '<HTTPHandlerError %d, %s>' % (self.code, self.message)

    def __str__(self):
        return 'HTTPHandlerError %d: %s' % (self.code, self.message)

    def __unicode__(self):
        return 'HTTPHandlerError %d: %s' % (self.code, self.message)

UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']

def format_size(size):
    """
    Format byte size into IEC prefixes, B, KiB, MiB ...
    """
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(UNITS):
        i += 1
        size /= 1024.0
    return (size, UNITS[i])

def format_speed(size):
    """
    Format bytes per second speed into IEC prefixes, B/s, KiB/s, MiB/s ...
    """
    (size, unit) = format_size(size)
    return (size, unit + '/s')

def format_timedelta(delta):
    """
    Format datetime.timedelta into <days> <hours>:<minutes>:<seconds>.
    """
    minutes, seconds = divmod(delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d %02d:%02d:%02d' % (delta.days, hours, minutes, seconds)

def format_timestamp(timestamp, utc=False):
    """
    Format unix timestamp into ISO date format.
    """
    if timestamp > 0:
        if utc:
            dt_timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        else:
            dt_timestamp = datetime.datetime.fromtimestamp(timestamp)
        return dt_timestamp.isoformat(' ')
    else:
        return '-'

class INetAddressError(Exception):
    """
    Error parsing / generating a internet address.
    """
    pass

def inet_address(address, default_port, default_address='localhost'):
    """
    Parse internet address.
    """
    addr = address.split(':')
    if len(addr) == 1:
        try:
            port = int(addr[0])
            addr = default_address
        except ValueError:
            addr = addr[0]
            port = default_port
    elif len(addr) == 2:
        try:
            port = int(addr[1])
        except ValueError:
            raise INetAddressError('Invalid address "%s".' % address)
        if len(addr[0]) == 0:
            addr = default_address
        else:
            addr = addr[0]
    else:
        raise INetAddressError('Invalid address "%s".' % address)
    try:
        socket.getaddrinfo(addr, port, socket.AF_INET, socket.SOCK_STREAM)
    except socket.gaierror:
        raise INetAddressError('Cannot look up address "%s".' % address)
    return (addr, port)

def rpc_bool(arg):
    """
    Convert between Python boolean and Transmission RPC boolean.
    """
    if isinstance(arg, string_types):
        try:
            arg = bool(int(arg))
        except ValueError:
            arg = arg.lower() in ['true', 'yes']
    return 1 if bool(arg) else 0

TR_TYPE_MAP = {
    'number' : int,
    'string' : str,
    'double': float,
    'boolean' : rpc_bool,
    'array': list,
    'object': dict
}

def make_python_name(name):
    """
    Convert Transmission RPC name to python compatible name.
    """
    return name.replace('-', '_')

def make_rpc_name(name):
    """
    Convert python compatible name to Transmission RPC name.
    """
    return name.replace('_', '-')

def argument_value_convert(method, argument, value, rpc_version):
    """
    Check and fix Transmission RPC issues with regards to methods, arguments and values.
    """
    if method in ('torrent-add', 'torrent-get', 'torrent-set'):
        args = TORRENT_ARGS[method[-3:]]
    elif method in ('session-get', 'session-set'):
        args = SESSION_ARGS[method[-3:]]
    else:
        return ValueError('Method "%s" not supported' % (method))
    if argument in args:
        info = args[argument]
        invalid_version = True
        while invalid_version:
            invalid_version = False
            replacement = None
            if rpc_version < info[1]:
                invalid_version = True
                replacement = info[3]
            if info[2] and info[2] <= rpc_version:
                invalid_version = True
                replacement = info[4]
            if invalid_version:
                if replacement:
                    LOGGER.warning(
                        'Replacing requested argument "%s" with "%s".'
                        % (argument, replacement))
                    argument = replacement
                    info = args[argument]
                else:
                    raise ValueError(
                        'Method "%s" Argument "%s" does not exist in version %d.'
                        % (method, argument, rpc_version))
        return (argument, TR_TYPE_MAP[info[0]](value))
    else:
        raise ValueError('Argument "%s" does not exists for method "%s".',
                         (argument, method))

def get_arguments(method, rpc_version):
    """
    Get arguments for method in specified Transmission RPC version.
    """
    if method in ('torrent-add', 'torrent-get', 'torrent-set'):
        args = TORRENT_ARGS[method[-3:]]
    elif method in ('session-get', 'session-set'):
        args = SESSION_ARGS[method[-3:]]
    else:
        return ValueError('Method "%s" not supported' % (method))
    accessible = []
    for argument, info in iteritems(args):
        valid_version = True
        if rpc_version < info[1]:
            valid_version = False
        if info[2] and info[2] <= rpc_version:
            valid_version = False
        if valid_version:
            accessible.append(argument)
    return accessible

def add_stdout_logger(level='debug'):
    """
    Add a stdout target for the transmissionrpc logging.
    """
    levels = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR}

    trpc_logger = logging.getLogger('transmissionrpc')
    loghandler = logging.StreamHandler()
    if level in list(levels.keys()):
        loglevel = levels[level]
        trpc_logger.setLevel(loglevel)
        loghandler.setLevel(loglevel)
    trpc_logger.addHandler(loghandler)

def add_file_logger(filepath, level='debug'):
    """
    Add a stdout target for the transmissionrpc logging.
    """
    levels = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR}

    trpc_logger = logging.getLogger('transmissionrpc')
    loghandler = logging.FileHandler(filepath, encoding='utf-8')
    if level in list(levels.keys()):
        loglevel = levels[level]
        trpc_logger.setLevel(loglevel)
        loghandler.setLevel(loglevel)
    trpc_logger.addHandler(loghandler)

Field = namedtuple('Field', ['value', 'dirty'])

class HTTPHandler(object):
    """
    Prototype for HTTP handling.
    """
    def set_authentication(self, uri, login, password):
        """
        Transmission use basic authentication in earlier versions and digest
        authentication in later versions.

         * uri, the authentication realm URI.
         * login, the authentication login.
         * password, the authentication password.
        """
        raise NotImplementedError("Bad HTTPHandler, failed to implement set_authentication.")

    def request(self, url, query, headers, timeout):
        """
        Implement a HTTP POST request here.

         * url, The URL to request.
         * query, The query data to send. This is a JSON data string.
         * headers, a dictionary of headers to send.
         * timeout, requested request timeout in seconds.
        """
        raise NotImplementedError("Bad HTTPHandler, failed to implement request.")

class DefaultHTTPHandler(HTTPHandler):
    """
    The default HTTP handler provided with transmissionrpc.
    """
    def __init__(self):
        HTTPHandler.__init__(self)
        self.http_opener = build_opener()

    def set_authentication(self, uri, login, password):
        password_manager = HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(realm=None, uri=uri, user=login, passwd=password)
        self.http_opener = build_opener(HTTPBasicAuthHandler(password_manager), HTTPDigestAuthHandler(password_manager))

    def request(self, url, query, headers, timeout):
        request = Request(url, query.encode('utf-8'), headers)
        try:
            if (sys.version_info[0] == 2 and sys.version_info[1] > 5) or sys.version_info[0] > 2:
                response = self.http_opener.open(request, timeout=timeout)
            else:
                response = self.http_opener.open(request)
        except HTTPError as error:
            if error.fp is None:
                raise HTTPHandlerError(error.filename, error.code, error.msg, dict(error.hdrs))
            else:
                raise HTTPHandlerError(error.filename, error.code, error.msg, dict(error.hdrs), error.read())
        except URLError as error:
            # urllib2.URLError documentation is horrendous!
            # Try to get the tuple arguments of URLError
            if hasattr(error.reason, 'args') and isinstance(error.reason.args, tuple) and len(error.reason.args) == 2:
                raise HTTPHandlerError(httpcode=error.reason.args[0], httpmsg=error.reason.args[1])
            else:
                raise HTTPHandlerError(httpmsg='urllib2.URLError: %s' % (error.reason))
        except BadStatusLine as error:
            raise HTTPHandlerError(httpmsg='httplib.BadStatusLine: %s' % (error.line))
        return response.read().decode('utf-8')

def get_status_old(code):
    """Get the torrent status using old status codes"""
    mapping = {
        (1<<0): 'check pending',
        (1<<1): 'checking',
        (1<<2): 'downloading',
        (1<<3): 'seeding',
        (1<<4): 'stopped',
    }
    return mapping[code]

def get_status_new(code):
    """Get the torrent status using new status codes"""
    mapping = {
        0: 'stopped',
        1: 'check pending',
        2: 'checking',
        3: 'download pending',
        4: 'downloading',
        5: 'seed pending',
        6: 'seeding',
    }
    return mapping[code]

class Torrent(object):
    """
    Torrent is a class holding the data received from Transmission regarding a bittorrent transfer.

    All fetched torrent fields are accessible through this class using attributes.
    This class has a few convenience properties using the torrent data.
    """

    def __init__(self, client, fields):
        if 'id' not in fields:
            raise ValueError('Torrent requires an id')
        self._fields = {}
        self._update_fields(fields)
        self._incoming_pending = False
        self._outgoing_pending = False
        self._client = client

    def _get_name_string(self, codec=None):
        """Get the name"""
        if codec is None:
            codec = sys.getdefaultencoding()
        name = None
        # try to find name
        if 'name' in self._fields:
            name = self._fields['name'].value
        # if name is unicode, try to decode
        if isinstance(name, text_type):
            try:
                name = name.encode(codec)
            except UnicodeError:
                name = None
        return name

    def __repr__(self):
        tid = self._fields['id'].value
        name = self._get_name_string()
        if isinstance(name, str):
            return '<Torrent %d \"%s\">' % (tid, name)
        else:
            return '<Torrent %d>' % (tid)

    def __str__(self):
        name = self._get_name_string()
        if isinstance(name, str):
            return 'Torrent \"%s\"' % (name)
        else:
            return 'Torrent'

    def __copy__(self):
        return Torrent(self._client, self._fields)

    def __getattr__(self, name):
        try:
            return self._fields[name].value
        except KeyError:
            raise AttributeError('No attribute %s' % name)

    def _rpc_version(self):
        """Get the Transmission RPC API version."""
        if self._client:
            return self._client.rpc_version
        return 2

    def _dirty_fields(self):
        """Enumerate changed fields"""
        outgoing_keys = ['bandwidthPriority', 'downloadLimit', 'downloadLimited', 'peer_limit', 'queuePosition'
            , 'seedIdleLimit', 'seedIdleMode', 'seedRatioLimit', 'seedRatioMode', 'uploadLimit', 'uploadLimited']
        fields = []
        for key in outgoing_keys:
            if key in self._fields and self._fields[key].dirty:
                fields.append(key)
        return fields

    def _push(self):
        """Push changed fields to the server"""
        dirty = self._dirty_fields()
        args = {}
        for key in dirty:
            args[key] = self._fields[key].value
            self._fields[key] = self._fields[key]._replace(dirty=False)
        if len(args) > 0:
            self._client.change_torrent(self.id, **args)

    def _update_fields(self, other):
        """
        Update the torrent data from a Transmission JSON-RPC arguments dictionary
        """
        fields = None
        if isinstance(other, dict):
            for key, value in iteritems(other):
                self._fields[key.replace('-', '_')] = Field(value, False)
        elif isinstance(other, Torrent):
            for key in list(other._fields.keys()):
                self._fields[key] = Field(other._fields[key].value, False)
        else:
            raise ValueError('Cannot update with supplied data')
        self._incoming_pending = False
    
    def _status(self):
        """Get the torrent status"""
        code = self._fields['status'].value
        if self._rpc_version() >= 14:
            return get_status_new(code)
        else:
            return get_status_old(code)

    def files(self):
        """
        Get list of files for this torrent.

        This function returns a dictionary with file information for each file.
        The file information is has following fields:
        ::

            {
                <file id>: {
                    'name': <file name>,
                    'size': <file size in bytes>,
                    'completed': <bytes completed>,
                    'priority': <priority ('high'|'normal'|'low')>,
                    'selected': <selected for download>
                }
                ...
            }
        """
        result = {}
        if 'files' in self._fields:
            files = self._fields['files'].value
            indices = range(len(files))
            priorities = self._fields['priorities'].value
            wanted = self._fields['wanted'].value
            for item in zip(indices, files, priorities, wanted):
                selected = True if item[3] else False
                priority = PRIORITY[item[2]]
                result[item[0]] = {
                    'selected': selected,
                    'priority': priority,
                    'size': item[1]['length'],
                    'name': item[1]['name'],
                    'completed': item[1]['bytesCompleted']}
        return result

    @property
    def status(self):
        """
        Returns the torrent status. Is either one of 'check pending', 'checking',
        'downloading', 'seeding' or 'stopped'. The first two is related to
        verification.
        """
        return self._status()

    @property
    def progress(self):
        """Get the download progress in percent."""
        try:
            size = self._fields['sizeWhenDone'].value
            left = self._fields['leftUntilDone'].value
            return 100.0 * (size - left) / float(size)
        except ZeroDivisionError:
            return 0.0

    @property
    def ratio(self):
        """Get the upload/download ratio."""
        return float(self._fields['uploadRatio'].value)

    @property
    def eta(self):
        """Get the "eta" as datetime.timedelta."""
        eta = self._fields['eta'].value
        if eta >= 0:
            return datetime.timedelta(seconds=eta)
        else:
            raise ValueError('eta not valid')

    @property
    def date_active(self):
        """Get the attribute "activityDate" as datetime.datetime."""
        return datetime.datetime.fromtimestamp(self._fields['activityDate'].value)

    @property
    def date_added(self):
        """Get the attribute "addedDate" as datetime.datetime."""
        return datetime.datetime.fromtimestamp(self._fields['addedDate'].value)

    @property
    def date_started(self):
        """Get the attribute "startDate" as datetime.datetime."""
        return datetime.datetime.fromtimestamp(self._fields['startDate'].value)

    @property
    def date_done(self):
        """Get the attribute "doneDate" as datetime.datetime."""
        return datetime.datetime.fromtimestamp(self._fields['doneDate'].value)

    def format_eta(self):
        """
        Returns the attribute *eta* formatted as a string.

        * If eta is -1 the result is 'not available'
        * If eta is -2 the result is 'unknown'
        * Otherwise eta is formatted as <days> <hours>:<minutes>:<seconds>.
        """
        eta = self._fields['eta'].value
        if eta == -1:
            return 'not available'
        elif eta == -2:
            return 'unknown'
        else:
            return format_timedelta(self.eta)

    def _get_download_limit(self):
        """
        Get the download limit.
        Can be a number or None.
        """
        if self._fields['downloadLimited'].value:
            return self._fields['downloadLimit'].value
        else:
            return None

    def _set_download_limit(self, limit):
        """
        Get the download limit.
        Can be a number, 'session' or None.
        """
        if isinstance(limit, integer_types):
            self._fields['downloadLimited'] = Field(True, True)
            self._fields['downloadLimit'] = Field(limit, True)
            self._push()
        elif limit == None:
            self._fields['downloadLimited'] = Field(False, True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    download_limit = property(_get_download_limit, _set_download_limit, None, "Download limit in Kbps or None. This is a mutator.")

    def _get_peer_limit(self):
        """
        Get the peer limit.
        """
        return self._fields['peer_limit'].value

    def _set_peer_limit(self, limit):
        """
        Set the peer limit.
        """
        if isinstance(limit, integer_types):
            self._fields['peer_limit'] = Field(limit, True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    peer_limit = property(_get_peer_limit, _set_peer_limit, None, "Peer limit. This is a mutator.")

    def _get_priority(self):
        """
        Get the priority as string.
        Can be one of 'low', 'normal', 'high'.
        """
        return PRIORITY[self._fields['bandwidthPriority'].value]

    def _set_priority(self, priority):
        """
        Set the priority as string.
        Can be one of 'low', 'normal', 'high'.
        """
        if isinstance(priority, string_types):
            self._fields['bandwidthPriority'] = Field(PRIORITY[priority], True)
            self._push()

    priority = property(_get_priority, _set_priority, None
        , "Bandwidth priority as string. Can be one of 'low', 'normal', 'high'. This is a mutator.")

    def _get_seed_idle_limit(self):
        """
        Get the seed idle limit in minutes.
        """
        return self._fields['seedIdleLimit'].value

    def _set_seed_idle_limit(self, limit):
        """
        Set the seed idle limit in minutes.
        """
        if isinstance(limit, integer_types):
            self._fields['seedIdleLimit'] = Field(limit, True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    seed_idle_limit = property(_get_seed_idle_limit, _set_seed_idle_limit, None
        , "Torrent seed idle limit in minutes. Also see seed_idle_mode. This is a mutator.")

    def _get_seed_idle_mode(self):
        """
        Get the seed ratio mode as string. Can be one of 'global', 'single' or 'unlimited'.
        """
        return IDLE_LIMIT[self._fields['seedIdleMode'].value]

    def _set_seed_idle_mode(self, mode):
        """
        Set the seed ratio mode as string. Can be one of 'global', 'single' or 'unlimited'.
        """
        if isinstance(mode, str):
            self._fields['seedIdleMode'] = Field(IDLE_LIMIT[mode], True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    seed_idle_mode = property(_get_seed_idle_mode, _set_seed_idle_mode, None,
        """
        Seed idle mode as string. Can be one of 'global', 'single' or 'unlimited'.

         * global, use session seed idle limit.
         * single, use torrent seed idle limit. See seed_idle_limit.
         * unlimited, no seed idle limit.

        This is a mutator.
        """
    )

    def _get_seed_ratio_limit(self):
        """
        Get the seed ratio limit as float.
        """
        return float(self._fields['seedRatioLimit'].value)

    def _set_seed_ratio_limit(self, limit):
        """
        Set the seed ratio limit as float.
        """
        if isinstance(limit, (integer_types, float)) and limit >= 0.0:
            self._fields['seedRatioLimit'] = Field(float(limit), True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    seed_ratio_limit = property(_get_seed_ratio_limit, _set_seed_ratio_limit, None
        , "Torrent seed ratio limit as float. Also see seed_ratio_mode. This is a mutator.")

    def _get_seed_ratio_mode(self):
        """
        Get the seed ratio mode as string. Can be one of 'global', 'single' or 'unlimited'.
        """
        return RATIO_LIMIT[self._fields['seedRatioMode'].value]

    def _set_seed_ratio_mode(self, mode):
        """
        Set the seed ratio mode as string. Can be one of 'global', 'single' or 'unlimited'.
        """
        if isinstance(mode, str):
            self._fields['seedRatioMode'] = Field(RATIO_LIMIT[mode], True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    seed_ratio_mode = property(_get_seed_ratio_mode, _set_seed_ratio_mode, None,
        """
        Seed ratio mode as string. Can be one of 'global', 'single' or 'unlimited'.

         * global, use session seed ratio limit.
         * single, use torrent seed ratio limit. See seed_ratio_limit.
         * unlimited, no seed ratio limit.

        This is a mutator.
        """
    )

    def _get_upload_limit(self):
        """
        Get the upload limit.
        Can be a number or None.
        """
        if self._fields['uploadLimited'].value:
            return self._fields['uploadLimit'].value
        else:
            return None

    def _set_upload_limit(self, limit):
        """
        Set the upload limit.
        Can be a number, 'session' or None.
        """
        if isinstance(limit, integer_types):
            self._fields['uploadLimited'] = Field(True, True)
            self._fields['uploadLimit'] = Field(limit, True)
            self._push()
        elif limit == None:
            self._fields['uploadLimited'] = Field(False, True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    upload_limit = property(_get_upload_limit, _set_upload_limit, None, "Upload limit in Kbps or None. This is a mutator.")

    def _get_queue_position(self):
        """Get the queue position for this torrent."""
        if self._rpc_version() >= 14:
            return self._fields['queuePosition'].value
        else:
            return 0

    def _set_queue_position(self, position):
        """Set the queue position for this torrent."""
        if self._rpc_version() >= 14:
            if isinstance(position, integer_types):
                self._fields['queuePosition'] = Field(position, True)
                self._push()
            else:
                raise ValueError("Not a valid position")
        else:
            pass

    queue_position = property(_get_queue_position, _set_queue_position, None, "Queue position")

    def update(self, timeout=None):
        """Update the torrent information."""
        self._push()
        torrent = self._client.get_torrent(self.id, timeout=timeout)
        self._update_fields(torrent)

    def start(self, bypass_queue=False, timeout=None):
        """
        Start the torrent.
        """
        self._incoming_pending = True
        self._client.start_torrent(self.id, bypass_queue=bypass_queue, timeout=timeout)

    def stop(self, timeout=None):
        """Stop the torrent."""
        self._incoming_pending = True
        self._client.stop_torrent(self.id, timeout=timeout)

    def move_data(self, location, timeout=None):
        """Move torrent data to location."""
        self._incoming_pending = True
        self._client.move_torrent_data(self.id, location, timeout=timeout)

    def locate_data(self, location, timeout=None):
        """Locate torrent data at location."""
        self._incoming_pending = True
        self._client.locate_torrent_data(self.id, location, timeout=timeout)

class Session(object):
    """
    Session is a class holding the session data for a Transmission daemon.

    Access the session field can be done through attributes.
    The attributes available are the same as the session arguments in the
    Transmission RPC specification, but with underscore instead of hyphen.
    ``download-dir`` -> ``download_dir``.
    """

    def __init__(self, client=None, fields=None):
        self._client = client
        self._fields = {}
        if fields is not None:
            self._update_fields(fields)

    def __getattr__(self, name):
        try:
            return self._fields[name].value
        except KeyError:
            raise AttributeError('No attribute %s' % name)

    def __str__(self):
        text = ''
        for key in sorted(self._fields.keys()):
            text += "% 32s: %s\n" % (key[-32:], self._fields[key].value)
        return text

    def _update_fields(self, other):
        """
        Update the session data from a Transmission JSON-RPC arguments dictionary
        """
        if isinstance(other, dict):
            for key, value in iteritems(other):
                self._fields[key.replace('-', '_')] = Field(value, False)
        elif isinstance(other, Session):
            for key in list(other._fields.keys()):
                self._fields[key] = Field(other._fields[key].value, False)
        else:
            raise ValueError('Cannot update with supplied data')

    def _dirty_fields(self):
        """Enumerate changed fields"""
        outgoing_keys = ['peer_port', 'pex_enabled']
        fields = []
        for key in outgoing_keys:
            if key in self._fields and self._fields[key].dirty:
                fields.append(key)
        return fields

    def _push(self):
        """Push changed fields to the server"""
        dirty = self._dirty_fields()
        args = {}
        for key in dirty:
            args[key] = self._fields[key].value
            self._fields[key] = self._fields[key]._replace(dirty=False)
        if len(args) > 0:
            self._client.set_session(**args)

    def update(self, timeout=None):
        """Update the session information."""
        self._push()
        session = self._client.get_session(timeout=timeout)
        self._update_fields(session)
        session = self._client.session_stats(timeout=timeout)
        self._update_fields(session)

    def from_request(self, data):
        """Update the session information."""
        self._update_fields(data)

    def _get_peer_port(self):
        """
        Get the peer port.
        """
        return self._fields['peer_port'].value

    def _set_peer_port(self, port):
        """
        Set the peer port.
        """
        if isinstance(port, integer_types):
            self._fields['peer_port'] = Field(port, True)
            self._push()
        else:
            raise ValueError("Not a valid limit")

    peer_port = property(_get_peer_port, _set_peer_port, None, "Peer port. This is a mutator.")

    def _get_pex_enabled(self):
        """Is peer exchange enabled?"""
        return self._fields['pex_enabled'].value

    def _set_pex_enabled(self, enabled):
        """Enable/disable peer exchange."""
        if isinstance(enabled, bool):
            self._fields['pex_enabled'] = Field(enabled, True)
            self._push()
        else:
            raise TypeError("Not a valid type")

    pex_enabled = property(_get_pex_enabled, _set_pex_enabled, None, "Enable peer exchange. This is a mutator.")

def debug_httperror(error):
    """
    Log the Transmission RPC HTTP error.
    """
    try:
        data = json.loads(error.data)
    except ValueError:
        data = error.data
    LOGGER.debug(
        json.dumps(
            {
                'response': {
                    'url': error.url,
                    'code': error.code,
                    'msg': error.message,
                    'headers': error.headers,
                    'data': data,
                }
            },
            indent=2
        )
    )

def parse_torrent_id(arg):
    """Parse an torrent id or torrent hashString."""
    torrent_id = None
    if isinstance(arg, integer_types):
        # handle index
        torrent_id = int(arg)
    elif isinstance(arg, float):
        torrent_id = int(arg)
        if torrent_id != arg:
            torrent_id = None
    elif isinstance(arg, string_types):
        try:
            torrent_id = int(arg)
            if torrent_id >= 2**31:
                torrent_id = None
        except (ValueError, TypeError):
            pass
        if torrent_id is None:
            # handle hashes
            try:
                int(arg, 16)
                torrent_id = arg
            except (ValueError, TypeError):
                pass
    return torrent_id

def parse_torrent_ids(args):
    """
    Take things and make them valid torrent identifiers
    """
    ids = []

    if args is None:
        pass
    elif isinstance(args, string_types):
        for item in re.split('[ ,]+', args):
            if len(item) == 0:
                continue
            addition = None
            torrent_id = parse_torrent_id(item)
            if torrent_id is not None:
                addition = [torrent_id]
            if not addition:
                # handle index ranges i.e. 5:10
                match = re.match('^(\d+):(\d+)$', item)
                if match:
                    try:
                        idx_from = int(match.group(1))
                        idx_to = int(match.group(2))
                        addition = list(range(idx_from, idx_to + 1))
                    except ValueError:
                        pass
            if not addition:
                raise ValueError('Invalid torrent id, \"%s\"' % item)
            ids.extend(addition)
    elif isinstance(args, (list, tuple)):
        for item in args:
            ids.extend(parse_torrent_ids(item))
    else:
        torrent_id = parse_torrent_id(args)
        if torrent_id == None:
            raise ValueError('Invalid torrent id')
        else:
            ids = [torrent_id]
    return ids

"""
Torrent ids

Many functions in Client takes torrent id. A torrent id can either be id or
hashString. When supplying multiple id's it is possible to use a list mixed
with both id and hashString.

Timeouts

Since most methods results in HTTP requests against Transmission, it is
possible to provide a argument called ``timeout``. Timeout is only effective
when using Python 2.6 or later and the default timeout is 30 seconds.
"""

class Client(object):
    """
    Client is the class handling the Transmission JSON-RPC client protocol.
    """

    def __init__(self, address='localhost', port=DEFAULT_PORT, user=None, password=None, http_handler=None, timeout=None):
        if isinstance(timeout, (integer_types, float)):
            self._query_timeout = float(timeout)
        else:
            self._query_timeout = DEFAULT_TIMEOUT
        urlo = urlparse(address)
        if urlo.scheme == '':
            base_url = 'http://' + address + ':' + str(port)
            self.url = base_url + '/transmission/rpc'
        else:
            if urlo.port:
                self.url = urlo.scheme + '://' + urlo.hostname + ':' + str(urlo.port) + urlo.path
            else:
                self.url = urlo.scheme + '://' + urlo.hostname + urlo.path
            LOGGER.info('Using custom URL "' + self.url + '".')
            if urlo.username and urlo.password:
                user = urlo.username
                password = urlo.password
            elif urlo.username or urlo.password:
                LOGGER.warning('Either user or password missing, not using authentication.')
        if http_handler is None:
            self.http_handler = DefaultHTTPHandler()
        else:
            if hasattr(http_handler, 'set_authentication') and hasattr(http_handler, 'request'):
                self.http_handler = http_handler
            else:
                raise ValueError('Invalid HTTP handler.')
        if user and password:
            self.http_handler.set_authentication(self.url, user, password)
        elif user or password:
            LOGGER.warning('Either user or password missing, not using authentication.')
        self._sequence = 0
        self.session = None
        self.session_id = 0
        self.server_version = None
        self.protocol_version = None
        self.get_session()
        self.torrent_get_arguments = get_arguments('torrent-get'
                                                   , self.rpc_version)

    def _get_timeout(self):
        """
        Get current timeout for HTTP queries.
        """
        return self._query_timeout

    def _set_timeout(self, value):
        """
        Set timeout for HTTP queries.
        """
        self._query_timeout = float(value)

    def _del_timeout(self):
        """
        Reset the HTTP query timeout to the default.
        """
        self._query_timeout = DEFAULT_TIMEOUT

    timeout = property(_get_timeout, _set_timeout, _del_timeout, doc="HTTP query timeout.")

    def _http_query(self, query, timeout=None):
        """
        Query Transmission through HTTP.
        """
        headers = {'x-transmission-session-id': str(self.session_id)}
        result = {}
        request_count = 0
        if timeout is None:
            timeout = self._query_timeout
        while True:
            LOGGER.debug(json.dumps({'url': self.url, 'headers': headers, 'query': query, 'timeout': timeout}, indent=2))
            try:
                result = self.http_handler.request(self.url, query, headers, timeout)
                break
            except HTTPHandlerError as error:
                if error.code == 409:
                    LOGGER.info('Server responded with 409, trying to set session-id.')
                    if request_count > 1:
                        raise TransmissionError('Session ID negotiation failed.', error)
                    session_id = None
                    for key in list(error.headers.keys()):
                        if key.lower() == 'x-transmission-session-id':
                            session_id = error.headers[key]
                            self.session_id = session_id
                            headers = {'x-transmission-session-id': str(self.session_id)}
                    if session_id is None:
                        debug_httperror(error)
                        raise TransmissionError('Unknown conflict.', error)
                else:
                    debug_httperror(error)
                    raise TransmissionError('Request failed.', error)
            request_count += 1
        return result

    def _request(self, method, arguments=None, ids=None, require_ids=False, timeout=None):
        """
        Send json-rpc request to Transmission using http POST
        """
        if not isinstance(method, string_types):
            raise ValueError('request takes method as string')
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise ValueError('request takes arguments as dict')
        ids = parse_torrent_ids(ids)
        if len(ids) > 0:
            arguments['ids'] = ids
        elif require_ids:
            raise ValueError('request require ids')

        query = json.dumps({'tag': self._sequence, 'method': method
                            , 'arguments': arguments})
        self._sequence += 1
        start = time.time()
        http_data = self._http_query(query, timeout)
        elapsed = time.time() - start
        LOGGER.info('http request took %.3f s' % (elapsed))

        try:
            data = json.loads(http_data)
        except ValueError as error:
            LOGGER.error('Error: ' + str(error))
            LOGGER.error('Request: \"%s\"' % (query))
            LOGGER.error('HTTP data: \"%s\"' % (http_data))
            raise

        LOGGER.debug(json.dumps(data, indent=2))
        if 'result' in data:
            if data['result'] != 'success':
                raise TransmissionError('Query failed with result \"%s\".' % (data['result']))
        else:
            raise TransmissionError('Query failed without result.')

        results = {}
        if method == 'torrent-get':
            for item in data['arguments']['torrents']:
                results[item['id']] = Torrent(self, item)
                if self.protocol_version == 2 and 'peers' not in item:
                    self.protocol_version = 1
        elif method == 'torrent-add':
            item = None
            if 'torrent-added' in data['arguments']:
                item = data['arguments']['torrent-added']
            elif 'torrent-duplicate' in data['arguments']:
                item = data['arguments']['torrent-duplicate']
            if item:
                results[item['id']] = Torrent(self, item)
            else:
                raise TransmissionError('Invalid torrent-add response.')
        elif method == 'session-get':
            self._update_session(data['arguments'])
        elif method == 'session-stats':
            # older versions of T has the return data in "session-stats"
            if 'session-stats' in data['arguments']:
                self._update_session(data['arguments']['session-stats'])
            else:
                self._update_session(data['arguments'])
        elif method in ('port-test', 'blocklist-update', 'free-space', 'torrent-rename-path'):
            results = data['arguments']
        else:
            return None

        return results

    def _update_session(self, data):
        """
        Update session data.
        """
        if self.session:
            self.session.from_request(data)
        else:
            self.session = Session(self, data)

    def _update_server_version(self):
        """Decode the Transmission version string, if available."""
        if self.server_version is None:
            version_major = 1
            version_minor = 30
            version_changeset = 0
            version_parser = re.compile('(\d).(\d+) \((\d+)\)')
            if hasattr(self.session, 'version'):
                match = version_parser.match(self.session.version)
                if match:
                    version_major = int(match.group(1))
                    version_minor = int(match.group(2))
                    version_changeset = match.group(3)
            self.server_version = (version_major, version_minor, version_changeset)

    @property
    def rpc_version(self):
        """
        Get the Transmission RPC version. Trying to deduct if the server don't have a version value.
        """
        if self.protocol_version is None:
            # Ugly fix for 2.20 - 2.22 reporting rpc-version 11, but having new arguments
            if self.server_version and (self.server_version[0] == 2 and self.server_version[1] in [20, 21, 22]):
                self.protocol_version = 12
            # Ugly fix for 2.12 reporting rpc-version 10, but having new arguments
            elif self.server_version and (self.server_version[0] == 2 and self.server_version[1] == 12):
                self.protocol_version = 11
            elif hasattr(self.session, 'rpc_version'):
                self.protocol_version = self.session.rpc_version
            elif hasattr(self.session, 'version'):
                self.protocol_version = 3
            else:
                self.protocol_version = 2
        return self.protocol_version

    def _rpc_version_warning(self, version):
        """
        Add a warning to the log if the Transmission RPC version is lower then the provided version.
        """
        if self.rpc_version < version:
            LOGGER.warning('Using feature not supported by server. RPC version for server %d, feature introduced in %d.'
                % (self.rpc_version, version))

    def add_torrent(self, torrent, timeout=None, **kwargs):
        """
        Add torrent to transfers list. Takes a uri to a torrent or base64 encoded torrent data in ``torrent``.
        Additional arguments are:

        ===================== ===== =========== =============================================================
        Argument              RPC   Replaced by Description
        ===================== ===== =========== =============================================================
        ``bandwidthPriority`` 8 -               Priority for this transfer.
        ``cookies``           13 -              One or more HTTP cookie(s).
        ``download_dir``      1 -               The directory where the downloaded contents will be saved in.
        ``files_unwanted``    1 -               A list of file id's that shouldn't be downloaded.
        ``files_wanted``      1 -               A list of file id's that should be downloaded.
        ``paused``            1 -               If True, does not start the transfer when added.
        ``peer_limit``        1 -               Maximum number of peers allowed.
        ``priority_high``     1 -               A list of file id's that should have high priority.
        ``priority_low``      1 -               A list of file id's that should have low priority.
        ``priority_normal``   1 -               A list of file id's that should have normal priority.
        ===================== ===== =========== =============================================================

        Returns a Torrent object with the fields.
        """
        if torrent is None:
            raise ValueError('add_torrent requires data or a URI.')
        torrent_data = None
        parsed_uri = urlparse(torrent)
        if parsed_uri.scheme in ['ftp', 'ftps', 'http', 'https']:
            # there has been some problem with T's built in torrent fetcher,
            # use a python one instead
            torrent_file = urlopen(torrent)
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
        if parsed_uri.scheme in ['file']:
            filepath = torrent
            # uri decoded different on linux / windows ?
            if len(parsed_uri.path) > 0:
                filepath = parsed_uri.path
            elif len(parsed_uri.netloc) > 0:
                filepath = parsed_uri.netloc
            torrent_file = open(filepath, 'rb')
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
        if not torrent_data:
            if torrent.endswith('.torrent') or torrent.startswith('magnet:'):
                torrent_data = None
            else:
                might_be_base64 = False
                try:
                    # check if this is base64 data
                    if PY3:
                        base64.b64decode(torrent.encode('utf-8'))
                    else:
                        base64.b64decode(torrent)
                    might_be_base64 = True
                except Exception:
                    pass
                if might_be_base64:
                    torrent_data = torrent
        args = {}
        if torrent_data:
            args = {'metainfo': torrent_data}
        else:
            args = {'filename': torrent}
        for key, value in iteritems(kwargs):
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('torrent-add', argument, value, self.rpc_version)
            args[arg] = val
        return list(self._request('torrent-add', args, timeout=timeout).values())[0]

    def add(self, data, timeout=None, **kwargs):
        """

        .. WARNING::
            Deprecated, please use add_torrent.
        """
        args = {}
        if data:
            args = {'metainfo': data}
        elif 'metainfo' not in kwargs and 'filename' not in kwargs:
            raise ValueError('No torrent data or torrent uri.')
        for key, value in iteritems(kwargs):
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('torrent-add', argument, value, self.rpc_version)
            args[arg] = val
        warnings.warn('add has been deprecated, please use add_torrent instead.', DeprecationWarning)
        return self._request('torrent-add', args, timeout=timeout)

    def add_uri(self, uri, **kwargs):
        """

        .. WARNING::
            Deprecated, please use add_torrent.
        """
        if uri is None:
            raise ValueError('add_uri requires a URI.')
        # there has been some problem with T's built in torrent fetcher,
        # use a python one instead
        parsed_uri = urlparse(uri)
        torrent_data = None
        if parsed_uri.scheme in ['ftp', 'ftps', 'http', 'https']:
            torrent_file = urlopen(uri)
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
        if parsed_uri.scheme in ['file']:
            filepath = uri
            # uri decoded different on linux / windows ?
            if len(parsed_uri.path) > 0:
                filepath = parsed_uri.path
            elif len(parsed_uri.netloc) > 0:
                filepath = parsed_uri.netloc
            torrent_file = open(filepath, 'rb')
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
        warnings.warn('add_uri has been deprecated, please use add_torrent instead.', DeprecationWarning)
        if torrent_data:
            return self.add(torrent_data, **kwargs)
        else:
            return self.add(None, filename=uri, **kwargs)

    def remove_torrent(self, ids, delete_data=False, timeout=None):
        """
        remove torrent(s) with provided id(s). Local data is removed if
        delete_data is True, otherwise not.
        """
        self._rpc_version_warning(3)
        self._request('torrent-remove',
                    {'delete-local-data':rpc_bool(delete_data)}, ids, True, timeout=timeout)

    def remove(self, ids, delete_data=False, timeout=None):
        """

        .. WARNING::
            Deprecated, please use remove_torrent.
        """
        warnings.warn('remove has been deprecated, please use remove_torrent instead.', DeprecationWarning)
        self.remove_torrent(ids, delete_data, timeout)

    def start_torrent(self, ids, bypass_queue=False, timeout=None):
        """Start torrent(s) with provided id(s)"""
        method = 'torrent-start'
        if bypass_queue and self.rpc_version >= 14:
            method = 'torrent-start-now'
        self._request(method, {}, ids, True, timeout=timeout)

    def start(self, ids, bypass_queue=False, timeout=None):
        """

        .. WARNING::
            Deprecated, please use start_torrent.
        """
        warnings.warn('start has been deprecated, please use start_torrent instead.', DeprecationWarning)
        self.start_torrent(ids, bypass_queue, timeout)

    def start_all(self, bypass_queue=False, timeout=None):
        """Start all torrents respecting the queue order"""
        torrent_list = self.get_torrents()
        method = 'torrent-start'
        if self.rpc_version >= 14:
            if bypass_queue:
                method = 'torrent-start-now'
            torrent_list = sorted(torrent_list, key=operator.attrgetter('queuePosition'))
        ids = [x.id for x in torrent_list]
        self._request(method, {}, ids, True, timeout=timeout)

    def stop_torrent(self, ids, timeout=None):
        """stop torrent(s) with provided id(s)"""
        self._request('torrent-stop', {}, ids, True, timeout=timeout)

    def stop(self, ids, timeout=None):
        """

        .. WARNING::
            Deprecated, please use stop_torrent.
        """
        warnings.warn('stop has been deprecated, please use stop_torrent instead.', DeprecationWarning)
        self.stop_torrent(ids, timeout)

    def verify_torrent(self, ids, timeout=None):
        """verify torrent(s) with provided id(s)"""
        self._request('torrent-verify', {}, ids, True, timeout=timeout)

    def verify(self, ids, timeout=None):
        """

        .. WARNING::
            Deprecated, please use verify_torrent.
        """
        warnings.warn('verify has been deprecated, please use verify_torrent instead.', DeprecationWarning)
        self.verify_torrent(ids, timeout)

    def reannounce_torrent(self, ids, timeout=None):
        """Reannounce torrent(s) with provided id(s)"""
        self._rpc_version_warning(5)
        self._request('torrent-reannounce', {}, ids, True, timeout=timeout)

    def reannounce(self, ids, timeout=None):
        """

        .. WARNING::
            Deprecated, please use reannounce_torrent.
        """
        warnings.warn('reannounce has been deprecated, please use reannounce_torrent instead.', DeprecationWarning)
        self.reannounce_torrent(ids, timeout)

    def get_torrent(self, torrent_id, arguments=None, timeout=None):
        """
        Get information for torrent with provided id.
        ``arguments`` contains a list of field names to be returned, when None
        all fields are requested. See the Torrent class for more information.

        Returns a Torrent object with the requested fields.
        """
        if not arguments:
            arguments = self.torrent_get_arguments
        torrent_id = parse_torrent_id(torrent_id)
        if torrent_id is None:
            raise ValueError("Invalid id")
        result = self._request('torrent-get', {'fields': arguments}, torrent_id, require_ids=True, timeout=timeout)
        if torrent_id in result:
            return result[torrent_id]
        else:
            for torrent in result.values():
                if torrent.hashString == torrent_id:
                    return torrent
            raise KeyError("Torrent not found in result")

    def get_torrents(self, ids=None, arguments=None, timeout=None):
        """
        Get information for torrents with provided ids. For more information see get_torrent.

        Returns a list of Torrent object.
        """
        if not arguments:
            arguments = self.torrent_get_arguments
        return list(self._request('torrent-get', {'fields': arguments}, ids, timeout=timeout).values())

    def info(self, ids=None, arguments=None, timeout=None):
        """

        .. WARNING::
            Deprecated, please use get_torrent or get_torrents. Please note that the return argument has changed in
            the new methods. info returns a dictionary indexed by torrent id.
        """
        warnings.warn('info has been deprecated, please use get_torrent or get_torrents instead.', DeprecationWarning)
        if not arguments:
            arguments = self.torrent_get_arguments
        return self._request('torrent-get', {'fields': arguments}, ids, timeout=timeout)

    def list(self, timeout=None):
        """

        .. WARNING::
            Deprecated, please use get_torrent or get_torrents. Please note that the return argument has changed in
            the new methods. list returns a dictionary indexed by torrent id.
        """
        warnings.warn('list has been deprecated, please use get_torrent or get_torrents instead.', DeprecationWarning)
        fields = ['id', 'hashString', 'name', 'sizeWhenDone', 'leftUntilDone'
            , 'eta', 'status', 'rateUpload', 'rateDownload', 'uploadedEver'
            , 'downloadedEver', 'uploadRatio', 'queuePosition']
        return self._request('torrent-get', {'fields': fields}, timeout=timeout)

    def get_files(self, ids=None, timeout=None):
        """
        Get list of files for provided torrent id(s). If ids is empty,
        information for all torrents are fetched. This function returns a dictionary
        for each requested torrent id holding the information about the files.

        ::

            {
                <torrent id>: {
                    <file id>: {
                        'name': <file name>,
                        'size': <file size in bytes>,
                        'completed': <bytes completed>,
                        'priority': <priority ('high'|'normal'|'low')>,
                        'selected': <selected for download (True|False)>
                    }

                    ...
                }

                ...
            }
        """
        fields = ['id', 'name', 'hashString', 'files', 'priorities', 'wanted']
        request_result = self._request('torrent-get', {'fields': fields}, ids, timeout=timeout)
        result = {}
        for tid, torrent in iteritems(request_result):
            result[tid] = torrent.files()
        return result

    def set_files(self, items, timeout=None):
        """
        Set file properties. Takes a dictionary with similar contents as the result
        of `get_files`.

        ::

            {
                <torrent id>: {
                    <file id>: {
                        'priority': <priority ('high'|'normal'|'low')>,
                        'selected': <selected for download (True|False)>
                    }

                    ...
                }

                ...
            }
        """
        if not isinstance(items, dict):
            raise ValueError('Invalid file description')
        for tid, files in iteritems(items):
            if not isinstance(files, dict):
                continue
            wanted = []
            unwanted = []
            high = []
            normal = []
            low = []
            for fid, file_desc in iteritems(files):
                if not isinstance(file_desc, dict):
                    continue
                if 'selected' in file_desc and file_desc['selected']:
                    wanted.append(fid)
                else:
                    unwanted.append(fid)
                if 'priority' in file_desc:
                    if file_desc['priority'] == 'high':
                        high.append(fid)
                    elif file_desc['priority'] == 'normal':
                        normal.append(fid)
                    elif file_desc['priority'] == 'low':
                        low.append(fid)
            args = {
                'timeout': timeout
            }
            if len(high) > 0:
                args['priority_high'] = high
            if len(normal) > 0:
                args['priority_normal'] = normal
            if len(low) > 0:
                args['priority_low'] = low
            if len(wanted) > 0:
                args['files_wanted'] = wanted
            if len(unwanted) > 0:
                args['files_unwanted'] = unwanted
            self.change_torrent([tid], **args)

    def change_torrent(self, ids, timeout=None, **kwargs):
        """
        Change torrent parameters for the torrent(s) with the supplied id's. The
        parameters are:

        ============================ ===== =============== =======================================================================================
        Argument                     RPC   Replaced by     Description
        ============================ ===== =============== =======================================================================================
        ``bandwidthPriority``        5 -                   Priority for this transfer.
        ``downloadLimit``            5 -                   Set the speed limit for download in Kib/s.
        ``downloadLimited``          5 -                   Enable download speed limiter.
        ``files_unwanted``           1 -                   A list of file id's that shouldn't be downloaded.
        ``files_wanted``             1 -                   A list of file id's that should be downloaded.
        ``honorsSessionLimits``      5 -                   Enables or disables the transfer to honour the upload limit set in the session.
        ``location``                 1 -                   Local download location.
        ``peer_limit``               1 -                   The peer limit for the torrents.
        ``priority_high``            1 -                   A list of file id's that should have high priority.
        ``priority_low``             1 -                   A list of file id's that should have normal priority.
        ``priority_normal``          1 -                   A list of file id's that should have low priority.
        ``queuePosition``            14 -                  Position of this transfer in its queue.
        ``seedIdleLimit``            10 -                  Seed inactivity limit in minutes.
        ``seedIdleMode``             10 -                  Seed inactivity mode. 0 = Use session limit, 1 = Use transfer limit, 2 = Disable limit.
        ``seedRatioLimit``           5 -                   Seeding ratio.
        ``seedRatioMode``            5 -                   Which ratio to use. 0 = Use session limit, 1 = Use transfer limit, 2 = Disable limit.
        ``speed_limit_down``         1 - 5 downloadLimit   Set the speed limit for download in Kib/s.
        ``speed_limit_down_enabled`` 1 - 5 downloadLimited Enable download speed limiter.
        ``speed_limit_up``           1 - 5 uploadLimit     Set the speed limit for upload in Kib/s.
        ``speed_limit_up_enabled``   1 - 5 uploadLimited   Enable upload speed limiter.
        ``trackerAdd``               10 -                  Array of string with announce URLs to add.
        ``trackerRemove``            10 -                  Array of ids of trackers to remove.
        ``trackerReplace``           10 -                  Array of (id, url) tuples where the announce URL should be replaced.
        ``uploadLimit``              5 -                   Set the speed limit for upload in Kib/s.
        ``uploadLimited``            5 -                   Enable upload speed limiter.
        ============================ ===== =============== =======================================================================================

        .. NOTE::
           transmissionrpc will try to automatically fix argument errors.
        """
        args = {}
        for key, value in iteritems(kwargs):
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('torrent-set' , argument, value, self.rpc_version)
            args[arg] = val

        if len(args) > 0:
            self._request('torrent-set', args, ids, True, timeout=timeout)
        else:
            ValueError("No arguments to set")

    def change(self, ids, timeout=None, **kwargs):
        """

        .. WARNING::
            Deprecated, please use change_torrent.
        """
        warnings.warn('change has been deprecated, please use change_torrent instead.', DeprecationWarning)
        self.change_torrent(ids, timeout, **kwargs)

    def move_torrent_data(self, ids, location, timeout=None):
        """Move torrent data to the new location."""
        self._rpc_version_warning(6)
        args = {'location': location, 'move': True}
        self._request('torrent-set-location', args, ids, True, timeout=timeout)

    def move(self, ids, location, timeout=None):
        """

        .. WARNING::
            Deprecated, please use move_torrent_data.
        """
        warnings.warn('move has been deprecated, please use move_torrent_data instead.', DeprecationWarning)
        self.move_torrent_data(ids, location, timeout)

    def locate_torrent_data(self, ids, location, timeout=None):
        """Locate torrent data at the provided location."""
        self._rpc_version_warning(6)
        args = {'location': location, 'move': False}
        self._request('torrent-set-location', args, ids, True, timeout=timeout)

    def locate(self, ids, location, timeout=None):
        """

        .. WARNING::
            Deprecated, please use locate_torrent_data.
        """
        warnings.warn('locate has been deprecated, please use locate_torrent_data instead.', DeprecationWarning)
        self.locate_torrent_data(ids, location, timeout)

    def rename_torrent_path(self, torrent_id, location, name, timeout=None):
        """
        Rename directory and/or files for torrent.
        Remember to use get_torrent or get_torrents to update your file information.
        """
        self._rpc_version_warning(15)
        torrent_id = parse_torrent_id(torrent_id)
        if torrent_id is None:
            raise ValueError("Invalid id")
        dirname = os.path.dirname(name)
        if len(dirname) > 0:
            raise ValueError("Target name cannot contain a path delimiter")
        args = {'path': location, 'name': name}
        result = self._request('torrent-rename-path', args, torrent_id, True, timeout=timeout)
        return (result['path'], result['name'])

    def queue_top(self, ids, timeout=None):
        """Move transfer to the top of the queue."""
        self._rpc_version_warning(14)
        self._request('queue-move-top', ids=ids, require_ids=True, timeout=timeout)

    def queue_bottom(self, ids, timeout=None):
        """Move transfer to the bottom of the queue."""
        self._rpc_version_warning(14)
        self._request('queue-move-bottom', ids=ids, require_ids=True, timeout=timeout)
        
    def queue_up(self, ids, timeout=None):
        """Move transfer up in the queue."""
        self._rpc_version_warning(14)
        self._request('queue-move-up', ids=ids, require_ids=True, timeout=timeout)

    def queue_down(self, ids, timeout=None):
        """Move transfer down in the queue."""
        self._rpc_version_warning(14)
        self._request('queue-move-down', ids=ids, require_ids=True, timeout=timeout)

    def get_session(self, timeout=None):
        """
        Get session parameters. See the Session class for more information.
        """
        self._request('session-get', timeout=timeout)
        self._update_server_version()
        return self.session

    def set_session(self, timeout=None, **kwargs):
        """
        Set session parameters. The parameters are:

        ================================ ===== ================= ==========================================================================================================================
        Argument                         RPC   Replaced by       Description
        ================================ ===== ================= ==========================================================================================================================
        ``alt_speed_down``               5 -                     Alternate session download speed limit (in Kib/s).
        ``alt_speed_enabled``            5 -                     Enables alternate global download speed limiter.
        ``alt_speed_time_begin``         5 -                     Time when alternate speeds should be enabled. Minutes after midnight.
        ``alt_speed_time_day``           5 -                     Enables alternate speeds scheduling these days.
        ``alt_speed_time_enabled``       5 -                     Enables alternate speeds scheduling.
        ``alt_speed_time_end``           5 -                     Time when alternate speeds should be disabled. Minutes after midnight.
        ``alt_speed_up``                 5 -                     Alternate session upload speed limit (in Kib/s).
        ``blocklist_enabled``            5 -                     Enables the block list
        ``blocklist_url``                11 -                    Location of the block list. Updated with blocklist-update.
        ``cache_size_mb``                10 -                    The maximum size of the disk cache in MB
        ``dht_enabled``                  6 -                     Enables DHT.
        ``download_dir``                 1 -                     Set the session download directory.
        ``download_queue_enabled``       14 -                    Enables download queue.
        ``download_queue_size``          14 -                    Number of slots in the download queue.
        ``encryption``                   1 -                     Set the session encryption mode, one of ``required``, ``preferred`` or ``tolerated``.
        ``idle_seeding_limit``           10 -                    The default seed inactivity limit in minutes.
        ``idle_seeding_limit_enabled``   10 -                    Enables the default seed inactivity limit
        ``incomplete_dir``               7 -                     The path to the directory of incomplete transfer data.
        ``incomplete_dir_enabled``       7 -                     Enables the incomplete transfer data directory. Otherwise data for incomplete transfers are stored in the download target.
        ``lpd_enabled``                  9 -                     Enables local peer discovery for public torrents.
        ``peer_limit``                   1 - 5 peer-limit-global Maximum number of peers.
        ``peer_limit_global``            5 -                     Maximum number of peers.
        ``peer_limit_per_torrent``       5 -                     Maximum number of peers per transfer.
        ``peer_port``                    5 -                     Peer port.
        ``peer_port_random_on_start``    5 -                     Enables randomized peer port on start of Transmission.
        ``pex_allowed``                  1 - 5 pex-enabled       Allowing PEX in public torrents.
        ``pex_enabled``                  5 -                     Allowing PEX in public torrents.
        ``port``                         1 - 5 peer-port         Peer port.
        ``port_forwarding_enabled``      1 -                     Enables port forwarding.
        ``queue_stalled_enabled``        14 -                    Enable tracking of stalled transfers.
        ``queue_stalled_minutes``        14 -                    Number of minutes of idle that marks a transfer as stalled.
        ``rename_partial_files``         8 -                     Appends ".part" to incomplete files
        ``script_torrent_done_enabled``  9 -                     Whether or not to call the "done" script.
        ``script_torrent_done_filename`` 9 -                     Filename of the script to run when the transfer is done.
        ``seed_queue_enabled``           14 -                    Enables upload queue.
        ``seed_queue_size``              14 -                    Number of slots in the upload queue.
        ``seedRatioLimit``               5 -                     Seed ratio limit. 1.0 means 1:1 download and upload ratio.
        ``seedRatioLimited``             5 -                     Enables seed ration limit.
        ``speed_limit_down``             1 -                     Download speed limit (in Kib/s).
        ``speed_limit_down_enabled``     1 -                     Enables download speed limiting.
        ``speed_limit_up``               1 -                     Upload speed limit (in Kib/s).
        ``speed_limit_up_enabled``       1 -                     Enables upload speed limiting.
        ``start_added_torrents``         9 -                     Added torrents will be started right away.
        ``trash_original_torrent_files`` 9 -                     The .torrent file of added torrents will be deleted.
        ``utp_enabled``                  13 -                    Enables Micro Transport Protocol (UTP).
        ================================ ===== ================= ==========================================================================================================================

        .. NOTE::
           transmissionrpc will try to automatically fix argument errors.
        """
        args = {}
        for key, value in iteritems(kwargs):
            if key == 'encryption' and value not in ['required', 'preferred', 'tolerated']:
                raise ValueError('Invalid encryption value')
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('session-set' , argument, value, self.rpc_version)
            args[arg] = val
        if len(args) > 0:
            self._request('session-set', args, timeout=timeout)

    def blocklist_update(self, timeout=None):
        """Update block list. Returns the size of the block list."""
        self._rpc_version_warning(5)
        result = self._request('blocklist-update', timeout=timeout)
        if 'blocklist-size' in result:
            return result['blocklist-size']
        return None

    def port_test(self, timeout=None):
        """
        Tests to see if your incoming peer port is accessible from the
        outside world.
        """
        self._rpc_version_warning(5)
        result = self._request('port-test', timeout=timeout)
        if 'port-is-open' in result:
            return result['port-is-open']
        return None

    def free_space(self, path, timeout=None):
        """
        Get the ammount of free space (in bytes) at the provided location.
        """
        self._rpc_version_warning(15)
        result = self._request('free-space', {'path': path}, timeout=timeout)
        if result['path'] == path:
            return result['size-bytes']
        return None

    def session_stats(self, timeout=None):
        """Get session statistics"""
        self._request('session-stats', timeout=timeout)
        return self.session
