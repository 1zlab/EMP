import network
import json
from emp_utils import rainbow

class WifiHelper():
    profile = 'wifi_config.json'

    @classmethod
    def create_profile(cls):
        default = ()
        records = []
        default_config = dict(default=default, records=records)
        cls.update_profile(default_config)
        print(rainbow('created wifi_config.json', color='blue'))

    @classmethod
    def update_profile(cls, config):
        with open(cls.profile, 'w') as f:
            f.write(json.dumps(config))

    @classmethod
    def read_config(cls):
        try:
            with open(cls.profile, 'r') as f:
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
    def set_default(cls,essid):
        pass

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
        if not cls.is_in_records(essid):
            config = cls.read_config()
            config['records'].append((essid, passwd))
            cls.update_profile(config)
            print(rainbow('record %s has been added' % essid, color='green'))

    @classmethod
    def del_record(cls, essid):
        config = cls.read_config()
        for index, i in enumerate(config.get('records')):
            if essid == i[0]:
                config['records'].pop(index)
                cls.update_profile(config)
                print(
                    rainbow(
                        'record %s has been deleted' % essid, color='green'))
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
    def auto_connect(cls, wifi):
        default = cls.get_default()
        if default:
            records = cls.get_records().insert(0, default)
        else:
            records = cls.get_records()
        print(records)
        networks = [i.get('essid')[7:-4] for i in wifi.scan()]

        for i in records:
            if i[0] in networks:
                print(
                    rainbow(
                        'trying to auto connect %s ...' % i[0], color='blue'))
                if not wifi.do_connect(*i):
                    print(
                        rainbow(
                            'trying to auto connect %s failed' % i[0],
                            color='red'))
                    cls.del_record(i[0])
                    wifi._wifi.active(True)
                    continue
                else:
                    print(
                        rainbow(
                            'auto connect %s succeed!' % i[0], color='green'))
                    return True
        print(rainbow('none of records available.', color='red'))
        wifi.before_connect()


class Wifi():
    def __init__(self):
        self._wifi = network.WLAN(network.STA_IF)
        self._wifi.active(True)

    def _list_wifi(self, index, essid, dbm):
        '''
        print format
        '''
        _index = ('[%s]' % str(index)).center(8).lstrip()
        _essid = essid + (40 - len(essid)) * ' '
        _dbm = dbm.center(10).lstrip()
        print('{0} {1} {2} dBm'.format(_index, _essid, _dbm))

    def scan(self):
        networks = [
            dict(
                essid=rainbow(i[0].decode(), color='red'),
                dbm=rainbow(str(i[3]), color='green'))
            for i in self._wifi.scan()
        ]
        for i, item in enumerate(networks):
            self._list_wifi(i, item['essid'], item['dbm'])
        return networks

    def before_connect(self):
        print('scaning networks...')
        networks = self.scan()
        selection = input(
            'Which one do you want to access? [0-%s]' % str(len(networks) - 1))
        if int(selection) > len(networks) - 1:
            print('your selection is out of range!')
            self.before_connect()
        essid = networks[int(selection)]['essid']

        passwd = input('Password for %s: ' % essid)
        print(essid, essid[7:-4], len(essid[7:-4]))
        if not self.do_connect(essid[7:-4], passwd):
            self.before_connect()

    def do_connect(self, essid, passwd):
        if not self._wifi.isconnected():
            print('connecting to network...')
            self._wifi.active(True)
            self._wifi.connect(essid, passwd)
            import utime

            for i in range(100):
                # print('第{}次尝试连接WIFI热点'.format(i))
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
                print(rainbow('network config:%s'%self._wifi.ifconfig(),color='green'))
                WifiHelper.add_record(essid, passwd)
                return True


if __name__ == '__main__':
    wifi = Wifi()
    WifiHelper.auto_connect(wifi)
    
