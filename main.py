
############################################# IMPORTING package ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import csv

import cv2, os
import numpy as np
import pandas as pd
from PIL import Image
import datetime
import time


############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'bhumikachuphal125@gmail.com' ")


###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()


###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if (newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()


###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")

    lbl4 = tk.Label(master, text='Enter Old Password', padx=10, bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    old.place(x=180, y=10)

    lbl5 = tk.Label(master, text='Enter New Password', padx=10, bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    new.place(x=180, y=45)

    lbl6 = tk.Label(master, text='Confirm New Password', padx=10, bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)

    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="red", height=1, width=25,
                       activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)

    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height=1, width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()


#####################################################################################

def psw(message):
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Create Password ', 'Please enter a new password ', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages(message)
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear1(txt):
    txt.delete(0, 'end')

def clear2(txt2):
    txt2.delete(0, 'end')


#######################################################################################

def TakeImages(txt, txt2):
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())

    if (Id == "" or Id.isnumeric() == False or name == "" or name.isalpha() == False):
        mess._show(title='Incorrect data ', message='Please enter id and name of the student correctly.')
        window.destroy()
        quit()
    else:
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        #### adding path for students picture #############
        newpath = "TrainingImage/" + name
        os.mkdir(newpath)


        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 3)     # 1.3 size reduced, 3 min neighbours
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1


                # saving the captured face in the dataset folder TrainingImage
                imgname = name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg"
                personpath = os.path.join(newpath,imgname)
                cv2.imwrite(personpath,gray[y:y + h, x:x + w])


                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()


        row = [serial,  Id,  name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    clear1(txt)
    clear2(txt2)



########################################################################################

def TrainImages(message):
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))


############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder

    imagePaths=[]
    try:
        for person in os.listdir(path):
            personfolder=os.path.join(path,person)
            for person_img in os.listdir(personfolder):
                imagePaths.append(os.path.join(personfolder,person_img))

    except:
        mess._show(title='No record found !!', message='Please enter records of students first')
        window.destroy()
        quit()

    faces = []
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


###########################################################################################

def TrackImages(tv):
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    '''The   get_children() method of Treeview returns a list of every row's iid. We're iterating this list, 
        passing each iid to the Treeview.delete() method, which, as you'd expect, deletes the row.
    '''
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()


######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }


######################################## GUI FRONT-END ###########################################


###################### Attendence Window ################
def TakeAttendence():
    window1 = tk.Tk()
    window1.geometry("900x650")
    window1.minsize(900, 650)
    window1.maxsize(900, 650)
    window1.resizable(True, False)
    window1.title("Taking Attendence")
    window1.configure(background='#262523')

    lbl1 = tk.Label(window1, text="Attendance", width=34, fg="White", bg="#00aeff", height=1, font=('times', 17, ' bold '))
    lbl1.place(x=120, y=160)


    ################## TREEVIEW ATTENDANCE TABLE ####################

    tv = ttk.Treeview(window1, height=15, columns=('name', 'date', 'time'))
    tv.column('#0', width=82)
    tv.column('name', width=130)
    tv.column('date', width=133)
    tv.column('time', width=133)
    tv.grid(row=2, column=0, padx=(120, 0), pady=(190, 0), columnspan=4)
    tv.heading('#0', text='ID')
    tv.heading('name', text='NAME')
    tv.heading('date', text='DATE')
    tv.heading('time', text='TIME')
    ### scrollBar
    scroll = ttk.Scrollbar(window1, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(160, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    ############ Button to take attendence ###############
    trackImg = tk.Button(window1, text="Take Attendance", command=lambda: TrackImages(tv), fg="black", bg="white", width=50,
                         height=2, font=('times', 15, ' bold '))
    trackImg.place(x=60, y=50)
    window1.mainloop()


################## Registration Window ##############################################
def Registration():
    window2=tk.Tk()
    window2.geometry("900x720")
    window2.minsize(900, 720)
    window2.resizable(True, False)
    window2.title("New Registration")
    window2.configure(background='#262523')
    message4 = tk.Label(window2, text="Registration", fg="white", bg="#262523", width=20,
                        height=1, font=('times', 29, ' bold '))
    message4.place(x=200, y=30)

    ####################### textboxes #################3
    lbl = tk.Label(window2, text="Enter ID", width=18, height=1, fg="white", bg="#262523", font=('times', 17, ' bold '))
    lbl.place(x=78, y=138)

    txt = tk.Entry(window2, width=32, fg="black", font=('times', 15, ' bold '))
    txt.place(x=400, y=138)

    lbl2 = tk.Label(window2, text="Enter Name", width=18, fg="white", bg="#262523", font=('times', 17, ' bold '))
    lbl2.place(x=78, y=223)

    txt2 = tk.Entry(window2, width=32, fg="black", font=('times', 15, ' bold '))
    txt2.place(x=400, y=223)

    ########### total registrations #######################3333
    message = tk.Label(window2, text="", bg="#262523", fg="white", width=40, height=1, font=('times', 16, ' bold '))
    message.place(x=200, y=550)
    res = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
    else:
        res = 0
    message.configure(text='Total Registrations till now  : ' + str(res))

    ################## buttons #########################
    clearButton1 = tk.Button(window2, text="Clear", command=lambda: clear1(txt), fg="black", bg="#00aeff", width=11,
                            activebackground="white", font=('times', 11, ' bold '))
    clearButton1.place(x=704, y=138)

    clearButton2 = tk.Button(window2, text="Clear", command=lambda: clear2(txt2), fg="black", bg="#00aeff", width=11,
                             activebackground="white", font=('times', 11, ' bold '))
    clearButton2.place(x=704, y=223)

    takeImg = tk.Button(window2, text="Take Images", command=lambda: TakeImages(txt, txt2), fg="white", bg="#00aeff", width=20,
                        height=1, font=('times', 15, ' bold '))
    takeImg.place(x=100, y=400)

    trainImg = tk.Button(window2, text="Save Profile", command=lambda: psw(message), fg="white", bg="#00aeff", width=20, height=1,
                         font=('times', 15, ' bold '))
    trainImg.place(x=500, y=400)
    window2.mainloop()


#################### Main Screen #########################
window = tk.Tk()
window.geometry("1280x720")
window.resizable(False, False)
window.title("Attendance System")
window.configure(background='#262523')

messageTop = tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#262523", width=55,
                    height=1, font=('times', 29, ' bold '))
messageTop.place(x=40, y=30)


######## for showing current time  ##########################3
frame1 = tk.Frame(window, bg="#c4c6ce")
frame1.place(x=400, y=100, width=260, height=30)

frame2 = tk.Frame(window, bg="#c4c6ce")
frame2.place(x=640, y=100, width=200, height=30)

datef = tk.Label(frame1, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,
                 height=1, font=('times', 20, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame2, fg="orange", bg="#262523", width=55, height=1, font=('times', 22, ' bold '))
clock.pack(fill='both', expand=1 )
tick()

###################### Buttons #################################3
TakeAttendence = tk.Button(window, text="Take Attendance", command=TakeAttendence, fg="black", bg="white", width=35,
                     height=5, font=('times', 17, ' bold '))
TakeAttendence.place(x=100, y=250)
Registration = tk.Button(window, text="Registration", command=Registration, fg="black", bg="white", width=35, height=5,
                     font=('times', 17, ' bold '))
Registration.place(x=730, y=250)

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)
window.configure(menu=menubar)

##################### END ######################################

window.mainloop()