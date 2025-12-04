from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, StreamingHttpResponse 
import random
import os
import uuid
from .models import File
from .dicts import name_size_file, file_extension_language, img_formats
import base64
from paste.models import pin
from django.conf import settings
import boto3
from gemldrive.storage_backends import MediaStorage

s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

class DriveView:
    def index(request):
        if request.method == 'POST':
            password = request.POST['password']
            data = {}
            data['server'] = 'GemlDrive'
            data['data'] = []
            if password == os.environ['PASSWORD_USER']:
                files = File.objects.all()
                files_size = {file['Key'].split('/')[1]: file['Size'] for file in s3.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='media/')['Contents'][1:]}
                total_size = sum(files_size.values())
                data['total_size_present'] = total_size * 100 / 5242880000
                if total_size != 0:
                    d = 0
                    while True:
                        if total_size / 1024 > 1:
                            d += 1
                            total_size = round(total_size / 1024, 2)
                        else:
                            break
                    total_size = str(total_size) + name_size_file[d]
                    data['total_size_text'] = total_size
                else:
                    data['total_size_text'] = '0.0GB'
                for file in files:
                    file_size = files_size[file.file_id]
                    d = 0
                    while True:
                        if file_size / 1024 > 1:
                            d += 1
                            file_size = round(file_size / 1024, 2)
                        else:
                            break
                    file_size = str(file_size) + name_size_file[d]
                    url = f'https://ipfs.filebase.io/ipfs/{file.cid}?filename={file.file_name}&download=true'
                    data['data'].append({'name': file.file_name, 'id': file.file_id, 'size': file_size, 'url': url, 'date': file.date.strftime('%Y-%m-%d %H:%M:%S')})
                data['pins'] = []
                for pins in pin.objects.all():
                    data['pins'].append({'url': pins.slug, 'date': pins.date.strftime('%Y-%m-%d %H:%M:%S')})
                return render(request, 'drive/index.html', data)
            else:
                sess_id = f"sess_{random.randint(100000,999999)}"
                request.session[sess_id] = 'Invalid password'
                return redirect(f'/login/?q={sess_id}')
        return redirect('/')

    def handle_uploaded_file(f, file_id, file_name):
        upload = s3.create_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f'media/{file_id}',
            ACL='public-read',
        )
        upload_id = upload['UploadId']
        parts = []
        part_number = 1
        chunk_size = 5 * 1024 * 1024
        for chunk in f.chunks(chunk_size):
            part = s3.upload_part(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=f'media/{file_id}',
                UploadId=upload_id,
                PartNumber=part_number,
                Body=chunk
            )
            parts.append({
                'PartNumber': part_number,
                'ETag': part['ETag']
            })
            yield str(50.00 if (chunk_size * part_number) * 100 / f.size / 2 > 50 else round((chunk_size * part_number) * 100 / f.size / 2, 2)) + ' '
            part_number += 1
        s3.complete_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f'media/{file_id}',
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        File(file_id=file_id, file_name=file_name, cid=s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f'media/{file_id}')['ResponseMetadata']['HTTPHeaders']['x-amz-meta-cid']).save()
        return

    def upload(request):
        if request.method == 'POST':
            try:
                file = request.FILES['upload_file']
            except:
                return HttpResponse('1')
            file_id = uuid.uuid4()
            file_name = file.name
            files = File.objects.all()
            list_files = [file.file_name for file in files]
            file_ids = [file.file_id for file in files]
            while file_id in file_ids:
                file_id = uuid.uuid4()
            del file_ids, files
            if file.name in list_files:
                i = 1
                while True:
                    index_dot = file_name.rindex('.')
                    if file_name[:index_dot] + f'({i})' + file_name[index_dot:] in list_files:
                        i += 1
                    else:
                        file_name = file_name[:index_dot] + f'({i})' + file_name[index_dot:]
                        break
            return StreamingHttpResponse(DriveView.handle_uploaded_file(file, file_id, file_name))
        return HttpResponse('1')

    def delete(request, file_id):
        try:
            if request.GET['1dbfb090cac3446b9fa93805f3a694f0'] == '198190':
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=f'media/{file_id}'
                )
                File.objects.get(file_id=file_id).delete()
        except:
            raise Http404()
        return HttpResponse('1')



    def preview(request, file_id):
        try:
            file = File.objects.get(file_id=file_id)
        except:
            raise Http404()
        suffix = '.'+file.file_name.split('.')[-1]
        if file_extension_language.get(suffix,None) != None:
            type_file = 'text'
            type_file_name = file_extension_language.get(suffix,None)
            storage = MediaStorage()
            content = storage.open(f'{file.file_id}', 'r').read()
        elif suffix in img_formats:
            type_file = 'img'
            type_file_name = 'image'
            storage = MediaStorage()
            content = base64.b64encode(storage.open(f'{file.file_id}', 'rb').read()).decode('utf-8')
        else:
            type_file = 'other'
            type_file_name = 'other'
            content = None

        file_size = s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,Key=f'media/{file.file_id}')['ContentLength']
        d = 0
        while True:
            if file_size / 1024 > 1:
                d += 1
                file_size = round(file_size / 1024, 2)
            else:
                break
        file_size = str(file_size) + name_size_file[d]

        data = {
            'type': type_file,
            'type_file_name': type_file_name,
            'file_suffix': suffix,
            'file_id': file.file_id,
            'file_size': file_size,
            'file_name': file.file_name,
            'file_date': file.date.strftime('%Y-%m-%d %H:%M:%S'),
            'data': content,
            'url': f'https://ipfs.filebase.io/ipfs/{file.cid}?filename={file.file_name}&download=true'
        }
        return render(request, 'drive/preview.html', data)
