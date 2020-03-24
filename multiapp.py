import urllib, os
import urllib.request, shutil, zipfile
def downloadFile(url,file_name):
    # https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3?noredirect=1&lq=1
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
curDir = os.getcwd()
def openFile(filepath):
    os.chdir(filepath[:filepath.rfind("\\")])
    os.startfile(filepath,"open")
    os.chdir(curDir)
def extractFile(filename, directory):
    try:
        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(directory)
    except:
        import py7zr
        archive = py7zr.SevenZipFile(filename, mode='r')
        archive.extractall(path=directory)
        archive.close()

def readRepo(filename):
    import json
    f = open(filename, "r")
    repo = json.loads(f.read())
    f.close()
    return repo
def readConfig(filename):
    import json
    f = open(filename, "r")
    repo = json.loads(f.read())
    f.close()
    return repo
