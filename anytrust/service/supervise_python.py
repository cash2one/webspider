import os  
import subprocess  
import time  
import smtplib    
from email.mime.text import MIMEText 

 
msg_from='python_warning@sohu.com'                       #发送方邮箱
passwd='123456WSC-'                                      #填入发送方邮箱的授权码
msg_to=["1587321194@qq.com"]                             #收件人邮箱

# 发送邮件
def send_mail(msg_to,subject,content):  #to_list：收件人；sub：主题；content：邮件内容  

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ";".join(msg_to)
    try:
        s = smtplib.SMTP_SSL("smtp.sohu.com",465)                 #邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        return False
    except:
        return True
    finally:
        s.quit()

def gushiwen_su():
    res = subprocess.Popen('ps -ef | grep "python gushiwen.py" | grep -v grep | wc -l',stdout=subprocess.PIPE,shell=True)    
    attn=res.stdout.readlines()  
    counts=int(attn[0].strip()) #获取ASRS下的进程个数
    # 假如counts不等于所开的进程个数，则需要发送邮件
    if counts != 3:
        f = open('nohup.out','r')  #报错信息存储的文件
        content = f.read()
        f.close()        
        return send_mail(msg_to,'程序崩溃',content)
    return True


def main():
    flag_gushiwen = True
    while 1:
        if flag_gushiwen:
            flag_gushiwen = gushiwen_su()
            time.sleep(60)

if __name__ == '__main__':
    main() 

                            
