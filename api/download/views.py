from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.vfs.models import VFSFile
from api import auth, libfiles
from edbw import settings
import os
import zipfile
import io

def files_callback(key, person, user_type, id_map={}):
    
    file_records = get_files(id_map['file'])
    
    if len(file_records) == 1 and ('mode' not in id_map or 'zip' not in id_map['mode']):
        # Return single files as txt
        
        f = file_records[0]
        
        resp = HttpResponse(open(f.path, 'r').read(), content_type='text/plain')
        resp['Content-Disposition'] = 'attachment; filename={}'.format(f.name)
        #resp['Content-Length'] = os.path.getsize(file_full_path)
    else:
        # Multiple files get returned as a zip
        s = io.BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for f in file_records:
            zf.write(f.path, f.name)
            
        zf.close()

        resp = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
        resp['Content-Disposition'] = 'attachment; filename=files.zip'
        #resp['Content-length'] = s.tell()

    return resp
    

def get_files(ids):
    files = []

    for id in ids:
      file = get_file(id);

      files.append(file)

    return files
    
    
def get_file(id):
    file = VFSFile.objects.get(id=id)
    
    # We do not use os.path.join because paths are stored in an
    # absolute form in the database so we just prefix with the real
    # path
    path = settings.DATA_DIR + file.path #os.path.join(settings.DATA_DIR, file.path)
    
    return libfiles.FileRecord(id, file.name, path)
    
  
def files(request):
    id_map = {}
    
    auth.parse_ids(request, 'file', id_map=id_map)
    auth.parse_params(request, 'mode', id_map=id_map)

    return auth.auth(request, files_callback, id_map=id_map, check_for={'file'})
