from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font as tkfont
import smtplib
from smtplib import *
import re
import time
import os
import subprocess
import requests

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):


    def __init__(self, parent, controller):

        current_HWID = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        hwidRequest = requests.get("https://pastebin.pl/view/c23b21db")
        hwidResult = False

        try:
            if current_HWID in hwidRequest.text:
                print("Your HWID is authorized")
                hwidResult = True
            else:
                print("Your HWID not in Database")
                hwidResult = False
                # time.sleep(5)
                # os._exit()

        except:
            print("Failed to connect databse")
            hwidResult = False
            # time.sleep(5)
            # os._exit    

        tk.Frame.__init__(self, parent)
        self.controller = controller

        labelemail = Label(self, text="Username").grid(column=0, row=2, sticky=E)
        e_email = Entry(self, bd =1)
        e_email.grid(column=1, row=2)
        labelpswd = Label(self, text="Password").grid(column=0, row=3, sticky=E)
        e_pswd = Entry(self, bd =1, show='*')
        e_pswd.grid(column=1, row=3)
        
        if hwidResult == False:
            button1 = tk.Button(self, text="UNAUTHORIZED",
                        command=lambda: controller.show_frame("PageOne"), state=DISABLED).grid(column=0, row=4, sticky=E)
            button2 = tk.Button(self, text="UNAUTHORIZED",
                        command=lambda: controller.show_frame("PageOne"), state=DISABLED).grid(column=0, row=5, sticky=E)            
        else:
            button1 = tk.Button(self, text="Login to Single Send",
                        command=lambda: controller.show_frame("PageOne")).grid(column=0, row=4, sticky=E)
            button2 = tk.Button(self, text="Login to Multiple Send",
                        command=lambda: controller.show_frame("PageTwo")).grid(column=0, row=5, sticky=E)
        
        labelHWID = Label(self, text=f"Your HWID = {current_HWID}").grid(column=2, row=6, sticky=E)
        print(current_HWID)


        # if 'nt' in os.name:
        #     return subprocess.Popen('dmidecode.exe -s system-uuid'.split())
        # else:
        #     return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())              


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        host = 'mail.echoscs.com'
        port = '587'

        def sending():
            email = "testing@echoscs.com"
            pswd = "4324201Ll."
            rcpt = e_rcpt.get()
            msg = e_msg.get()
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(email, pswd)
            server.sendmail(email,rcpt,msg)
            server.quit()
            e_msg.delete(0, 'end')

        labelname = Label(self, text="Single SMS Send").grid(column=0, row=1, sticky=E)
        labelrcpt = Label(self, text="Recipient").grid(column=0, row=2, sticky=E)
        e_rcpt = Entry(self, bd =1)
        e_rcpt.grid(column=1, row=2)
        labelmsg = Label(self, text="Message").grid(column=0, row=3, sticky=E)
        e_msg = Entry(self, bd =1)
        e_msg.grid(column=1, row=3)
        send = Button(self, text ="Send", command = sending, bd =1).grid(column=2, row=3)

        button = tk.Button(self, text="Go to Login Page",
                           command=lambda: controller.show_frame("StartPage")).grid(column=0,row=4,sticky=E)

        lambda: controller.show_frame("StartPage")    


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        f = open('emails.txt', 'r')
        emails = f.readlines()
        emailsSayac = 0

        p = open('smtp.txt', 'r')

        # host = 'mail.echoscs.com' 
        # port = '587'

        def sendEmailList():
            number = 0
            size = len(emails)
            print(f"Total numbers to sent : {size}")
            
            while True:
                for smtpList in p:
                    smtps = smtpList.split(":")
                    smtpHost = smtps[0]
                    smtpPort = smtps[1]
                    smtpMail = smtps[2]
                    smtpPswd = smtps[3]
                    print(smtpHost,smtpPort,smtpMail,smtpPswd)
                    rcpt = emails[emailsSayac]
                    msg = e_msg.get()
                    number = number + 1
                    try:
                        server = smtplib.SMTP(smtpHost, smtpPort)
                        server.starttls()
                        server.login(smtpMail, smtpPswd)
                        server.sendmail(smtpMail,rcpt,msg)
                        server.quit()
                        emailsSayac+1
                        print(f"SMS Succesfully sent to : {rcpt} and transaction ID is {number}")
                        print(msg)
                        time.sleep(1)
                    except SMTPResponseException:
                        error_code = SMTPResponseException.smtp_code
                        error_messagE = SMTPResponseException.smtp_error
                        print ("Error code : ")+error_code
                        print ("Error Message")+error_messagE
                if(number == size):
                    return False
            print("while bitti amk")


        
        labelrcpt = Label(self, text="Multiple SMS Send").grid(column=0, row=2, sticky=E)
        labelmsg = Label(self, text="Message").grid(column=0, row=3, sticky=E)
        e_msg = Entry(self, bd =1)
        e_msg.grid(column=1, row=3)
        send = Button(self, text ="Send", command = sendEmailList, bd =1).grid(column=2, row=3)

        button = tk.Button(self, text="Go to Login Page",
                           command=lambda: controller.show_frame("StartPage")).grid(column=0,row=4,sticky=E)

        lambda: controller.show_frame("StartPage")                   


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()