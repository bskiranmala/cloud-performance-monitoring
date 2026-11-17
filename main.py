from MailSent import send_email
import requests
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import base64
import pyautogui
from flask import Response
import psutil
import time
import platform
import wmi
import subprocess
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import Flask, render_template, redirect, request, session
from flask import Flask, render_template
import random
import os
from flask import Flask, request, jsonify
import os
import pythoncom
import wmi
import threading
import firebase_admin
import random
from flask import Flask, request
from firebase_admin import credentials, firestore
import urllib.request

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# Configuration       
cloudinary.config( 
    cloud_name = "dz7knwg0z", 
    api_key = "554627271213752", 
    api_secret = "b_JSm4Faya6nVLFDHZLqaT9JvPI", # Click 'View API Keys' above to copy your API secret
    secure=True)

app = Flask(__name__)
app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def save_image_from_url(image_url, filename):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  
        # Raise an exception for bad status codes (4xx or 5xx)

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Image '{filename}' downloaded successfully from {image_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {image_url}: {e}")
    except IOError as e:
        print(f"Error saving image to {filename}: {e}")

def wmi_thread_function():
    pythoncom.CoInitialize() # Initialize COM for this thread
    try:
        c = wmi.WMI()
        # Perform WMI operations here
        print("\nWMI Details : ")
        data1=[]
        for process in c.Win32_Process():
            print(f"Process: {process.Name}, ID: {process.ProcessId}")
            data1.append(f"Process: {process.Name}, ID: {process.ProcessId}")
        my_system = c.Win32_ComputerSystem()[0]
        print(f"Manufacturer: {my_system.Manufacturer}")
        print(f"Model: {my_system.Model}")
        print(f"Name: {my_system.Name}")
        print(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
        print(f"SystemType: {my_system.SystemType}")
        print(f"SystemFamily: {my_system.SystemFamily}")
        print(f"Memory :{psutil.virtual_memory()}")
        
        temp["Manufacturer"]=f"{my_system.Manufacturer}"
        temp["Model"]=f"{my_system.Model}"
        temp["Name"]=f"{my_system.Name}"
        temp["NumberOfProcessors"]=f"{my_system.NumberOfProcessors}"
        temp["SystemType"]=f"{my_system.SystemType}"
        temp["SystemFamily"]=f"{my_system.SystemFamily}"
        temp["Memory"]=f"{psutil.virtual_memory()}"
        temp["processes"]=data1
    finally:
        pythoncom.CoUninitialize() # Uninitialize COM for this thread

data, temp=[], {}
@app.route('/getdatafromurl')
def get_system_resources():
    print("--- System Resource Usage ---")
    
    id=request.args['id']
    ipaddress=request.args['ipaddress']
    userid=request.args['userid']
    
    print("Id : ", id)
    print("Ip Address : ", ipaddress)
    print("User Id : ", userid)

    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)  # CPU utilization over 1 second
    print(f"CPU Usage: {cpu_percent}%")
    temp['CPU_Usage']=f"{cpu_percent}%"
    temp['UserId']=userid
    # Memory Usage
    virtual_memory = psutil.virtual_memory()
    print(f"Total Memory: {round(virtual_memory.total / (1024**3), 2)} GB")
    print(f"Used Memory: {round(virtual_memory.used / (1024**3), 2)} GB")
    print(f"Available Memory: {round(virtual_memory.available / (1024**3), 2)} GB")
    print(f"Memory Usage Percentage: {virtual_memory.percent}%")
    
    temp['TotalMemory']=f"{round(virtual_memory.total / (1024**3), 2)} GB"
    temp['UsedMemory']=f"{round(virtual_memory.used / (1024**3), 2)} GB"
    temp['AvailableMemory']=f"{round(virtual_memory.available / (1024**3), 2)} GB"
    temp['MemoryUsagePercentage']=f"{virtual_memory.percent}%"

    # Disk Usage (for the root directory or a specific path)
    disk_usage = psutil.disk_usage('C:/')
    print(f"Total Disk Space: {round(disk_usage.total / (1024**3), 2)} GB")
    print(f"Used Disk Space: {round(disk_usage.used / (1024**3), 2)} GB")
    print(f"Free Disk Space: {round(disk_usage.free / (1024**3), 2)} GB")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")
    
    temp["TotalDiskSpace"]=f"{round(disk_usage.total / (1024**3), 2)} GB"
    temp["UsedDiskSpace"]=f"{round(disk_usage.used / (1024**3), 2)} GB"
    temp["FreeDiskSpace"]=f"{round(disk_usage.free / (1024**3), 2)} GB"
    temp["DiskUsagePercentage"]=f"{disk_usage.percent}%"
    
    temp["used_disk_space"]=f"{round(disk_usage.used / (1024**3), 2)}"
    temp["free_disk_space"]=f"{round(disk_usage.free / (1024**3), 2)}"
    temp["cpuusage"]=f"{cpu_percent}"
    temp["disk_usage_percentage"]=f"{disk_usage.percent}"
    
    # Network I/O (bytes sent and received)
    net_io = psutil.net_io_counters()
    print(f"Bytes Sent: {round(net_io.bytes_sent / (1024**2), 2)} MB")
    print(f"Bytes Received: {round(net_io.bytes_recv / (1024**2), 2)} MB")
    
    temp["BytesSent"]=f"{round(net_io.bytes_sent / (1024**2), 2)} MB"
    temp["BytesReceived"]=f"{round(net_io.bytes_recv / (1024**2), 2)} MB"

    # Other information (optional)
    print(f"Number of CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
    print(f"Number of CPU Cores (Logical): {psutil.cpu_count(logical=True)}")
    print(f"Boot Time: {time.ctime(psutil.boot_time())}")
    
    temp["NumberofCPUCoresPhysical"]=f"{psutil.cpu_count(logical=False)}"
    temp["NumberofCPUCoresLogical"]=f"{psutil.cpu_count(logical=True)}"
    temp["BootTime"]=f"{time.ctime(psutil.boot_time())}"

    my_system = platform.uname()

    print(f"System: {my_system.system}")
    print(f"Node Name: {my_system.node}")
    print(f"Release: {my_system.release}")
    print(f"Version: {my_system.version}")
    print(f"Machine: {my_system.machine}")
    print(f"Processor: {my_system.processor}")
    
    temp["System"]=f"{my_system.system}"
    temp["NodeName"]=f"{my_system.node}"
    temp["Release"]=f"{my_system.release}"
    temp["Version"]=f"{my_system.version}"
    temp["Machine"]=f"{my_system.machine}"
    temp["Processor"]=f"{my_system.processor}"    
    
    # Create and start the thread
    thread = threading.Thread(target=wmi_thread_function)
    thread.start()
    thread.join()
    
    # traverse the info
    Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
    new = []
    # arrange the string into clear info
    print("\nSub Process Infm : ")
    for item in Id:
        new.append(str(item.split("\r")[:-1]))
    sub_procesess=[]
    for i in new:
        #print(i[2:-2])
        print(" ".join(i.split()))
        sub_procesess.append(" ".join(i.split()))    
    temp["SubProcess"] = sub_procesess
    
    # Take a screenshot of the entire screen
    screenshot_image = pyautogui.screenshot()
    # Save the screenshot to a file (e.g., "my_screenshot.png")
    
    filename = "Img"+id+".jpg"
    screenshot_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #screenshot_image.save("my_screenshot.png")
    print("Screenshot saved as my_screenshot.png")
    #print("Temp Data : ", temp)    
        
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as img:
        imagebase64 = base64.b64encode(img.read())
        
    # Upload an image
    upload_result = cloudinary.uploader.upload(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                           public_id="Img"+id)
    print("Secure Url : ", upload_result["secure_url"])

    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url(filename, fetch_format="auto", quality="auto")
    print(optimize_url)

    # Transform the image: auto-crop to square aspect_ratio
    auto_crop_url, _ = cloudinary_url(filename, width=500, height=500, crop="auto", gravity="auto")
    print(auto_crop_url)
    
    temp['imagebase64']=imagebase64
    temp['id']=id
    temp['ipaddress']=ipaddress
    temp['imageurl']=upload_result["secure_url"]    
    db = firestore.client()
    newdb_ref = db.collection('systemdetails')
    newdb_ref.document(id).set(temp)
        
    #print(imagebase64)
    response = jsonify({"id":id})
    #return Response([id,imagebase64], status=201, mimetype='text/json', headers={'X-App-Info': 'FlaskApp'})
    return response

@app.route('/getsystemdetailsfromipaddress', methods=['GET','POST'])
def getsystemdetailsfromipaddress():
    try:
        msg,data,graph_data='','',[]
        if(request.method=="POST"):
            id=str(round(time.time()))
            userid=session['userid']
            ipaddress=request.form['ipaddress']
            url=f"http://{ipaddress}:5000/getdatafromurl?ipaddress={ipaddress}&id={id}&userid={userid}"
            print("Url : ", url)
            #id="1763037509"            
            with urllib.request.urlopen(url) as response:
                data = response.read()
                # Decode the data if it's text-based (e.g., HTML, JSON)
                decoded_data = data.decode('utf-8')
                print("Data : ", jsonify(decoded_data))
                #id=decoded_data['id']
                print("Id : ", id)
                #byte=decoded_data['imagebase64']
                #filename = "Img"+id+".jpg"
                #decode = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb')  # Open image file to save.
                #decode.write(base64.b64decode(byte))  # Decode and write data.
                #decode.close()
                db = firestore.client()
                data = db.collection('systemdetails').document(id).get().to_dict()
                imageurl = data['imageurl']
                output_filename= "Img"+id+".jpg"
                save_image_from_url(imageurl, output_filename)            
                #print("Image Url ", imageurl)
                print("Image Saved Success")
                msg="Data Fetched Success"
            #db = firestore.client()
            #data = db.collection('systemdetails').document(id).get().to_dict()
            #return "Data Fetched Success"
                freediskspace = data['free_disk_space']
                useddiskspace = data['used_disk_space']
                cpu_percent = data["cpuusage"]
                disk_usage_percentage = data["disk_usage_percentage"]                
                graph_data = [
                    { "label": "Free Disk Space", "y": freediskspace },
                    { "label": "Used Disk Space", "y": useddiskspace },
                    { "label": "Cpu Percent", "y": cpu_percent },
                    { "label": "Disk Usage Percentage", "y": disk_usage_percentage }]
                print("Graph Data : ", graph_data)
        return render_template('getsystemdetailsfromipaddress.html',
                               data=data,msg=msg, graph_data=graph_data)
    except urllib.error.URLError as e:
        print(f"Error fetching URL: {e.reason}")
        return render_template('getsystemdetailsfromipaddress.html',
                               data=data,msg=f"Error fetching URL: {e.reason}")

@app.route('/')
@app.route('/index')
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts', methods=['GET','POST'])
def adminviewhosts():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        allhosts,data = [],[]
        for doc in dbdata:
            data.append(doc.to_dict()['IPAddress'])
        allhosts=list(set(data))
        if(request.method=="POST"):
            ipaddress = request.form['choice']
            session['ipaddress']=ipaddress
            print("IP Address : ", ipaddress)
            return render_template("adminviewhosts1.html",allhosts=allhosts)
        print("Host : ", allhosts)
        return render_template("adminviewhosts.html",allhosts=allhosts)
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts_cpuusage', methods=['GET','POST'])
def adminviewhosts_cpuusage():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        graph_data=[]
        ipaddress=session['ipaddress']
        allhosts,cpuusage,ip_address,system_time = [],[],[],[]
        for doc in dbdata:
            ip_address.append(doc.to_dict()['IPAddress'])
            if(doc.to_dict()['IPAddress']==ipaddress):
                cpuusage.append(doc.to_dict()['CPU_Usage'])
                system_time.append(doc.to_dict()['Time'])
        allhosts=list(set(ip_address))
        for x in range(0, len(cpuusage)):
            temp={}
            temp["y"]=float(cpuusage[x])
            temp["label"]=system_time[x]
            graph_data.append(temp)
        print("Graph Data : ", graph_data)
        return render_template("adminviewhosts_cpuusage.html",allhosts=allhosts, 
                                   graph_data=graph_data)
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts_available_memory', methods=['GET','POST'])
def adminviewhosts_available_memory():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        graph_data=[]
        ipaddress=session['ipaddress']
        allhosts,available_memory,ip_address,system_time = [],[],[],[]
        for doc in dbdata:
            ip_address.append(doc.to_dict()['IPAddress'])
            if(doc.to_dict()['IPAddress']==ipaddress):
                available_memory.append(doc.to_dict()['AvailableMemory'])
                system_time.append(doc.to_dict()['Time'])
        allhosts=list(set(ip_address))
        for x in range(0, len(available_memory)):
            temp={}
            temp["y"]=float(available_memory[x])
            temp["label"]=system_time[x]
            graph_data.append(temp)
        print("Graph Data : ", graph_data)
        return render_template("adminviewhosts_available_memory.html",allhosts=allhosts, 
                                   graph_data=graph_data)
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts_memoryusage', methods=['GET','POST'])
def adminviewhosts_memoryusage():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        graph_data=[]
        ipaddress=session['ipaddress']
        allhosts,memoryusage,ip_address,system_time = [],[],[],[]
        for doc in dbdata:
            ip_address.append(doc.to_dict()['IPAddress'])
            if(doc.to_dict()['IPAddress']==ipaddress):
                memoryusage.append(doc.to_dict()['MemoryUsagePercentage'])
                system_time.append(doc.to_dict()['Time'])
        allhosts=list(set(ip_address))
        for x in range(0, len(memoryusage)):
            temp={}
            temp["y"]=float(memoryusage[x])
            temp["label"]=system_time[x]
            graph_data.append(temp)
        print("Graph Data : ", graph_data)
        return render_template("adminviewhosts_memoryusage.html",allhosts=allhosts, 
                                   graph_data=graph_data)
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts_bytessent_received', methods=['GET','POST'])
def adminviewhosts_bytessent_received():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        graph_data1, graph_data2=[],[]
        ipaddress=session['ipaddress']
        allhosts,bytesreceived,bytessent,ip_address,system_time = [],[],[],[],[]
        for doc in dbdata:
            ip_address.append(doc.to_dict()['IPAddress'])
            if(doc.to_dict()['IPAddress']==ipaddress):
                bytesreceived.append(doc.to_dict()['BytesReceived'])
                bytessent.append(doc.to_dict()['BytesSent'])
                system_time.append(doc.to_dict()['id'])
        allhosts=list(set(ip_address))
        for x in range(0, len(bytessent)):
            temp={}
            temp["y"]=float(bytessent[x])
            temp["x"]=int(system_time[x])
            graph_data1.append(temp)
            temp={}
            temp["y"]=float(bytesreceived[x])
            temp["x"]=int(system_time[x])
            graph_data2.append(temp)
            
        print("Graph Data1 : ", graph_data1)
        print("\nGraph Data2 : ", graph_data2)
        return render_template("adminviewhosts_bytessent_received.html",allhosts=allhosts, 
                                   datapoints1=graph_data1, datapoints2=graph_data2)
    except Exception as e:
        return str(e)

@app.route('/adminviewhosts1', methods=['GET','POST'])
def adminviewhosts1():
    try:
        db = firestore.client()
        dbref = db.collection('cpudetails')
        dbdata = dbref.get()
        graph_data, graph_title=[],""
        allhosts, ip_address = [],[]
        for doc in dbdata:
            ip_address.append(doc.to_dict()['IPAddress'])
        allhosts=list(set(ip_address))
        if(request.method=="POST"):
            choice = request.form['choice1']
            ipaddress=session['ipaddress']
            print("IP Address : ", ipaddress)
            print("Choice : ", choice)
            if(choice=='cpuusage'):
                return redirect(url_for("adminviewhosts_cpuusage"))
            elif(choice=='availablememory'):
                return redirect(url_for("adminviewhosts_available_memory"))
            elif(choice=='memoryusage'):
                return redirect(url_for("adminviewhosts_memoryusage"))
            elif(choice=='bytessent_received'):
                return redirect(url_for("adminviewhosts_bytessent_received"))
            return render_template("adminviewhosts1.html",allhosts=allhosts, 
                                   graph_data=graph_data, graph_title=graph_title)
        print("Host : ", allhosts)
        return render_template("adminviewhosts1.html", allhosts=allhosts)
    except Exception as e:
        return str(e)

@app.route('/usermainpage')
def usermainpage():
    try:
        return render_template("usermainpage.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logoutpage():
    try:
        session['id']=None
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/about')
def aboutpage():
    try:
        return render_template("about.html")
    except Exception as e:
        return str(e)

@app.route('/services')
def servicespage():
    try:
        return render_template("services.html")
    except Exception as e:
        return str(e)

@app.route('/gallery')
def gallerypage():
    try:
        return render_template("gallery.html")
    except Exception as e:
        return str(e)

@app.route('/adminlogin', methods=['GET','POST'])
def adminloginpage():
    msg=""
    if request.method == 'POST':
        uname = request.form['uname'].lower()
        pwd = request.form['pwd'].lower()
        print("Uname : ", uname, " Pwd : ", pwd)
        if uname == "admin" and pwd == "admin":
            return render_template("adminmainpage.html")
        else:
            msg = "UserName/Password is Invalid"
    return render_template("adminlogin.html", msg=msg)

@app.route('/userlogin', methods=['GET','POST'])
def userlogin():
    msg=""
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']

        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        flag = False
        for temp in data:
            print("Pwd : ", temp['Password'])
            #decMessage = fernet.decrypt(temp['Password']).decode()
            decode = base64.b64decode(temp['Password']).decode("utf-8")
            if uname == temp['UserName'] and pwd == decode:
                session['userid'] = temp['id']
                flag = True
                break
        if (flag):
            return render_template("usermainpage.html")
        else:
            msg = "UserName/Password is Invalid"
    return render_template("userlogin.html", msg=msg)

@app.route('/userviewprofile', methods=['GET','POST'])
def userviewprofile():
    try:
        id=session['userid']
        db = firestore.client()
        dbref = db.collection('newuser')
        data = dbref.document(id).get().to_dict()
        print("User Data ", data)
        return render_template("userviewprofile.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewfullreport', methods=['GET','POST'])
def adminviewfullreport():
    try:
        id=request.args['id']
        db = firestore.client()
        dbref = db.collection('systemdetails')
        data = dbref.document(id).get().to_dict()
        print("Cart Data ", data)
        return render_template("adminviewfullreport.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/userviewfullreport', methods=['GET','POST'])
def userviewfullreport():
    try:
        id=request.args['id']
        db = firestore.client()
        dbref = db.collection('systemdetails')
        data = dbref.document(id).get().to_dict()
        print("Cart Data ", data)
        return render_template("userviewfullreport.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/newuser', methods=['POST','GET'])
def newuser():
    try:
        msg=""
        print("Add New user page")
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phnum']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            #encMessage = fernet.encrypt(pwd.encode())
            encode = base64.b64encode(pwd.encode("utf-8"))
            print("str-byte : ", encode)
            json = {'id': id,
                        'FirstName': fname, 'LastName': lname,
                        'UserName': uname, 'Password': encode,
                        'EmailId': email, 'PhoneNumber': phnum,
                        'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newuser')
            newuser_ref.document(id).set(json)
            print("User User Success")
            msg = "New User Inserted Success"
        return render_template("newuser.html", msg=msg)
    except Exception as e:
        return str(e)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/contact', methods=['POST','GET'])
def contactpage():
    try:
        msg=""
        if request.method == 'POST':
            cname = str(request.form['cname'])# + " " + str(request.form['lname'])
            subject = request.form['subject']
            message = request.form['message']
            email = request.form['email']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'ContactName': cname, 'Subject': subject,
                    'Message': message,
                    'EmailId': email}
            db = firestore.client()
            newdb_ref = db.collection('newcontact')
            id = json['id']
            newdb_ref.document(id).set(json)
            body = "Thank you for contacting us, " + str(cname) + " We will keep in touch with in 24 Hrs"
            receipients = [email]
            send_email(subject,body,recipients=receipients)
            msg = "New Contact Added Success"
        return render_template("contact.html", msg=msg)
    except Exception as e:
        return str(e)

@app.route('/userviewreports', methods=['POST','GET'])
def userviewreports():
    try:
        db = firestore.client()
        id = session['userid']
        newdata_ref = db.collection('systemdetails')
        newdata = newdata_ref.get()
        data=[]
        for doc in newdata:
            temp=doc.to_dict()
            if(str(temp['UserId'])==str(id)):
                data.append(doc.to_dict())
        print("Reports Data " , data)
        return render_template("userviewreports.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewusers', methods=['POST','GET'])
def adminviewusers():
    try:
        db = firestore.client()
        newdata_ref = db.collection('newuser')
        newdata = newdata_ref.get()
        data=[]
        for doc in newdata:
            data.append(doc.to_dict())
        print("Users Data " , data)
        return render_template("adminviewusers.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewcontacts', methods=['POST','GET'])
def adminviewcontacts():
    try:
        db = firestore.client()
        newdata_ref = db.collection('newcontact')
        newdata = newdata_ref.get()
        data=[]
        for doc in newdata:
            data.append(doc.to_dict())
        print("Contact Data " , data)
        return render_template("adminviewcontacts.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewreports', methods=['POST','GET'])
def adminviewreports():
    try:
        db = firestore.client()
        newdata_ref = db.collection('systemdetails')
        newdata = newdata_ref.get()
        data=[]
        for doc in newdata:
            data.append(doc.to_dict())
        #print("Report Data " , data)
        return render_template("adminviewreports.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminmainpage')
def adminmainpage():
    try:
        return render_template("adminmainpage.html")
    except Exception as e:
        return str(e)

if __name__ == "__main__":        
    app.run(host='0.0.0.0', debug=True)