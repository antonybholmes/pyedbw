from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.vfs.models import VFSFile
from api import auth, libfiles
from edbw import settings
import os
import zipfile
import io
import tempfile
import s3fs
import libhttp

def files_callback(key, person, user_type, id_map={}):
    file_records = get_files(id_map['file'])
    
    fs = s3fs.S3FileSystem(anon=True)
    
    if id_map['mode'][0] == 'zip':
        # Multiple files get returned as a zip
        s = io.BytesIO()
        
        # The zip compressor
        zf = zipfile.ZipFile(s, "w")
        
        # at least one of the specified files must be put in the zip for
        # it to be sent to the client
        exists = False
                
        for record in file_records:
            tmp = download_s3_file(fs, record.path)
            
            if tmp is not None:
                #zf.write(record.path, record.name)
                zf.write(tmp.name, record.name)
                tmp.close()
                # Flag that we found at least one valid file, so zip can be
                # returned
                exists = True
        
        # close zip writer. zip contents are in s bytebuffer.
        zf.close()
        
        if exists:
            resp = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
            resp['Content-Disposition'] = 'attachment; filename=files.zip'
            #resp['Content-length'] = s.tell()
        else:
            raise PermissionDenied
    else:
        # Return single file
        record = file_records[0]
        
        tmp = download_s3_file(fs, record.path)
        
        if tmp is not None:
            resp = HttpResponse(open(tmp.name, 'rb').read(), content_type='application/octet-stream') #'text/plain')
            resp['Content-Disposition'] = 'attachment; filename={}'.format(record.name)
            tmp.close()
        else:
            raise PermissionDenied
        #resp['Content-Length'] = os.path.getsize(file_full_path)
        
    return resp

def download_s3_file(fs, path):
    # If obj does not exist on s3, return none
    if not fs.exists(path):
        return None
    
    # download to tmp file
    tmp = tempfile.NamedTemporaryFile()
    print(tmp.name)
    tmp.write(fs.open(path).read())
    return tmp
    

def get_files(ids):
    files = []

    for id in ids:
      file = get_file(id);
      
      if file is not None:
          files.append(file)

    return files
    
    
def get_file(id):
    if id < 1:
        return None
    
    file = VFSFile.objects.get(id=id)
    
    # We do not use os.path.join because paths are stored in an
    # absolute form in the database so we just prefix with the real
    # path
    #path = settings.DATA_DIR + file.path #os.path.join(settings.DATA_DIR, file.path)
    path = settings.AWS_BUCKET + file.path
    
    return libfiles.FileRecord(id, file.name, path)
    
  
def files(request):
    id_map = libhttp.parse_params(request, {'file':-1, 'mode':'plain'})
    
    #auth.parse_ids(request, 'file', id_map=id_map)
    #auth.parse_params(request, {'mode':'plain'}, id_map=id_map) #, id_map=id_map)

    return auth.auth(request, files_callback, id_map=id_map)
