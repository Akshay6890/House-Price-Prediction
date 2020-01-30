import numpy as np
import joblib
from tkinter import *
from tkinter.ttk import Combobox
import tkinter
import pymysql
import time


def app():
    result=0
    #databasecode
    con=pymysql.connect(host="localhost",user="root",passwd="",database="houseprice")
    b_cursor=con.cursor()

    #login_window_code
    e=Tk()
    #e.configure(background='lightgreen')
    e.title('Login')
    e.geometry("340x340")
    e.resizable(False,False)
    head=Label(e,text='Login to 99Acres',font='Bahnschrift')
    head.place(x=120,y=20)
    #head.config(background='white')
    l1=Label(e,text='Email')
    l1.place(x=60,y=80)
    email=Entry(e,text='')
    email.place(x=140,y=80)
    l2=Label(e,text='Password')
    l2.place(x=60,y=140)
    password=Entry(e,text='')
    password.place(x=140,y=140)
    status=Label(e,text='')
    status.place(x=120,y=170)
    def signup():
        e.destroy()
        s=Tk()
        s.geometry("600x400")
        s.title("SIGN UP")
        s.resizable(False,False)
        fn=Label(s,text='First Name')
        fn.place(x=180,y=60)
        fni=Entry(s)
        fni.place(x=300,y=60)
        ln=Label(s,text='Last Name')
        ln.place(x=180,y=90)
        lni=Entry(s)
        lni.place(x=300,y=90)
        em=Label(s,text='Email')
        em.place(x=180,y=120)
        emi=Entry(s)
        emi.place(x=300,y=120)
        mng=IntVar()
        mn=Label(s,text='Mobile Number')
        mn.place(x=180,y=150)
        mni=Entry(s,textvariable=mng)
        mni.place(x=300,y=150)
        pwd=Label(s,text='Password')
        pwd.place(x=180,y=180)
        pwdi=Entry(s)
        pwdi.place(x=300,y=180)
        stat_s=Label(s,text='')
        stat_s.place(x=250,y=210)
        def validate():
            if fni.get()=='' or lni.get()=='' or emi.get()=='' or mon.get=='' or pwdi.get()=='':
                stat_s['text']='Please fill in all fields'
                return 0
            else:
                fin=str(fni.get())
                lin=str(lni.get())
                e=str(emi.get())
                mon=int(mng.get())
                p=str(pwdi.get())
                b_cursor.execute('INSERT INTO user_details(FirstName,LastName,Email,MobileNumber,Password) VALUES(%s,%s,%s,%s,%s)',[fin,lin,e,mon,p])
                status['text']='Sign Up Successful, Login to continue !'
                con.commit()
                con.close()
                s.destroy()
                app()
        sgn=Button(s,text='Sign Up',command=validate)
        sgn.place(x=260,y=240)
        status=Label(s,text='')
        status.place(x=250,y=300)
    def main():
        login="SELECT Email, Password FROM user_details WHERE Email= %s"
        validation=b_cursor.execute(login, (email.get()))
        if validation==0:
            status['text']='Account not found, Please Sign Up'
            return 0
        else:
            b_cursor.execute(login, (email.get()))
            for c in b_cursor:
                email_valid=c[0]
                pwd_valid=c[1]
            if email.get()=='' or password.get()=='':
                status['text']='Please fill all fields'
                return 0
            elif email.get()!=email_valid and password.get()!=pwd_valid:
                status['text']='Email and password are Incorrect'
                return 0
            elif email.get()!=email_valid:
                status['text']='Incorrect Email'
                return 0
            elif password.get()!=pwd_valid:
                status['text']='Incorrect Password'
                return 0
            else:
                #check_price_code
                e.destroy()
                m=Tk()
                m.title('Check House Price')
                m.geometry("600x400")
                m.resizable(False,False)
                l1=Label(m,text='CHECK PRICE',font='Bahnschrift')
                l1.place(x=340,y=30)
                l2=Label(m,text='Location')
                l2.place(x=280,y=80)
                l3=Label(m,text='BHK')
                l3.place(x=280,y=110)
                l4=Label(m,text='Sq.ft.')
                l4.place(x=280,y=140)
                l5=Label(m,text='Years Old')
                l5.place(x=280,y=170)
                l6=Label(m,text='No. of floors')
                l6.place(x=280,y=200)
                loc=StringVar()
                locations=("Bomanahalli","Whitefield")
                cb=Combobox(m,values=locations,textvariable=loc,state='readonly',width=20)
                cb.place(x=400,y=80)
                cb.current(0)
                sbhk=IntVar()
                bhk=(1,2,3)
                cb1=Combobox(m,values=bhk,textvariable=sbhk,state='readonly',width=20)
                cb1.place(x=400,y=110)
                cb1.current(0)
                sqft=Entry(m,width=23)
                sqft.place(x=400,y=140)
                syear=IntVar()
                years=(1,2,3,4,5,6,7,8,9,10)
                cb2=Combobox(m,values=years,textvariable=syear,state='readonly',width=20)
                cb2.place(x=400,y=170)
                cb2.current(0)
                s_old=IntVar()
                cb3=Combobox(m,values=years,textvariable=s_old,state='readonly',width=20)
                cb3.place(x=400,y=200)
                cb3.current(0)
                l7=Label(m,text='Price of House is')
                l7.place(x=280,y=250)
                l8=Label(m,text='')
                l8.place(x=400,y=250)
                def cal():
                    if loc.get()=='Bomanahalli':
                        locv=0
                    else:
                        locv=1
                    data = [locv,int(sbhk.get()),1,int(sqft.get()),int(syear.get()),int(s_old.get())]
                    data= np.array(data)
                    sav = joblib.load('house_price.sav')
                    pred = sav.predict(data.reshape(1,-1))
                    result = format(int(round(pred[0],0)),',')
                    l8['text']=result
                    return 0
                def add_prop():
                    b_cursor.execute('INSERT INTO properties(location,BHK,sqft,years_old,floors,price) VALUES(%s,%s,%s,%s,%s,%s)',[loc.get(),sbhk.get(),sqft.get(),syear.get(),s_old.get(),l8['text']])
                    con.commit()              
                last=Button(m,text='Check Price',command=cal)
                last.place(x=340,y=300)
                add_p=Button(m,text='Add Property',command=add_prop)
                add_p.place(x=430,y=300)
                m.mainloop()
    r=Button(e,text='Login',command=main)
    r.place(x=150,y=210)
    sign_up=Button(e,text='Sign Up',command=signup)
    sign_up.place(x=210,y=210)
    e.mainloop()
app()
