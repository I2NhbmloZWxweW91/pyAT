#
# pyAT.py -- AT Commands Handler v0.1 by @_hddananjaya
#                                                                             ^_^ 
                                                           
# import requried modules
import serial
import sys
import os
#import time
#import io

class base_view():
   # Banner and other stuff
   banner="""
   ##### #  #      #     ########                                                                 
   #   # #  #     #1#       #                                                              
   ##### ####    #001#      #                                                                
   #        #   #10010#     #                                                               
   #        #  #1010101#    #                                                                
   #     #### ###########   #   v0.1
          
       AT Commands Handler
  ----------------------------------
  Author : @_hddananjaya
  Web    : hddananjaya.wordpress.com
  ----------------------------------

   """

   note="""
 Some automated AT commands are not supported by all products. Giving a
 command which is not supported by the product causes an error response.
 So make sure to use 'Give me a Terminal' option when requried.
   """

   menu="""
   (0) Connection Availability  ~ *     ~
   (1) Import Contacts          ~ ***** ~
   (2) Current Status           ~ ***   ~
   (3) Dial a Number            ~ ****  ~
   (4) Give me a Terminal       ~ ***** ~
   """

# Config and connection for communicate
class config:
   
   # Maintain a log file
   log=open("pyAT.txt","a")

   # get port number to communicate with && connects
   valid_info=False
   while (valid_info==False):
      port = input("[+] Port :")
      try:
         ser = serial.Serial(port,115200,timeout=5)
         print("Connected "+port)
         print("Detecting. . . .")
         
         cgmi="AT+CGMI\r"
         ser.write(cgmi.encode())
         res_cgmi=ser.read(64).decode('utf-8').replace("AT+CGMI","").replace("OK","").strip()
         
         cgmm="AT+CGMM\r"
         ser.write(cgmm.encode())
         res_cgmm=ser.read(64).decode('utf-8').replace("AT+CGMM","").replace("OK","").strip()

         cgsn="AT+CGSN\r"
         ser.write(cgsn.encode())
         res_cgsn=ser.read(64).decode('utf-8').replace("AT+CGSN","").replace("OK","").strip()         
         print("-------------------------------------------------------------------")
         print("Device Manufacturer Identification  :",res_cgmi)
         print("Device Model Identification         :",res_cgmm)
         print("Device Serial Number Identification :",res_cgsn)                  
         print("-------------------------------------------------------------------")
         valid_info=True
      except serial.serialutil.SerialException:
         print("Could not open the port: "+port)
         


# Define main process
def main():
   
   port=config.port
   ser=config.ser
   log=config.log
   
   print(base_view.banner)
   print (base_view.menu)
   
   choice = int(input("[+] What Do You Want to Do :"))


   # Multiple choices
   if(choice== 0):
       cmd="AT\r"
       config.ser.write(cmd.encode())
       res = ser.read(64)
       print("-------------------------------------------------------------------")
       print("Response of: "+port)
       print (res.decode())
       if("OK" in res.decode()):
          print("Connection of "+port+" is up!")
       else:
          print("Connection error in "+port)
       print("-------------------------------------------------------------------")


   if(choice== 1):
       os.system("cls")
       av_opt="AT+CPBS=?\r"
       ser.write(av_opt.encode())
       res = ser.read(100).decode('utf-8')       
       res=res.replace("AT+CPBS=?","").replace("+CPBS:","").replace("OK","").strip()   
       print("-------------------------------------------------------------------")
       print("Response of: "+port)
       print("Available Options in your device : "+res)
       av_opt_menu="""
       EXPLANATION
       -----------
       FD :- SIM fixdialling-phonebook
       LD :- SIM last-dialling-phonebook
       ME :- ME Phonebook
       MT :- combined ME and SIM phonebook
       TA :- TA phonebook
       RC :- Remote controlled phonebook   and more...
       
   Select one or one options which are available in
   your device. Use comma ',' to separate.

   If errors are corrupting, please use these options
   one by one.

   Contacs will copy to pyAT_log.txt
       """
       print(av_opt_menu)
       print("-------------------------------------------------------------------")       
       lau_opt=input("[+] Select one or more :")
       lau_opt_li=lau_opt.split(",")
        
       # Put it in the log.txt
       log.write("Imported Contacts form "+port+" [Selected Options by User :-"+lau_opt+" ]\ncls\n") 

       # Take one by one from lauch option list
       for i in lau_opt_li:
          # Change the option
          av_opt='AT+CPBS="'+i+'"\r'
          ser.write(av_opt.encode())
          res = ser.readlines()
          #print(res)
          #time.sleep(3)
          
          # Get avaiable ranges
          chk_range="AT+CPBR=?\r"
          ser.write(chk_range.encode())
          res = ser.read(100).decode('utf-8')
          res=res.replace("AT+CPBR=?","").replace("+CPBR:","").replace("OK","").strip()          
          print("-------------------------------------------------------------------")
          print("Response of: "+port)
          note="""
   Select contact range. Simplest option is just input the maxmimum value
   """
          print(note)
          print("Available ranges in phonebook : "+res+"  [MODE:- "+i+"]")
          phnbk_range=input("[+] Range you need :")
          #time.sleep(3)
          # Import contacts in range
          cmd="AT+CPBR=1,"+phnbk_range+"\r"
          ser.write(cmd.encode())
          res = ser.readlines()
          #print (res)
          for contact in res:
             contact=contact.decode('utf-8').replace("+CPBR:","").strip()
             print(contact)
             log.write(contact+"\n")

   elif(choice==2):
      av_opt="AT+CPAS\r"
      ser.write(av_opt.encode())
      res = ser.read(100).decode('utf-8')
      print("-------------------------------------------------------------------")
      if ("ERROR" in res):
         print("Unable to check.")
      else:
         if ("0" in res):
            print("Device Status : Ready")
         elif ("1" in res):
            print("Device Status : Unavailable")         
         elif ("2" in res):
            print("Device Status : Unknown")
         elif ("3" in res):
            print("Device Status : Ringing")              
         elif ("4" in res):
            print("Device Status : Call in process")
         elif ("5" in res):
            print("Device Status : Asleep!")  
      print("-------------------------------------------------------------------")
   elif(choice==3):
      num=input("[+] Phone Number: ")
      av_opt="ATD"+num+";\r"
      ser.write(av_opt.encode())
      res = ser.read(100).decode('utf-8')       
      res=res.replace("AT+CPBS=?","").replace("+CPBS:","").strip()   
      
   elif(choice==4):
      try:
         print("Press any key to access terminal")
         input()
         bat=open("terminal.bat","w")
         bat.write("@echo off\ncd c:\python34\npython -m serial.tools.miniterm "+port)
         bat.close()
         ser.close()
         log.close()
         os.system("cls")
         os.system("call terminal.bat")
      except KeyboardInterrupt:
         print("")
         

while True:
   try:
      main()
   except ImportError:
      print("Required modules can not be found!\nMake Sure you have installed pySerial")
   except KeyboardInterrupt:
      do_exit=input("[-] Do You Want to Exit?(Y/N): ")
      if (do_exit=="Y" or do_exit=="y"):
         config.ser.close()
         print("Exiting. . . . . . .  .")
         print("Disconnect successfully in port "+config.port)
         config.log.close()
      else:
         os.system("cls")
         print(base_view.banner)
         print (base_view.menu)
         main()


      
                 
