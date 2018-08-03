# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
import logging
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header

class HtmlTable:
    """
    用于生成一个报表的html代码
    add_header: 添加表头
    add_tr：添加行
    to_str: 生成html代码
    """
    def __init__(self):
        self._t_start = '<table border="1" cellspacing="0" cellpadding="0" bordercolor="#666666">'
        self._content = ''
        self._t_end = '</table>'
        self._k = 1

    def add_header(self, headers):
        """
        headers: 表头
        """
        val = '<tr style="background:rgb(51, 122, 183);color:rgb(255, 255, 255)" >'
        for td in headers:
            val += '<td width="140">' + str(td) + "</td>"
        val += '</tr>'
        self._content += val

    def add_tr(self, tr_list):
        """
        tr_list: 表中的一行
        """
        if self._k == 1:
            val = '<tr style="background:rgb(223, 240, 216);color:rgb(60, 118, 61)">'
        else:
            val = '<tr style="background:rgb(252, 248, 227);color:rgb(138, 109, 59)">'
        self._k = 1 - self._k
        for td in tr_list:
            val += '<td width="140">' + str(td) + "</td>"
        val += '</tr>'
        self._content += val

    def to_str(self):
        """
        返回html表示
        """
        return self._t_start + self._content + self._t_end

class MailUtil(object):
    """
    封装的一个mail工具。
    支持添加附件，图片，文件，html，text
    添加完成之后send发送邮件
    """
    def __init__(self, user, passwd, host='localhost', port=587):
        """
        user: 发送人邮箱
        passwd: 发送人邮箱密码
        host: 邮件服务器
        port: 服务器端口
        """
        self._user = user
        self._passwd = passwd
        self._host = host
        self._port = port
        self._body = ""
        self._msg = MIMEMultipart()
        self._image_count = 0
        self._h_begin = '<html><body>'
        self._h_end = '</body></html>'

    def reset(self):
        """
        清空添加的内容，重新添加的时候用
        """
        self._image_count = 0
        self._body = ""
        self._msg = MIMEMultipart()

    def add_text(self, text):
        """
        text:待添加文本
        """
        text = "<pre>%s</pre>" % text
        self._body += text

    def add_html(self, htmlText):
        """
        htmlText: 待添加的html片段，不做任何处理
        """
        self._body += htmlText

    def add_image(self, image_file):
        """
        image_file: 待添加的图片，会展示在邮件正文中
        """
        basename = os.path.basename(image_file)
        image = MIMEImage('image', basename.split('.')[-1], filename=basename)
        cid = self._image_count

        image.add_header('Content-Disposition', 'attachment', filename=basename)
        image.add_header("Content-ID", "<{cid}>".format(cid=cid))
        image.add_header('X-Attachment-Id', '{cid}'.format(cid=cid))

        with open(image_file) as f:
            image.set_payload(f.read())

        encoders.encode_base64(image)
        self._msg.attach(image)

        self.add_html('<strong>{filename}</strong><center><img src="cid:{cid}"></center>'
                .format(filename=basename, cid=cid))
        self._image_count += 1
        logging.info('add image:%s, image count:%s' % (basename, self._image_count))

    def add_extra(self, filename):
        """
        filename: 待添加的附件
        """
        with open(filename, 'rb') as f:
            extra = MIMEText(f.read(), 'base64', 'utf-8')

        basename = os.path.basename(filename)
        extra.add_header('Content-Type', 'application/octet-stream')
        extra.add_header('Content-Disposition', 'attachment', filename=basename)

        self._msg.attach(extra)
        logging.info('add extra:%s' % basename)

    def get_html_text(self):
        """
        返回邮件的html部分，附件部分不会返回
        """
        htmlText = self._h_begin + self._body + self._h_end
        return htmlText

    def send(self, subject, to_addr_list, cc_addr_list = []):
        """
        brief: 发送邮件
        subject: 邮件主题
        to_addr_list: 收件人列表
        cc_addr_list: 抄送人列表
        """
        msgText = MIMEText(self.get_html_text(), 'html', 'utf-8')
        self._msg.attach(msgText)

        from_addr = self._user
        self._msg['From'] = from_addr
        self._msg['To'] = ','.join(to_addr_list)
        self._msg['Cc'] = ','.join(cc_addr_list)
        self._msg['Subject'] = subject
        smtp = smtplib.SMTP(self._host, self._port)
        smtp.starttls()
        smtp.login(self._user, self._passwd)
        smtp.sendmail(self._user, to_addr_list + cc_addr_list, self._msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    import mail_conf
    mail = MailUtil(user=mail_conf.user, passwd=mail_conf.passwd, host=mail_conf.host, port=mail_conf.port)

    mail.add_html('<h1>test for mail util</h1>')

    tbl = HtmlTable()
    tbl.add_header(['id', 'bool', 'val'])
    tbl.add_tr([1, True, 1])
    tbl.add_tr([2, False, 2.0])

    mail.add_html('<h1>test add table</h1>')
    mail.add_html(tbl.to_str())

    mail.add_text('test for add image')
    mail.add_text('image 1')
    mail.add_image('test1.png')
    mail.add_text('image 2')
    mail.add_image('test2.png')

    mail.add_text('test for add extra')
    mail.add_extra('mail.py')

    mail.send(to_addr_list=[],cc_addr_list=['akxxsb@vip.qq.com'], subject='测试邮件工具')
