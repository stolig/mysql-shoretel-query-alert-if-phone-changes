#!/usr/bin/python

# Find out if mac address changed on shoretel extension. If it did, email an alert.
# If the ip/mac changes for an extension, we ARE NOT recording calls in versadial that NEED recorded.
# written by: github/stolig

# sudo pip install mysql-connector-python-rf # if you don't have the mysql module

# example: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html

import mysql.connector
import smtplib

mailServer = smtplib.SMTP('mysmtpserver.mydomain.com')
FROM = "email@domain.com"
TO = ["toemail@domain.com"]

d1 = {}

# known good extension to mac addresses...update this to suit your env:

d2 = {'5910':'00104917E190',
      '5913':'00104917E2A0',
      '5908':'0010494E3BB3',
      '5909':'001049242CC6',
      '5910':'00104917E2B3',
      '5917':'0010495358721',
      '5914':'001049242CBA',
      '5916':'00104955F6E1'
     }

def queryShoretel():

    # don't forget to update the creds/host in this connection string:

    cnx = mysql.connector.connect(user='myuser', password='mypassword', database='shoreware', host='mysqlhost', port=4308)
    
    cursor = cnx.cursor()

    query = ("SELECT HomeDN, MACAddress FROM ports "
             "WHERE IsIPPhone = 1 and CurrentDN not like 'None'")

    cursor.execute(query)
    
    for row in cursor:
        
        for item in row:

            shoretelExt = row[0]
            shoretelMac = row[1]

            d1[shoretelExt] = shoretelMac
    
    cursor.close()
    cnx.close()

    for row in d2.items():

        targetExt = row[0]
        targetMac = row[1]

        for user in d1.items():

            shoretelExt = user[0]
            shoretelMac = user[1]
            
            if targetExt == shoretelExt and targetMac != shoretelMac:

                print "static ", targetExt, targetMac, "don't match shoretel ", shoretelExt, shoretelMac

                SUBJECT = "versadial mac change on ext %s" % targetExt
                TEXT = "static %s %s doesn't match shoretel: %s %s" % (targetExt, targetMac, shoretelExt, shoretelMac)
                msg = "Subject: {}\n\n{}".format(SUBJECT, TEXT)

                mailServer.sendmail(FROM, TO, msg)

queryShoretel()
