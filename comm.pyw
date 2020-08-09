#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################################
#
# EXEMPLO DE CONTROLE DE INSTRUMENTOS 
# UTILIZANDO PYTHON ATRAVES DO PROTOCOLO HTTP
#
# 06/10/2014
# ESCRITO POR: RICARDO LOPES
#
# ESTE CODIGO E FORNECIDO COMO ESTA, SEM NENHUMA
# GARANTIA IMPLICITA OU EXPLICITA.
# O USUARIO PODE MODIFICAR E UTILIZAR ESTE CODIGO
# COMO QUISER.
#
###################################################

###############
import httplib
import base64
import string
import time
import os
from threading import Thread
import Tkinter
import tkMessageBox


class mcsxv_app(Tkinter.Tk):

    host = "192.168.31.222:5000"
    url = "/mcsxvserver/getinput.cgi"
    changesp = "/mcsxvserver/setoutputvalue.cgi?newOutputValue="
    changeinput = "/mcsxvserver/setinputtype.cgi?newInput="
    changeoutput = "/mcsxvserver/setoutputtype.cgi?newOutput="
    getCtor = "/mcsxvserver/getctor.cgi?type="
    username = 'admin'
    password = 'xvmaster'

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def readActualInput(self):
        try:
            auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            webservice = httplib.HTTP(self.host)
            webservice.putrequest("GET", self.url)
            webservice.putheader("Host", self.host)
            webservice.putheader("User-Agent", "Python http auth")
            webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
            webservice.putheader("Authorization", "Basic %s" % auth)
            webservice.endheaders()
            statuscode, statusmessage, header = webservice.getreply()
            res = webservice.getfile().read()
           
            st = res.split('|')
            return ('Input value: '+ st[0]+st[1])
        except Exception as e:
             if "401" in res: #erro 401 - Autorizacao necessaria
                 return "Auth required"
             else:            #retorna a mensagem recebida
                return str(e)

    def changeSetPoint(self, setpoint):
        auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        webservice = httplib.HTTP(self.host)
        webservice.putrequest("GET", self.changesp + setpoint)
        webservice.putheader("Host", self.host)
        webservice.putheader("User-Agent", "Python http auth")
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Authorization", "Basic %s" % auth)
        webservice.endheaders()
        statuscode, statusmessage, header = webservice.getreply()
        return webservice.getfile().read()

    def changeInputType(self, newType):
        auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        webservice = httplib.HTTP(self.host)
        webservice.putrequest("GET", self.changeinput + newType)
        webservice.putheader("Host", self.host)
        webservice.putheader("User-Agent", "Python http auth")
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Authorization", "Basic %s" % auth)
        webservice.endheaders()
        statuscode, statusmessage, header = webservice.getreply()
        return webservice.getfile().read()
    

    def changeOutputType(self, newType):
        auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        webservice = httplib.HTTP(self.host)
        webservice.putrequest("GET", self.changeoutput + newType)
        webservice.putheader("Host", self.host)
        webservice.putheader("User-Agent", "Python http auth")
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Authorization", "Basic %s" % auth)
        webservice.endheaders()
        statuscode, statusmessage, header = webservice.getreply()
        return webservice.getfile().read()

    def initialize(self):
        self.grid()
        
        self.ipLblTxt = Tkinter.StringVar()
        self.spLblTxt = Tkinter.StringVar()

        #labels
        ipLbl = Tkinter.Label(self,textvariable=self.ipLblTxt,anchor="w")
        self.ipLblTxt.set(u"IP Address:")
        ipLbl.grid(column=0,row=0,columnspan=1)

        spLbl = Tkinter.Label(self,textvariable=self.spLblTxt,anchor="w")
        self.spLblTxt.set(u"Output Value:")
        spLbl.grid(column=0,row=1,columnspan=1)

        #input text
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable,width=16)
        self.entry.grid(column=1,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"0.0000")

        self.entryIP = Tkinter.StringVar()
        self.ip = Tkinter.Entry(self,textvariable=self.entryIP,width=16)
        self.ip.grid(column=1,row=0,sticky='EW')
        self.entryIP.set(self.host)

        #buttons
        readInputBtn = Tkinter.Button(self,text=u"Read input",command=self.OnButtonClick,width=15)
        alterSpBtn = Tkinter.Button(self,text=u"Apply Setpoint",command=self.OnAlterSetPointClick,width=15)
        setIpBtn = Tkinter.Button(self,text=u"Change IP",command=self.OnAlterIPClick,width=15)

        setIpBtn.grid(column=2,row=0)
        readInputBtn.grid(column=0,row=2)
        alterSpBtn.grid(column=1,row=2)

        self.optionsCbo = Tkinter.StringVar()
        self.optionsCbo.set("Volt") # default value
        w = Tkinter.OptionMenu(self,self.optionsCbo, "Volt", "mA", "mV")
        w.grid(column=0,row=3,columnspan=1,sticky='EW')

        self.outOptionsCbo = Tkinter.StringVar()
        self.outOptionsCbo.set("Volt") # default value
        outCbo = Tkinter.OptionMenu(self,self.outOptionsCbo, "Volt", "mA", "mV")
        outCbo.grid(column=0,row=4,columnspan=1,sticky='EW')

        setInputBtn = Tkinter.Button(self,text=u"Change input", command=self.OnChangeInputClick,width=15)
        setInputBtn.grid(column=1,row=3)

        setOutputBtn = Tkinter.Button(self,text=u"Change output",command=self.OnChangeOutputClick,width=15)
        setOutputBtn.grid(column=1,row=4)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=5,columnspan=3,sticky='EW')
        self.labelVariable.set(u"Welcome to MCS XV commander!")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        self.labelVariable.set(self.readActualInput())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def OnAlterSetPointClick(self):
        self.labelVariable.set(self.changeSetPoint(self.entryVariable.get()))
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnAlterIPClick(self):
        self.host = self.entryIP.get()
        self.labelVariable.set(self.entryIP.get())

    def OnChangeInputClick(self):
        typen = self.optionsCbo.get()
        if typen == "Volt":
            self.labelVariable.set(self.changeInputType("General:V"))
        if typen == "mA":
            self.labelVariable.set(self.changeInputType("General:mA"))
        if typen == "mV":
            self.labelVariable.set(self.changeInputType("General:mV"))
        tkMessageBox.showinfo("Input Changed", "New input: " + typen)

    def OnChangeOutputClick(self):
        typen = self.outOptionsCbo.get()
        if typen == "Volt":
            self.labelVariable.set(self.changeOutputType("General:V"))
        if typen == "mA":
            self.labelVariable.set(self.changeOutputType("General:mA"))
        if typen == "mV":
            self.labelVariable.set(self.changeOutputType("General:mV"))
        tkMessageBox.showinfo("Output Changed", "New output: " + typen)
         

    def OnPressEnter(self,event):
        self.labelVariable.set(self.changeSetPoint(self.entryVariable.get()))
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = mcsxv_app(None)
    app.title('MCS XV Python Commander')
    app.mainloop()



