#!/usr/bin/python

"""mp3md5: MP3 checksums stored in ID3v2

mp3md5 calculates MD5 checksums for all MP3's on the command line
(either individual files, or directories which are recursively
processed).

Checksums are calculated by skipping the ID3v2 tag at the start of the
file and any ID3v1 tag at the end (does not however know about APEv2
tags).  The checksum is stored in an ID3v2 UFID (Unique File ID) frame
with owner 'md5' (the ID3v2 tag is created if necessary).

Usage: mp3md5.py [options] [files or directories]

-h/--help
  Output this message and exit.

-l/--license
  Output license terms for mp3md5 and exit.

-n/--nocheck
  Do not check existing checksums (so no CONFIRMED or CHANGED lines
  will be output). Causes --update to be ignored.

-r/--remove
  Remove checksums, outputting REMOVED lines (outputs NOCHECKSUM for
  files already without them).  Ignores --nocheck and --update.

-u/--update
  Instead of printing changes, update the checksum aand output UPDATED
  lines.

Depends on the eyeD3 module (http://eyeD3.nicfit.net)

Copyright 2007 G raham P oulter
"""

__copyright__ = "2007 G raham P oulter"
__author__ = "G raham P oulter"
__license__ = """This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>."""

import eyeD3
from getopt import getopt
import md5
import os
import struct
import sys

pretend = False # Whether to pretend to write tags
nocheck = False # Whether to not check existing sums
remove = False  # Whether to remove checksums
update = False  # Whether to update changed checksums
    
def log(head, body, *args):
    """Print a message to standard output"""
    print head + " "*(12-len(head)) + (body % args)

def openTag(fpath):
    """Attempt to open ID3 tag, creating a new one if not present"""
    if not eyeD3.tag.isMp3File(fpath):
        raise ValueError("NOT AN MP3: %s" % fpath)
    try:
        audioFile = eyeD3.tag.Mp3AudioFile(fpath, eyeD3.ID3_V2)
    except eyeD3.tag.InvalidAudioFormatException, ex:
        raise ValueError("ERROR IN MP3: %s" % fpath)
    tag = audioFile.getTag()
    if tag is None:
        tag = eyeD3.Tag(fpath)
        tag.header.setVersion(eyeD3.ID3_V2_3)
        if not pretend:
            tag.update()
    return tag

### WARNING: REMEMBER TO UPDATE THE COPY IN MD5DIR
def calculateUID(filepath):
    """Calculate MD5 for an MP3 excluding ID3v1 and ID3v2 tags if
    present. See www.id3.org for tag format specifications."""
    f = open(filepath, "rb")
    # Detect ID3v1 tag if present
    finish = os.stat(filepath).st_size;
    f.seek(-128, 2)
    if f.read(3) == "TAG":
        finish -= 128
    # ID3 at the start marks ID3v2 tag (0-2)
    f.seek(0)
    start = f.tell()
    if f.read(3) == "ID3":
        # Bytes w major/minor version (3-4)
        version = f.read(2)
        # Flags byte (5)
        flags = struct.unpack("B", f.read(1))[0]
        # Flat bit 4 means footer is present (10 bytes)
        footer = flags & (1<<4)
        # Size of tag body synchsafe integer (6-9)
        bs = struct.unpack("BBBB", f.read(4))
        bodysize = (bs[0]<<21) + (bs[1]<<14) + (bs[2]<<7) + bs[3]
        # Seek to end of ID3v2 tag
        f.seek(bodysize, 1)
        if footer:
            f.seek(10, 1)
        # Start of rest of the file
        start = f.tell()
    # Calculate MD5 using stuff between tags
    f.seek(start)
    h = md5.new()
    h.update(f.read(finish-start))
    f.close()
    return h.hexdigest()

def readUID(fpath):
    """Read MD5 UID from ID3v2 tag of fpath."""
    tag = openTag(fpath)
    for x in tag.getUniqueFileIDs():
        if x.owner_id == "md5":
            return x.id
    return None

def removeUID(fpath):
    """Remove MD5 UID from ID3v2 tag of fpath"""
    tag = openTag(fpath)
    todel = None
    for i, x in enumerate(tag.frames):
        if isinstance(x, eyeD3.frames.UniqueFileIDFrame) \
               and x.owner_id == "md5":
            todel = i
            break
    if todel is not None:
        del tag.frames[i]
        if not pretend:
            tag.update(eyeD3.ID3_V2_3)
        return True
    else:
        return False

def writeUID(fpath, uid):
    """Write the MD5 UID in the ID3v2 tag of fpath."""
    tag = openTag(fpath)
    present = False
    for x in tag.getUniqueFileIDs():
        if x.owner_id == "md5":
            present = True
            x.id = uid
            break
    if not present:
        tag.addUniqueFileID("md5", uid)
    if not pretend:
        tag.update(eyeD3.ID3_V2_3)

def mungeUID(fpath):
    "Update the MD5 UID on the tag"""
    if remove:
        if removeUID(fpath):
            log("REMOVED", fpath)
        else:
            log("NOCHECKSUM", fpath)
    else:
        cur_uid = readUID(fpath)
        if cur_uid is None:
            new_uid = calculateUID(fpath)
            writeUID(fpath, new_uid)
            log("ADDED", fpath)
        elif not nocheck:
            new_uid = calculateUID(fpath)
            if cur_uid == new_uid:
                log("CONFIRMED", fpath)
            elif update:
                writeUID(fpath, new_uid)
                log("UPDATED", fpath)
            else:
                log("BROKEN", fpath)

if __name__ == "__main__":
    optlist, args = getopt(sys.argv[1:], "hlnru", ["help","license","nocheck","remove","update"])
    for key, value in optlist:
        if key in ("-h","--help"):
            print __doc__
            sys.exit(0)
        elif key in ("-l","--license"):
            print license
            sys.exit(0)
        elif key in ("-n","--nocheck"):
            nocheck = True
        elif key in ("-r", "--remove"):
            remove = True
        elif key in ("-u", "--update"):
            update = True
    for start in args:
        if os.path.isfile(start):
            if start.endswith(".mp3"):
                mungeUID(start)
        elif os.path.isdir(start):
            for root, dirs, files in os.walk(start):
                dirs.sort()
                files.sort()
                for fname in files:
                    if fname.endswith(".mp3"):
                        mungeUID(os.path.join(root,fname))
        else:
            log("WARNING", "%s does not exist", start)
