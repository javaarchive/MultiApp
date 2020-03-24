import multiapp as ma
print("====Loading Multiapp=====")
print("Enter help for help, and exit to exit!")
import time
import os,json,itertools
import shutil
animation = not os.path.isfile("noanimation")
def animate(message):
    if animation == False:
        print(message)
        return
    for x in message:
        print(x,end="")
        time.sleep(0.02)
    print()
def smartSplit(cmd):
    l = cmd.split(" ")
    merging = []
    curMerge = False
    newsplit = []
    for x in l:
        if x.startswith("\""):
            merging = [x[1:]]
            curMerge = True
        elif x.endswith("\"") and curMerge:
            curMerge = False
            merging.append(x[:-1])
            newsplit.append(" ".join(merging))
        elif merging:
            merging.append(x)
        else:
            newsplit.append(x)
    return newsplit
def showLicense(fileiter):
    animate("Press any key and enter to stop")
    while True:
        try:
            line = next(fileiter)
        except Exception as e:
            line = "File End"
            print(e)
            break
        print(line)
        donext = input("")
        if donext != "":
            break
    answer = ""
    while answer == "":
        answer= input("Now do you agree to the license(s)?")
    return answer
prompt = "MutliApp>"
repo = ma.readRepo("repo.json")
config = ma.readRepo("multiapp.json")
while True:
    command = input(prompt)
    lcmd = smartSplit(command)
    try:
        if len(lcmd) == 0:
            print("No command?")
        elif lcmd[0] == "changeprompt":
            prompt = lcmd[1]
        elif lcmd[0] == "help":
            print('''
            Hi
            Try running listapps 1 or start <appname>
            ''')
        elif lcmd[0] == "listapps":
            if len(lcmd)<2:
                animate("Not enough options. Use \" to ignore spaces in options")
            else:
                each = 10
                if len(lcmd) >= 3:
                    each = int(lcmd[2])
                startnum = int(lcmd[1])-1
                startIndex = startnum * each
                endIndex = (startnum+1) * each
                if endIndex >= len(repo):
                    endIndex = len(repo)
                for x in range(startIndex,endIndex):
                    app = repo[x]
                    print(str(x)+" | "+app["name"])
        elif lcmd[0] == "install":
            if len(lcmd) >= 3:
                reponum = int(lcmd[1])
                location = lcmd[2]
                app = repo[reponum]
                animate("Download App...")
                ma.downloadFile(app["url"],"app.zip")
                animate("Extracting App...")
                ma.extractFile("app.zip",os.path.join(os.getcwd(),location))
                if "license" in app.keys():
                    animate("Reading LICENSE")
                    f = open("LICENSES.txt","r",encoding = "UTF-8")
                    fileiter = itertools.islice(f, app["license"], None)
                    if not showLicense(fileiter).lower().startswith("y"):
                        print("Deleting software")
                        shutil.rmtree(os.path.join(os.getcwd(),location))
                    f.close()
                animate("Finished")
                f = open(os.path.join(os.getcwd(),location,"app.json"),"w")
                f.write(json.dumps(app))
                f.close()
            else:
                print("Not enough information")
        elif lcmd[0] == "start":
            if len(lcmd) >= 2:
                appname = lcmd[1]
                f = open(os.path.join(os.getcwd(),appname,"app.json"))
                app = json.loads(f.read())
                f.close()
                ma.openFile(os.path.join(os.getcwd(),location,app["startfile"]))
            else:
                print("Not enough info")
        elif lcmd[0] == "update":
            answer = input("Are you sure about this? If the response sent is invalid your multiapp insatllation can break. ")
            if answer.lower().startswith("y"):
                ma.downloadFile(config["repourl"],"repo.json")
                ma.downloadFile(config["self"],"multiapp.json")
                ma.downloadFile(config["license"],"LISCENSES")
            else:
                print("ok")
        elif lcmd[0] == "reload":
            print("Reloading repo")
            repo = ma.readRepo("repo.json")
        elif lcmd[0] == "delete":
            if len(lcmd) > 1:
                response = input("Delete "+lcmd[1])
                if response.lower().startswith("y"):
                    shutil.rmtree(os.path.join(os.getcwd(),lcmd[1]))
        elif lcmd[0] == "exit":
            break
        else:
            print("Error: That's not a command :(")
    except Exception as e:
        print("Command Failure to "+str(e))
