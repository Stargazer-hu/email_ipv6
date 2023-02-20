import smtplib
from email.mime.text import MIMEText
from time import sleep
import requests
import json


def check_and_send():
    # 账号设置
    f = open('email_info.txt', encoding='utf-8')
    f_text = f.readlines()
    f_list = []
    for j in f_text:
        f_list.append(j.split('=')[1].strip())
    username = f_list[0]  # qq邮箱用户名
    password = f_list[1]  # qq邮箱授权码
    send_mail = f_list[2]  # 发送地址，可以同上用户名
    receive_mail = f_list[3]  # 接受邮件的地址，可以用发件箱，自发自收
    mail_host = f_list[4]  # QQ邮箱的mail host
    port = int(f_list[5])  # 设置端口号
    mail_subject = str(f_list[6])  # 设置邮件主题
    f.close()


    # 查找上次的ip地址，作为是否要发邮件的判断条件
    f1 = open('run_log.txt')
    former_ips = f1.readlines()
    former_ip = former_ips[-1]
    f1.close()

    ip = ''
    for i in range(3):
        # 获取IP地址
        url = "https://6.ipw.cn/api/ip/myip?json"
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                ip = json.loads(response.content)['IP']
                # print(ip)
                break
        except Exception as e:
            pass


    if (ip != '') and (ip != former_ip):
        # 保存记录
        f2 = open('run_log.txt', mode='a+')
        f2.write('\n'+ip)
        f2.close()

        # 内容设置
        mes = MIMEText(ip, 'plain', 'utf-8')
        mes['Subject'] = mail_subject
        mes['From'] = send_mail
        mes['To'] = receive_mail

        # 发送
        server = smtplib.SMTP(mail_host, port)
        server.ehlo() 
        server.starttls()
        server.login(username, password)
        sleep(1)
        server.sendmail(send_mail, receive_mail, mes.as_string())
        server.quit()
    return ip


cnt = 0
while(1):
    ip = check_and_send()
    sleep(1)
    cnt += 1
    print(cnt, ':', ip)