from sendsms import Send_Sms
import socket
from MailSent import send_email
import psutil
import time
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

def get_system_resources():
    while(True):
        temp={}
        print("--- System Resource Usage ---")
        ip_address=get_local_ip_address();
        print(f"Your local IP address is: {ip_address}")
        
        seconds_since_epoch = time.time()
        # Convert to milliseconds by multiplying by 1000 and casting to an integer
        id = str(int(seconds_since_epoch * 1000))
        
        print("Ip Address : ", ip_address)
        
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime("%H:%M")
        print(f"Formatted current time: {formatted_time}")
        
        temp['Time']=f"{formatted_time}"
        temp['id']=f"{id}"

        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)  # CPU utilization over 1 second
        print(f"CPU Usage: {cpu_percent}%")
        temp['CPU_Usage']=f"{cpu_percent}"
    
        # Memory Usage
        virtual_memory = psutil.virtual_memory()
        print(f"Total Memory: {round(virtual_memory.total / (1024**3), 2)} GB")
        print(f"Used Memory: {round(virtual_memory.used / (1024**3), 2)} GB")
        print(f"Available Memory: {round(virtual_memory.available / (1024**3), 2)} GB")
        print(f"Memory Usage Percentage: {virtual_memory.percent}%")
    
        temp['TotalMemory']=f"{round(virtual_memory.total / (1024**3), 2)}"
        temp['UsedMemory']=f"{round(virtual_memory.used / (1024**3), 2)}"
        temp['AvailableMemory']=f"{round(virtual_memory.available / (1024**3), 2)}"
        temp['MemoryUsagePercentage']=f"{virtual_memory.percent}"

        # Disk Usage (for the root directory or a specific path)
        disk_usage = psutil.disk_usage('C:/')
        temp["DiskUsagePercentage"]=f"{disk_usage.percent}"
    
        # Network I/O (bytes sent and received)
        net_io = psutil.net_io_counters()
        print(f"Bytes Sent: {round(net_io.bytes_sent / (1024**2), 2)} MB")
        print(f"Bytes Received: {round(net_io.bytes_recv / (1024**2), 2)} MB")
    
        temp["BytesSent"]=f"{round(net_io.bytes_sent / (1024**2), 2)}"
        temp["BytesReceived"]=f"{round(net_io.bytes_recv / (1024**2), 2)}"

        temp['IPAddress']=ip_address
        db = firestore.client()
        newdb_ref = db.collection('cpudetails')
        newdb_ref.document(id).set(temp)
        print("Data Saved Success")
        if(float(virtual_memory.percent)>60):
            message=f"System with IP Address {ip_address} is utilizing {virtual_memory.percent} of usage kindly have a look"
            subject="CPU is utilizing the memory > 60%"
            #Send_Sms("9591612491", message=message)
            #Send_Sms("9113236923", message=message)
            print("Message Sent")
            send_email(subject=subject, body=message, recipients=['devarajpolicepatilmsd@gmail.com','diliptk24@gmail.com'])
            print("Mail Sent")
        print("-----------------")
        time.sleep(10)
        
def get_local_ip_address():
    """ Retrieves the local IP address of the machine. """
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to an external address (doesn't send data) to determine the local IP used for outbound connections
        s.connect(("8.8.8.8", 80)) # Google's public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error getting local IP address: {e}"

if __name__ == "__main__":
    get_system_resources()