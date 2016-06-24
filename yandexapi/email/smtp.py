import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SMTP:
    def __init__(self, host):
        self.host = host
        # self.username = username
        # self.password = password
        self.server = smtplib.SMTP(self.host)

    def _make_connection(self):
        if self._connection_status() is not True:
            self.server.connect(self.host)
            # self.server.login(self.username, self.password)

    def _connection_status(self):
        try:
            status = self.server.noop()[0]
        except smtplib.SMTPServerDisconnected:
            status = None
        return True if status is not None else False

    # def send_mail(self, body, subject, to_addrs, from_addr):
    #     msg = MIMEText(body, '', 'utf-8')
    #
    #     msg['To'] = to_addrs
    #     msg['From'] = from_addr
    #     msg['Subject'] = subject
    #
    #     self._make_connection()
    #     self.server.sendmail(from_addr, to_addrs, msg.as_string())

    def send_mail(self, email_recipient, subject, html):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        part1 = MIMEText(' ', 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        self.server.sendmail('noreply@uraltep.ru', email_recipient, msg.as_string())