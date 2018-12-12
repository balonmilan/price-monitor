from datetime import datetime, timedelta
import time as mod_time
import json
from jinja2 import Environment, PackageLoader
import smtplib
from email.mime.text import MIMEText
import argparse

jinja_env = Environment(loader=PackageLoader('price_monitor', 'templates'))

def main(args):
    filename = "data/" + datetime.now().strftime("%Y%m%d")
    data_stores = {}
    try:
        with open(filename + ".json", 'r') as fp:
            data_stores = json.load(fp)
    except:
        pass
    
    html_body = ""    
    html_body = jinja_env.get_template('report.html').render(items=data_stores)
    with open(filename + ".html", 'w') as fp:
        fp.write(html_body.encode('utf8'))
        
    send_email(html_body, args.meEmail, args.mePassword, args.youEmail)
        
def send_email(html_body, meEmail, mePassword, youEmail):    
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = 'Report'
    msg['From'] = meEmail
    msg['To'] = youEmail
     
    # Send the message via remote SMTP server.
    print("create server")
    s = smtplib.SMTP('smtp.seznam.cz',25)
    print("logging in")
    s.login(meEmail, mePassword)
    print("logged in")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    
    s.sendmail(me, you, msg.as_string())
    print("message sent")
    s.quit()
    
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--meEmail', required=True,
                        help='Email server username')
    parser.add_argument('--mePassword', required=True,
                        help='Email server password')
    parser.add_argument('--youEmail', required=True,
                        help='Email where to send report')

    return parser.parse_args()
       
if __name__ == '__main__':
    main(parse_args())