import network
import json
from emp_utils import rainbow
from emp_utils import print_as_a_list_item
from emp_utils import selection
from emp_utils import config_path


class Wifi():
    _profile = 'config/emp_wifi.json'

    @classmethod
    def create_profile(cls):
        default = ()
        records = []
        default_config = dict(default=default, records=records)
        cls.update_profile(default_config)
        print(rainbow('created config/wifi_cfg.json', color='blue'))

    @classmethod
    def update_profile(cls, config):
        config_path()
        with open(cls._profile, 'w') as f:
            f.write(json.dumps(config))

    @classmethod
    def read_config(cls):
        try:
            with open(cls._profile, 'r') as f:
                return json.loads(f.read())
        except:
            cls.create_profile()
            default = ()
            records = []
            return dict(default=default, records=records)

    @classmethod
    def get_default(cls):
        config = cls.read_config()
        return config.get('default') if config else ()

    @classmethod
    def set_default(cls, essid):
        config = cls.read_config()
        records = config.get('records')

        for index, item in enumerate(records):
            print(print_as_a_list_item(index, item))

        default = selection(
            'Please select an option as default wifi connection [0-%s]' % str(
                len(records - 1)), len(records - 1))
        
        config['default'] = records[default]
        cls.update_profile(config)

    @classmethod
    def get_records(cls):
        config = cls.read_config()
        return config.get('records') if config else []

    @classmethod
    def is_in_records(cls, essid):
        for i in cls.get_records():
            if essid == i[0]:
                return i
        return ()

    @classmethod
    def add_record(cls, essid, passwd):
        config = cls.read_config()
        config['records'].append((essid, passwd))
        cls.update_profile(config)
        print(rainbow('Added record: %s' % essid, color='green'))

    @classmethod
    def del_record(cls, essid):
        config = cls.read_config()
        for index, i in enumerate(config.get('records')):
            if essid == i[0]:
                config['records'].pop(index)
                cls.update_profile(config)
                print(rainbow('Record deleted: %s' % essid, color='green'))
                return True
        return False

    @classmethod
    def update_record(cls, essid, passwd):
        config = cls.read_config()
        for index, i in enumerate(config['records']):
            if i[0] == essid:
                config['records'][index] = (essid, passwd)
                return True
        return False

    @classmethod
    def ifconfig(cls):
        return NetWorker.worker().ifconfig()

    @classmethod
    def connect(cls):
        worker = NetWorker.worker()
        if worker.is_connected():
            s0 = 'You have already established a Wifi connection.'
            print(rainbow(s0, color='green'))
        else:   
            default = cls.get_default()
            if default:
                records = cls.get_records().insert(0, default)
            else:
                records = cls.get_records()
            # print(records)
            networks = [i.get('essid') for i in worker.scan()]
            for i in records:
                if i[0] in networks:
                    s1 = 'Trying to connect automatically to %s ...' % i[0]
                    print(rainbow(s1, color='blue'))
                    if not worker.do_connect(*i):
                        s2 = 'Automatic connection to %s failed' % i[0]
                        print(rainbow(s2,color='red'))
                        cls.del_record(i[0])
                        worker._wifi.active(True)
                        continue
                    else:
                        s3 = 'Automatically connect to %s successfully' % i[0]
                        print(rainbow(s3, color='green'))
                        return True
            print(rainbow('No record available', color='red'))
            worker.before_connect()

    @classmethod
    def disconnect(cls):
        NetWorker.worker().disconnect()


class NetWorker():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(NetWorker, cls).__new__(cls)
            cls._instance._wifi = network.WLAN(network.STA_IF)
            cls._instance._wifi.active(True)
            cls._instance._essid = None
        return cls._instance
            
    def scan(self):
        def _list_wifi(index, essid, dbm):
            _index = ('[%s]' % str(index)).center(8).lstrip()
            _essid = rainbow(essid + (40 - len(essid)) * ' ',color='red')
            _dbm = rainbow(dbm.center(10).lstrip(),color='blue')
            print('{0} {1} {2} dBm'.format(_index, _essid, _dbm))
        # TODO 字符编码容错

        networks = []
        for i in self._wifi.scan():
            try:
                nw = dict(essid=i[0].decode(), dbm=str(i[3]))
            except:
                nw = dict(essid=i[0] , dbm=str(i[3]))
            finally:
                networks.append(nw)
        # networks = [dict(essid=i[0].decode(),dbm=str(i[3])) for i in self._wifi.scan()]

        for i, item in enumerate(networks):
            _list_wifi(i, item['essid'], item['dbm'])

        return networks

    def ifconfig(self):
        info = self._wifi.ifconfig()
        print(rainbow('You are connected to %s' % self._essid))
        print(rainbow('IP: ' + info[0], color='red'))
        print(rainbow('Netmask: ' + info[1], color='green'))
        print(rainbow('Gateway: ' + info[2], color='blue'))
        return info, self._essid

    def is_connected(self):
        return self._wifi.isconnected()

    def before_connect(self):
        print('scaning networks...')
        networks = self.scan()
        selection = input(
            'Which one do you want to access? [0-%s]' % str(len(networks) - 1))
        if int(selection) > len(networks) - 1:
            print('your choice is out of range!')
            self.before_connect()
        essid = networks[int(selection)]['essid']

        passwd = input('Password for %s: ' % essid)

        if not self.do_connect(essid, passwd):
            self.before_connect()

    def do_connect(self, essid, passwd):
        if not self._wifi.isconnected():
            print('connecting to network...')
            self._wifi.active(True)
            self._wifi.connect(essid, passwd)
            import utime

            for i in range(300):
                if self._wifi.isconnected():
                    break
                utime.sleep_ms(100)

            if not self._wifi.isconnected():
                self._wifi.active(False)
                print(
                    rainbow(
                        'wifi connection error, please reconnect',
                        color='red'))
                return False

            else:
                self._essid = essid
                self.ifconfig()
                if not Wifi.is_in_records(essid):
                    Wifi.add_record(essid, passwd)
                
                return True
        else:
            print(rainbow('You have already established a Wifi connection.',color='green'))
            return True

    def disconnect(self):
        self._wifi.active(False)
        print(rainbow('WIFI connection has been disconnected',color='red'))
    
    @classmethod
    def worker(cls):
        return NetWorker()

    

if __name__ == '__main__':
    Wifi.connect()
