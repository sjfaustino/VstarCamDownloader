#VstarCamDownloader v1.0.0 by RB
#Edited by Sergio Faustino
#Usage Example: VstarCamDownloader.py cameraip.changeip.net 28080 videos/IPCam1 MOVE admin 88888888

import sys
import os
import urllib2
import base64
import socket

def downloadfile(url, filename, directory, username, password):

    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    up = urllib2.urlopen(request)
    meta = up.info();
    file_size = int(meta.getheaders("Content-Length")[0])

    #Check if file already downloaded
    if os.path.exists(directory + '/' + filename) and os.path.getsize(directory + '/' + filename) == file_size:
        print 'Already downloaded, skipping file ' + filename + ' with size ' + str(file_size);
    else:
        fp = open(directory + '/' + filename, 'wb');
        print "Downloading: %s Bytes: %s" % (filename, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = up.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            fp.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        fp.close()

def deletefile(fileurl):
    try:
        response = urllib2.urlopen(fileurl, timeout = 10);
    except urllib2.URLError as e:
        print "Error - Failed to access URL";
        sys.exit(5);
    except socket.timeout as e:
        print "Error - Failed to access URL";
        sys.exit(6);
    except:
        print "Error - Is this IP a vstarcam camera?";
        sys.exit(7)

    print "Deleted file " + file
 
def isgoodipv4(s):
    ip = socket.gethostbyname(s)
    pieces = ip.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False

if len(sys.argv) < 6:
  print "VstarCamDownloader.py [IP] [PORT] [OUTPUT DIRECTORY] [COPY/MOVE] [USERNAME] [PASSWORD]";
  sys.exit(1);

ip = sys.argv[1];
directory = sys.argv[3];
operation = sys.argv[4];
username = sys.argv[5];
password = sys.argv[6];

try:
    port = int(sys.argv[2]);
except:
    print "Error Port isn't valid";
    sys.exit(2);

#check if ip is valid
if isgoodipv4(ip) == False:
    print "Error - IP address isn't valid";
    sys.exit(3);

#check if port is in range
if port < 0 or port > 65535:
    print "Error - Port isn't valid 2";
    sys.exit(4);

#make directory if doesnt exist
if os.path.exists(directory) == False:
    os.mkdir(directory, 0755);

#test creds
url = 'http://' + ip + ':' + str(port) + '/get_record_file.cgi?loginuse=' + username + '&loginpas=' + password;

try:
    response = urllib2.urlopen(url, timeout = 10);
except urllib2.URLError as e:
    print "Error - Failed to access URL";
    sys.exit(5);
except socket.timeout as e:
    print "Error - Failed to access URL";
    sys.exit(6);
except:
    print "Error - Is this IP a vstarcam camera?";
    sys.exit(7)

#return output
output = response.read();

#check if page returns creds failure
if "Auth Failed" in output:
    print "Error - Invalid user credentials";
    sys.exit(8);

lines = output.split('\n');

files = [];
filelength = [];

#trim file name and length from scraping output
for line in lines:
    if "h264" in line:
        files.append(line[-26:-3]);

    if "record_size0[" in line:
        filelength.append(line[-10:-2]);

#Get files and put them into the output directory
print 'Found ' + str(len(files)) + ' files';
for file in files:
    fileurl = 'http://' + ip + ':' + str(port) + '/record/' + file;
    downloadfile(fileurl, file, directory, username, password);

    if operation == 'MOVE':
        fileurl = 'http://' + ip + ':' + str(port) + '/del_file.cgi?name=' + file + '&loginuse=' + username + '&loginpas=' + password;
        deletefile(fileurl);

print "Finished downloading files to " + directory;
