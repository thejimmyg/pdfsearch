import os
import sys
import subprocess
import hashlib
from common import schema
from whoosh.index import create_in

os.makedirs('build/search_index', exist_ok=True)
ix = create_in('build/search_index', schema)
writer = ix.writer()

for root, dirs, files in os.walk('src'):
    if root == 'src':
        for directory in dirs:
            os.makedirs(os.path.join('build/page', directory), exist_ok=True)
            os.makedirs(os.path.join('build/text', directory), exist_ok=True)
            os.makedirs(os.path.join('build/png', directory), exist_ok=True)
    for filename in files:
        name, ext = os.path.splitext(filename)
        authority = os.path.relpath(root, 'src')
        print('Generating ID for', authority, 'PDF', "'"+name+ext+"'", end=' ... ')
        m = hashlib.sha1()
        fp = open(os.path.join(root, filename), 'rb')
        m.update(fp.read())
        fp.close()
        uid = m.hexdigest()
        print('done. ID is', uid)
        name = os.path.join(authority, name)
        os.makedirs(os.path.join('build/page', name), exist_ok=True)
        os.makedirs(os.path.join('build/text', name), exist_ok=True)
        os.makedirs(os.path.join('build/png', name), exist_ok=True)
        print('Splitting PDF', "'"+name+ext+"'", 'into pages', end=' ... ')
        sys.stdout.flush()
        split_process = subprocess.Popen([
            'pdfseparate',
            os.path.join(root, filename),
            os.path.join('build/page', name, '%d.pdf')
        ])
        exit_code = split_process.wait()
        if exit_code != 0:
            print('ERROR')
            continue
        if exit_code == 0:
            print('done.')
            for page_filename in os.listdir(os.path.join('build/page', name)):
                page_number, ext = os.path.splitext(page_filename)
                print('Converting PDF page', "'"+os.path.join('build/page', name, page_filename)+"'", 'into a PNG', end=' ... ')
                sys.stdout.flush()
                png_process = subprocess.Popen([
                    'convert',
                    '-density', '300',
                    os.path.join('build/page', name, page_filename),
                    os.path.join('build/png', name, page_number+'.png')
                ])
                exit_code = png_process.wait()
                if exit_code != 0:
                    print('ERROR')
                if exit_code == 0:
                    print('done.')
                print('Extracting text from PDF', "'"+os.path.join('build/page', name, page_filename)+"'", end=' ...')
                sys.stdout.flush()
                text_process = subprocess.Popen([
                    'env/bin/pdf2txt.py',
                    os.path.join('build/page', name, page_filename),
                ], stdout=subprocess.PIPE)
                stdout, stderr = text_process.communicate()
                exit_code = text_process.wait()
                if exit_code == 0:
                    fp = open(os.path.join('build/text', name, page_number+'.txt'), 'wb')
                    fp.write(stdout)
                    fp.close()
                    writer.add_document(
                      uid=uid,
                      name=name,
                      page_number=page_number,
                      authority=authority,
                      content=stdout.decode('utf8')
                    )
                    print('done.')
                else:
                    print('ERROR')

writer.commit()
