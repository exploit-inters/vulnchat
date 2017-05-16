import sleekxmpp as xmpp
import queue
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.util.misc_ops import setdefaultencoding


class Message:
    def __init__(self, messageid, time, dst, text):
        self.messageid = messageid
        self.time = time
        self.dst = dst
        self.text = text


class Client(xmpp.ClientXMPP):
    def __init__(self, userid, jid, displayname, password, useragent):
        """
        Initially, 
        :param userid: 
        :param jid: 
        :param displayname: 
        :param password: 
        :param useragent: 
        """
        xmpp.ClientXMPP.__init__(self,jid,password)
        self.password = password
        self.message_queue = queue.PriorityQueue()
        self.registration_status = 0
        self.connection_status = 0
        setdefaultencoding('utf8')

    def get_reg_status(self):
        return self.registration_status

    def get_conn_status(self):
        return self.connection_status

    def add_message(self, tmp_message):
        """
        Inserts message into this user's queue sorted by time needs to be sent
        :param tmp_message: Message object to be added to priority queue based on time 
        :return: 1 on success, 0 on fail
        """
        self.message_queue.put((int(tmp_message.time), tmp_message))

    def register(self, server, port):
        print server
        print port
        self.connect((server,int(port)))
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        print resp
        try:
            resp.send(now=True)
        except IqError as e:
            print "ERROR"
            self.disconnect()
        except IqTimeout:
            print "TIMEOUT"
            self.disconnect()




    def poll_message(self):
        # type: () -> object
        """
        :return: Next Message on queue or None if queue empty
        """
        try:
            return self.message_queue.get(block=False)
        except queue.Empty:
            return None

    def send_message(self, message):
        """
        :param message: string message to send
        :return: 1-delivered, 0-failed
        """
        print message.text

