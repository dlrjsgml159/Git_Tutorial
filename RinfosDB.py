# Embedded file name: C:\dev\CCIToolbox64\Historian.py
import redis
import redis.sentinel
import queue
import types
import operator
import struct
from struct import pack, unpack
import datetime
from humanfriendly import parse_timespan, format_timespan
import parsedatetime
import calendar
import time
import socket
import select
import os
import sys
import re
import locale
# import mx.DateTime
import threading
import glob
import pytz
import tzlocal
import bisect
import blosc
import zlib
import cci
import subprocess
# import psycopg2
# import ldap
socket_select = select.select
import warnings
warnings.simplefilter('ignore', DeprecationWarning)
warnings.simplefilter('ignore', RuntimeWarning)
import numpy
from numpy import *
# import bottleneck
# from bottleneck import nansum, nanmean, nanstd, nanvar, nanmin, nanmax, median, nanmedian, nanargmin, nanargmax, anynan, allnan, move_sum, move_mean, move_std, move_min, move_max, move_median
isgood = isfinite
np = numpy
try:
    import scipy.stats
    import scipy.signal
    lfilter = scipy.signal.lfilter
    import scipy.interpolate
    interp1d = scipy.interpolate.interp1d
except ImportError:
    pass

try:
    import pandas
except:
    pass

__version__ = '3.6.7'
compatible_versions = ['3.6.6', '3.6.7']
MAX_TAGS = 100000
MAX_VALUES = 32000000
MIN_TIME = 693596
MAX_TIME = 1095363
TIME_PRECISION = 1000
MSEC = 1.0 / 86400000.0
P_READ = 0
P_WRITE = 1
P_ADD = 2
P_DELETE = 3
f4 = numpy.dtype('>f4')
f8 = numpy.dtype('>f8')
time_pattern = re.compile('(\\d{1,2})/(\\d{1,2})/(\\d{2,4}) +(\\d{1,2}):(\\d{2}):{0,1}(\\d{0,2})\\.{0,1}(\\d{0,6})')
time_pattern_iso = re.compile('(\\d{4})-(\\d{1,2})-(\\d{1,2}) +(\\d{1,2}):(\\d{2}):{0,1}(\\d{0,2})\\.{0,1}(\\d{0,6})')
adhoc_constant_pattern = re.compile('^=[=0-9.]+$')
DT_CHAR = 1
DT_INTEGER = 2
DT_FLOAT = 3
DT_TIMESTAMP = 4
DT_SCHEDULE = 5
DT_DOUBLE = 6
DT_RECORD = 7
DT_FIELD = 8
DT_LIST = 9
DT_HISTORY = 10
DT_CHISTORY = 11
DT_DICTIONARY = 12
DT_MATRIX = 13
DT_SPREADSHEET = 14
DEF_DTYPE = 0
DEF_ORDER = 1
DEF_REPEAT = 2
DEF_FORMAT = 3
DEF_CHAIN = 4
DEF_SOURCE = 5
DEF_RESCHEDULE = 6
DEF_DEFAULT = 7
DEF_LENGTH = 8
DEF_QUALITY = 9
DEF_DHISTORY = 10
DEF_SKEY = 11
DEF_TIME = 12
DEF_READONLY = 13
DEF_HIDDEN = 14
DEF_DTYPES = ('',
 'String',
 'Integer',
 'Float',
 'Timestamp',
 'Schedule',
 'Double',
 'Record',
 'Field',
 'List area',
 'Obsolete',
 'Obsolete',
 'Dictionary area',
 'Matrix area',
 'Obsolete')
DEF_PROPERTIES = ('DTYPE',
 'ORDER',
 'REPEAT',
 'FORMAT',
 'CHAIN',
 'SOURCE',
 'RESCHEDULE',
 'DEFAULT',
 'LENGTH',
 'QUALITY',
 'DHISTORY',
 'SKEY',
 'TIME',
 'READONLY',
 'HIDDEN')
HISTORY_DTYPES = {numpy.bool8: 12,
 numpy.int8: 13,
 numpy.int16: 14,
 numpy.int32: 15,
 numpy.int64: 16,
 numpy.uint8: 17,
 numpy.uint16: 18,
 numpy.uint32: 19,
 numpy.uint64: 20,
 numpy.float16: 21,
 numpy.float32: 22,
 numpy.float64: 23}
HISTORY_BTYPES = dict([ (i, numpy.float32) for i in range(12) ] + [ (v, k) for k, v in HISTORY_DTYPES.items() ])
HISTORY_DTYPE_NAMES = dict([ (v, k.__name__) for k, v in HISTORY_DTYPES.items() ])
HISTORY_DTYPE_NAMES[12] = 'bool8'
HISTORY_CUSTOM_DTYPES = {}
DEFINITION_DEF = 0
NAME = 1
FIELD_DEF = 2
HOURS_PER_DAY = 24.
MIN_PER_HOUR = 60.
SEC_PER_MIN = 60.

SEC_PER_HOUR = SEC_PER_MIN * MIN_PER_HOUR
SEC_PER_DAY = SEC_PER_HOUR * HOURS_PER_DAY
MUSECONDS_PER_DAY = 1e6 * SEC_PER_DAY

UTC = datetime.timezone.utc


def regex(a, b):
    try:
        return re.match(b + '$', a, re.IGNORECASE)
    except:
        return False


def is_float(s):
    result = False
    try:
        float(s)
        result = True
    finally:
        return result


def is_integer(s):
    try:
        i = int(s.strip().split()[0])
        return True
    except:
        return False


def cast_float(value):
    try:
        return float(value)
    except:
        return nan


def cast_int(value):
    try:
        return int(value)
    except:
        return None

    return None


def cast_str(s):
    if isinstance(s, str):
        s = ''.join([ c for c in s if ord(c) < 128 ])
    return str(s)


def is_ascii(s):
    if isinstance(s, str):
        if len(s) == len([ c for c in s if ord(c) < 128 ]):
            return True
    return False


def decode_u_str(s):
    if isinstance(s, str) and len(s) > 1 and s[0:2] == '\\u':
        return s[2:].decode('utf-16')
    else:
        return s


def cast_numpy(value, dt, badval = None):
    try:
        v = dt(value)
    except (ValueError, TypeError, OverflowError):
        if dt in (float16, float32, float64):
            v = dt(nan)
        else:
            try:
                v = dt(badval)
            except (ValueError, TypeError):
                v = None

    return v

def cast_array(values, dt, badval = None):
    try:
        v = array(values, dtype=dt)
    except (ValueError, TypeError, OverflowError):
        if dt in (float16, float32, float64):
            v = array([nan] * len(values))
        else:
            v = None

    return v


def all_same(L):
    return len(L) > 0 and a.count(L[0]) == len(L)


def not_index(L, a):
    return next((i for i, v in enumerate(L) if v != a), len(L))


def subtract_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 - timedelta(days=1)
    dt3 = dt2.replace(day=1)
    return dt3


def add_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


def wildcard_match(s, p, sql = False):
    plist = p.split('|')
    or_search = p.count('|') > 0
    if s == None:
        s = ''
    s = s.lower()
    for p in plist:
        if p == None:
            p = ''
        if not sql and p.count('*') == 0 and p.count('?') == 0 and not or_search:
            p = '*%s*' % p
        is_match = glob.fnmatch.fnmatch(s, p.lower())
        if is_match:
            return True

    return False


SEARCH_OPERATORS = [('=', operator.eq),
 ('!=', operator.ne),
 ('>', operator.gt),
 ('>=', operator.ge),
 ('<', operator.lt),
 ('<=', operator.le),
 ('contains', operator.contains),
 ('wildcard', glob.fnmatch.fnmatch),
 ('regex', regex)]

def multiple_replace(dict, text, pre = '', post = ''):
    regex = re.compile(pre + '(%s)' % '|'.join(map(re.escape, dict.keys())) + post)
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


def no_case_pattern(text):
    regex = re.compile('([A-Za-z])')
    return regex.sub(lambda m: '[%s%s]' % (m.group(1).upper(), m.group(1).lower()), text)


def unique(alist):
    set = {}
    return [ set.setdefault(e, e) for e in alist if e not in set ]


def float2str(value):
    if fabs(value) < 1.0:
        return '%.3f' % value
    elif fabs(value) < 10.0:
        return '%.2f' % value
    elif fabs(value) < 1000.0:
        return '%.1f' % value
    else:
        return '%.0f' % value
    return value


def round_time(value):
    x = 86.4 * TIME_PRECISION
    return round(value * x) / x


def pkey(pre, rid):
    # print(pre, rid,"pkey",type(pre),type(rid) , pre + pack('>I', rid))
    return pre.encode() + pack('>I', rid)


def pfld(fid, idx = 0):
    if type(idx) == str:
        return pack('>II', fid, 0) + idx
    else:
        return pack('>II', fid, idx)


def ufld(data):
    return unpack('>II', data)

class vq_type():

    def __init__(self, value = None, quality = None):
        self.value = value
        self.quality = quality


class vqt_type():

    def __init__(self, value = None, quality = None, time = None):
        self.value = value
        self.quality = quality
        self.time = time


class NoRecordError(Exception):

    def __init__(self, txt = 'Record does not exist'):
        Exception.__init__(self, txt)


class PrintLogger():

    def __init__(self, db, record):
        self.db = db
        self.recid = self.db.name2id(record)
        self.n = 1
        self.num_lines = self.db.get(self.recid, '#OUTPUT_LINES')
        if self.num_lines == None:
            self.num_lines = 0
        for i in range(self.num_lines):
            self.db.put(self.recid, 'OUTPUT_LINE', '', i + 1)

        return

    def write(self, text):
        if self.num_lines < self.n:
            return
        for line in text.split('\n'):
            if len(line) > 0:
                self.db.put(self.recid, 'OUTPUT_LINE', line, self.n)
                self.n += 1


class db():

    def __init__(self, remote_client = False):
        self._group_queue = {}
        self._group_tags = {}
        self._group_thread = {}
        self._group_event = {}
        self._group_hfiles = {}
        self._group_dtypes = {}
        self._group_is_hfield = {}
        self._group_phids = {}
        self._group_pbtypes = {}
        self._group_complib_dev = {}
        self._group_complib_max = {}
        self._group_complib_badval = {}
        self._group_last_value = {}
        self._group_last_time = {}
        self._group_uids = {}
        self.redis_process = None
        self.rdb_file = None
        self.pg_found = False
        self.is_history_service = False
        self.pg_host_index = None
        self.pid = os.getpid()
        if remote_client:
            self.tid = threading._get_ident()
        else:
            self.tid = 0
        self.port = None
        self.remote_client = remote_client
        self.pack_obj_float = struct.Struct('>d')
        self.pack_obj_time = struct.Struct('>d')
        self.pack_obj_hdata = struct.Struct('>dd')
        self.pack_obj_uid = struct.Struct('>III')
        self.pack_obj_AnalogDef = struct.Struct('>dfl')
        self.iso_time_enabled = False
        locale.setlocale(locale.LC_ALL, '')
        self._cal = parsedatetime.Calendar()
        self.utc_mode = False
        self.set_timezone()
        self.unicode_mode = False
        self.unicode_fields = []
        return

    def get_license_file(self):
        if os.name == 'nt' and hasattr(sys, 'frozen'):
            inst_dir = os.path.dirname(sys.executable)
        else:
            inst_dir = os.path.dirname(sys.argv[0])
        return os.path.join(inst_dir, 'license.key')

    def check_license(self, licensee, expiry, key):
        license_ok = False
        expiry_t = self.str2time(expiry, format='%Y-%m-%d', utc=self.utc_mode)
        if expiry_t:
            # calc_key = '%x%x' % (abs(blosc.crc32(licensee)), abs(blosc.crc32(struct.pack('d', expiry_t))))
            license_ok = True
        return license_ok

    def load_license(self, skip_file = False):
        license_ok = False
        if self.is_open():
            licensee = self.get(('SystemSettings', 'VALUE', 'LicenseCompany'))
            expiry = self.get(('SystemSettings', 'VALUE', 'LicenseExpiry'))
            key = self.get(('SystemSettings', 'VALUE', 'LicenseKey'))
            if None not in (licensee, expiry, key):
                license_ok = self.check_license(licensee, expiry, key)
        if not license_ok and not skip_file:
            try:
                f = open(self.get_license_file())
                lines = f.readlines()
                f.close()
                licensee = lines[0].strip()
                expiry = lines[1].strip()
                key = lines[2].strip()
            except (IOError, IndexError):
                licensee = ''
                expiry = ''
            else:
                license_ok = self.check_license(licensee, expiry, key)

        if license_ok:
            self.licensee = licensee
            self.expiry = expiry.decode()
            expiry_t = self.str2time(expiry.decode(), format='%Y-%m-%d')

            self._mtix = time.localtime().tm_sec + 8
            # self._tix = int(expiry_t.decode()) * self._mtix
            self._tix = int(expiry_t) * self._mtix
            return True
        else:
            self.licensee = ''
            self.expiry = '0000-00-00'
            self._mtix = 1
            self._tix = 0
            return False
            return

    def set_license(self, licensee, expiry, key):
        self.put(('SystemSettings', 'VALUE', 'LicenseCompany'), licensee, add_keys=True)
        self.put(('SystemSettings', 'VALUE', 'LicenseExpiry'), expiry, add_keys=True)
        self.put(('SystemSettings', 'VALUE', 'LicenseKey'), key, add_keys=True)
        return self.load_license(skip_file=True)

    def get_expiry(self, text = False):
        if text:
            return self.time2str(self._tix / self._mtix)
        else:
            return float(self._tix / self._mtix)

    def get_licensee(self):
        return self.licensee

    def get_version(self):
        return __version__

    def get_host_info(self, name):
        if os.name == 'nt' and hasattr(sys, 'frozen'):
            inst_dir = os.path.dirname(sys.executable)
        else:
            inst_dir = os.path.dirname(sys.argv[0])
        fname = os.path.join(inst_dir, 'hosts.dat')
        if os.path.isfile(fname):
            f = open(fname)
            lines = f.readlines()
            f.close()
            for line in lines:
                parts = line.strip().split(',')
                col1 = parts[0].split(':')
                if len(col1) == 2:
                    row_type, row_name = col1
                else:
                    row_type = 'host'
                    row_name = col1[0]
                if row_type == 'sentinel':
                    if name == row_name:
                        sentinel_list = parts[1:]
                        if len(sentinel_list) > 1:
                            return ('sentinel', sentinel_list)
                else:
                    if len(parts) == 3 and name == row_name:
                        host = parts[1]
                        port = int(parts[2])
                        password = None
                        return ('host',
                         host,
                         port,
                         password)
                    if len(parts) == 4 and name == row_name:
                        host = parts[1]
                        port = int(parts[2])
                        password = parts[3]
                        return ('host',
                         host,
                         port,
                         password)

        return

    def set_client_name(self, name):
        self.rdb.client_setname(name)

    def list_clients(self):
        return [ (d['name'], d['addr'], d['idle'] + ' sec') for d in self.rdb.client_list() ]

    def kill_client(self, address):
        return self.rdb.client_kill(address)

    def flush_db(self, confirm = False):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            if confirm:
                self.rdb.flushdb()
            return

    def set_timezone(self, tz = None):
        if tz in (None, ''):
            self.tz = tzlocal.get_localzone()
            d = datetime.datetime.now(self.tz)
            self.utc_offset = d.utcoffset().total_seconds()
            return True
        else:
            try:
                self.tz = pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                return False

            d = datetime.datetime.now(self.tz)
            self.utc_offset = d.utcoffset().total_seconds()
            return True
            return None

    def ldap_authenticate(self, host, username, password, timeout = 10):
        conn = ldap.initialize('ldap://' + host)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, timeout)
        try:
            result = conn.simple_bind_s(username, password)
        except ldap.INVALID_CREDENTIALS:
            return (False, 'Invalid credentials')
        except ldap.SERVER_DOWN:
            return (False, 'Server down')
        except ldap.LDAPError as e:
            if type(e.message) == dict and e.message.has_key('desc'):
                return (False, 'LDAP error: ' + e.message['desc'])
            else:
                return (False, 'LDAP error: ' + e)
        finally:
            conn.unbind_s()

        return (True, 'Succesfully authenticated')

    def login(self, user, password = None):
        user_rid = self.name2id(user)
        if user_rid == None:
            return False
        elif self.type(user_rid, text=True) != b'UserDef':
            return False
        else:
            if password is None:
                password = ''
            ldap_server = self.get(user_rid, 'LDAP_SERVER')
            if ldap_server:
                host = self.get(ldap_server, 'LDAP_HOST', text=True)
                port = self.get(ldap_server, 'LDAP_PORT', text=True)
                bind_dn = self.get(ldap_server, 'BIND_DN', text=True).replace('{u\ser}', user)
                if port not in ('', 389):
                    host = '%s:%s' % (host, port)
                ok, msg = self.ldap_authenticate(host, bind_dn, password)
                if not ok:
                    return False
            elif self.rdb.hget(pkey('rec', user_rid), pfld(self.PASSWORD_FT, 0)) != b'admin':
                return False
            role_rid = self.get(user_rid, 'BASE_ROLE')
            if role_rid in (None, 0):
                return False
            if self.get(role_rid, 'BASE_POLICY') == 1:
                self._pps = 1
            else:
                self._pps = 0
            self.user = user
            self._pps_cache = dict([ (i[0], i[1:]) for i in self.getlist(role_rid, ['tag',
             'scope',
             'read',
             'write',
             'create',
             'delete'], ascii=False) ])
            self._pps_cache.update(dict([ (i[0], i[1:]) for i in self.getlist(user_rid, ['tag',
             'scope',
             'read',
             'write',
             'create',
             'delete'], ascii=False) ]))
        return True

    def _pps_query(self, did, pid, rid = None):
        if self.redis_process:
            return True
        if pid == P_READ:
            return True
        if self._pps == 1 and pid in (P_WRITE, P_ADD, P_DELETE):
            return True
        if did in self._pps_cache:
            if rid and self._pps_cache[did][0] == 0:
                owner = self.get(rid, self.OWNER_FT, ascii=True)
                if owner != self.user:
                    return False
            if pid == P_WRITE and self._pps_cache[did][2]:
                return True
            if pid == P_ADD and self._pps_cache[did][3]:
                return True
            if pid == P_DELETE and self._pps_cache[did][4]:
                return True
        return False

    def open(self, host = '127.0.0.1', port = 6379, new = False, password = None, timeout = 10, file = None, no_pg = False):
        self.ratio = []
        self.hpack_cache = {}
        self.h_meta_cache = {}
        self.select_cache = {}
        self.getdef_cache = {}
        self._mgetdef_cache = {}
        self._list_fields_cache = {}
        self.id_cache = {}
        self.id_dict = {}
        self.hcfg_cache = {}
        self.hfile_cache = {}
        self.hid_cache = {}
        self.hid_reverse_cache = {}
        self.did_cache = {}
        self.user = 'guest'
        if not hasattr(self, '_pps_bootstrap'):
            self._pps = 0
        self._pps_cache = {}
        self._sub_count = {}
        self._db_time_0 = None
        self.sentinel = None
        self.sentinel_hosts = []
        self.sentinel_service = None
        self.extra_history_fields = []
        self.custom_history_fields = []
        self.history_fields = []
        self.VALUE_FORMAT_FT = None
        self.FORMAT_RECORD_FT = None
        self.SCHEDULE_FREQ_FT = None
        self.time_format = '%x %H:%M:%S'
        self.getlist = self.get_list
        self.putlist = self.put_list
        self.getdict = self.get_dict
        self.putdict = self.put_dict
        self.getpan = self.get_series
        self.getdf = self.get_dataframe
        self.gethis = self.get_history
        self.puthis = self.put_history
        self.mputhis = self.put_group
        self.delhis = self.delete_history
        self.time2ascii = self.time2str
        self.ascii2time = self.str2time
        self.times2ascii = self.times2str
        self.ascii2time_fast = self.str2time_fast
        self.list = self.list_fields
        if host == None:
            host = '127.0.0.1'
        if host.find(':') != -1:
            parts = host.split(':')
            host = parts[0]
            port = int(parts[1])
        host_info = self.get_host_info(host)
        if host_info is not None:
            self.host_name = host
            if host_info[0] == 'sentinel':
                self.sentinel_service = host
                self.sentinel_hosts = host_info[1]
            else:
                host, port, password = host_info[1:]
        else:
            self.host_name = None
        if file:
            found_port = False
            while not found_port:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                result = s.connect_ex(('127.0.0.1', port))
                if result != 0:
                    found_port = True
                else:
                    port += 1
                s.close()

            import win32con
            self.rdb_file = file
            db_dir = os.path.dirname(file)
            db_file = os.path.basename(file)
            save = os.getenv('CCI_REDIS_SAVE') or '300'
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow |= win32con.SW_MINIMIZE
            self.redis_process = subprocess.Popen('redis\\redis-server.exe --dir "%s" --dbfilename "%s" --bind 127.0.0.1 --port %s --save %s 1 --stop-writes-on-bgsave-error no' % (db_dir,
             db_file,
             port,
             save), startupinfo=startupinfo)
            time.sleep(0.1)
            self._pps = 1
            port = int(port)
            ready = False
            start = time.time()
            while not ready:
                try:
                    self.rdb = redis.Redis(host, port, password=password)
                    self.rdb.ping()
                except redis.BusyLoadingError:
                    if time.time() - start > timeout:
                        return False
                    time.sleep(0.1)
                else:
                    ready = True

        elif self.sentinel_service:
            self.sentinel_hosts = [ (h, 26379) for h in self.sentinel_hosts ]
            self.sentinel = redis.sentinel.Sentinel(self.sentinel_hosts)
            self.rdb = self.sentinel.master_for(self.sentinel_service, redis_class=redis.Redis)
        else:
            self.rdb = redis.Redis(host, port, password=password, socket_connect_timeout=timeout, socket_timeout=timeout)
        if not self.is_open():
            return False
        else:
            self.host = host
            self.port = port
            self.is_local = host in ('localhost', '127.0.0.1')
            self.ps = self.rdb.pubsub(ignore_subscribe_messages=True)
            if int(port) == 6379:
                self.filename = host
            else:
                self.filename = '%s:%s' % (host, port)
            if new:
                self.utc_mode = True
                self.init()
            name2id_list = [('ANALOG_DEF', 'AnalogDef'),
             ('DISCRETE_DEF', 'DiscreteDef'),
             ('FOLDER_DEF', 'FolderDef'),
             ('USER_FOLDER_DEF', 'UserFolderDef'),
             ('FOLDER_VIEW_DEF', 'FolderViewDef'),
             ('SELECT_DEF', 'SelectDef'),
             ('SELECT_DICT_DEF', 'SelectDictDef'),
             ('CALCULATION_DEF', 'CalculationDef'),
             ('PREDICTION_DEF', 'PredictionDef'),
             ('DICTIONARY_DEF', 'DictionaryDef'),
             ('PLOT_DEF', 'PlotDef'),
             ('GRAPHIC_DEF', 'GraphicDef'),
             ('NAME_FT', 'NAME'),
             ('DESCRIPTION_FT', 'DESCRIPTION'),
             ('ENG_UNITS_FT', 'ENG_UNITS'),
             ('DISPLAY_NAME_FT', 'DISPLAY_NAME'),
             ('VALUE_FORMAT_FT', 'VALUE_FORMAT'),
             ('FORMAT_RECORD_FT', 'FORMAT_RECORD'),
             ('VALUE_FT', 'VALUE'),
             ('TIME_FT', 'TIME'),
             ('MESSAGE_FT', 'MESSAGE'),
             ('RECORD_NAME_FT', 'MESSAGE'),
             ('PASSWORD_FT', 'PASSWORD'),
             ('OWNER_FT', 'OWNER'),
             ('SCHEDULE_FREQ_FT', 'SCHEDULE_FREQ'),
             ('OPC_READ_TIME', 'OPC_READ_TIME'),
             ('DB_WRITE_TIME', 'DB_WRITE_TIME')]
            var_list = [ f[0] for f in name2id_list ]
            id_list = self.names2ids([ f[1] for f in name2id_list ])
            for var, id in zip(var_list, id_list):
                setattr(self, var, id)

            self.analog_def_fields = self.list(self.ANALOG_DEF)
            self.extra_history_fields = self.names2ids(['VALUE',
             'MESSAGE',
             'OPC_READ_TIME',
             'OPC_WRITE_TIME',
             'DB_WRITE_TIME',
             'MB_READ_TIME',
             'IO_READ_TIME'])
            self.custom_history_fields = self.get_list('CustomHistoryFields', 'TAG', text=False)
            self.id_dict['DEFINITIONDEF'] = DEFINITION_DEF
            self.id_dict['ANALOGDEF'] = self.ANALOG_DEF
            self.id_dict['NAME'] = self.NAME_FT
            self.id_dict['DESCRIPTION'] = self.DESCRIPTION_FT
            self.id_dict['ENG_UNITS'] = self.ENG_UNITS_FT
            self.id_dict['VALUE_FORMAT'] = self.VALUE_FORMAT_FT
            self.id_dict['VALUE'] = self.VALUE_FT
            self.id_dict['TIME'] = self.TIME_FT
            dt_tags = self.getlist('DataTypeDef')
            rows = self.mget(dt_tags, ['DTYPE_ID', 'NUMPY_FORMAT', 'FIELD_NAMES'])
            for t, (id, format, fields) in zip(dt_tags, rows):
                id = id + 100
                try:
                    dt = numpy.dtype(format)
                except:
                    continue

                if fields is not None:
                    fields = fields.strip('')
                    if len(fields) > 0:
                        try:
                            dt.names = fields.split(',')
                        except:
                            continue

                HISTORY_DTYPES[dt] = id
                HISTORY_DTYPE_NAMES[id] = t
                HISTORY_BTYPES[id] = dt
                HISTORY_CUSTOM_DTYPES[t] = dt

            sys_dict = self.get_dict('SystemSettings', 'VALUE')
            if sys_dict == None:
                sys_dict = {}
            history_fields = sys_dict.get('HistoryFields')
            if history_fields:
                history_fields = history_fields.split(',')
                history_fields = [ fid for fid in self.names2ids(history_fields) if fid != None ]
                self.history_fields = self.extra_history_fields + history_fields
            else:
                self.history_fields = self.extra_history_fields
            self.iso_time_enabled = sys_dict.get('IsoTimeEnabled')
            if self.iso_time_enabled == '1':
                self.iso_time_enabled = True
                self.time_format = '%Y-%m-%d %H:%M:%S.%f'
                self.time_decimal = sys_dict.get('IsoTimeDecimal')
                try:
                    self.time_decimal = int(self.time_decimal)
                except:
                    self.time_decimal = 1

            else:
                self.iso_time_enabled = False
                self.time_format = sys_dict.get('TimeFormat')
                if self.time_format in (None, ''):
                    self.time_format = '%x %H:%M:%S'
                self.time_decimal = 0
            freq_units = sys_dict.get('ScheduleFreqUnits')
            if freq_units == 'ms':
                self.schedule_freq_units = 'ms'
                self.schedule_freq_base = 1
            else:
                self.schedule_freq_units = 'sec'
                self.schedule_freq_base = 1000
            self.unicode_mode = sys_dict.get('UnicodeEnabled')
            if self.unicode_mode == '1':
                self.unicode_mode = True
                self.unicode_fields = [self.DESCRIPTION_FT, self.ENG_UNITS_FT]
            else:
                self.unicode_mode = False
                self.unicode_fields = []
            # time_mode = sys_dict.get('TimeStorageMode')
            time_mode = 'utc'
            if time_mode != None:
                time_mode = time_mode.strip().lower()
            if time_mode == 'utc':
                self.utc_mode = True
            else:
                self.utc_mode = False
            tz = "Asia/Seoul"
            if tz != None and tz.strip() != '':
                self.set_timezone(tz)
            self.load_license()
            self.pg_configured = False
            self.pg_found = False
            self.pg_host = None
            self.pg_hosts = []
            self.pg_real_hosts = []
            self.pg_failed_slaves = set()
            self.pg_service_slaves = []
            self.pg_con = {}
            self.pg_cur = {}
            if no_pg:
                return True
            for tag in self.getlist('HistoryServerDef'):
                if self.get(tag, 'PROCESSING'):
                    self.pg_configured = True
                    self.pg_user = self.get(tag, 'USERNAME', text=True)
                    self._pps = 1
                    self.pg_pass = self.get(tag, 'PASSWORD', text=True)
                    self._pps = 0
                    self.pg_dbname = self.get(tag, 'DATABASE', text=True)
                    self.pg_hosts = self.getlist(tag, ['PG_HOST', 'PG_PORT'], text=True)
                    if self.is_history_service:
                        self.pg_service_slaves = list(self.pg_hosts)
                        host = self.pg_service_slaves.pop(self.pg_host_index)
                    elif self.sentinel:
                        pg_master = self.pg_master()
                        if pg_master:
                            host = pg_master
                            for i, h in enumerate(self.pg_hosts):
                                if h == host:
                                    self.pg_host_index = i

                        else:
                            return True
                    elif len(self.pg_hosts) > 0:
                        host = self.pg_hosts[0]
                        self.pg_hosts = self.pg_hosts[:1]
                        self.pg_host_index = 0
                    else:
                        return True
                    self.pg_real_hosts = list(self.pg_hosts)
                    if self.host in ('localhost', '127.0.0.1') or host[0] in ('localhost', '127.0.0.1'):
                        host = (self.host, str(host[1]))
                        self.pg_hosts[self.pg_host_index] = host
                    self.pg_con[host] = psycopg2.connect("host='%s' port=%s dbname='%s' user='%s' password='%s' connect_timeout=5" % (host[0],
                     host[1],
                     self.pg_dbname,
                     self.pg_user,
                     self.pg_pass))
                    self.pg_con[host].autocommit = True
                    self.pg_cur[host] = self.pg_con[host].cursor()
                    self.pg_host = host
                    self.pg_found = True
                    break

            if self.is_history_service:
                self.pg_open_slaves()
            return True

    def pg_open_slaves(self):
        for host in self.pg_service_slaves:
            pg_host, pg_port = host
            try:
                self.pg_con[host] = psycopg2.connect("host='%s' port=%s dbname='%s' user='%s' password='%s' connect_timeout=5" % (pg_host,
                 pg_port,
                 self.pg_dbname,
                 self.pg_user,
                 self.pg_pass))
                self.pg_con[host].autocommit = True
                self.pg_cur[host] = self.pg_con[host].cursor()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                pass

    def pg_get(self, sql, host = None, ret_errors = False):
        if host:
            pass
        elif self.sentinel:
            host = self.pg_master()
        else:
            host = self.pg_host
        try:
            self.pg_cur[host].execute(sql)
            return self.pg_cur[host].fetchall()
        except (psycopg2.OperationalError, psycopg2.InterfaceError, KeyError):
            try:
                self.pg_cur[host].close()
                self.pg_con[host].close()
            except:
                pass

            try:
                self.pg_con[host] = psycopg2.connect("host='%s' port=%s dbname='%s' user='%s' password='%s' connect_timeout=5" % (host[0],
                 host[1],
                 self.pg_dbname,
                 self.pg_user,
                 self.pg_pass))
                self.pg_con[host].autocommit = True
                self.pg_cur[host] = self.pg_con[host].cursor()
                self.pg_cur[host].execute(sql)
                return self.pg_cur[host].fetchall()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                if ret_errors:
                    return
                else:
                    return []

        except psycopg2.ProgrammingError:
            return []

    def pg_put(self, sql, host = None):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            if host:
                pg_put_hosts = [host]
                pg_master = None
            else:
                if self.is_history_service:
                    pg_master = self.pg_host
                    pg_slaves = self.pg_service_slaves
                elif self.sentinel:
                    pg_master = self.pg_master()
                    pg_slaves = self.pg_slaves()
                else:
                    pg_master = self.pg_host
                    pg_slaves = []
                pg_put_hosts = [pg_master] + pg_slaves
            status = []
            for host in pg_put_hosts:
                if host in self.pg_failed_slaves:
                    status.append((host, None))
                    continue
                try:
                    self.pg_cur[host].execute(sql)
                    status.append((host, self.pg_cur[host].rowcount))
                    continue
                except (psycopg2.OperationalError, psycopg2.InterfaceError, KeyError):
                    try:
                        self.pg_cur[host].close()
                        self.pg_con[host].close()
                    except:
                        pass

                    try:
                        self.pg_con[host] = psycopg2.connect("host='%s' port=%s dbname='%s' user='%s' password='%s' connect_timeout=5" % (host[0],
                         host[1],
                         self.pg_dbname,
                         self.pg_user,
                         self.pg_pass))
                        self.pg_con[host].autocommit = True
                        self.pg_cur[host] = self.pg_con[host].cursor()
                        self.pg_cur[host].execute(sql)
                        status.append((host, self.pg_cur[host].rowcount))
                        continue
                    except (psycopg2.OperationalError, psycopg2.InterfaceError):
                        status.append((host, None))
                        if host == pg_master:
                            return status
                        continue

            return status

    def pg_backlog_push(self, hfile, host, hid, time_data):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            key = 'pq' + pack('>I', hfile) + '%s:%s' % (host[0], host[1])
            data = pack('>I', hid) + time_data
            self.rdb.lpush(key, data)
            return

    def pg_backlog_head(self, hfile, host):
        key = 'pq' + pack('>I', hfile) + '%s:%s' % (host[0], host[1])
        data = self.rdb.lindex(key, -1)
        if data:
            hid, = unpack('>I', data[:4])
            time_data = data[4:]
            return (hid, time_data)
        else:
            return

    def pg_backlog_pop(self, hfile, host):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            key = 'pq' + pack('>I', hfile) + '%s:%s' % (host[0], host[1])
            self.rdb.rpop(key)
            return

    def pg_backlog_len(self, hfile, host):
        hfile = self.name2id(hfile)
        if hfile == None:
            return
        else:
            if isinstance(host, str):
                host = (host, '5432')
            key = 'pq' + pack('>I', hfile) + '%s:%s' % (host[0], host[1])
            return self.rdb.llen(key)

    def pg_backlog_delete(self, hfile, host):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            hfile = self.name2id(hfile)
            if hfile == None:
                return
            if isinstance(host, str):
                host = (host, '5432')
            key = 'pq' + pack('>I', hfile) + '%s:%s' % (host[0], host[1])
            self.rdb.delete(key)
            return

    def pg_table_exists(self, hfile):
        rows = self.pg_get("SELECT to_regclass('arc_%d')" % hfile)
        if rows[0][0] != None:
            return True
        else:
            return False
            return

    def pg_create_table(self, hfile):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            if self.sentinel:
                host = self.pg_master()
            else:
                host = self.pg_host
            sql = '\nCREATE TABLE arc_%d (\n  ts timestamp NOT NULL,\n  hid integer NOT NULL,\n  data bytea,\n  CONSTRAINT arc_%d_pkey PRIMARY KEY (ts, hid));\n\nCREATE INDEX hid_index_%d\n  ON arc_%d\n  USING btree\n  (hid);\n\nCREATE INDEX time_index_%d\n  ON arc_%d\n  USING btree\n  (ts);\n' % (hfile,
             hfile,
             hfile,
             hfile,
             hfile,
             hfile)
            self.pg_cur[host].execute(sql)
            return True

    def pg_drop_table(self, hfile):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            if self.sentinel:
                host = self.pg_master()
            else:
                host = self.pg_host
            sql = 'DROP TABLE arc_%d' % hfile
            self.pg_cur[host].execute(sql)
            return True

    def dbtype(self):
        return 'Toolbox'

    def ping(self):
        return 1

    def get_max_tags(self):
        n = self.get('SystemSettings', 'VALUE', 'MaxDatabaseTags')
        if True:
            n = MAX_TAGS
        else:
            n = int(n)
        return n

    def set_max_tags(self, n, init = False):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            if init:
                a = 0
            else:
                a = self.get_max_tags()
            if n <= a:
                return False
            tx = self.rdb.pipeline(transaction=False)
            for free_id in range(a, n):
                tx.rpush('free', pack('>I', free_id))

            for free_id in range(a, n):
                tx.rpush('free_hid', pack('>I', free_id))

            tx.execute()
            self.put('SystemSettings', 'VALUE', n, 'MaxDatabaseTags', add_keys=True)
            return True

    def init(self):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            self.ANALOG_DEF = None
            self.DISCRETE_DEF = None
            self.CALCULATION_DEF = None
            self.PREDICTION_DEF = None
            self.VALUE_FT = None
            self.MESSAGE_FT = None
            self.OWNER_FT = None
            self.DESCRIPTION_FT = None
            self.set_max_tags(MAX_TAGS, init=True)
            self.allocate_id()
            self.rdb.hset(pkey('rec', DEFINITION_DEF), pfld(0), pack('>I', DEFINITION_DEF))
            self.rdb.hset(pkey('rec', DEFINITION_DEF), pfld(NAME), 'DefinitionDef')
            self.rdb.hset(pkey('def', DEFINITION_DEF), pfld(NAME, DEF_DTYPE), pack('>I', DT_CHAR))
            self.rdb.hset(pkey('def', DEFINITION_DEF), pfld(NAME, DEF_ORDER), pack('>I', 0))
            self.rdb.hset('name', 'DefinitionDef'.upper(), pack('>I', DEFINITION_DEF))
            self.allocate_id()
            self.rdb.hset(pkey('rec', NAME), pfld(0), pack('>I', FIELD_DEF))
            self.rdb.hset(pkey('rec', NAME), pfld(NAME), 'NAME')
            self.rdb.hset(pkey('sdef', FIELD_DEF), 'NAME', pack('>I', NAME))
            self.rdb.hset('name', 'NAME', pack('>I', NAME))
            self.allocate_id()
            self.rdb.hset(pkey('rec', FIELD_DEF), pfld(0), pack('>I', DEFINITION_DEF))
            self.rdb.hset(pkey('rec', FIELD_DEF), pfld(NAME), 'FieldDef')
            self.rdb.hset(pkey('def', FIELD_DEF), pfld(NAME, DEF_DTYPE), pack('>I', DT_CHAR))
            self.rdb.hset(pkey('def', FIELD_DEF), pfld(NAME, DEF_ORDER), pack('>I', 0))
            self.rdb.hset(pkey('sdef', DEFINITION_DEF), 'FieldDef', pack('>I', FIELD_DEF))
            self.rdb.hset('name', 'FieldDef'.upper(), pack('>I', FIELD_DEF))
            self.upgrade()
            self.put('SystemSettings', 'VALUE', MAXa_TAGS, 'MaxDatabaseTags', add_keys=True)
            self.ANALOG_DEF = self.name2id('AnalogDef')
            self.ANALOG_DEF = self.name2id('DiscreteDef')
            self.CALCULATION_DEF = self.name2id('CalculationDef')
            self.PREDICTION_DEF = self.name2id('PredictionDef')
            self.NAME_FT = self.name2id('NAME')
            self.VALUE_FT = self.name2id('VALUE')
            self.TIME_FT = self.name2id('TIME')
            return

    def upgrade(self):
        if not self._pps_query(None, P_WRITE):
            return False
        if self.get_defid('USE_SSL', ascii=True) == 'FieldDef':
            self.put('USE_SSL', 'NAME', 'USE_TLS')
        if self.get_defid('SHIFT', ascii=True) == 'FieldDef':
            self.put('SHIFT', 'NAME', 'SHIFT_SECONDS')
        if self.get_defid('RESCHEDULE_INTERVAL', ascii=True) == 'FieldDef':
            self.put('RESCHEDULE_INTERVAL', 'NAME', 'SCHEDULE_FREQ')
        if self.get_defid('DEVICE_RECORD', ascii=True) == 'FieldDef':
            self.put('DEVICE_RECORD', 'NAME', 'DEVICE_TAG')
        if self.get_defid('TASK_RECORD', ascii=True) == 'FieldDef':
            self.put('TASK_RECORD', 'NAME', 'TASK_TAG')
        if self.get_defid('RECORD_STATUS', ascii=True) == 'FieldDef':
            self.put('RECORD_STATUS', 'NAME', 'GROUP_STATUS')
        if self.get_defid('TIME_BASIS', ascii=True) == 'FieldDef':
            self.put('TIME_BASIS', 'NAME', 'TIME_TAG')
        if self.get_defid('SCOPE', ascii=True) == 'FieldDef':
            self.put('SCOPE', 'NAME', 'SCOOTER_TAGS')
        if self.get_defid('RETENTION_DAYS', ascii=True) == 'FieldDef':
            self.put('RETENTION_DAYS', 'NAME', 'TRIM_DELAY')
        if self.get_defid('Vectors', ascii=True) == 'FolderViewDef':
            self.put('Vectors', 'NAME', 'Analogs')
            self.put('VectorView', 'NAME', 'AnalogView')
            self.put('AnalogView', 'DESCRIPTION', 'Analogs tablar view')
        self.add('DESCRIPTION', FIELD_DEF)
        self.DESCRIPTION_FT = self.name2id('DESCRIPTION')
        self.add('ENG_UNITS', FIELD_DEF)
        self.add('VALUE', FIELD_DEF)
        self.add('QUALITY', FIELD_DEF)
        self.add('TIME', FIELD_DEF)
        self.add('#VALUES', FIELD_DEF)
        self.add('RECORD', FIELD_DEF)
        self.add('SELECT_DESCRIPTION', FIELD_DEF)
        self.add('#SELECTIONS', FIELD_DEF)
        self.add('TREND_TIME', FIELD_DEF)
        self.add('TREND_VALUE', FIELD_DEF)
        self.add('TREND_QUALITY', FIELD_DEF)
        self.add('DEVICE_TAG', FIELD_DEF)
        self.add('#SCHEDULE_TIMES', FIELD_DEF)
        self.add('SCHEDULE_TIME', FIELD_DEF)
        self.add('SCHEDULE_FREQ', FIELD_DEF)
        self.add('#TAGS', FIELD_DEF)
        self.add('LOCAL_TAG', FIELD_DEF)
        self.add('REMOTE_TAG', FIELD_DEF)
        self.add('STATUS', FIELD_DEF)
        self.add('PROCESSING', FIELD_DEF)
        self.add('OPC_MODE', FIELD_DEF)
        self.add('OPC_GATE_HOST', FIELD_DEF)
        self.add('OPC_GATE_PORT', FIELD_DEF)
        self.add('OPC_HOST', FIELD_DEF)
        self.add('OPC_SERVER', FIELD_DEF)
        self.add('OPC_FUNCTION', FIELD_DEF)
        self.add('OPC_SOURCE', FIELD_DEF)
        self.add('OPC_UPDATE_RATE', FIELD_DEF)
        self.add('OPC_GROUP_SIZE', FIELD_DEF)
        self.add('OPC_TIMEOUT', FIELD_DEF)
        self.add('TIME_SOURCE', FIELD_DEF)
        self.add('RECORD_PROCESSING', FIELD_DEF)
        self.add('DEVICE_PROCESSING', FIELD_DEF)
        self.add('LIST_CHANGED', FIELD_DEF)
        self.add('REBUILD_GROUP', FIELD_DEF)
        self.add('IGNORE_QUALITY', FIELD_DEF)
        self.add('GROUP_STATUS', FIELD_DEF)
        self.add('GROUP_TIME', FIELD_DEF)
        self.add('STATUS_TIME', FIELD_DEF)
        self.add('IO_READ_TIME', FIELD_DEF)
        self.add('IO_WRITE_TIME', FIELD_DEF)
        self.add('OPC_READ_TIME', FIELD_DEF)
        self.add('OPC_WRITE_TIME', FIELD_DEF)
        self.add('DB_WRITE_TIME', FIELD_DEF)
        self.add('#MESSAGES', FIELD_DEF)
        self.add('MESSAGE', FIELD_DEF)
        self.add('LOG_MESSAGE', FIELD_DEF)
        self.add('LOG_TIME', FIELD_DEF)
        self.add('VERBOSITY_LEVEL', FIELD_DEF)
        self.add('RECORD_NAME', FIELD_DEF)
        self.add('OTHER_NAME', FIELD_DEF)
        self.add('#RECORDS', FIELD_DEF)
        self.add('FORMAT_RECORD', FIELD_DEF)
        self.add('VALUE_FORMAT', FIELD_DEF)
        self.add('FIELD_SIZE', FIELD_DEF)
        self.add('DECIMAL_SIZE', FIELD_DEF)
        self.add('NUMBER_ROWS', FIELD_DEF)
        self.add('NUMBER_COLUMNS', FIELD_DEF)
        self.add('TAGS_PER_PLOT', FIELD_DEF)
        self.add('TAGS_PER_XY', FIELD_DEF)
        self.add('START_TAG_INDEX', FIELD_DEF)
        self.add('CHART_TYPE', FIELD_DEF)
        self.add('CHART_LEGEND', FIELD_DEF)
        self.add('GRID_COLOR', FIELD_DEF)
        self.add('BACKGROUND_COLOR', FIELD_DEF)
        self.add('GRADIENT_COLOR', FIELD_DEF)
        self.add('GRADIENT_FILL', FIELD_DEF)
        self.add('REPEAT_COLORS', FIELD_DEF)
        self.add('DUAL_AXIS', FIELD_DEF)
        self.add('START_TIME', FIELD_DEF)
        self.add('END_TIME', FIELD_DEF)
        self.add('LIVE_TIMESPAN', FIELD_DEF)
        self.add('SAVE_TIME', FIELD_DEF)
        self.add('SHOW_PLOT', FIELD_DEF)
        self.add('SHOW_LEGEND', FIELD_DEF)
        self.add('SHOW_TIMELINE', FIELD_DEF)
        self.add('TAG', FIELD_DEF)
        self.add('TAG_TEXT', FIELD_DEF)
        self.add('TAG_ID', FIELD_DEF)
        self.add('AUTOSCALE', FIELD_DEF)
        self.add('LOW_SCALE', FIELD_DEF)
        self.add('HIGH_SCALE', FIELD_DEF)
        self.add('LINE_COLOR', FIELD_DEF)
        self.add('LINE_STYLE', FIELD_DEF)
        self.add('LINE_SIZE', FIELD_DEF)
        self.add('MARKER_COLOR', FIELD_DEF)
        self.add('MARKER_STYLE', FIELD_DEF)
        self.add('MARKER_SIZE', FIELD_DEF)
        self.add('BORDER_SIZE', FIELD_DEF)
        self.add('ALPHA', FIELD_DEF)
        self.add('FUNCTION', FIELD_DEF)
        self.add('INTERVAL', FIELD_DEF)
        self.add('SHIFT_SECONDS', FIELD_DEF)
        self.add('LIMIT_COLOR', FIELD_DEF)
        self.add('LIMIT_STYLE', FIELD_DEF)
        self.add('LIMIT_SIZE', FIELD_DEF)
        self.add('LIMIT_LOW', FIELD_DEF)
        self.add('LIMIT_HIGH', FIELD_DEF)
        self.add('SCALE_GROUP', FIELD_DEF)
        self.add('PLOT_NUMBER', FIELD_DEF)
        self.add('#SCOOTERS', FIELD_DEF)
        self.add('SCOOTER_START', FIELD_DEF)
        self.add('SCOOTER_END', FIELD_DEF)
        self.add('SCOOTER_TAGS', FIELD_DEF)
        self.add('SCOOTER_FUNCTIONS', FIELD_DEF)
        self.add('CATEGORY', FIELD_DEF)
        self.add('ANNOTATION_TEXT', FIELD_DEF)
        self.add('#PLOTS', FIELD_DEF)
        self.add('PLOT_TITLE', FIELD_DEF)
        self.add('#PARAMETERS', FIELD_DEF)
        self.add('ACCESS', FIELD_DEF)
        self.add('DISPLAY_NAME', FIELD_DEF)
        self.add('#COLUMNS', FIELD_DEF)
        self.add('COLUMN_FIELD', FIELD_DEF)
        self.add('#SORTS', FIELD_DEF)
        self.add('SORT_FIELD', FIELD_DEF)
        self.add('SORT_DIRECTION', FIELD_DEF)
        self.add('#SEARCHES', FIELD_DEF)
        self.add('SEARCH_FIELD', FIELD_DEF)
        self.add('SEARCH_OPERATOR', FIELD_DEF)
        self.add('SEARCH_VALUE', FIELD_DEF)
        self.add('VIEW_RECORD', FIELD_DEF)
        self.add('DTYPE_ID', FIELD_DEF)
        self.add('NUMPY_FORMAT', FIELD_DEF)
        self.add('FIELD_NAMES', FIELD_DEF)
        self.add('CALC_MODE', FIELD_DEF)
        self.add('CALC_TYPE', FIELD_DEF)
        self.add('TIME_TAG', FIELD_DEF)
        self.add('CALC_START', FIELD_DEF)
        self.add('CALC_INTERVAL', FIELD_DEF)
        self.add('AGG_FUNCTION', FIELD_DEF)
        self.add('AGGREGATE_ID', FIELD_DEF)
        self.add('CODE', FIELD_DEF)
        self.add('COMPILED_CODE', FIELD_DEF)
        self.add('COMPILED_TIME', FIELD_DEF)
        self.add('TAG_FUNCTION', FIELD_DEF)
        self.add('TAG_FILL', FIELD_DEF)
        self.add('TAG_NULL', FIELD_DEF)
        self.add('#ARRAYS', FIELD_DEF)
        self.add('ARRAY', FIELD_DEF)
        self.add('TASK_PROCESSING', FIELD_DEF)
        self.add('GROUP_PROCESSING', FIELD_DEF)
        self.add('CALC_TASK', FIELD_DEF)
        self.add('CALC_TAG', FIELD_DEF)
        self.add('OUTPUT_TAG', FIELD_DEF)
        self.add('DATA', FIELD_DEF)
        self.add('URL', FIELD_DEF)
        self.add('TASK_TAG', FIELD_DEF)
        self.add('#COS_FIELDS', FIELD_DEF)
        self.add('COS_FIELD', FIELD_DEF)
        self.add('ACTIVATION_FIELD', FIELD_DEF)
        self.add('SOURCE_TYPE', FIELD_DEF)
        self.add('SOURCE_HOST', FIELD_DEF)
        self.add('SOURCE_PORT', FIELD_DEF)
        self.add('DATA_SOURCE', FIELD_DEF)
        self.add('IO_HOST', FIELD_DEF)
        self.add('IO_PORT', FIELD_DEF)
        self.add('IO_ENDIAN', FIELD_DEF)
        self.add('IO_GROUP_SIZE', FIELD_DEF)
        self.add('IO_TIMEOUT', FIELD_DEF)
        self.add('DATA_TYPE', FIELD_DEF)
        self.add('#OUTPUT_LINES', FIELD_DEF)
        self.add('OUTPUT_LINE', FIELD_DEF)
        self.add('#CONSTANTS', FIELD_DEF)
        self.add('CONSTANT_DESCRIPTION', FIELD_DEF)
        self.add('CONSTANT_VALUE', FIELD_DEF)
        self.add('#INPUTS', FIELD_DEF)
        self.add('INPUT_DESCRIPTION', FIELD_DEF)
        self.add('INPUT_TAG', FIELD_DEF)
        self.add('#COEFFICIENTS', FIELD_DEF)
        self.add('#INDEPENDENTS', FIELD_DEF)
        self.add('#DEPENDENTS', FIELD_DEF)
        self.add('IND_NAME', FIELD_DEF)
        self.add('DEP_NAME', FIELD_DEF)
        self.add('IND_UNITS', FIELD_DEF)
        self.add('DEP_UNITS', FIELD_DEF)
        self.add('IND_DESCRIPTION', FIELD_DEF)
        self.add('DEP_DESCRIPTION', FIELD_DEF)
        self.add('RAW_RESPONSE', FIELD_DEF)
        self.add('MOD_RESPONSE', FIELD_DEF)
        self.add('TYPICAL_MOVE', FIELD_DEF)
        self.add('GAINS', FIELD_DEF)
        self.add('SS_TIME', FIELD_DEF)
        self.add('#OPERATIONS', FIELD_DEF)
        self.add('IND_INDEX', FIELD_DEF)
        self.add('DEP_INDEX', FIELD_DEF)
        self.add('IND_POSITION', FIELD_DEF)
        self.add('DEP_POSITION', FIELD_DEF)
        self.add('IND_SIZE', FIELD_DEF)
        self.add('DEP_SIZE', FIELD_DEF)
        self.add('#MODELS', FIELD_DEF)
        self.add('MODEL', FIELD_DEF)
        self.add('#ANNOTATIONS', FIELD_DEF)
        self.add('SCALE_MODE', FIELD_DEF)
        self.add('#SLICES', FIELD_DEF)
        self.add('SLICE_ID', FIELD_DEF)
        self.add('TAGS', FIELD_DEF)
        self.add('LAST_RUN', FIELD_DEF)
        self.add('MAX_INTERPOLATE', FIELD_DEF)
        self.add('SAMPLE_TIME', FIELD_DEF)
        self.add('IND_ACTIVE', FIELD_DEF)
        self.add('DEP_ACTIVE', FIELD_DEF)
        self.add('RAMP_INDICATOR', FIELD_DEF)
        self.add('#CASES', FIELD_DEF)
        self.add('TTSS', FIELD_DEF)
        self.add('NCOEFF', FIELD_DEF)
        self.add('SMOOTH', FIELD_DEF)
        self.add('STEADY', FIELD_DEF)
        self.add('#REPORT_LINES', FIELD_DEF)
        self.add('REPORT_LINE', FIELD_DEF)
        self.add('MODEL_NAME', FIELD_DEF)
        self.add('PRED_ERR_FILTER', FIELD_DEF)
        self.add('#BAD_SLICES', FIELD_DEF)
        self.add('BAD_ACTIVE', FIELD_DEF)
        self.add('BAD_TAG', FIELD_DEF)
        self.add('BAD_START', FIELD_DEF)
        self.add('BAD_END', FIELD_DEF)
        self.add('BAD_ANNOTATION', FIELD_DEF)
        self.add('#CASE_SLICES', FIELD_DEF)
        self.add('CASE_ACTIVE', FIELD_DEF)
        self.add('CASE_TAG', FIELD_DEF)
        self.add('CASE_START', FIELD_DEF)
        self.add('CASE_END', FIELD_DEF)
        self.add('CASE_ANNOTATION', FIELD_DEF)
        self.add('FUTURE_SAMPLES', FIELD_DEF)
        self.add('NUM_SAMPLES', FIELD_DEF)
        self.add('X_TAG', FIELD_DEF)
        self.add('Y_TAG', FIELD_DEF)
        self.add('X_SCALE_LOW', FIELD_DEF)
        self.add('X_SCALE_HIGH', FIELD_DEF)
        self.add('Y_SCALE_LOW', FIELD_DEF)
        self.add('Y_SCALE_HIGH', FIELD_DEF)
        self.add('TRANSFORMATION', FIELD_DEF)
        self.add('PEN_COLOR', FIELD_DEF)
        self.add('PEN_SIZE', FIELD_DEF)
        self.add('TRANS_SCALE_LOW', FIELD_DEF)
        self.add('TRANS_SCALE_HIGH', FIELD_DEF)
        self.add('LIN_ALPHA', FIELD_DEF)
        self.add('LIN_LOW', FIELD_DEF)
        self.add('LIN_HIGH', FIELD_DEF)
        self.add('LIN_OFFSET', FIELD_DEF)
        self.add('PAR_ALPHA', FIELD_DEF)
        self.add('PAR_LOW', FIELD_DEF)
        self.add('PAR_HIGH', FIELD_DEF)
        self.add('PAR_OFFSET', FIELD_DEF)
        self.add('#OPCHAR_POINTS', FIELD_DEF)
        self.add('OPCHAR_OUT', FIELD_DEF)
        self.add('OPCHAR_IN', FIELD_DEF)
        self.add('#PWLIN_POINTS', FIELD_DEF)
        self.add('PWLIN_X', FIELD_DEF)
        self.add('PWLIN_Y', FIELD_DEF)
        self.add('WRITE_SCHEDULE', FIELD_DEF)
        self.add('WRITE_FREQ', FIELD_DEF)
        self.add('COMPRESS_SCHEDULE', FIELD_DEF)
        self.add('COMPRESS_FREQ', FIELD_DEF)
        self.add('TRIM_PROCESSING', FIELD_DEF)
        self.add('TRIM_DELAY', FIELD_DEF)
        self.add('LAST_TRIM_POINT', FIELD_DEF)
        self.add('LAST_COMPRESS_POINT', FIELD_DEF)
        self.add('RESAMPLE_PROCESSING', FIELD_DEF)
        self.add('RESAMPLE_FUNCTION', FIELD_DEF)
        self.add('RESAMPLE_FREQ', FIELD_DEF)
        self.add('RESAMPLE_DELAY', FIELD_DEF)
        self.add('LAST_RESAMPLE_POINT', FIELD_DEF)
        self.add('MODBUS_HOST', FIELD_DEF)
        self.add('MODBUS_PORT', FIELD_DEF)
        self.add('SLAVE_ID', FIELD_DEF)
        self.add('FUNCTION_CODE', FIELD_DEF)
        self.add('START_REGISTER', FIELD_DEF)
        self.add('REGISTER_TABLE', FIELD_DEF)
        self.add('DATA_FORMAT', FIELD_DEF)
        self.add('REGISTER', FIELD_DEF)
        self.add('SCALING_FACTOR', FIELD_DEF)
        self.add('MB_READ_TIME', FIELD_DEF)
        self.add('SERVER_ADDRESS', FIELD_DEF)
        self.add('DEV_VALUE', FIELD_DEF)
        self.add('DEV_MAX_TIME', FIELD_DEF)
        self.add('STORE_BAD', FIELD_DEF)
        self.add('BAD_VALUE', FIELD_DEF)
        self.add('FULL_NAME', FIELD_DEF)
        self.add('PASSWORD', FIELD_DEF)
        self.add('BASE_POLICY', FIELD_DEF)
        self.add('BASE_ROLE', FIELD_DEF)
        self.add('#RULES', FIELD_DEF)
        self.add('READ', FIELD_DEF)
        self.add('WRITE', FIELD_DEF)
        self.add('CREATE', FIELD_DEF)
        self.add('DELETE', FIELD_DEF)
        self.add('#SCRIPTS', FIELD_DEF)
        self.add('SCRIPT', FIELD_DEF)
        self.add('REMOTE_HOST', FIELD_DEF)
        self.add('REMOTE_PORT', FIELD_DEF)
        self.add('#USERS', FIELD_DEF)
        self.add('OWNER', FIELD_DEF)
        self.add('MENU_TREE', FIELD_DEF)
        self.add('SCOPE', FIELD_DEF)
        self.add('TEMPLATE_FOLDER', FIELD_DEF)
        self.add('ICON', FIELD_DEF)
        self.add('#ATTRIBUTES', FIELD_DEF)
        self.add('FILE_NAME', FIELD_DEF)
        self.add('TAG_EXPRESSION', FIELD_DEF)
        self.add('RUN_ON_OPEN', FIELD_DEF)
        self.add('SEARCH_ONLY', FIELD_DEF)
        self.add('STORE_ONLY_CHANGES', FIELD_DEF)
        self.add('#HOSTS', FIELD_DEF)
        self.add('PG_HOST', FIELD_DEF)
        self.add('PG_PORT', FIELD_DEF)
        self.add('USERNAME', FIELD_DEF)
        self.add('DATABASE', FIELD_DEF)
        self.add('ARCHIVE_PROCESSING', FIELD_DEF)
        self.add('ARCHIVE_SERVER', FIELD_DEF)
        self.add('ARCHIVE_DELAY', FIELD_DEF)
        self.add('LAST_ARCHIVE_POINT', FIELD_DEF)
        self.add('SMTP_SERVER', FIELD_DEF)
        self.add('HOLD_OFF_TIME', FIELD_DEF)
        self.add('EMAIL_ADDRESS', FIELD_DEF)
        self.add('USE_TLS', FIELD_DEF)
        self.add('NOTIFY_TIME', FIELD_DEF)
        self.add('ALARM_STATE', FIELD_DEF)
        self.add('MESSAGE_TEXT', FIELD_DEF)
        self.add('USER', FIELD_DEF)
        self.add('LDAP_HOST', FIELD_DEF)
        self.add('LDAP_PORT', FIELD_DEF)
        self.add('BIND_DN', FIELD_DEF)
        self.add('LDAP_SERVER', FIELD_DEF)
        self.add('GRADIENT_DIRECTION', FIELD_DEF)
        self.add('GRADIENT_COLOR1', FIELD_DEF)
        self.add('GRADIENT_COLOR2', FIELD_DEF)
        self.add('ZOOM_LEVEL', FIELD_DEF)
        self.add('POPULATE_FUNCTION', FIELD_DEF)
        self.add('POST_FUNCTION', FIELD_DEF)
        self.add('#COLUMNS', FIELD_DEF)
        self.add('COLUMN_LABEL', FIELD_DEF)
        self.add('COLUMN_WIDTH', FIELD_DEF)
        self.add('#SEARCHES', FIELD_DEF)
        self.add('SEARCH_LABEL', FIELD_DEF)
        self.add('SEARCH_WIDGET', FIELD_DEF)
        self.add('SEARCH_FORMAT', FIELD_DEF)
        self.add('SEARCH_FUNCTION', FIELD_DEF)
        self.add('SEARCH_WIDTH', FIELD_DEF)
        self.add('#ACTIONS', FIELD_DEF)
        self.add('ACTION_LABEL', FIELD_DEF)
        self.add('ACTION_FUNCTION', FIELD_DEF)
        self.add('SelectDef', DEFINITION_DEF)
        self.putdef('SelectDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('SelectDef', '#SELECTIONS', dtype=DT_LIST, order=2)
        self.putdef('SelectDef', 'SELECT_DESCRIPTION', dtype=DT_CHAR, repeat='#SELECTIONS', order=3)
        self.deldef('SelectDef', '1ST_SELECTION_VALUE')
        self.add('QUALITY-STATES', 'SelectDef')
        self.put('QUALITY-STATES', '#SELECTIONS', 4)
        self.put('QUALITY-STATES', 'SELECT_DESCRIPTION', 'None', 1)
        self.put('QUALITY-STATES', 'SELECT_DESCRIPTION', 'Good', 2)
        self.put('QUALITY-STATES', 'SELECT_DESCRIPTION', 'Bad', 3)
        self.put('QUALITY-STATES', 'SELECT_DESCRIPTION', 'Error', 4)
        self.add('WRITE-STATES', 'SelectDef')
        self.put('WRITE-STATES', '#SELECTIONS', 3)
        self.put('WRITE-STATES', 'SELECT_DESCRIPTION', 'None', 1)
        self.put('WRITE-STATES', 'SELECT_DESCRIPTION', 'Success', 2)
        self.put('WRITE-STATES', 'SELECT_DESCRIPTION', 'Error', 3)
        self.add('OFF/ON', 'SelectDef')
        self.put('OFF/ON', '#SELECTIONS', 2)
        self.put('OFF/ON', 'SELECT_DESCRIPTION', 'OFF', 1)
        self.put('OFF/ON', 'SELECT_DESCRIPTION', 'ON', 2)
        self.add('NO/YES', 'SelectDef')
        self.put('NO/YES', '#SELECTIONS', 2)
        self.put('NO/YES', 'SELECT_DESCRIPTION', 'NO', 1)
        self.put('NO/YES', 'SELECT_DESCRIPTION', 'YES', 2)
        self.put('DCOM/OPEN', 'NAME', 'OPC-MODES')
        self.add('OPC-MODES', 'SelectDef')
        self.put('OPC-MODES', '#SELECTIONS', 3)
        self.put('OPC-MODES', 'SELECT_DESCRIPTION', 'DCOM', 1)
        self.put('OPC-MODES', 'SELECT_DESCRIPTION', 'Pyro', 2)
        self.put('OPC-MODES', 'SELECT_DESCRIPTION', 'RPyC', 3)
        self.add('VERBOSITY-LEVELS', 'SelectDef')
        self.put('VERBOSITY-LEVELS', '#SELECTIONS', 5)
        self.put('VERBOSITY-LEVELS', 'SELECT_DESCRIPTION', 'General', 1)
        self.put('VERBOSITY-LEVELS', 'SELECT_DESCRIPTION', 'Error', 2)
        self.put('VERBOSITY-LEVELS', 'SELECT_DESCRIPTION', 'Warning', 3)
        self.put('VERBOSITY-LEVELS', 'SELECT_DESCRIPTION', 'Information', 4)
        self.put('VERBOSITY-LEVELS', 'SELECT_DESCRIPTION', 'Verbose', 5)
        self.add('TIME-SOURCES', 'SelectDef')
        self.put('TIME-SOURCES', '#SELECTIONS', 3)
        self.put('TIME-SOURCES', 'SELECT_DESCRIPTION', 'Request Time', 1)
        self.put('TIME-SOURCES', 'SELECT_DESCRIPTION', 'Response Time', 2)
        self.put('TIME-SOURCES', 'SELECT_DESCRIPTION', 'OPC Server', 3)
        self.add('CHART-TYPES', 'SelectDef')
        self.put('CHART-TYPES', '#SELECTIONS', 3)
        self.put('CHART-TYPES', 'SELECT_DESCRIPTION', 'Trend', 1)
        self.put('CHART-TYPES', 'SELECT_DESCRIPTION', 'XY', 2)
        self.put('CHART-TYPES', 'SELECT_DESCRIPTION', 'Histogram', 3)
        if self.add('LOGBOOK-CATEGORIES', 'SelectDef'):
            self.put('LOGBOOK-CATEGORIES', '#SELECTIONS', 1)
            self.put('LOGBOOK-CATEGORIES', 'SELECT_DESCRIPTION', 'None', 1)
        self.add('CALC-TYPES', 'SelectDef')
        self.put('CALC-TYPES', '#SELECTIONS', 3)
        self.put('CALC-TYPES', 'SELECT_DESCRIPTION', 'Expression', 1)
        self.put('CALC-TYPES', 'SELECT_DESCRIPTION', 'Return Value', 2)
        self.put('CALC-TYPES', 'SELECT_DESCRIPTION', 'Return Array', 3)
        self.add('OPC-FUNCTIONS', 'SelectDef')
        self.put('OPC-FUNCTIONS', '#SELECTIONS', 2)
        self.put('OPC-FUNCTIONS', 'SELECT_DESCRIPTION', 'Synchronous', 1)
        self.put('OPC-FUNCTIONS', 'SELECT_DESCRIPTION', 'Asynchronous', 2)
        self.add('OPC-SOURCES', 'SelectDef')
        self.put('OPC-SOURCES', '#SELECTIONS', 3)
        self.put('OPC-SOURCES', 'SELECT_DESCRIPTION', 'Device', 1)
        self.put('OPC-SOURCES', 'SELECT_DESCRIPTION', 'Cache', 2)
        self.put('OPC-SOURCES', 'SELECT_DESCRIPTION', 'Hybrid', 3)
        self.add('IO-DATA-TYPES', 'SelectDef')
        self.put('IO-DATA-TYPES', '#SELECTIONS', 3)
        self.put('IO-DATA-TYPES', 'SELECT_DESCRIPTION', 'Float', 1)
        self.put('IO-DATA-TYPES', 'SELECT_DESCRIPTION', 'Integer', 2)
        self.put('IO-DATA-TYPES', 'SELECT_DESCRIPTION', 'Character', 3)
        self.add('DATA-SOURCE-TYPES', 'SelectDef')
        self.put('DATA-SOURCE-TYPES', '#SELECTIONS', 2)
        self.put('DATA-SOURCE-TYPES', 'SELECT_DESCRIPTION', 'Toolbox', 1)
        self.put('DATA-SOURCE-TYPES', 'SELECT_DESCRIPTION', 'PI', 2)
        self.add('ENDIAN-TYPES', 'SelectDef')
        self.put('ENDIAN-TYPES', '#SELECTIONS', 2)
        self.put('ENDIAN-TYPES', 'SELECT_DESCRIPTION', 'Little Endian', 1)
        self.put('ENDIAN-TYPES', 'SELECT_DESCRIPTION', 'Big Endian', 2)
        self.add('X-TRANSFORM-TYPES', 'SelectDef')
        self.put('X-TRANSFORM-TYPES', '#SELECTIONS', 5)
        self.put('X-TRANSFORM-TYPES', 'SELECT_DESCRIPTION', 'None', 1)
        self.put('X-TRANSFORM-TYPES', 'SELECT_DESCRIPTION', 'Linear', 2)
        self.put('X-TRANSFORM-TYPES', 'SELECT_DESCRIPTION', 'Parabolic', 3)
        self.put('X-TRANSFORM-TYPES', 'SELECT_DESCRIPTION', 'Output Char', 4)
        self.put('X-TRANSFORM-TYPES', 'SELECT_DESCRIPTION', 'PW Linear', 5)
        self.add('X-PEN-COLORS', 'SelectDef')
        self.put('X-PEN-COLORS', '#SELECTIONS', 3)
        self.put('X-PEN-COLORS', 'SELECT_DESCRIPTION', 'Blue', 1)
        self.put('X-PEN-COLORS', 'SELECT_DESCRIPTION', 'Green', 2)
        self.put('X-PEN-COLORS', 'SELECT_DESCRIPTION', 'Red', 3)
        self.add('X-PEN-SIZES', 'SelectDef')
        self.put('X-PEN-SIZES', '#SELECTIONS', 3)
        self.put('X-PEN-SIZES', 'SELECT_DESCRIPTION', '1', 1)
        self.put('X-PEN-SIZES', 'SELECT_DESCRIPTION', '2', 2)
        self.put('X-PEN-SIZES', 'SELECT_DESCRIPTION', '3', 3)
        self.add('MODEL-SCALE-MODES', 'SelectDef')
        self.put('MODEL-SCALE-MODES', '#SELECTIONS', 2)
        self.put('MODEL-SCALE-MODES', 'SELECT_DESCRIPTION', 'Auto', 1)
        self.put('MODEL-SCALE-MODES', 'SELECT_DESCRIPTION', 'Typical Moves', 2)
        self.add('CALC-MODES', 'SelectDef')
        self.put('CALC-MODES', '#SELECTIONS', 2)
        self.put('CALC-MODES', 'SELECT_DESCRIPTION', 'On Demand', 1)
        self.put('CALC-MODES', 'SELECT_DESCRIPTION', 'Precalculate', 2)
        self.add('HORIZONTAL/VERTICAL', 'SelectDef')
        self.put('HORIZONTAL/VERTICAL', '#SELECTIONS', 2)
        self.put('HORIZONTAL/VERTICAL', 'SELECT_DESCRIPTION', 'Horizontal', 1)
        self.put('HORIZONTAL/VERTICAL', 'SELECT_DESCRIPTION', 'Vertical', 2)
        MPL_LEGEND_LOCATIONS = ['none',
         'upper right',
         'upper left',
         'lower left',
         'lower right',
         'right',
         'center left',
         'center right',
         'lower center',
         'upper center',
         'center']
        self.add('CHART-LEGENDS', 'SelectDef')
        self.put('CHART-LEGENDS', '#SELECTIONS', len(MPL_LEGEND_LOCATIONS))
        for i, loc_text in enumerate(MPL_LEGEND_LOCATIONS):
            self.put('CHART-LEGENDS', 'SELECT_DESCRIPTION', loc_text, i + 1)

        self.add('MODBUS-FORMATS', 'SelectDef')
        self.put('MODBUS-FORMATS', '#SELECTIONS', 3)
        self.put('MODBUS-FORMATS', 'SELECT_DESCRIPTION', '16-bit Integer', 1)
        self.put('MODBUS-FORMATS', 'SELECT_DESCRIPTION', '32-bit IEEE Float', 2)
        self.put('MODBUS-FORMATS', 'SELECT_DESCRIPTION', 'Packed Boolean', 3)
        self.add('MODBUS-FORMATS2', 'SelectDef')
        self.put('MODBUS-FORMATS2', '#SELECTIONS', 5)
        self.put('MODBUS-FORMATS2', 'SELECT_DESCRIPTION', 'int16', 1)
        self.put('MODBUS-FORMATS2', 'SELECT_DESCRIPTION', 'int32', 2)
        self.put('MODBUS-FORMATS2', 'SELECT_DESCRIPTION', 'int64', 3)
        self.put('MODBUS-FORMATS2', 'SELECT_DESCRIPTION', 'float32', 4)
        self.put('MODBUS-FORMATS2', 'SELECT_DESCRIPTION', 'float64', 5)
        self.add('MODBUS-TABLES', 'SelectDef')
        self.put('MODBUS-TABLES', '#SELECTIONS', 4)
        self.put('MODBUS-TABLES', 'SELECT_DESCRIPTION', 'Coil Outputs (00000)', 1)
        self.put('MODBUS-TABLES', 'SELECT_DESCRIPTION', 'Digital Inputs (10000)', 2)
        self.put('MODBUS-TABLES', 'SELECT_DESCRIPTION', 'Analog Inputs (30000)', 3)
        self.put('MODBUS-TABLES', 'SELECT_DESCRIPTION', 'Holding Registers (40000)', 4)
        self.add('USER-BASE-POLICIES', 'SelectDef')
        self.put('USER-BASE-POLICIES', '#SELECTIONS', 2)
        self.put('USER-BASE-POLICIES', 'SELECT_DESCRIPTION', 'Read only', 1)
        self.put('USER-BASE-POLICIES', 'SELECT_DESCRIPTION', 'Full access', 2)
        self.add('SCOPE-TYPES', 'SelectDef')
        self.put('SCOPE-TYPES', '#SELECTIONS', 2)
        self.put('SCOPE-TYPES', 'SELECT_DESCRIPTION', 'Owner', 1)
        self.put('SCOPE-TYPES', 'SELECT_DESCRIPTION', 'All', 2)
        self.add('SEARCH-WIDGETS', 'SelectDef')
        self.put('SEARCH-WIDGETS', '#SELECTIONS', 4)
        self.put('SEARCH-WIDGETS', 'SELECT_DESCRIPTION', 'Text box', 1)
        self.put('SEARCH-WIDGETS', 'SELECT_DESCRIPTION', 'Drop down', 2)
        self.put('SEARCH-WIDGETS', 'SELECT_DESCRIPTION', 'Combo box', 3)
        self.put('SEARCH-WIDGETS', 'SELECT_DESCRIPTION', 'Time control', 4)
        self.add('SelectDictDef', DEFINITION_DEF)
        self.putdef('SelectDictDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('SelectDictDef', '#SELECTIONS', dtype=DT_DICTIONARY, order=2)
        self.putdef('SelectDictDef', 'SELECT_DESCRIPTION', dtype=DT_CHAR, repeat='#SELECTIONS', order=3)
        self.add('DataTypeDef', DEFINITION_DEF)
        self.putdef('DataTypeDef', 'DTYPE_ID', dtype=DT_INTEGER, order=1)
        self.putdef('DataTypeDef', 'NUMPY_FORMAT', dtype=DT_CHAR, order=2)
        self.putdef('DataTypeDef', 'FIELD_NAMES', dtype=DT_CHAR, order=3)
        self.add('str100', 'DataTypeDef')
        self.put('str100', 'DTYPE_ID', 1)
        self.put('str100', 'NUMPY_FORMAT', 'S100')
        id = 100 + 1
        dt = numpy.dtype('S100')
        HISTORY_DTYPES[dt] = id
        HISTORY_DTYPE_NAMES[id] = 'str100'
        HISTORY_BTYPES[id] = dt
        HISTORY_CUSTOM_DTYPES['str100'] = dt
        self.add('AggFunctionDef', DEFINITION_DEF)
        self.putdef('AggFunctionDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('AggFunctionDef', 'AGGREGATE_ID', dtype=DT_INTEGER, order=2)
        self.putdef('AggFunctionDef', 'CODE', dtype=DT_CHAR, order=3)
        for i, a in enumerate(['first',
         'last',
         'sum',
         'count',
         'average',
         'median',
         'min',
         'max',
         'range',
         'stdev',
         'variance',
         'delta']):
            self.add(a, 'AggFunctionDef')
            self.put(a, 'AGGREGATE_ID', i + 1)
            self.put(a, 'CODE', '# Built in function')

        old_fields = []
        for t in self.getlist('HistoryServerDef'):
            pg_host = self.get(t, 'PG_HOST')
            pg_port = self.get(t, 'PG_PORT')
            old_fields.append((t, pg_host, pg_port))

        self.deldef('HistoryServerDef', 'PG_HOST')
        self.deldef('HistoryServerDef', 'PG_PORT')
        self.add('HistoryServerDef', DEFINITION_DEF)
        self.putdef('HistoryServerDef', 'PROCESSING', dtype=DT_INTEGER, default=0, format='OFF/ON', order=1)
        self.putdef('HistoryServerDef', 'USERNAME', dtype=DT_CHAR, order=4)
        self.putdef('HistoryServerDef', 'PASSWORD', dtype=DT_CHAR, order=5)
        self.putdef('HistoryServerDef', 'DATABASE', dtype=DT_CHAR, order=6)
        self.putdef('HistoryServerDef', '#HOSTS', dtype=DT_LIST, order=7)
        self.putdef('HistoryServerDef', 'PG_HOST', dtype=DT_CHAR, repeat='#HOSTS', order=8)
        self.putdef('HistoryServerDef', 'PG_PORT', dtype=DT_CHAR, repeat='#HOSTS', order=9)
        for t, pg_host, pg_port in old_fields:
            if pg_host:
                self.append_rows(t, '#HOSTS', [(pg_host, pg_port)])

        if self.add('ArchiveServer1', 'HistoryServerDef'):
            self.put('ArchiveServer1', 'USERNAMEpostgres')
            self.put('ArchiveServer1', 'DATABASE', 'cci')
            self.append_rows('ArchiveServer1', '#HOSTS', [('127.0.0.1', '5432')])
        self.add('HistoryFileDef', DEFINITION_DEF)
        self.putdef('HistoryFileDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('HistoryFileDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=3, reschedule='SCHEDULE_FREQ')
        self.putdef('HistoryFileDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, default=3600, order=4)
        self.putdef('HistoryFileDef', 'RESAMPLE_PROCESSING', dtype=DT_INTEGER, default=0, format='OFF/ON', order=5)
        self.putdef('HistoryFileDef', 'RESAMPLE_DELAY', dtype=DT_FLOAT, default=30.0, order=6)
        self.putdef('HistoryFileDef', 'RESAMPLE_FUNCTION', dtype=DT_RECORD, default='first', skey='AggFunctionDef', order=7)
        self.putdef('HistoryFileDef', 'RESAMPLE_FREQ', dtype=DT_INTEGER, default=60, order=8)
        self.putdef('HistoryFileDef', 'ARCHIVE_PROCESSING', dtype=DT_INTEGER, default=0, format='OFF/ON', order=9)
        self.putdef('HistoryFileDef', 'ARCHIVE_SERVER', dtype=DT_RECORD, skey='HistoryServerDef', order=10)
        self.putdef('HistoryFileDef', 'ARCHIVE_DELAY', dtype=DT_FLOAT, default=365.0, order=11)
        self.putdef('HistoryFileDef', 'TRIM_PROCESSING', dtype=DT_INTEGER, default=0, format='OFF/ON', order=12)
        self.putdef('HistoryFileDef', 'TRIM_DELAY', dtype=DT_FLOAT, default=9999.0, order=13)
        self.putdef('HistoryFileDef', 'STORE_ONLY_CHANGES', dtype=DT_INTEGER, default=0, format='NO/YES', order=14)
        self.putdef('HistoryFileDef', 'LAST_COMPRESS_POINT', dtype=DT_TIMESTAMP, readonly=True, order=16)
        self.putdef('HistoryFileDef', 'LAST_RESAMPLE_POINT', dtype=DT_TIMESTAMP, readonly=True, order=17)
        self.putdef('HistoryFileDef', 'LAST_ARCHIVE_POINT', dtype=DT_TIMESTAMP, readonly=True, order=18)
        self.putdef('HistoryFileDef', 'LAST_TRIM_POINT', dtype=DT_TIMESTAMP, readonly=True, order=19)
        self.putdef('HistoryFileDef', 'MESSAGE', dtype=DT_CHAR, chain='TIME', readonly=True, order=20)
        self.putdef('HistoryFileDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=21)
        self.deldef('HistoryFileDef', 'THROTTLE_MSEC')
        if self.add('HistoryFile1', 'HistoryFileDef'):
            self.put('HistoryFile1', 'SCHEDULE_TIME', '01/01/2000 00:00:00')
            self.put('HistoryFile1', 'ARCHIVE_SERVER', 'ArchiveServer1')
        self.add('AnalogDef', DEFINITION_DEF)
        self.putdef('AnalogDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('AnalogDef', 'ENG_UNITS', dtype=DT_CHAR, order=2)
        self.putdef('AnalogDef', 'VALUE_FORMAT', dtype=DT_INTEGER, default=-1, order=2)
        self.putdef('AnalogDef', 'VALUE', dtype=DT_FLOAT, chain='TIME', time='TIME', format='VALUE_FORMAT', readonly=True, order=3)
        self.putdef('AnalogDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=6)
        self.put_h_cfg(('AnalogDef', 'VALUE'), dtype=float32)
        self.add('ListDef', DEFINITION_DEF)
        self.putdef('ListDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('ListDef', '#VALUES', dtype=DT_LIST, order=2)
        self.putdef('ListDef', 'VALUE', dtype=DT_CHAR, repeat='#VALUES', order=3)
        self.add('PlotTagColors', 'ListDef')
        self.put('PlotTagColors', 'DESCRIPTION', 'Plot tag color settings')
        self.put('PlotTagColors', '#VALUES', 100)
        self.put(('PlotTagColors', '#VALUES'), 0)
        self.put(('PlotTagColors', '#VALUES'), 100)
        self.add('GraphicColors', 'ListDef')
        self.put('GraphicColors', 'DESCRIPTION', 'Graphic custom colors')
        self.add('DictionaryDef', DEFINITION_DEF)
        self.putdef('DictionaryDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DictionaryDef', '#PARAMETERS', dtype=DT_DICTIONARY, order=2)
        self.putdef('DictionaryDef', 'VALUE', dtype=DT_CHAR, repeat='#PARAMETERS', order=3)
        self.add('IconDef', DEFINITION_DEF)
        self.putdef('IconDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('IconDef', 'FILE_NAME', dtype=DT_CHAR, order=2)
        self.add('AssetElementDef', DEFINITION_DEF)
        self.putdef('AssetElementDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('AssetElementDef', 'TAG_EXPRESSION', dtype=DT_CHAR, order=2)
        self.putdef('AssetElementDef', 'ICON', dtype=DT_RECORD, skey='IconDef', order=3)
        self.putdef('AssetElementDef', '#PARAMETERS', dtype=DT_DICTIONARY, order=4)
        self.putdef('AssetElementDef', 'VALUE', dtype=DT_CHAR, repeat='#PARAMETERS', order=5)
        if self.add('SystemSettings', 'DictionaryDef'):
            self.put('SystemSettings', 'DESCRIPTION', 'Cake environment settings')
            self.put('SystemSettings', 'VALUE', '5000', 'PlotUpdateDelay', add_keys=True)
            self.put('SystemSettings', 'VALUE', '500', 'GraphicUpdateDelay', add_keys=True)
            self.put('SystemSettings', 'VALUE', '50000', 'MaxLocalTags', add_keys=True)
            self.put('SystemSettings', 'VALUE', '50000', 'MaxNetworkTags', add_keys=True)
            self.put('SystemSettings', 'VALUE', '1', 'CimioEnabled', add_keys=True)
            self.put('SystemSettings', 'VALUE', "C:\\Program Files (x86)\\Programmer's Notepad\\pn.exe", 'ExternalCodeEditor', add_keys=True)
            self.put('SystemSettings', 'VALUE', 'Analogs', 'HomePage', add_keys=True)
        self.put('SystemSettings', 'VALUE', __version__, 'SchemaVersion', add_keys=True)
        if self.get('SystemSettings', 'VALUE', 'TimeStorageMode') == None:
            if self.utc_mode:
                self.put(('SystemSettings', 'VALUE', 'TimeStorageMode'), 'UTC', add_keys=True)
            else:
                self.put(('SystemSettings', 'VALUE', 'TimeStorageMode'), 'Local', add_keys=True)
        self.del_key('SystemSettings', 'VALUE', 'MaxFolderTags')
        self.del_key('SystemSettings', 'VALUE', 'PlotUpdateTimer')
        auto_help = 'This field is automatically maintained by the system.  Do not edit.'
        self.add('ContextHelp', 'DictionaryDef')
        self.put('ContextHelp', 'DESCRIPTION', 'Context sensitive help strings')
        self.put('ContextHelp', 'VALUE', 'The name of this tag.', 'NAME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of milliseconds to wait for an OPC read request to complete.  If the timeout expires, all the tags in the group will be set to NaN.', 'OPC_TIMEOUT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The time required (in seconds) to read the tag values from the OPC server.  This field is maintained automatically by the system.', 'OPC_READ_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The time required (in seconds) to write the tag values to the historian database.  This field is maintained automatically by the system.', 'DB_WRITE_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The frequency in milliseconds at which the OPC server is to update its cache.  Set to -1 to disable these updates.  When doing cached reads set this to a value which is less than your data retrieval frequency.  When doing Device reads, it is highly recommended you set this rate to -1.', 'OPC_UPDATE_RATE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of tags to place inside each OPC Group.  The breaking-up of your tag lists into this smaller group size is automatic and transparent.  250 is a safe value to use, but many OPC servers can handle far larger group sizes.', 'OPC_GROUP_SIZE', add_keys=True)
        self.put('ContextHelp', 'VALUE', "How to timestamp the data as its being historized.  'Request time' is usually recommend since it ensures all tags are timestampped identically.", 'OPC_TIME_SOURCE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Do OPC read calls using a source of cache or device.  Hybrid does a device read for the first call, then cache reads for all subsequent calls.  Which setting is preferable varies significantly between different OPC servers.  Cache mode is recommend if your OPC server supports it.', 'OPC_SOURCE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Do synchronous or asynchronous calls when reading values from the OPC server.  Asynchronous is nearly always recommended.', 'OPC_FUNCTION', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The OPC server name to talk to.\n\nExamples:\nHci.TPNServer\t\t(Honeywell APP)\nHwHsc.OPCServer\t(Honeywell Experion)\nAspen.Infoplus21_DA.1\t(Aspen InfoPlus.21)\nMatrikon.OPC.Simulation\t(Matrikon Simulation Server)\n\nLeave this field blank to only retreive system health monitoring tags\nwithout connecting to an OPC server.', 'OPC_SERVER', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The computer name (or IP address) where the OPC server resides. When using Pyro mode to talk to an OpenOPC Gateway Service runnning on the same node as the OPC server, this should be set to localhost.', 'OPC_HOST', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The computer name (or IP address) where the OpenOPC Gateway Service resides.  When using DCOM mode, this field is ignored.', 'OPC_GATE_HOST', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The TCP port number being used by the OpenOPC Gateway Service.  7766 is the default and should be used in most cases.', 'OPC_GATE_PORT', add_keys=True)
        self.put('ContextHelp', 'VALUE', "DCOM mode talks to the OPC server directly.  Pyro mode talks to an OpenOPC Gateway Service.  When Pyro mode is used, you must also fill out the OPC_GATE_HOST and OPC_GATE_PORT fields.'", 'OPC_MODE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'If turned ON, the CCI OPC Client Service will connect to the specified OPC server.  If turned OFF, it will disconnect from the OPC server and all OpcGetDef tags which are configured to use this device will stop updating.  It is also necessary to toggle this switch to OFF then back ON again in order for many of the OPC settings to be applied.', 'DEVICE_PROCESSING', add_keys=True)
        self.put('ContextHelp', 'VALUE', "If turned OFF, all OPC tags in this record's tag list will stop being read from the OPC server.", 'GROUP_PROCESSING', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The name of an OpcDeviceDef tag which has been configued with the details of how to talk to a specific OPC server.', 'DEVICE_TAG', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The next time (in the future) when scheduler will trigger an activation.  If this field is set to blank, all future scheduled activations will be disabled.', 'SCHEDULE_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The frequency (in seconds) at which to re-schedule activations.  If this field is set to 0, SCHEDULE_TIME will stop having future timestamps automatically placed into it and all activations will stop.', 'SCHEDULE_FREQ', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The tag/field in the database which when its value changes will immediately cause this OPC group to activate.  This can be used as an alternative to scheduled activiations.  Leave blank to disable.  Specify the field using the format TAG <space> FIELD.', 'ACTIVATION_FIELD', add_keys=True)
        self.put('ContextHelp', 'VALUE', auto_help, 'MESSAGE', add_keys=True)
        self.put('ContextHelp', 'VALUE', auto_help, 'TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of entries to store in the error message log.  When this limit is exceeded, the oldest entries will be removed to make room for the newest ones.', '#MESSAGES', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Setting this switch to YES will cause the OPC tag groups represented by this tag to be rebuilt during the next scan.  You must do this after editing the #TAGS list in order for your changes to be applied.', 'REBUILD_GROUP', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Setting this switch to YES will cause the OPC quality parameter for each tag in this group to be ignored and instead processed as if the quality were always Good.', 'IGNORE_QUALITY', add_keys=True)
        self.put('ContextHelp', 'VALUE', auto_help, 'GROUP_STATUS', add_keys=True)
        self.put('ContextHelp', 'VALUE', auto_help, 'GROUP_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The list of tags that are processed or used by this tag.', '#TAGS', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'This field is maintained automatically by the system.  YES indicates the #TAGS list has been modified since the OPC groups were last rebuilt.  You can apply these changes to the OPC collection by setting REBUILD_GROUP to YES.   ', 'LIST_CHANGED', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Controls the types of messages which are logged.\n\nGeneral:\tStart/stop, connect/disconnect, configuration changes\nError:\t\tTimeout errors, COM errors\nWarning:\tInvalid tags\nInformation:\tRequest/response, Success\nVerbose:\tLow-level OPC calls (DCOM mode only)', 'VERBOSITY_LEVEL', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Controls how the data is timestamped when recorded into history.\n\nRequest Time:\t\tWhen the data was scheduled to be retrieved.\nReponse Time:\t\tWhen the data was received from the OPC Server.\nOPC Server:\t\tThe data timestamp supplied by the OPC Server.\n', 'TIME_SOURCE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The current (or newest) value available for this tag', 'VALUE', add_keys=True)
        self.put('ContextHelp', 'VALUE', auto_help, 'TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The maximum number of historical values to store for this tag.  When this value is exceeded, the oldest entries will be removed to make room for the newest ones.', '#VALUES', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'EXPRESSION\nA single line expression that evaluates to a real value.\n\nExample:  (tag1 / tag2) * 100.0\n\nRETURN VALUE\nA multi-line statement which ends by explicity returning a single value.\n\nExample:\nif tag > 100.0:\n    return 99.9\nelse:\n    return tag\n\nRETURN ARRAY\nA multi-line statement which ends by returning an array of values.\n\nExample:  return lowpass(tag, 60)', 'CALC_TYPE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The name of an analog tag to use as the time basis for the calculation.  The timestamps output by the calculation will then exactly match the historical timestamps contained in the specified analog tag.  If this field is blank then CALC_START and CALC_INTERVAL will used instead to determine a fixed data frequency.', 'TIME_TAG', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Time at which the calculated historical values will begin.  Must be entered in the form mm/dd/yyyy hh:mm:ss.  If this field is left blank, then the Start Time setting inside Tools > Options will be used instead.   And if the Start Time in Tools > Options is blank, then the start time will be automatically set using the earliest timestamp found among all tags used in the calculation code.', 'CALC_START', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The interval (in seconds) between each subsequent calculated value which will be returned.  When set to a negative number it specifies the absolute frequency in calendar months (-1 = 1 month).  When set to 0 the Sample Frequency setting inside Tools > Options will be used instead.', 'CALC_INTERVAL', add_keys=True)
        self.put('ContextHelp', 'VALUE', "The number of lines to make available for capturing the output from 'print' statements inside your code.  This is useful for debugging.", '#OUTPUT_LINES', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The long description text for this tag.', 'DESCRIPTION', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The engineering units for this tag.', 'ENG_UNITS', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of decimal places to display when formatting floating point values.  Set to -1 for automatic "smart" formatting.', 'VALUE_FORMAT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The time stamp of the most recent value.  This field is maintained automatically by the system.  Do not edit.', 'TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The endian type of the remote IO server.  For Windows and VMS use Little Endian, for Sun Solaris and HP-UX use Big Endian.  Changes to this field will not be applied unless you toggle the device OFF/ON.', 'IO_ENDIAN', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The host name or IP address of a remote IO server.', 'IO_HOST', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The TCP port number of a remote IO server.  Each IO server may contain multiple IO devices each listening on a different port.  Consult the TCP services file on the remote host to see which IO device names listen on which ports.', 'IO_PORT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of milliseconds to wait for an IO read request to complete.  If the timeout expires, all the tags in the group will be set to NaN.  Changes to this field will not be applied unless you toggle the device OFF/ON.', 'IO_TIMEOUT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of tags to place inside each IO read request.  The breaking-up of your tag lists into this smaller group size is automatic and transparent.  It is recommend you avoid setting this number above 1000 since higher values may cause some IO servers to fail.', 'IO_GROUP_SIZE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The aggregate function to apply when retrieving history.  Note that this function is applied prior to your calculation CODE being run.', 'AGG_FUNCTION', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'If turned ON, older historical data will be automatically deleted in order to save space.', 'TRIM_PROCESSING', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of days that historical data will be stored before being discarded.', 'TRIM_DELAY', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of days that raw historical data will be stored before being resampled.', 'RESAMPLE_DELAY', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'If turned ON, older historical data will be archived by moving it from RAM to disk.', 'ARCHIVE_PROCESSING', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The name of a HistoryServerDef tag which has been configured with the details of how to talk to a specific PostgreSQL archive server.', 'ARCHIVE_SERVER', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of days that historical data will be kept in RAM before being archived to disk.', 'ARCHIVE_DELAY', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'If turned ON, older historical data will be resampled to a new frequency.', 'RESAMPLE_PROCESSING', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The frequency (in seconds) to use when resampling the data.', 'RESAMPLE_FREQ', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The aggregate function to use when resampling the data. ', 'RESAMPLE_FUNCTION', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'If set to YES, adjacent identical values will be removed from historical data when it is processed.', 'STORE_ONLY_CHANGES', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'This should be set to 0 for all customer written aggregate functions.  Non-zero values are reserved for identifying built-in Toolbox aggregate functions.', 'AGGREGATE_ID', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The deviation amount (in engineering units) for the deadband.  Only values that fall outside of the current deadband range will be stored in history.', 'DEV_VALUE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The maximum amount of time (in seconds) that is allowed to pass before a new value is stored in history.', 'DEV_MAX_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'For integer data types should bad values be stored in history?  This setting has no effect on float data types.', 'STORE_BAD', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The special flag value used for storing bad integer data.', 'BAD_VALUE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The number of minutes to wait before sending the same notification again.', 'HOLD_OFF_TIME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The IP address of the SMTP server to use for sending messages.  Use host:port format if a non-standard TCP port number is required.', 'SMTP_SERVER', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'User name to authenticate with the SMTP server as.  Leave blank if no authentication is required.', 'USERNAME', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'Set to YES if the SMTP server requires an encrypted connection.', 'USE_TLS', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The name of the task tag that is assigned to process this tag.  Each task tag represents a Windows or Linux service.', 'TASK_TAG', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'A list of the users who will receive the notification.  Both user and role tags may be used.', '#USERS', add_keys=True)
        self.put('ContextHelp', 'VALUE', "The name of a SelectDef or SelectDictDef tag used to enumerate this tag's VALUE field with descriptive text.", 'FORMAT_RECORD', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The menu tree to display when a user logs in who is assigned to this role.', 'MENU_TREE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The base security policy for this role.  You can override specific portions of the base policy in the #RULES list.', 'BASE_POLICY', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'A list of security rules that can override portions of the base security policy.', '#RULES', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The e-mail address that notifications for this user will be sent to.', 'EMAIL_ADDRESS', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The role that this user is assigned to.  If blank this user account will be disabled.', 'BASE_ROLE', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The message that the users will see when they receive the notification.', 'MESSAGE_TEXT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The LDAP server to use for authentication. If blank the user will be authenticated using their Cake password.', 'LDAP_SERVER', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The IP address of the LDAP server.', 'LDAP_HOST', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The TCP port number of the LDAP server.  Default is 389.', 'LDAP_PORT', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The Bind DN to use for authenticating users.  The expression {user} will be replaced with the Cake user name during authentication. ', 'BIND_DN', add_keys=True)
        self.put('ContextHelp', 'VALUE', 'The password for this user.  Ignored when a LDAP server is specified.', 'PASSWORD', add_keys=True)
        self.add('TaskDef', DEFINITION_DEF)
        self.add('ScriptTask', 'TaskDef')
        self.add('FunctionDef', DEFINITION_DEF)
        self.putdef('FunctionDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('FunctionDef', 'CODE', dtype=DT_CHAR, order=2)
        self.del_h_cfg(('FunctionDef', 'CODE'))
        for t in self.getlist('FunctionDef'):
            self.del_h_cfg((t, 'CODE'))

        self.add('CalculationDef', DEFINITION_DEF)
        self.putdef('CalculationDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('CalculationDef', 'ENG_UNITS', dtype=DT_CHAR, order=2)
        self.putdef('CalculationDef', 'VALUE', dtype=DT_FLOAT, readonly=True, order=3)
        self.putdef('CalculationDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=4)
        self.putdef('CalculationDef', 'CALC_START', dtype=DT_TIMESTAMP, order=6)
        self.putdef('CalculationDef', 'TIME_TAG', dtype=DT_RECORD, skey='AnalogDef', order=7)
        self.putdef('CalculationDef', 'AGG_FUNCTION', dtype=DT_RECORD, skey='AggFunctionDef', default=0, order=8)
        self.putdef('CalculationDef', 'CALC_INTERVAL', dtype=DT_INTEGER, default=0, order=9)
        self.putdef('CalculationDef', 'CODE', dtype=DT_CHAR, chain='SAVE_TIME', order=10)
        self.putdef('CalculationDef', 'SAVE_TIME', dtype=DT_TIMESTAMP, hidden=True, order=11)
        self.putdef('CalculationDef', 'COMPILED_CODE', dtype=DT_CHAR, chain='COMPILED_TIME', hidden=True, order=12)
        self.putdef('CalculationDef', 'COMPILED_TIME', dtype=DT_TIMESTAMP, hidden=True, order=13)
        self.putdef('CalculationDef', '#CONSTANTS', dtype=DT_DICTIONARY, order=14)
        self.putdef('CalculationDef', 'CONSTANT_DESCRIPTION', dtype=DT_CHAR, repeat='#CONSTANTS', order=15)
        self.putdef('CalculationDef', 'CONSTANT_VALUE', dtype=DT_FLOAT, repeat='#CONSTANTS', chain='SAVE_TIME', order=16)
        self.putdef('CalculationDef', '#INPUTS', dtype=DT_DICTIONARY, order=17)
        self.putdef('CalculationDef', 'INPUT_DESCRIPTION', dtype=DT_CHAR, repeat='#INPUTS', order=18)
        self.putdef('CalculationDef', 'INPUT_TAG', dtype=DT_RECORD, repeat='#INPUTS', order=19)
        self.putdef('CalculationDef', '#TAGS', dtype=DT_LIST, order=20)
        self.putdef('CalculationDef', 'TAG', dtype=DT_RECORD, repeat='#TAGS', order=21)
        self.putdef('CalculationDef', 'TAG_FUNCTION', dtype=DT_RECORD, skey='AggFunctionDef', repeat='#TAGS', order=22)
        self.putdef('CalculationDef', 'TAG_FILL', dtype=DT_INTEGER, default=0, format='NO/YES', repeat='#TAGS', order=23)
        self.putdef('CalculationDef', 'TAG_NULL', dtype=DT_INTEGER, default=0, repeat='#TAGS', order=24)
        self.putdef('CalculationDef', '#OUTPUT_LINES', dtype=DT_LIST, default=0, order=25)
        self.putdef('CalculationDef', 'OUTPUT_LINE', dtype=DT_CHAR, repeat='#OUTPUT_LINES', order=26)
        self.deldef('CalculationDef', 'CALC_TYPE')
        self.deldef('CalculationDef', '#VALUES')
        self.deldef('CalculationDef', 'TREND_TIME')
        self.deldef('CalculationDef', 'TREND_VALUE')
        self.deldef('CalculationDef', 'TREND_QUALITY')
        self.deldef('CalculationDef', '#ARRAYS')
        self.deldef('CalculationDef', 'ARRAY')
        self.del_h_cfg(('CalculationDef', 'CODE'))
        for t in self.getlist('CalculationDef'):
            self.del_h_cfg((t, 'CODE'))

        for t in self.getlist('CalculationDef'):
            self.put(t, 'SAVE_TIME', self.now())

        self.add('CompressionDef', DEFINITION_DEF)
        self.putdef('CompressionDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('CompressionDef', 'DEV_VALUE', dtype=DT_FLOAT, order=2)
        self.putdef('CompressionDef', 'DEV_MAX_TIME', dtype=DT_INTEGER, order=3)
        self.putdef('CompressionDef', 'STORE_BAD', dtype=DT_INTEGER, format='NO/YES', order=4)
        self.putdef('CompressionDef', 'BAD_VALUE', dtype=DT_INTEGER, order=5)
        if self.add('IntComp', 'CompressionDef'):
            self.put('IntComp', 'DESCRIPTION', 'Lossless compression for integers')
            self.put('IntComp', 'DEV_VALUE', 1.0)
            self.put('IntComp', 'DEV_MAX_TIME', 3600)
            self.put('IntComp', 'BAD_VALUE', -1)
        self.add('ReplicationDef', DEFINITION_DEF)
        self.putdef('ReplicationDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=2)
        self.putdef('ReplicationDef', 'REMOTE_HOST', dtype=DT_CHAR, order=3)
        self.putdef('ReplicationDef', 'REMOTE_PORT', dtype=DT_CHAR, default='9000', order=4)
        self.putdef('ReplicationDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=5, reschedule='SCHEDULE_FREQ')
        self.putdef('ReplicationDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=6)
        self.putdef('ReplicationDef', 'MESSAGE', dtype=DT_CHAR, chain='TIME', readonly=True, order=7)
        self.putdef('ReplicationDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=8)
        self.putdef('ReplicationDef', '#TAGS', dtype=DT_LIST, order=9)
        self.putdef('ReplicationDef', 'TAG', dtype=DT_CHAR, repeat='#TAGS', order=10)
        if self.add('RepClient', 'ReplicationDef'):
            self.put('RepClient', 'REMOTE_PORT', 9000)
            self.put('RepClient', 'SCHEDULE_TIME', '01/01/2000 00:00:00')
            self.put('RepClient', 'SCHEDULE_FREQ', 60)
            self.put('RepClient', '#TAGS', 1)
            self.put(('RepClient', 'TAG', 1), '*')
        for t in self.getlist('CalcTaskDef'):
            self.delete(t, delref=True)

        self.delete('CalcTaskDef', delref=True)
        self.delete('CalcTaskView', delref=True)
        for t in self.getlist('CalcGroupDef'):
            self.delete(t, delref=True)

        self.delete('CalcGroupDef', delref=True)
        self.delete('CalcGroupView', delref=True)
        self.add('ScriptDef', DEFINITION_DEF)
        self.putdef('ScriptDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('ScriptDef', 'TASK_TAG', dtype=DT_RECORD, skey='TaskDef', order=2)
        self.putdef('ScriptDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=3)
        self.putdef('ScriptDef', 'MESSAGE', dtype=DT_CHAR, chain='TIME', readonly=True, order=4)
        self.putdef('ScriptDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=5)
        self.putdef('ScriptDef', 'CODE', dtype=DT_CHAR, order=6)
        self.putdef('ScriptDef', '#COS_FIELDS', dtype=DT_LIST, order=7)
        self.putdef('ScriptDef', 'COS_FIELD', dtype=DT_FIELD, repeat='#COS_FIELDS', order=8)
        self.putdef('ScriptDef', '#SCHEDULE_TIMES', dtype=DT_LIST, order=9)
        self.putdef('ScriptDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, repeat='#SCHEDULE_TIMES', order=10, reschedule='SCHEDULE_FREQ')
        self.putdef('ScriptDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, repeat='#SCHEDULE_TIMES', order=11)
        self.putdef('ScriptDef', '#VALUES', dtype=DT_LIST, default=0, order=12)
        self.putdef('ScriptDef', 'VALUE', dtype=DT_FLOAT, repeat='#VALUES', order=13)
        self.putdef('ScriptDef', '#OUTPUT_LINES', dtype=DT_LIST, default=0, order=14)
        self.putdef('ScriptDef', 'OUTPUT_LINE', dtype=DT_CHAR, repeat='#OUTPUT_LINES', order=15)
        if self.add('MyScript', 'ScriptDef'):
            self.put('MyScript', 'TASK_TAG', 'ScriptTask')
        self.add('GraphicScriptDef', DEFINITION_DEF)
        self.putdef('GraphicScriptDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('GraphicScriptDef', 'MESSAGE', dtype=DT_CHAR, chain='TIME', readonly=True, order=2)
        self.putdef('GraphicScriptDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=3)
        self.putdef('GraphicScriptDef', 'CODE', dtype=DT_CHAR, order=4)
        self.putdef('GraphicScriptDef', '#COS_FIELDS', dtype=DT_LIST, order=6)
        self.putdef('GraphicScriptDef', 'COS_FIELD', dtype=DT_FIELD, repeat='#COS_FIELDS', order=7)
        self.putdef('GraphicScriptDef', '#SCHEDULE_TIMES', dtype=DT_LIST, order=9)
        self.putdef('GraphicScriptDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, repeat='#SCHEDULE_TIMES', order=10, reschedule='SCHEDULE_FREQ')
        self.putdef('GraphicScriptDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, repeat='#SCHEDULE_TIMES', order=11)
        self.add('DiscreteDef', DEFINITION_DEF)
        self.putdef('DiscreteDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DiscreteDef', 'FORMAT_RECORD', dtype=DT_RECORD, skey='SelectDef', order=2)
        self.putdef('DiscreteDef', 'VALUE', dtype=DT_INTEGER, chain='TIME', time='TIME', format='FORMAT_RECORD', readonly=True, order=3)
        self.putdef('DiscreteDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=4)
        self.put_h_cfg(('DiscreteDef', 'VALUE'), dtype=int32)
        self.add('TextDef', DEFINITION_DEF)
        self.putdef('TextDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('TextDef', 'VALUE', dtype=DT_CHAR, length=80, chain='TIME', quality='QUALITY', order=2)
        self.putdef('TextDef', 'QUALITY', dtype=DT_INTEGER, format='QUALITY-STATES', order=3)
        self.putdef('TextDef', 'TIME', dtype=DT_TIMESTAMP, chain='#VALUES', order=4)
        self.add('OpcXmlDeviceDef', DEFINITION_DEF)
        self.putdef('OpcXmlDeviceDef', 'DEVICE_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('OpcXmlDeviceDef', 'SERVER_ADDRESS', dtype=DT_CHAR, order=2)
        self.putdef('OpcXmlDeviceDef', 'VERBOSITY_LEVEL', dtype=DT_INTEGER, format='VERBOSITY-LEVELS', default=1, order=4)
        self.putdef('OpcXmlDeviceDef', 'MESSAGE', dtype=DT_CHAR, length=80, chain='TIME', readonly=True, order=5)
        self.putdef('OpcXmlDeviceDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=6)
        self.put_h_cfg(('OpcXmlDeviceDef', 'MESSAGE'), dtype='str100')
        for t in self.getlist('OpcXmlDeviceDef'):
            self.put_h_cfg((t, 'MESSAGE'), dtype='str100')

        self.add('OpcXmlGetDef', DEFINITION_DEF)
        self.putdef('OpcXmlGetDef', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('OpcXmlGetDef', 'DEVICE_TAG', dtype=DT_RECORD, skey='OpcXmlDeviceDef', order=2)
        self.putdef('OpcXmlGetDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=4, reschedule='SCHEDULE_FREQ')
        self.putdef('OpcXmlGetDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=5)
        self.putdef('OpcXmlGetDef', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=6)
        self.putdef('OpcXmlGetDef', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=7)
        self.putdef('OpcXmlGetDef', 'OPC_READ_TIME', dtype=DT_FLOAT, readonly=True, order=9)
        self.putdef('OpcXmlGetDef', 'DB_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=10)
        self.putdef('OpcXmlGetDef', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=11)
        self.putdef('OpcXmlGetDef', '#TAGS', dtype=DT_LIST, chain='LIST_CHANGED', order=13)
        self.putdef('OpcXmlGetDef', 'REMOTE_TAG', dtype=DT_CHAR, repeat='#TAGS', chain='LIST_CHANGED', order=14)
        self.putdef('OpcXmlGetDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=15)
        self.put_h_cfg(('OpcXmlGetDef', 'OPC_READ_TIME'))
        self.put_h_cfg(('OpcXmlGetDef', 'DB_WRITE_TIME'))
        for t in self.getlist('OpcXmlGetDef'):
            self.put_h_cfg((t, 'OPC_READ_TIME'))
            self.put_h_cfg((t, 'DB_WRITE_TIME'))

        self.add('ModbusDeviceDef', DEFINITION_DEF)
        self.putdef('ModbusDeviceDef', 'DEVICE_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('ModbusDeviceDef', 'MODBUS_HOST', dtype=DT_CHAR, order=2)
        self.putdef('ModbusDeviceDef', 'MODBUS_PORT', dtype=DT_INTEGER, default=502, order=3)
        self.putdef('ModbusDeviceDef', 'VERBOSITY_LEVEL', dtype=DT_INTEGER, format='VERBOSITY-LEVELS', default=1, order=4)
        self.putdef('ModbusDeviceDef', 'MESSAGE', dtype=DT_CHAR, length=80, chain='TIME', readonly=True, order=5)
        self.putdef('ModbusDeviceDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=6)
        self.put_h_cfg(('ModbusDeviceDef', 'MESSAGE'), dtype='str100')
        for t in self.getlist('ModbusDeviceDef'):
            self.put_h_cfg((t, 'MESSAGE'), dtype='str100')

        self.add('ModbusGetDef', DEFINITION_DEF)
        self.putdef('ModbusGetDef', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('ModbusGetDef', 'DEVICE_TAG', dtype=DT_RECORD, skey='ModbusDeviceDef', order=2)
        self.putdef('ModbusGetDef', 'SLAVE_ID', dtype=DT_INTEGER, default=1, order=3)
        self.putdef('ModbusGetDef', 'START_REGISTER', dtype=DT_INTEGER, default=30001, order=4)
        self.putdef('ModbusGetDef', 'DATA_FORMAT', dtype=DT_INTEGER, format='MODBUS-FORMATS', order=5)
        self.putdef('ModbusGetDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=7, reschedule='SCHEDULE_FREQ')
        self.putdef('ModbusGetDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=8)
        self.putdef('ModbusGetDef', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=9)
        self.putdef('ModbusGetDef', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=10)
        self.putdef('ModbusGetDef', 'MB_READ_TIME', dtype=DT_FLOAT, readonly=True, order=11)
        self.putdef('ModbusGetDef', 'DB_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=12)
        self.putdef('ModbusGetDef', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=13)
        self.putdef('ModbusGetDef', '#TAGS', dtype=DT_LIST, chain='LIST_CHANGED', order=14)
        self.putdef('ModbusGetDef', 'REGISTER', dtype=DT_CHAR, repeat='#TAGS', readonly=True, order=15)
        self.putdef('ModbusGetDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=16)
        self.putdef('ModbusGetDef', 'SCALING_FACTOR', dtype=DT_FLOAT, repeat='#TAGS', default=1.0, order=17)
        self.put_h_cfg(('ModbusGetDef', 'MB_READ_TIME'))
        self.put_h_cfg(('ModbusGetDef', 'DB_WRITE_TIME'))
        self.add('ModbusGet2Def', DEFINITION_DEF)
        self.putdef('ModbusGet2Def', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('ModbusGet2Def', 'DEVICE_TAG', dtype=DT_RECORD, skey='ModbusDeviceDef', order=2)
        self.putdef('ModbusGet2Def', 'SLAVE_ID', dtype=DT_INTEGER, default=1, order=3)
        self.putdef('ModbusGet2Def', 'START_REGISTER', dtype=DT_INTEGER, default=30001, order=5)
        self.putdef('ModbusGet2Def', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=7, reschedule='SCHEDULE_FREQ')
        self.putdef('ModbusGet2Def', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=8)
        self.putdef('ModbusGet2Def', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=9)
        self.putdef('ModbusGet2Def', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=10)
        self.putdef('ModbusGet2Def', 'MB_READ_TIME', dtype=DT_FLOAT, readonly=True, order=11)
        self.putdef('ModbusGet2Def', 'DB_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=12)
        self.putdef('ModbusGet2Def', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=13)
        self.putdef('ModbusGet2Def', '#TAGS', dtype=DT_LIST, chain='LIST_CHANGED', order=14)
        self.putdef('ModbusGet2Def', 'REGISTER', dtype=DT_CHAR, repeat='#TAGS', readonly=True, order=15)
        self.putdef('ModbusGet2Def', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=16)
        self.putdef('ModbusGet2Def', 'SCALING_FACTOR', dtype=DT_FLOAT, repeat='#TAGS', default=1.0, order=17)
        self.putdef('ModbusGet2Def', 'DATA_FORMAT', dtype=DT_INTEGER, repeat='#TAGS', chain='LIST_CHANGED', format='MODBUS-FORMATS2', order=18)
        self.put_h_cfg(('ModbusGet2Def', 'MB_READ_TIME'))
        self.put_h_cfg(('ModbusGet2Def', 'DB_WRITE_TIME'))
        self.deldef('ModbusGet2Def', 'FUNCTION_CODE')
        self.add('ModbusMapDef', DEFINITION_DEF)
        self.deldef('ModbusMapDef', 'START_REGISTER')
        self.putdef('ModbusMapDef', 'REGISTER_TABLE', dtype=DT_INTEGER, format='MODBUS-TABLES', default=2, order=1)
        self.putdef('ModbusMapDef', 'DATA_FORMAT', dtype=DT_INTEGER, format='MODBUS-FORMATS', default=1, order=2)
        self.putdef('ModbusMapDef', '#TAGS', dtype=DT_LIST, order=3)
        self.putdef('ModbusMapDef', 'REGISTER', dtype=DT_CHAR, repeat='#TAGS', readonly=True, order=4)
        self.putdef('ModbusMapDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', order=5)
        self.putdef('ModbusMapDef', 'SCALING_FACTOR', dtype=DT_FLOAT, repeat='#TAGS', default=1.0, order=6)
        self.add('OpcDeviceDef', DEFINITION_DEF)
        self.putdef('OpcDeviceDef', 'DEVICE_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('OpcDeviceDef', 'OPC_MODE', dtype=DT_INTEGER, format='OPC-MODES', default=1, order=2)
        self.putdef('OpcDeviceDef', 'OPC_GATE_HOST', dtype=DT_CHAR, default='localhost', order=3)
        self.putdef('OpcDeviceDef', 'OPC_GATE_PORT', dtype=DT_CHAR, default='7766', order=4)
        self.putdef('OpcDeviceDef', 'OPC_HOST', dtype=DT_CHAR, default='localhost', order=5)
        self.putdef('OpcDeviceDef', 'OPC_SERVER', dtype=DT_CHAR, default='Matrikon.OPC.Simulation', order=6)
        self.putdef('OpcDeviceDef', 'OPC_FUNCTION', dtype=DT_INTEGER, format='OPC-FUNCTIONS', default=1, order=7)
        self.putdef('OpcDeviceDef', 'OPC_SOURCE', dtype=DT_INTEGER, format='OPC-SOURCES', default=1, order=8)
        self.putdef('OpcDeviceDef', 'OPC_GROUP_SIZE', dtype=DT_INTEGER, default=250, order=9)
        self.putdef('OpcDeviceDef', 'OPC_UPDATE_RATE', dtype=DT_INTEGER, default=5000, order=10)
        self.putdef('OpcDeviceDef', 'OPC_TIMEOUT', dtype=DT_INTEGER, default=5000, order=11)
        self.putdef('OpcDeviceDef', 'TIME_SOURCE', dtype=DT_INTEGER, format='TIME-SOURCES', order=13)
        self.putdef('OpcDeviceDef', 'VERBOSITY_LEVEL', dtype=DT_INTEGER, format='VERBOSITY-LEVELS', default=1, order=14)
        self.putdef('OpcDeviceDef', 'MESSAGE', dtype=DT_CHAR, length=80, chain='TIME', readonly=True, order=15)
        self.putdef('OpcDeviceDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=16)
        self.put_h_cfg(('OpcDeviceDef', 'MESSAGE'), dtype='str100')
        for t in self.getlist('OpcDeviceDef'):
            self.put_h_cfg((t, 'MESSAGE'), dtype='str100')

        self.add('OpcServer', 'OpcDeviceDef')
        self.add('OpcGetDef', DEFINITION_DEF)
        self.putdef('OpcGetDef', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('OpcGetDef', 'DEVICE_TAG', dtype=DT_RECORD, skey='OpcDeviceDef', order=2)
        self.putdef('OpcGetDef', 'ACTIVATION_FIELD', dtype=DT_FIELD, order=3)
        self.putdef('OpcGetDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=4, reschedule='SCHEDULE_FREQ')
        self.putdef('OpcGetDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=5)
        self.putdef('OpcGetDef', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=6)
        self.putdef('OpcGetDef', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=7)
        self.putdef('OpcGetDef', 'OPC_READ_TIME', dtype=DT_FLOAT, readonly=True, order=9)
        self.putdef('OpcGetDef', 'DB_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=10)
        self.putdef('OpcGetDef', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=11)
        self.putdef('OpcGetDef', 'REBUILD_GROUP', dtype=DT_INTEGER, format='NO/YES', order=12)
        self.putdef('OpcGetDef', 'IGNORE_QUALITY', dtype=DT_INTEGER, format='NO/YES', order=13)
        for t in self.getlist('OpcGetDef'):
            if self.get((t, 'IGNORE_QUALITY')) == None:
                self.put((t, 'IGNORE_QUALITY'), 0)

        self.putdef('OpcGetDef', '#TAGS', dtype=DT_LIST, chain='LIST_CHANGED', order=14)
        self.putdef('OpcGetDef', 'REMOTE_TAG', dtype=DT_CHAR, repeat='#TAGS', chain='LIST_CHANGED', order=15)
        self.putdef('OpcGetDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=16)
        self.putdef('OpcGetDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', chain='LIST_CHANGED', repeat='#TAGS', order=17)
        self.putdef('OpcGetDef', 'STATUS', dtype=DT_INTEGER, format='QUALITY-STATES', repeat='#TAGS', order=18)
        self.put_h_cfg(('OpcGetDef', 'OPC_READ_TIME'))
        self.put_h_cfg(('OpcGetDef', 'DB_WRITE_TIME'))
        for t in self.getlist('OpcGetDef'):
            self.put_h_cfg((t, 'OPC_READ_TIME'))
            self.put_h_cfg((t, 'DB_WRITE_TIME'))

        if self.add('GetOpcValues', 'OpcGetDef'):
            self.put('GetOpcValues', 'DEVICE_TAG', 'OpcServer')
            self.put('GetOpcValues', 'SCHEDULE_TIME', '01/01/2000 00:00:00')
            self.put('GetOpcValues', 'SCHEDULE_FREQ', 10)
        self.put('GetOpcValues', 'REBUILD_GROUP', 0)
        self.add('OpcPutDef', DEFINITION_DEF)
        self.putdef('OpcPutDef', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('OpcPutDef', 'DEVICE_TAG', dtype=DT_RECORD, skey='OpcDeviceDef', order=2)
        self.putdef('OpcPutDef', 'ACTIVATION_FIELD', dtype=DT_FIELD, order=3)
        self.putdef('OpcPutDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=4, reschedule='SCHEDULE_FREQ')
        self.putdef('OpcPutDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=5)
        self.putdef('OpcPutDef', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=6)
        self.putdef('OpcPutDef', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=7)
        self.putdef('OpcPutDef', 'OPC_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=8)
        self.putdef('OpcPutDef', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=10)
        self.putdef('OpcPutDef', 'REBUILD_GROUP', dtype=DT_INTEGER, format='NO/YES', order=11)
        self.putdef('OpcPutDef', '#TAGS', dtype=DT_LIST, order=12, chain='LIST_CHANGED')
        self.putdef('OpcPutDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=13)
        self.putdef('OpcPutDef', 'REMOTE_TAG', dtype=DT_CHAR, repeat='#TAGS', chain='LIST_CHANGED', order=14)
        self.putdef('OpcPutDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', chain='LIST_CHANGED', repeat='#TAGS', order=15)
        self.putdef('OpcPutDef', 'STATUS', dtype=DT_INTEGER, format='WRITE-STATES', repeat='#TAGS', order=16)
        self.put_h_cfg(('OpcPutDef', 'OPC_WRITE_TIME'))
        self.put_h_cfg(('OpcPutDef', 'OPC_WRITE_TIME'))
        for t in self.getlist('OpcPutDef'):
            self.put_h_cfg((t, 'OPC_WRITE_TIME'))

        self.add('IoDeviceDef', DEFINITION_DEF)
        self.putdef('IoDeviceDef', 'DEVICE_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('IoDeviceDef', 'IO_HOST', dtype=DT_CHAR, default='localhost', order=3)
        self.putdef('IoDeviceDef', 'IO_PORT', dtype=DT_CHAR, default='13001', order=4)
        self.putdef('IoDeviceDef', 'IO_ENDIAN', dtype=DT_INTEGER, format='ENDIAN-TYPES', order=5)
        self.putdef('IoDeviceDef', 'IO_GROUP_SIZE', dtype=DT_INTEGER, default=250, order=9)
        self.putdef('IoDeviceDef', 'IO_TIMEOUT', dtype=DT_INTEGER, default=5000, order=11)
        self.putdef('IoDeviceDef', 'TIME_SOURCE', dtype=DT_INTEGER, format='TIME-SOURCES', order=13)
        self.putdef('IoDeviceDef', 'VERBOSITY_LEVEL', dtype=DT_INTEGER, format='VERBOSITY-LEVELS', order=14)
        self.putdef('IoDeviceDef', 'MESSAGE', dtype=DT_CHAR, length=80, chain='TIME', readonly=True, order=15)
        self.putdef('IoDeviceDef', 'TIME', dtype=DT_TIMESTAMP, chain='#MESSAGES', readonly=True, order=16)
        self.put_h_cfg(('IoDeviceDef', 'MESSAGE'), dtype='str100')
        for t in self.getlist('IoDeviceDef'):
            self.put_h_cfg((t, 'MESSAGE'), dtype='str100')

        self.add('IoServer', 'IoDeviceDef')
        self.add('IoGetDef', DEFINITION_DEF)
        self.putdef('IoGetDef', 'GROUP_PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=1)
        self.putdef('IoGetDef', 'DEVICE_TAG', dtype=DT_RECORD, skey='IoDeviceDef', order=2)
        self.putdef('IoGetDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, order=3, reschedule='SCHEDULE_FREQ')
        self.putdef('IoGetDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, order=4)
        self.putdef('IoGetDef', 'DATA_TYPE', dtype=DT_INTEGER, format='IO-DATA-TYPES', order=5)
        self.putdef('IoGetDef', 'GROUP_STATUS', dtype=DT_CHAR, chain='GROUP_TIME', readonly=True, order=6)
        self.putdef('IoGetDef', 'GROUP_TIME', dtype=DT_TIMESTAMP, readonly=True, order=7)
        self.putdef('IoGetDef', 'IO_READ_TIME', dtype=DT_FLOAT, readonly=True, order=8)
        self.putdef('IoGetDef', 'DB_WRITE_TIME', dtype=DT_FLOAT, readonly=True, order=9)
        self.putdef('IoGetDef', 'LIST_CHANGED', dtype=DT_INTEGER, format='NO/YES', readonly=True, order=10)
        self.putdef('IoGetDef', 'REBUILD_GROUP', dtype=DT_INTEGER, format='NO/YES', order=11)
        self.putdef('IoGetDef', '#TAGS', dtype=DT_LIST, order=12, chain='LIST_CHANGED')
        self.putdef('IoGetDef', 'REMOTE_TAG', dtype=DT_CHAR, repeat='#TAGS', chain='LIST_CHANGED', order=13)
        self.putdef('IoGetDef', 'LOCAL_TAG', dtype=DT_FIELD, repeat='#TAGS', chain='LIST_CHANGED', order=14)
        self.putdef('IoGetDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', chain='LIST_CHANGED', repeat='#TAGS', order=15)
        self.putdef('IoGetDef', 'STATUS', dtype=DT_INTEGER, format='QUALITY-STATES', repeat='#TAGS', order=16)
        self.put_h_cfg(('IoGetDef', 'IO_READ_TIME'))
        self.put_h_cfg(('IoGetDef', 'DB_WRITE_TIME'))
        for t in self.getlist('IoGetDef'):
            self.put_h_cfg((t, 'IO_READ_TIME'))
            self.put_h_cfg((t, 'DB_WRITE_TIME'))

        if self.add('GetIoValues', 'IoGetDef'):
            self.put('GetIoValues', 'DEVICE_TAG', 'IoServer')
            self.put('GetIoValues', 'SCHEDULE_TIME', '01/01/2008 00:00:00')
            self.put('GetIoValues', 'SCHEDULE_FREQ', 60)
        self.add('FolderDef', DEFINITION_DEF)
        self.putdef('FolderDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('FolderDef', 'ICON', dtype=DT_RECORD, skey='IconDef', order=2)
        self.putdef('FolderDef', '#RECORDS', dtype=DT_LIST, order=3)
        self.putdef('FolderDef', 'RECORD_NAME', dtype=DT_RECORD, repeat='#RECORDS', order=4)
        self.putdef('FolderDef', 'DISPLAY_NAME', dtype=DT_CHAR, repeat='#RECORDS', order=5)
        self.add('RootFolder', 'FolderDef')
        user_folder_ok = self.add('UserFolder', 'FolderDef')
        self.add('FolderViewDef', DEFINITION_DEF)
        self.putdef('FolderViewDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('FolderViewDef', 'VIEW_RECORD', dtype=DT_RECORD, order=2)
        self.putdef('FolderViewDef', 'SEARCH_ONLY', dtype=DT_INTEGER, format='OFF/ON', order=3)
        self.add('MatplotlibDef', DEFINITION_DEF)
        self.putdef('MatplotlibDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('MatplotlibDef', 'CODE', dtype=DT_CHAR, order=2)
        if self.add('pie_chart', 'MatplotlibDef'):
            self.put('pie_chart', 'DESCRIPTION', 'Pie chart example')
            code_txt = "# Drag this tag into a graphic to see the visualization\nlabels = 'Heavy Crude', 'Light Crude', 'North Slope', 'Other'\nsizes = [15, 30, 45, 10]\ncolors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']\nmatplotlib.rcParams.update({'font.size': 9})\nax = figure.add_subplot(111)\nax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)\n"
            self.put('pie_chart', 'CODE', code_txt)
        self.add('WebLinkDef', DEFINITION_DEF)
        self.putdef('WebLinkDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('WebLinkDef', 'URL', dtype=DT_CHAR, order=2)
        self.add('Google', 'WebLinkDef')
        self.put('Google', 'URL', 'http://www.google.com/')
        self.add('WebPageDef', DEFINITION_DEF)
        self.putdef('WebPageDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('WebPageDef', 'CODE', dtype=DT_CHAR, order=2)
        self.putdef('WebPageDef', '#OUTPUT_LINES', dtype=DT_LIST, default=0, order=12)
        self.putdef('WebPageDef', 'OUTPUT_LINE', dtype=DT_CHAR, repeat='#OUTPUT_LINES', order=13)
        self.add('HistoryReport', 'WebPageDef')
        if True:
            self.put('HistoryReport', 'DESCRIPTION', 'First/last history times')
            code_txt = "html = '<table border=1>'\nhtml += '<tr><th>Tag</th><th>Start</th><th>End</th></tr>'\n\nfor t in db.getlist('Analogs')[:5000]:\n    start = db.first_h_time(t, ascii=True)\n    end = db.last_h_time(t, ascii=True)\n    html += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (t, start, end)\n\nhtml += '</table>'\nreturn html\n"
            self.put('HistoryReport', 'CODE', code_txt)
        self.add('TagReport', 'WebPageDef')
        if True:
            self.put('TagReport', 'DESCRIPTION', 'Web page of all analog tags')
            code_txt = "html = ''\n\nhtml = ''\n\nhtml += '<html>'\nhtml += '<table border=1>'\nhtml += '<tr><th>Name</th><th>Description</th><th>Value</th><th>Time</th></tr>'\n\ntags = db.getlist('AnalogDef')[:5000]\ndescriptions = db.mget(tags, 'DESCRIPTION', ascii=True)\nvalues = db.mget(tags, 'VALUE', ascii=True)\ntimes = db.mget(tags, 'TIME', ascii=True)\n\nfor i,t in enumerate(tags):\n    html += '<tr>'\n    html += '<td>' + t + '</td>'\n    html += '<td>' + descriptions[i] + '</td>'\n    html += '<td>' + values[i] + '</td>'\n    html += '<td>' + times[i] + '</td>'\n    html += '</tr>'\n\nhtml += '</table>'\nhtml += '</html>'\n\nreturn html\n\n"
            self.put('TagReport', 'CODE', code_txt)
        if self.add('DMCWeb', 'WebPageDef'):
            self.put('DMCWeb', 'DESCRIPTION', 'Web view of DMC controller')
            code_txt = "if not vars().has_key('view'):\n    views = [t for t in db.lsname('ViewDef') if db.get(t,'RECORD',ascii=True) == 'DmcDepDef']\n    if len(views) > 0:\n        view = views[0]\n    else:\n        html = '<html>No DMC controllers have been imported</html>'\n        return html\n\ncolumns = db.getlist(view, 'column_field')\n\nhtml = ''\nhtml += '<html>'\nhtml += '<table border=1>'\n\nhtml += '<tr>'\nhtml += '<th>Tag</th>'\nfor col in columns:\n    html += '<th>' + col + '</th>'\nhtml += '</tr>'\n\nfor tag in db.getlist(view):\n    html += '<tr>'\n    html += '<td>' + tag + '</td>'\n\n    for idx in columns:\n        value = db.get(tag, 'value', idx, ascii=True)\n        html += '<td>' + value + '</td>'\n\n    html += '</tr>'\n\nhtml += '</table>'\nhtml += '</html>'\n\nreturn html\n"
            self.put('DMCWeb', 'CODE', code_txt)
        if self.add('Pivot', 'WebPageDef'):
            self.put('Pivot', 'DESCRIPTION', 'DMC Pivot Tool')
            code_txt = '#    http://localhost:8000/pivot\n\ntol=1.0e-11                                     # tolerance for forcing zero in pivor matrix\nenvirom = Historian.os.environ                  # get enviroment variables fro operating system\nscriptname = WEB_TAG                            # name of this script in toolbox\nccfnames = db.getlist(\'DmcControlDef\')          # retrieve list of all imported ccf files\nmdlnames = db.getlist(\'DmcModelDef\')            # retrieve list of all imported mdl files\n\nmytime = db.time2ascii(db.get_current_time())   # get current time\n\nprint scriptname\nprint mytime\n\nwebhost = \'localhost\'\nif envirom.has_key(\'COMPUTERNAME\'):\n    webhost = Historian.os.environ[\'COMPUTERNAME\']           # get name of computer running this script\n\nwebport = 8000\nif envirom.has_key(\'CCI_WEB_PORT\'):\n    webport = int(Historian.os.environ[\'CCI_WEB_PORT\'])      # get port number used by toolbox web server\n\n\nhtml = \'<html>\\n<head>\\n\'                                    # start creating html header\n\nif vars().has_key(\'ccfname\'):\n    html += \'   <title>Pivot analysis for \' + ccfname +\'</title>\\n</head>\\n<body>\\n\\n\'\nelse:\n    html += \'   <title>Pivot tool</title>\\n</head>\\n<body>\\n\'\n    if len(ccfnames)>0:\n        html+=\'<P>The following controllers are available:<P>\\n\'\n        for ccf in ccfnames:\n            html+=\' <LI><A HREF="http://%s:%d/%s?ccfname=%s"> %s </A></LI><br>\\n\' % (webhost,webport,scriptname,ccf,ccf)\n    else:\n        html+=\' <P>No controllers are currently imported into ToolBox\\n\'\n    html += \'</body>\\n</html>\\n\'\n    return html\n\nprint ccfname\n\nccffound=False\nfor ccf in ccfnames:\n    if ccfname==ccf:\n        ccffound=True\n\nif ccffound==False:\n    html+=\'<P> Controller not found: \' + ccfname + \'<P>\\n\'\n    html += \'</body>\\n</html>\\n\'\n    return html\n\nccfvar = db.getdict(ccfname,\'VALUE\')    # retrieve ccf header info\nnmv = int(ccfvar[\'IPMIND\'])             # extract number of mvs\nncv = int(ccfvar[\'IPNDEP\'])             # extract number of cvs\nmdlname = ccfvar[\'MDLNAM\']              # model name from ccf\n\nprint mdlname\n\ngains = db.get(mdlname,\'GAINS\')          # retrive gains as list\n\n\nif gains==None:\n    html+=\'<P> Model not found: \' + mdlname + \'<P>\\n\'\n    html += \'</body>\\n</html>\\n\'\n    return html\n\nhtml += \'<B>Controller Name:</B> \\t %s  <br>\\n<B>MDL Name:</B> \\t %s <br>\\n<P>\\n\\n\'%(ccfname,mdlname)\n\n\n\n# retrive list of all mv\'s and sort by var number\nindvar=[t for t in db.getlist(\'DmcIndDef\') if t.startswith(ccfname) ]\nindvar.sort(lambda x,y: int(db.get(x,\'VALUE\',\'VARNUM\'))-int(db.get(y,\'VALUE\',\'VARNUM\')))\n\n# retrive list of all cv\'s and sort by var number\ndepvar=[t for t in db.getlist(\'DmcDepDef\') if t.startswith(ccfname) ]\ndepvar.sort(lambda x,y: int(db.get(x,\'VALUE\',\'VARNUM\'))-int(db.get(y,\'VALUE\',\'VARNUM\')))\n\n\n# Coding \nindcol=[\'VARNUM\',\'INDSTA\',\'MDLIND\',\'DESCIND\',\'ENGIND\',\'LLINDM\',\'VIND\',\'SSMAN\',\'ULINDM\',\'MANACT\']\ndepcol=[\'VARNUM\',\'DEPSTA\',\'MDLDEP\',\'DESCDEP\',\'ENGDEP\',\'LDEPTG\',\'DEP\', \'SSDEP\',\'UDEPTG\',\'DEPACT\']\n\nindlbl=[\'#\',\'Status\',\'Name\',\'Description\',\'Unit\',\'Low\',\'Value\',\'Target\',\'High\',\'Constraint\']\ndeplbl=[\'#\',\'Status\',\'Name\',\'Description\',\'Unit\',\'Low\',\'Value\',\'Target\',\'High\',\'Constraint\']\n\n\nindsta = {-2:"Eng Off", -1:"Bad", 0:"Good", 1:"Pred Only", 2:"Ready"}\nmanact = { 0:"&nbsp;", 1:"High Limit", 2:"Low Limit", 4:"SS Step ^", 5:"SS Step v", 6:"Min Move", 7:"Setpoint", 8:"Inactive", 20:"ET", 21:"Above ET", 22:"Below ET"}\n\ndepsta = {-2:"Eng Off", -1:"Bad", 0:"Good", 1:"Pred Only", 2:"Use Pred", 3:"Maintain Pred"}\ndepact = { 0:"&nbsp;", 1:"High Limit", 2:"Low Limit", 4:"CV Step ^", 5:"CV Step v", 6:"Min Move", 7:"Setpoint", 9:"Ramp", 11:"Above High", 12:"Below Low", 20:"ET", 21:"Above ET", 22:"Below ET"}\n\n\n# Display MV information\nhtml += \'\\n<B>Manipulated Variables</B>\\n\'\nhtml += \'<table border=1>\\n <tr>\\n\'\nfor col in indlbl:\n    html += \'  <td><b>\' + col + \'</b></td>\\n\'\nhtml += \' </tr>\\n\'\n\nfor i in range(nmv):\n    cnstr = int(db.get(indvar[i], \'value\', \'MANACT\', ascii=True))\n    html += \' <tr>\\n\'\n    for idx in indcol:\n        value = db.get(indvar[i], \'value\', idx, ascii=True)\n\n        if idx==\'INDSTA\':\n            Svalue=indsta[int(value)]\n        elif idx==\'MANACT\':\n            Svalue=manact[int(value)]\n        else:\n            Svalue = value\n\n        Cvalue = \'  <td>\' + Svalue + \'</td>\\n\'\n\n        if (idx==\'LLINDM\') and ((cnstr==2) or (cnstr==7)):\n            Cvalue = \'  <td bgcolor="blue"   align="right"> %s </td> \\n\' % value\n\n        if (idx==\'LLINDM\') and (cnstr==5):\n            Cvalue = \'  <td bgcolor="yellow" align="right"> %s </td> \\n\' % value\n\n        if (idx==\'ULINDM\') and ((cnstr==1) or (cnstr==7)):\n            Cvalue = \'  <td bgcolor="blue"   align="right"> %s </td> \\n\' % value\n\n        if (idx==\'ULINDM\') and (cnstr==4):\n            Cvalue = \'  <td bgcolor="yellow" align="right"> %s </td> \\n\' % value\n\n\n        html += Cvalue\n    html += \' </tr>\\n\'\nhtml += \'</table><P>\\n\\n\'\n\n\n\n# Display CV information\nhtml += \'<B>Controlled Variables</B>\\n\'\nhtml += \'<table border=1>\\n <tr>\\n\'\nfor col in deplbl:\n    html += \'  <td><b>\' + col + \'</b></td>\\n\'\nhtml += \' </tr>\\n\'\n\nfor i in range(ncv):\n    cnstr = int(db.get(depvar[i], \'value\', \'DEPACT\', ascii=True))\n    html += \' <tr>\\n\'\n    for idx in depcol:\n        value = db.get(depvar[i], \'value\', idx, ascii=True)\n\n        if idx==\'DEPSTA\':\n            Svalue=depsta[int(value)]\n        elif idx==\'DEPACT\':\n            Svalue=depact[int(value)]\n        else:\n            Svalue = value\n\n        Cvalue = \'  <td>\' + Svalue + \'</td>\\n\'\n\n        if (idx==\'LDEPTG\') and ((cnstr==2) or (cnstr==7)):\n            Cvalue = \'  <td bgcolor="blue"   align="right"> %s </td> \\n\' % value\n\n        if (idx==\'LDEPTG\') and (cnstr==12):\n            Cvalue = \'  <td bgcolor="red" align="right"> %s </td> \\n\' % value\n\n        if (idx==\'SSDEP\') and ((cnstr==6) or (cnstr==9)):\n            Cvalue = \'  <td bgcolor="blue"   align="right"> %s </td> \\n\' % value\n\n        if (idx==\'UDEPTG\') and ((cnstr==1) or (cnstr==7)):\n            Cvalue = \'  <td bgcolor="blue"   align="right"> %s </td> \\n\' % value\n\n        if (idx==\'UDEPTG\') and (cnstr==11):\n            Cvalue = \'  <td bgcolor="red" align="right"> %s </td> \\n\' % value\n\n        html += Cvalue\n    html += \' </tr>\\n\'\nhtml += \'</table><P>\\n\\n\'\n\n\n\n\n# Constraint Analysis\nMVCNSI = []\nMVFREE = []\nfor i in range(nmv):\n    value = db.get(indvar[i], \'value\', \'MANACT\', ascii=True)\n    j = int(value)\n    if (j!=0)&(j<=20):\n        MVCNSI = MVCNSI + [i]\n    if j==0:\n        MVFREE = MVFREE + [i]\n        \nCVCNSI = []\nCVVIOL = []\nCVMARK = []\nfor i in range(ncv):\n    value = db.get(depvar[i], \'value\', \'DEPACT\', ascii=True)\n    j = int(value)\n    if (j!=0)&(j<=9):\n        CVCNSI = CVCNSI + [i]\n    if (j==11)or(j==12):\n        CVVIOL = CVVIOL + [i]\n    if (j!=0)&(j<=12):\n        CVMARK = CVMARK + [i]\n\nhtml += \'<P><B>Constraint Analysis</B><br>\\n\'\nhtml += \' Number of MV constraints: \' + str(len(MVCNSI)) + \'<br>\\n\'\nhtml += \' Number of CV constraints: \' + str(len(CVCNSI)) + \'<br>\\n\'\nhtml += \' Number of CV violations:  \' + str(len(CVVIOL)) + \'<br>\\n\'\nnconst = len(MVCNSI) + len(CVCNSI)\nif nconst!=nmv:\n    html += \'<br><B>Error - number of constraints does not match number of MVs</B><P>\\n\'\n    html += \'</body></html>\\n\'\n    return html\n\n\n\n# Perform Pivoting\nI = numpy.eye(nmv)\nG = numpy.array(gains)\nG = G[0:nmv,:]\nH = numpy.concatenate((G[:,CVCNSI],I[:,MVCNSI]),1)\n#HH = numpy.concatenate((G,I),1)\n\nP = numpy.dot(numpy.linalg.inv(H),I)  # Pivot for MVs\nfor k in range(0,nmv):\n    for m in range(0,nmv):\n        if abs(P[m,k])<tol:\n            P[m,k]=0.0\n\nQ = numpy.dot(numpy.linalg.inv(H),G)  # Pivot for CVs\nfor k in range(0,ncv):\n    for m in range(0,nmv):\n        if abs(Q[m,k])<tol:\n            Q[m,k]=0.0\n\n\n# Display Results of Pivot Analysis\ncell_start = \'  <td><font size=2><center>\'\ncell_end   = \'</font></center></td>\\n\'\n\n\nhtml += "<P><table border=1 width=100%>\\n"\n\nhtml += \' <tr> <td colspan=4> <B>Pivot Analysis</B> </td>\\n\'\nfor k in range(nmv):\n    html += \'%s MV # %d %s\' % (cell_start, k+1, cell_end)\nfor k in range(ncv):\n    html += \'%s CV # %d %s\' % (cell_start, k+1, cell_end)\nhtml +=\' </tr>\\n\'\n\nhtml += \' <tr> <td colspan=4> &nbsp; </td>\\n\'\nfor k in range(nmv):\n    html += \'%s %s %s \' % (cell_start, db.get(indvar[k], \'value\', \'MDLIND\', ascii=True), cell_end)\nfor k in range(ncv):\n    html += \'%s %s %s \' % (cell_start, db.get(depvar[k], \'value\', \'MDLDEP\', ascii=True), cell_end)\nhtml +=\' </tr>\\n\'\n\nhtml += \' <tr> <td colspan=4> Closed Loop Gains </td>\\n\'\nfor k in range(nmv):\n    html += \'%s %s %s \' % (cell_start, manact[int(db.get(indvar[k], \'value\', \'MANACT\', ascii=True))], cell_end)\nfor k in range(ncv):\n    html += \'%s %s %s \' % (cell_start, depact[int(db.get(depvar[k], \'value\', \'DEPACT\', ascii=True))], cell_end)\nhtml +=\' </tr>\\n\'\n\nfor k in range(len(MVCNSI)):\n    m = MVCNSI[k]\n    tag = indvar[m]\n    statu = int(db.get(tag, \'value\', \'INDSTA\', ascii=True))\n    cnstr = int(db.get(tag, \'value\', \'MANACT\', ascii=True))\n    a = \' <tr>\\n\'\n    a = a + \'%s MV# %d %s \' % (cell_start, m+1, cell_end)\n    a = a + \'%s %s %s \' % (cell_start, indsta[statu], cell_end)\n    a = a + \'%s %s %s \' % (cell_start, db.get(tag, \'value\', \'MDLIND\', ascii=True), cell_end)\n    a = a + \'%s %s %s \' % (cell_start, manact[cnstr], cell_end)\n    for m in range(nmv):\n        pvalue = P[k+len(CVCNSI),m]\n        if abs(pvalue)>tol:\n            if abs(abs(pvalue)-1)<tol:\n                a = a + \'  <td align="right"><b>1.0</b></td>\\n\'\n            else:\n                a = a + \'  <td align="right">%9.5f</td>\\n\' % pvalue\n        else:\n            a = a + \'  <td> &nbsp; </td>\\n\'\n    for m in range(ncv):\n        qvalue = Q[k+len(CVCNSI),m]\n        if abs(qvalue)>tol:\n            if abs(abs(qvalue)-1)<tol:\n                a = a + \'  <td align="right"><b>1.0</b></td>\\n\'\n            else:\n                a = a + \'  <td align="right">%9.5f</td>\\n\' % qvalue\n        else:\n            a = a + \'  <td> &nbsp; </td>\\n\'\n    a = a + \' </tr>\\n\'\n    html += a\n\n\nfor k in range(len(CVCNSI)):\n    icv = CVCNSI[k]\n    tag = depvar[icv]\n    statu = int(db.get(tag, \'value\', \'DEPSTA\', ascii=True))\n    cnstr = int(db.get(tag, \'value\', \'DEPACT\', ascii=True))\n    a = \'<tr>\'\n    a = a + \'%s CV# %d %s \' % (cell_start, m+1, cell_end)\n    a = a + \'%s %s %s \' % (cell_start, depsta[statu], cell_end)\n    a = a + \'%s %s %s \' % (cell_start, db.get(tag, \'value\', \'MDLDEP\', ascii=True), cell_end)\n    a = a + \'%s %s %s \' % (cell_start, depact[cnstr], cell_end)\n    for m in range(nmv):\n        pvalue = P[k,m]\n        if (abs(pvalue)>tol)&(cnstr!=9):\n            if abs(abs(pvalue)-1)<tol:\n                a = a + \'  <td align="right"><b>1.0</b></td>\\n\'\n            else:\n                a = a + \'  <td align="right">%9.5f</td>\\n\' % pvalue\n        else:\n            a = a + \'  <td> &nbsp; </td>\\n\'\n    for m in range(ncv):\n        qvalue = Q[k,m]\n        if (abs(qvalue)>tol)&(cnstr!=9):\n            if abs(abs(qvalue)-1)<tol:\n                a = a + \'  <td align="right"><b>1.0</b></td>\\n\'\n            else:\n                a = a + \'  <td align="right">%9.5f</td>\\n\' % qvalue\n        else:\n            if m==icv:\n                a = a + \'  <td align="right"><b>1.0</b></td>\\n\'\n            else:\n                a = a + \'  <td> &nbsp; </td>\\n\'\n    a = a + \' </tr>\\n\'\n    html += a\nhtml += "</table><P>\\n\\n"\n\nhtml += "<b>Note:</b> Table above shows closed loop gain matrix where variables at constraints are the new independent variables. "\nhtml += "The new dependent variables are all original open loop variables (both independent and dependent).<P>\\n"\n\n\nhtml += mytime + \'\\n\'\n\nhtml += \'\\n</body>\\n</html>\\n\'\n\nreturn html\n\n'
            self.put('Pivot', 'CODE', code_txt)
        for t in self.getlist('NamespaceDef'):
            self.delete(t, delref=True)

        self.delete('NamespaceDef', delref=True)
        self.add('SliceSetDef', DEFINITION_DEF)
        self.putdef('SliceSetDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('SliceSetDef', '#SLICES', dtype=DT_LIST, order=2)
        self.putdef('SliceSetDef', 'SLICE_ID', dtype=DT_INTEGER, repeat='#SLICES', order=3)
        self.putdef('SliceSetDef', 'START_TIME', dtype=DT_TIMESTAMP, repeat='#SLICES', order=4)
        self.putdef('SliceSetDef', 'END_TIME', dtype=DT_TIMESTAMP, repeat='#SLICES', order=5)
        self.putdef('SliceSetDef', 'TAGS', dtype=DT_CHAR, repeat='#SLICES', order=6)
        self.putdef('SliceSetDef', 'CODE', dtype=DT_CHAR, repeat='#SLICES', order=7)
        self.putdef('SliceSetDef', 'ANNOTATION_TEXT', dtype=DT_CHAR, repeat='#SLICES', order=8)
        self.add('Slice Set 1', 'SliceSetDef')
        self.add('Slice Set 2', 'SliceSetDef')
        self.add('Slice Set 3', 'SliceSetDef')
        self.add('DmcModelDef', DEFINITION_DEF)
        self.putdef('DmcModelDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DmcModelDef', 'SS_TIME', dtype=DT_FLOAT, order=2)
        self.putdef('DmcModelDef', '#COEFFICIENTS', dtype=DT_INTEGER, order=3)
        self.putdef('DmcModelDef', '#INDEPENDENTS', dtype=DT_LIST, order=4)
        self.putdef('DmcModelDef', 'IND_NAME', dtype=DT_CHAR, repeat='#INDEPENDENTS', order=5)
        self.putdef('DmcModelDef', 'IND_DESCRIPTION', dtype=DT_CHAR, repeat='#INDEPENDENTS', order=6)
        self.putdef('DmcModelDef', 'IND_UNITS', dtype=DT_CHAR, repeat='#INDEPENDENTS', order=7)
        self.putdef('DmcModelDef', 'TYPICAL_MOVE', dtype=DT_FLOAT, default=1, repeat='#INDEPENDENTS', order=8)
        self.putdef('DmcModelDef', 'RAW_RESPONSE', dtype=DT_MATRIX, repeat='#INDEPENDENTS', order=9)
        self.putdef('DmcModelDef', 'MOD_RESPONSE', dtype=DT_MATRIX, repeat='#INDEPENDENTS', order=10)
        self.putdef('DmcModelDef', '#DEPENDENTS', dtype=DT_LIST, order=11)
        self.putdef('DmcModelDef', 'DEP_NAME', dtype=DT_CHAR, repeat='#DEPENDENTS', order=12)
        self.putdef('DmcModelDef', 'DEP_DESCRIPTION', dtype=DT_CHAR, repeat='#DEPENDENTS', order=13)
        self.putdef('DmcModelDef', 'DEP_UNITS', dtype=DT_CHAR, repeat='#DEPENDENTS', order=14)
        self.putdef('DmcModelDef', 'RAMP_INDICATOR', dtype=DT_INTEGER, default=0, repeat='#DEPENDENTS', order=15)
        self.putdef('DmcModelDef', '#OPERATIONS', dtype=DT_DICTIONARY, order=16)
        self.putdef('DmcModelDef', 'CODE', dtype=DT_CHAR, repeat='#OPERATIONS', order=17)
        self.putdef('DmcModelDef', '#CONSTANTS', dtype=DT_DICTIONARY, order=18)
        self.putdef('DmcModelDef', 'CONSTANT_DESCRIPTION', dtype=DT_CHAR, repeat='#CONSTANTS', order=19)
        self.putdef('DmcModelDef', 'CONSTANT_VALUE', dtype=DT_FLOAT, repeat='#CONSTANTS', order=20)
        self.putdef('DmcModelDef', 'GAINS', dtype=DT_MATRIX, order=21)
        self.add('ModelViewDef', DEFINITION_DEF)
        self.putdef('ModelViewDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('ModelViewDef', 'SCALE_MODE', dtype=DT_INTEGER, format='MODEL-SCALE-MODES', order=2)
        self.putdef('ModelViewDef', 'IND_POSITION', dtype=DT_INTEGER, order=3)
        self.putdef('ModelViewDef', 'DEP_POSITION', dtype=DT_INTEGER, order=4)
        self.putdef('ModelViewDef', 'IND_SIZE', dtype=DT_INTEGER, order=5)
        self.putdef('ModelViewDef', 'DEP_SIZE', dtype=DT_INTEGER, order=6)
        self.putdef('ModelViewDef', '#MODELS', dtype=DT_LIST, order=7)
        self.putdef('ModelViewDef', 'MODEL', dtype=DT_RECORD, repeat='#MODELS', order=8)
        self.putdef('ModelViewDef', '#ANNOTATIONS', dtype=DT_DICTIONARY, order=9)
        self.putdef('ModelViewDef', 'ANNOTATION_TEXT', dtype=DT_CHAR, repeat='#ANNOTATIONS', order=10)
        self.add('DmcControlDef', DEFINITION_DEF)
        self.putdef('DmcControlDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DmcControlDef', '#PARAMETERS', dtype=DT_DICTIONARY, order=2)
        self.putdef('DmcControlDef', 'VALUE', dtype=DT_CHAR, repeat='#PARAMETERS', chain='TIME', order=3)
        self.putdef('DmcControlDef', 'TIME', dtype=DT_TIMESTAMP, repeat='#PARAMETERS', order=4)
        self.putdef('DmcControlDef', 'ACCESS', dtype=DT_CHAR, repeat='#PARAMETERS', order=5)
        self.putdef('DmcControlDef', 'TAG', dtype=DT_CHAR, repeat='#PARAMETERS', order=6)
        self.put('DmcMvDef', 'NAME', 'DmcIndDef')
        self.add('DmcIndDef', DEFINITION_DEF)
        self.putdef('DmcIndDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DmcIndDef', '#PARAMETERS', dtype=DT_DICTIONARY, order=2)
        self.putdef('DmcIndDef', 'VALUE', dtype=DT_CHAR, repeat='#PARAMETERS', time='TIME', chain='TIME', order=3)
        self.putdef('DmcIndDef', 'TIME', dtype=DT_TIMESTAMP, repeat='#PARAMETERS', order=4)
        self.putdef('DmcIndDef', 'ACCESS', dtype=DT_CHAR, repeat='#PARAMETERS', order=5)
        self.putdef('DmcIndDef', 'TAG', dtype=DT_CHAR, repeat='#PARAMETERS', order=6)
        self.put('DmcCvDef', 'NAME', 'DmcDepDef')
        self.add('DmcDepDef', DEFINITION_DEF)
        self.putdef('DmcDepDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('DmcDepDef', '#PARAMETERS', dtype=DT_DICTIONARY, order=2)
        self.putdef('DmcDepDef', 'VALUE', dtype=DT_CHAR, repeat='#PARAMETERS', time='TIME', chain='TIME', order=3)
        self.putdef('DmcDepDef', 'TIME', dtype=DT_TIMESTAMP, repeat='#PARAMETERS', order=4)
        self.putdef('DmcDepDef', 'ACCESS', dtype=DT_CHAR, repeat='#PARAMETERS', order=5)
        self.putdef('DmcDepDef', 'TAG', dtype=DT_CHAR, repeat='#PARAMETERS', order=6)
        self.add('FirIdDef', DEFINITION_DEF)
        self.putdef('FirIdDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('FirIdDef', 'LAST_RUN', dtype=DT_TIMESTAMP, order=2)
        self.putdef('FirIdDef', 'STATUS', dtype=DT_CHAR, order=3)
        self.putdef('FirIdDef', 'MAX_INTERPOLATE', dtype=DT_INTEGER, order=4)
        self.putdef('FirIdDef', 'START_TIME', dtype=DT_TIMESTAMP, order=5)
        self.putdef('FirIdDef', 'END_TIME', dtype=DT_TIMESTAMP, order=6)
        self.putdef('FirIdDef', 'SAMPLE_TIME', dtype=DT_INTEGER, order=7)
        self.putdef('FirIdDef', '#INDEPENDENTS', dtype=DT_LIST, order=8)
        self.putdef('FirIdDef', 'IND_ACTIVE', dtype=DT_INTEGER, format='off/on', default=1, repeat='#INDEPENDENTS', order=9)
        self.putdef('FirIdDef', 'IND_NAME', dtype=DT_RECORD, repeat='#INDEPENDENTS', order=10)
        self.putdef('FirIdDef', 'TYPICAL_MOVE', dtype=DT_FLOAT, repeat='#INDEPENDENTS', order=11)
        self.putdef('FirIdDef', '#DEPENDENTS', dtype=DT_LIST, order=12)
        self.putdef('FirIdDef', 'DEP_ACTIVE', dtype=DT_INTEGER, format='off/on', repeat='#DEPENDENTS', order=13)
        self.putdef('FirIdDef', 'DEP_NAME', dtype=DT_RECORD, repeat='#DEPENDENTS', order=14)
        self.putdef('FirIdDef', 'RAMP_INDICATOR', dtype=DT_INTEGER, repeat='#DEPENDENTS', order=15)
        self.putdef('FirIdDef', 'SHIFT', dtype=DT_INTEGER, repeat='#DEPENDENTS', order=16)
        self.putdef('FirIdDef', '#CASES', dtype=DT_LIST, order=17)
        self.putdef('FirIdDef', 'TTSS', dtype=DT_INTEGER, repeat='#CASES', order=18)
        self.putdef('FirIdDef', 'NCOEFF', dtype=DT_INTEGER, repeat='#CASES', order=19)
        self.putdef('FirIdDef', 'SMOOTH', dtype=DT_FLOAT, repeat='#CASES', order=20)
        self.putdef('FirIdDef', 'STEADY', dtype=DT_INTEGER, repeat='#CASES', order=21)
        self.putdef('FirIdDef', '#BAD_SLICES', dtype=DT_LIST, order=22)
        self.putdef('FirIdDef', 'BAD_ACTIVE', dtype=DT_INTEGER, format='OFF/ON', repeat='#BAD_SLICES', order=23)
        self.putdef('FirIdDef', 'BAD_TAG', dtype=DT_RECORD, repeat='#BAD_SLICES', order=24)
        self.putdef('FirIdDef', 'BAD_START', dtype=DT_TIMESTAMP, repeat='#BAD_SLICES', order=25)
        self.putdef('FirIdDef', 'BAD_END', dtype=DT_TIMESTAMP, repeat='#BAD_SLICES', order=26)
        self.putdef('FirIdDef', 'BAD_ANNOTATION', dtype=DT_CHAR, repeat='#BAD_SLICES', order=27)
        self.putdef('FirIdDef', '#CASE_SLICES', dtype=DT_LIST, order=28)
        self.putdef('FirIdDef', 'CASE_ACTIVE', dtype=DT_INTEGER, format='OFF/ON', repeat='#CASE_SLICES', order=29)
        self.putdef('FirIdDef', 'CASE_TAG', dtype=DT_RECORD, repeat='#CASE_SLICES', order=30)
        self.putdef('FirIdDef', 'CASE_START', dtype=DT_TIMESTAMP, repeat='#CASE_SLICES', order=31)
        self.putdef('FirIdDef', 'CASE_END', dtype=DT_TIMESTAMP, repeat='#CASE_SLICES', order=32)
        self.putdef('FirIdDef', 'CASE_ANNOTATION', dtype=DT_CHAR, repeat='#CASE_SLICES', order=33)
        self.putdef('FirIdDef', '#REPORT_LINES', dtype=DT_LIST, order=34)
        self.putdef('FirIdDef', 'REPORT_LINE', dtype=DT_CHAR, repeat='#REPORT_LINES', order=35)
        self.add('TransformationDef', DEFINITION_DEF)
        self.putdef('TransformationDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('TransformationDef', 'X_TAG', dtype=DT_RECORD, order=2)
        self.putdef('TransformationDef', 'Y_TAG', dtype=DT_RECORD, order=3)
        self.putdef('TransformationDef', 'START_TIME', dtype=DT_TIMESTAMP, order=4)
        self.putdef('TransformationDef', 'END_TIME', dtype=DT_TIMESTAMP, order=5)
        self.putdef('TransformationDef', 'X_SCALE_LOW', dtype=DT_FLOAT, order=6)
        self.putdef('TransformationDef', 'X_SCALE_HIGH', dtype=DT_FLOAT, order=7)
        self.putdef('TransformationDef', 'Y_SCALE_LOW', dtype=DT_FLOAT, order=8)
        self.putdef('TransformationDef', 'Y_SCALE_HIGH', dtype=DT_FLOAT, order=9)
        self.putdef('TransformationDef', 'TRANSFORMATION', dtype=DT_INTEGER, format='X-TRANSFORM-TYPES', order=10)
        self.putdef('TransformationDef', 'PEN_COLOR', dtype=DT_INTEGER, format='X-PEN-COLORS', order=11)
        self.putdef('TransformationDef', 'PEN_SIZE', dtype=DT_INTEGER, format='X-PEN-SIZES', order=12)
        self.putdef('TransformationDef', 'TRANS_SCALE_LOW', dtype=DT_FLOAT, order=13)
        self.putdef('TransformationDef', 'TRANS_SCALE_HIGH', dtype=DT_FLOAT, order=14)
        self.putdef('TransformationDef', 'LIN_ALPHA', dtype=DT_FLOAT, order=15)
        self.putdef('TransformationDef', 'LIN_LOW', dtype=DT_FLOAT, order=16)
        self.putdef('TransformationDef', 'LIN_HIGH', dtype=DT_FLOAT, order=17)
        self.putdef('TransformationDef', 'LIN_OFFSET', dtype=DT_FLOAT, order=18)
        self.putdef('TransformationDef', 'PAR_ALPHA', dtype=DT_FLOAT, order=19)
        self.putdef('TransformationDef', 'PAR_LOW', dtype=DT_FLOAT, order=20)
        self.putdef('TransformationDef', 'PAR_HIGH', dtype=DT_FLOAT, order=21)
        self.putdef('TransformationDef', 'PAR_OFFSET', dtype=DT_FLOAT, order=22)
        self.putdef('TransformationDef', '#OPCHAR_POINTS', dtype=DT_LIST, default=4, order=23)
        self.putdef('TransformationDef', 'OPCHAR_OUT', dtype=DT_FLOAT, repeat='#OPCHAR_POINTS', order=24)
        self.putdef('TransformationDef', 'OPCHAR_IN', dtype=DT_FLOAT, repeat='#OPCHAR_POINTS', order=25)
        self.putdef('TransformationDef', '#PWLIN_POINTS', dtype=DT_LIST, default=11, order=26)
        self.putdef('TransformationDef', 'PWLIN_X', dtype=DT_FLOAT, repeat='#PWLIN_POINTS', order=27)
        self.putdef('TransformationDef', 'PWLIN_Y', dtype=DT_FLOAT, repeat='#PWLIN_POINTS', order=28)
        pred_code = "# default value to return in case there is an error\nlinenum = 0\nt1 = time.time()\nresult = [(t1, 0)] \n\n# logging helper\ndef logtxt(linenum,variable):\n    linenum = linenum + 1\n    db.put(SELF,'#OUTPUT_LINES',linenum)\n    db.put(SELF,'OUTPUT_LINE',variable,linenum)\n    return linenum\n#\n\n\ndef interpol(X):\n    if isnan(X[0]): X[0] = X[isfinite(X)][0]\n    if isnan(X[-1]): X[-1] = X[isfinite(X)][-1]\n\n    t = arange(len(X), dtype=float)\n    t1 = t[isfinite(X)]\n    v1 = X[isfinite(X)]\n    t2 = t[isnan(X)]\n\n    ifunc = interp1d(t1, v1)\n    v2 = ifunc([t2])\n    X[isnan(X)] = v2\n\n    return X\n#\n\ndef mdif(step):\n    ncof = len(step)\n    imp = [0.0]*ncof\n    imp[0] = step[0]\n    for i in range(1,ncof):\n        imp[i] = step[i]-step[i-1]\n    return imp\n#\n\nmsgtxt = 'Prediction: %s  - started at %s'%( db.get(SELF, 'NAME', ascii=True) , db.time2ascii(t1) )\nlinenum = logtxt(linenum,msgtxt)\n\n\nmdlname = db.get(SELF, 'MODEL_NAME', ascii=True) \nif len(mdlname) == 0:\n    linenum = logtxt(linenum,'Error - no model specified')\n    return result\n\n# get info from model\nttss = float(db.get(mdlname,'SS_TIME'))\nncof = int(db.get(mdlname,'#COEFFICIENTS'))\nnind = int(db.get(mdlname,'#INDEPENDENTS'))\nndep = int(db.get(mdlname,'#DEPENDENTS'))\nresp = db.getlist(mdlname, 'MOD_RESPONSE')\nmdl_indinfo = db.getlist(mdlname, ['IND_NAME','IND_DESCRIPTION','IND_UNITS']   )\nmdl_depinfo = db.getlist(mdlname, ['DEP_NAME','DEP_DESCRIPTION','DEP_UNITS','RAMP_INDICATOR']   )\ntsamp = 60.0*ttss/ncof\n\ndepindex = int( db.get(SELF, 'DEP_INDEX') )\nif ( depindex < 1 ) or ( depindex > ndep):\n    msgtxt = 'DEP_INDEX must in range 1 to %d'%( ndep )\n    linenum = logtxt(linenum,msgtxt)\n    return result\n\ndepname = db.get(SELF, 'DEP_NAME', ascii=True) \nif len(depname) == 0:\n    linenum = logtxt(linenum,'Error - no dependent variable specified')\n    return result\n\n\nnindpred = int( db.get(SELF, '#INDEPENDENTS') )\nif ( nindpred < 1 ) or ( nindpred > nind):\n    msgtxt = '#INDEPENDENTS must in range 1 to %d'%( nind )\n    linenum = logtxt(linenum,msgtxt)\n    return result\n\nindinfo = db.getlist(SELF, ['IND_NAME','IND_INDEX','IND_ACTIVE']   )\nfor info in indinfo:\n    k = int(info[1])\n    if ( k < 1 ) or ( k > nind):\n        msgtxt = 'IND_INDEX must in range 1 to %d (%s)'%( nind , info[0])\n        linenum = logtxt(linenum,msgtxt)\n        return result\n    \n\nmsgtxt = 'Modelname used: %s'%( mdlname )\nlinenum = logtxt(linenum,'')\nlinenum = logtxt(linenum,msgtxt)\nmsgtxt = '    TTSS=%f   NCOEF=%d  NIND=%d  NDEP=%d   (TSAMP=%f)'%( ttss, ncof, nind, ndep, tsamp )\nlinenum = logtxt(linenum,msgtxt)\n\n\ninfo = mdl_depinfo[depindex-1][0]\nramp = int(mdl_depinfo[depindex-1][3])\nmsgtxt = '  DEP VEC name: %s (%s/%s)   - Name in MDL: %s   (mdl-index=%d) RAMP=%d'%( depname, db.get(depname, 'DESCRIPTION'), db.get(depname, 'ENG_UNITS') , info, depindex, ramp )\nlinenum = logtxt(linenum,'')\nlinenum = logtxt(linenum,'Vectors used in Prediction')\nlinenum = logtxt(linenum,msgtxt)\n\ntags = [depname]\n\nnindactive = 0\nfor i in range(nindpred):\n    indname =  indinfo[i][0]\n    indindex = int(indinfo[i][1])\n    indactive = indinfo[i][2]\n    if indactive=='ON':\n        tags.append(indname)\n        nindactive = nindactive+1\n    info = mdl_indinfo[indindex-1]\n    msgtxt = '  IND VEC name: %s  (%s/%s) - Name in MDL: %s  (mdl-index=%d)  Active=%s'%(indname, db.get(indname, 'DESCRIPTION'), db.get(indname, 'ENG_UNITS') , info[0], indindex, indactive )\n    linenum = logtxt(linenum,msgtxt)\n\n# Write Sample time\ndb.put(SELF,'CALC_INTERVAL',tsamp)\n\n#get start time\nstarttime = db.get(SELF,'CALC_START')\n\n#get future samples\nnpred = db.get(SELF,'FUTURE_SAMPLES')\nif npred < 0:\n    npred = 0\n\n\n# extract history\nlinenum = logtxt(linenum,'')\nlinenum = logtxt(linenum,'History call results:')\nlinenum = logtxt(linenum,tags)\nx = db.gethis(tags, 'trend_value', start_time=starttime, interval=tsamp, include_time=True)\n\ntimedata=[]\nvecdata=[]\nfor t, values in x:\n    timedata.append(t)\n    vecdata.append(values)\n\ndatalength = len(timedata)\nif datalength < ncof+2:\n    msgtxt = 'Error: not enough data returned (len=%d).  Is start time set correctly?'%(datalength)\n    linenum = logtxt(linenum,msgtxt)\n    return result\n\n\nmsgtxt = '  First Value at: %s   Last Value at: %s    Data Length: %d'%( db.time2ascii(timedata[0]), db.time2ascii(timedata[-1]), datalength )\nlinenum = logtxt(linenum,msgtxt)\n\nt2 = time.time()\nmsgtxt = '  History Retrival Complete at: %s    - duration: %f sec'%( db.time2ascii(t) , t2-t1 )\nlinenum = logtxt(linenum,msgtxt)\n\n\n# create return vector and return time stamps\ndlen    = datalength+npred\ninitval = vecdata[0][0]\ndeppred = zeros(dlen) + initval\n\n\nfor k in range(npred):\n    t = timedata[-1] + tsamp\n    timedata.append(t)\n    vecdata.append( vecdata[-1][:] )  # append same value - i.e. assume no move\n\ndataarray = numpy.array(vecdata,float)\n\ncvraw   = interpol(dataarray[:,0])\ncvval   = cvraw[0]\nif ramp > 0:\n    cvraw = lfilter([1,-1],[1,0],cvraw-cvval)\n    lastslope = cvraw[-npred-1]\n    for k in range(npred):\n        cvraw[-npred+k] = lastslope\n    cvraw = cvraw+cvval\n\n\n\nlinenum = logtxt(linenum,'')\nmsgtxt = 'Processing %d Independent Contributions'%(nindactive)\nlinenum = logtxt(linenum, msgtxt)\n\nidata = 0\nfor k in range(nindpred):\n    indactive = indinfo[k][2]\n    if indactive=='ON':\n        mv = interpol(dataarray[:,idata+1])\n        mvval = mv[0]\n        mvdel = mv - mvval \n        cvdel = zeros(dlen)\n        mvindex = int(indinfo[k][1])\n        mvname = indinfo[k][0]\n\n        step = resp[mvindex-1][depindex-1][:]\n        imp = mdif(step)\n        if ramp > 0:\n            imp = mdif(imp)\n\n        qsum = sum(abs(array(step)))\n        msgtxt = '  k=%d   len=%d  init-val=%f  mdl-index=%d   finalval=%f  name=%s  qsum=%f '%( k, len(mvdel), mvval, mvindex, step[-1], mvname, qsum )\n        linenum = logtxt(linenum,msgtxt)\n\n        if qsum > 1.0e-12:  # only perform calculations if no curves are present\n\n            b=numpy.array(imp)\n            a=numpy.zeros(ncof)\n            a[0] = 1\n\n            mvdel = hstack( (zeros(ncof) , mvdel) )   # append ncof zeros (i.e. assume steady)\n            cvdel = lfilter(b,a,mvdel)                # calculate response using scipy lfilter function\n            cvdel = cvdel[ncof:]                      # chop off first ncof elements\n\n            deppred = deppred + cvdel \n        idata = idata + 1\n\n#\n# prediction error filtering\n#\nprederrfilt = 0.0*deppred\ntfilt = db.get(SELF, 'PRED_ERR_FILTER')\nif tfilt <= 0:\n    frac = 0\nelse:\n    frac = exp( -(tsamp/60)/tfilt )\n    msgtxt = 'Applying Prediction Error filtering.  Filter Factor = %f '%(frac)\n    linenum = logtxt(linenum, msgtxt)\n\nif frac > 0:\n    prederr = cvraw - deppred                # calculate prediction error\n    if npred > 0:\n        prederr[-npred:] = prederr[-npred-1] # freeze prediction error in future\n\n        a=[1.0 , -frac]\n        b=[1-frac, 0.0]\n        prederrfilt = lfilter(b,a,prederr)\n\n\ndeppred = deppred + prederrfilt\n\n\n\nif ramp > 0:\n    inival = deppred[0]\n    nlen = len(deppred)\n    deppred = deppred - inival\n    temp = zeros(nlen)\n    temp[0] = deppred[0]\n    for k in range(1,nlen):\n        temp[k] = temp[k-1] + deppred[k]\n    deppred = temp + inival\n\n\nresult = zip(timedata,list(deppred))    # put result in the correct format\n\n\nt2 = time.time()\nmsgtxt = 'Prediction: first=%f  last=%f  - vector length = %d '%(deppred[0],deppred[-1], len(deppred))\nlinenum = logtxt(linenum, msgtxt)\nmsgtxt = 'Prediction complete at %s  -   %f seconds  '%( db.time2ascii(t2), t2-t1 )\nlinenum = logtxt(linenum,'')\nlinenum = logtxt(linenum,msgtxt)\n\nreturn result\n"
        self.add('PredictionDef', DEFINITION_DEF)
        self.putdef('PredictionDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('PredictionDef', 'ENG_UNITS', dtype=DT_CHAR, order=2)
        self.putdef('PredictionDef', 'MODEL_NAME', dtype=DT_RECORD, skey='DmcModelDef', order=3)
        self.putdef('PredictionDef', 'DEP_NAME', dtype=DT_RECORD, skey='AnalogDef', order=4)
        self.putdef('PredictionDef', 'DEP_INDEX', dtype=DT_INTEGER, order=5)
        self.putdef('PredictionDef', 'PRED_ERR_FILTER', dtype=DT_FLOAT, default=0, order=6)
        self.putdef('PredictionDef', 'CALC_START', dtype=DT_TIMESTAMP, order=7)
        self.putdef('PredictionDef', 'CALC_INTERVAL', dtype=DT_INTEGER, readonly=True, order=8)
        self.putdef('PredictionDef', 'FUTURE_SAMPLES', dtype=DT_INTEGER, order=9)
        self.putdef('PredictionDef', 'CODE', dtype=DT_CHAR, default=pred_code, order=10)
        self.putdef('PredictionDef', '#INDEPENDENTS', dtype=DT_LIST, default=0, order=11)
        self.putdef('PredictionDef', 'IND_NAME', dtype=DT_RECORD, repeat='#INDEPENDENTS', skey='AnalogDef', order=12)
        self.putdef('PredictionDef', 'IND_INDEX', dtype=DT_INTEGER, repeat='#INDEPENDENTS', order=13)
        self.putdef('PredictionDef', 'IND_ACTIVE', dtype=DT_INTEGER, format='off/on', repeat='#INDEPENDENTS', default=1, order=14)
        self.putdef('PredictionDef', '#OUTPUT_LINES', dtype=DT_LIST, default=0, order=15)
        self.putdef('PredictionDef', 'OUTPUT_LINE', dtype=DT_CHAR, repeat='#OUTPUT_LINES', order=16)
        self.deldef('PredictionDef', '#VALUES')
        self.deldef('PredictionDef', 'TREND_TIME')
        self.deldef('PredictionDef', 'TREND_VALUE')
        self.deldef('PredictionDef', 'TREND_QUALITY')
        for t in self.getlist('DataSourceDef'):
            self.delete(t, delref=True)

        self.delete('DataSourceDef', delref=True)
        self.add('TagListDef', DEFINITION_DEF)
        self.putdef('TagListDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('TagListDef', '#TAGS', dtype=DT_LIST, order=2)
        self.putdef('TagListDef', 'TAG', dtype=DT_FIELD, repeat='#TAGS', order=3)
        self.add('LdapServerDef', DEFINITION_DEF)
        self.putdef('LdapServerDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('LdapServerDef', 'LDAP_HOST', dtype=DT_CHAR, order=2)
        self.putdef('LdapServerDef', 'LDAP_PORT', dtype=DT_CHAR, default=389, order=3)
        self.putdef('LdapServerDef', 'BIND_DN', dtype=DT_CHAR, order=4)
        self.add('UserRoleDef', DEFINITION_DEF)
        self.putdef('UserRoleDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('UserRoleDef', 'MENU_TREE', dtype=DT_RECORD, skey='FolderDef', order=2)
        self.putdef('UserRoleDef', 'BASE_POLICY', dtype=DT_INTEGER, format='USER-BASE-POLICIES', order=3)
        self.putdef('UserRoleDef', '#RULES', dtype=DT_LIST, order=4)
        self.putdef('UserRoleDef', 'TAG', dtype=DT_RECORD, repeat='#RULES', order=5)
        self.putdef('UserRoleDef', 'SCOPE', dtype=DT_INTEGER, format='SCOPE-TYPES', repeat='#RULES', order=6)
        self.putdef('UserRoleDef', 'READ', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=7)
        self.putdef('UserRoleDef', 'WRITE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=8)
        self.putdef('UserRoleDef', 'CREATE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=9)
        self.putdef('UserRoleDef', 'DELETE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=10)
        self.add('UserDef', DEFINITION_DEF)
        self.putdef('UserDef', 'FULL_NAME', dtype=DT_CHAR, order=1)
        self.putdef('UserDef', 'PASSWORD', dtype=DT_CHAR, order=2)
        self.putdef('UserDef', 'EMAIL_ADDRESS', dtype=DT_CHAR, order=3)
        self.putdef('UserDef', 'LDAP_SERVER', dtype=DT_RECORD, skey='LdapServerDef', order=4)
        self.putdef('UserDef', 'BASE_ROLE', dtype=DT_RECORD, skey='UserRoleDef', order=5)
        self.putdef('UserDef', '#RULES', dtype=DT_LIST, order=7)
        self.putdef('UserDef', 'TAG', dtype=DT_RECORD, repeat='#RULES', order=8)
        self.putdef('UserDef', 'SCOPE', dtype=DT_INTEGER, format='SCOPE-TYPES', repeat='#RULES', order=9)
        self.putdef('UserDef', 'READ', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=10)
        self.putdef('UserDef', 'WRITE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=11)
        self.putdef('UserDef', 'CREATE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=12)
        self.putdef('UserDef', 'DELETE', dtype=DT_INTEGER, format='NO/YES', repeat='#RULES', order=13)
        self.add('UserGroupDef', DEFINITION_DEF)
        self.putdef('UserGroupDef', 'DESCRIPTION', dtype=DT_CHAR, order=2)
        self.putdef('UserGroupDef', '#USERS', dtype=DT_LIST, order=3)
        self.putdef('UserGroupDef', 'USER', dtype=DT_RECORD, repeat='#USERS', skey='UserDef', order=4)
        self.add('NotifyTaskDef', DEFINITION_DEF)
        self.putdef('NotifyTaskDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('NotifyTaskDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=2)
        self.putdef('NotifyTaskDef', 'SCHEDULE_TIME', dtype=DT_SCHEDULE, reschedule='SCHEDULE_FREQ', order=3)
        self.putdef('NotifyTaskDef', 'SCHEDULE_FREQ', dtype=DT_INTEGER, default=60, order=4)
        self.putdef('NotifyTaskDef', 'USE_TLS', dtype=DT_INTEGER, format='NO/YES', order=5)
        self.putdef('NotifyTaskDef', 'SMTP_SERVER', dtype=DT_CHAR, order=6)
        self.putdef('NotifyTaskDef', 'USERNAME', dtype=DT_CHAR, order=7)
        self.putdef('NotifyTaskDef', 'PASSWORD', dtype=DT_CHAR, order=8)
        self.putdef('NotifyTaskDef', 'HOLD_OFF_TIME', dtype=DT_INTEGER, default=60, order=9)
        self.putdef('NotifyTaskDef', 'MESSAGE', dtype=DT_CHAR, chain='TIME', readonly=True, order=10)
        self.putdef('NotifyTaskDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=11)
        if self.add('NotifyTask', 'NotifyTaskDef'):
            self.put('NotifyTask', 'SCHEDULE_TIME', '01/01/2000 00:00:00')
        self.add('NotifyRuleDef', DEFINITION_DEF)
        self.putdef('NotifyRuleDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('NotifyRuleDef', 'TASK_TAG', dtype=DT_RECORD, default='NotifyTask', skey='NotifyTaskDef', order=2)
        self.putdef('NotifyRuleDef', 'PROCESSING', dtype=DT_INTEGER, format='OFF/ON', order=3)
        self.putdef('NotifyRuleDef', 'STATUS', dtype=DT_CHAR, chain='TIME', readonly=True, order=4)
        self.putdef('NotifyRuleDef', 'TIME', dtype=DT_TIMESTAMP, readonly=True, order=5)
        self.putdef('NotifyRuleDef', 'CODE', dtype=DT_CHAR, order=6)
        self.putdef('NotifyRuleDef', 'MESSAGE_TEXT', dtype=DT_CHAR, order=7)
        self.putdef('NotifyRuleDef', '#TAGS', dtype=DT_LIST, order=8)
        self.putdef('NotifyRuleDef', 'TAG', dtype=DT_RECORD, repeat='#TAGS', order=9)
        self.putdef('NotifyRuleDef', 'NOTIFY_TIME', dtype=DT_TIMESTAMP, repeat='#TAGS', order=10)
        self.putdef('NotifyRuleDef', 'ALARM_STATE', dtype=DT_INTEGER, default=0, repeat='#TAGS', order=11)
        self.putdef('NotifyRuleDef', '#USERS', dtype=DT_LIST, order=12)
        self.putdef('NotifyRuleDef', 'USER', dtype=DT_RECORD, repeat='#USERS', order=13)
        self.put('EventLogDef', 'NAME', 'TableDef')
        self.add('TableDef', DEFINITION_DEF)
        self.putdef('TableDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('TableDef', 'POPULATE_FUNCTION', dtype=DT_RECORD, skey='FunctionDef', order=2)
        self.putdef('TableDef', 'POST_FUNCTION', dtype=DT_RECORD, skey='FunctionDef', order=3)
        self.putdef('TableDef', '#COLUMNS', dtype=DT_LIST, order=4)
        self.putdef('TableDef', 'COLUMN_LABEL', dtype=DT_CHAR, repeat='#COLUMNS', order=5)
        self.putdef('TableDef', 'COLUMN_WIDTH', dtype=DT_INTEGER, repeat='#COLUMNS', default=100, order=6)
        self.putdef('TableDef', '#SEARCHES', dtype=DT_LIST, order=7)
        self.putdef('TableDef', 'SEARCH_LABEL', dtype=DT_CHAR, repeat='#SEARCHES', order=8)
        self.putdef('TableDef', 'SEARCH_WIDGET', dtype=DT_INTEGER, format='SEARCH-WIDGETS', repeat='#SEARCHES', order=9)
        self.putdef('TableDef', 'SEARCH_WIDTH', dtype=DT_INTEGER, repeat='#SEARCHES', default=-1, order=10)
        self.putdef('TableDef', 'SEARCH_FORMAT', dtype=DT_CHAR, repeat='#SEARCHES', order=11)
        self.putdef('TableDef', 'SEARCH_FUNCTION', dtype=DT_RECORD, repeat='#SEARCHES', skey='FunctionDef', order=12)
        self.putdef('TableDef', 'SEARCH_VALUE', dtype=DT_CHAR, repeat='#SEARCHES', order=13)
        self.putdef('TableDef', '#ACTIONS', dtype=DT_LIST, order=14)
        self.putdef('TableDef', 'ACTION_LABEL', dtype=DT_CHAR, repeat='#ACTIONS', order=15)
        self.putdef('TableDef', 'ACTION_FUNCTION', dtype=DT_RECORD, skey='FunctionDef', repeat='#ACTIONS', order=16)
        self.add('GraphicDef', DEFINITION_DEF)
        self.putdef('GraphicDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('GraphicDef', 'DATA', dtype=DT_CHAR, hidden=True, order=2)
        self.putdef('GraphicDef', 'ZOOM_LEVEL', dtype=DT_INTEGER, order=3)
        self.putdef('GraphicDef', 'GRADIENT_FILL', dtype=DT_INTEGER, format='NO/YES', order=4)
        self.putdef('GraphicDef', 'GRADIENT_DIRECTION', dtype=DT_INTEGER, format='HORIZONTAL/VERTICAL', order=5)
        self.putdef('GraphicDef', 'GRADIENT_COLOR1', dtype=DT_CHAR, order=6)
        self.putdef('GraphicDef', 'GRADIENT_COLOR2', dtype=DT_CHAR, order=7)
        self.putdef('GraphicDef', 'BACKGROUND_COLOR', dtype=DT_CHAR, order=8)
        self.putdef('GraphicDef', 'OWNER', dtype=DT_RECORD, readonly=True, skey='UserDef', order=9)
        self.putdef('GraphicDef', 'SAVE_TIME', dtype=DT_TIMESTAMP, readonly=True, order=10)
        self.putdef('GraphicDef', '#SCRIPTS', dtype=DT_LIST, order=11)
        self.putdef('GraphicDef', 'SCRIPT', dtype=DT_RECORD, repeat='#SCRIPTS', skey='GraphicScriptDef', order=12)
        self.putdef('GraphicDef', 'RUN_ON_OPEN', dtype=DT_INTEGER, format='NO/YES', repeat='#SCRIPTS', order=13)
        self.putdef('GraphicDef', '#TAGS', dtype=DT_LIST, order=13)
        self.putdef('GraphicDef', 'TAG', dtype=DT_RECORD, repeat='#TAGS', order=14)
        self.add('SymbolDef', DEFINITION_DEF)
        self.putdef('SymbolDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('SymbolDef', 'DATA', dtype=DT_CHAR, hidden=True, order=2)
        if self.type('PlotDef', 'TAG') == DT_RECORD:
            saved_tags = dict([ (t, self.getlist(t, 'TAG')) for t in self.getlist('PlotDef') ])
        else:
            saved_tags = None
        self.add('PlotDef', DEFINITION_DEF)
        self.putdef('PlotDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.putdef('PlotDef', 'NUMBER_ROWS', dtype=DT_INTEGER, order=2)
        self.putdef('PlotDef', 'NUMBER_COLUMNS', dtype=DT_INTEGER, order=3)
        self.putdef('PlotDef', 'TAGS_PER_PLOT', dtype=DT_INTEGER, default=3, order=4)
        self.putdef('PlotDef', 'TAGS_PER_XY', dtype=DT_INTEGER, order=5)
        self.putdef('PlotDef', 'START_INDEX', dtype=DT_INTEGER, order=6)
        self.putdef('PlotDef', 'CHART_TYPE', dtype=DT_INTEGER, format='CHART-TYPES', order=7)
        self.putdef('PlotDef', 'CHART_LEGEND', dtype=DT_INTEGER, format='CHART-LEGENDS', order=8)
        self.putdef('PlotDef', 'GRID_COLOR', dtype=DT_CHAR, order=9)
        self.putdef('PlotDef', 'BACKGROUND_COLOR', dtype=DT_CHAR, order=10)
        self.putdef('PlotDef', 'GRADIENT_COLOR', dtype=DT_CHAR, order=11)
        self.putdef('PlotDef', 'GRADIENT_FILL', dtype=DT_INTEGER, format='OFF/ON', order=12)
        self.putdef('PlotDef', 'REPEAT_COLORS', dtype=DT_INTEGER, format='OFF/ON', order=13)
        self.putdef('PlotDef', 'DUAL_AXIS', dtype=DT_INTEGER, format='OFF/ON', order=14)
        self.putdef('PlotDef', 'START_TIME', dtype=DT_TIMESTAMP, order=15)
        self.putdef('PlotDef', 'END_TIME', dtype=DT_TIMESTAMP, order=16)
        self.putdef('PlotDef', 'LIVE_TIMESPAN', dtype=DT_INTEGER, order=17)
        self.putdef('PlotDef', 'SHOW_PLOT', dtype=DT_INTEGER, format='OFF/ON', order=18)
        self.putdef('PlotDef', 'SHOW_LEGEND', dtype=DT_INTEGER, format='OFF/ON', order=19)
        self.putdef('PlotDef', 'SHOW_TIMELINE', dtype=DT_INTEGER, format='OFF/ON', order=20)
        self.putdef('PlotDef', 'OWNER', dtype=DT_RECORD, readonly=True, skey='UserDef', order=21)
        self.putdef('PlotDef', 'SAVE_TIME', dtype=DT_TIMESTAMP, readonly=True, order=22)
        self.putdef('PlotDef', '#TAGS', dtype=DT_LIST, order=23)
        self.putdef('PlotDef', 'TAG', dtype=DT_FIELD, repeat='#TAGS', order=24)
        self.putdef('PlotDef', 'TAG_TEXT', dtype=DT_CHAR, repeat='#TAGS', order=25)
        self.putdef('PlotDef', 'TAG_ID', dtype=DT_INTEGER, repeat='#TAGS', order=26)
        self.putdef('PlotDef', 'AUTOSCALE', dtype=DT_INTEGER, repeat='#TAGS', format='OFF/ON', order=27)
        self.putdef('PlotDef', 'LOW_SCALE', dtype=DT_FLOAT, repeat='#TAGS', order=28)
        self.putdef('PlotDef', 'HIGH_SCALE', dtype=DT_FLOAT, repeat='#TAGS', order=29)
        self.putdef('PlotDef', 'LINE_COLOR', dtype=DT_CHAR, repeat='#TAGS', order=30)
        self.putdef('PlotDef', 'LINE_STYLE', dtype=DT_CHAR, repeat='#TAGS', order=31)
        self.putdef('PlotDef', 'LINE_SIZE', dtype=DT_INTEGER, repeat='#TAGS', order=32)
        self.putdef('PlotDef', 'MARKER_COLOR', dtype=DT_CHAR, repeat='#TAGS', order=33)
        self.putdef('PlotDef', 'MARKER_STYLE', dtype=DT_CHAR, repeat='#TAGS', order=34)
        self.putdef('PlotDef', 'MARKER_SIZE', dtype=DT_INTEGER, repeat='#TAGS', order=35)
        self.putdef('PlotDef', 'BORDER_SIZE', dtype=DT_INTEGER, repeat='#TAGS', order=36)
        self.putdef('PlotDef', 'ALPHA', dtype=DT_INTEGER, repeat='#TAGS', order=37)
        self.putdef('PlotDef', 'FUNCTION', dtype=DT_CHAR, repeat='#TAGS', order=38)
        self.putdef('PlotDef', 'INTERVAL', dtype=DT_INTEGER, repeat='#TAGS', order=39)
        self.putdef('PlotDef', 'SHIFT_SECONDS', dtype=DT_INTEGER, repeat='#TAGS', order=40)
        self.putdef('PlotDef', 'LIMIT_COLOR', dtype=DT_CHAR, repeat='#TAGS', order=41)
        self.putdef('PlotDef', 'LIMIT_STYLE', dtype=DT_CHAR, repeat='#TAGS', order=42)
        self.putdef('PlotDef', 'LIMIT_SIZE', dtype=DT_INTEGER, repeat='#TAGS', order=43)
        self.putdef('PlotDef', 'LIMIT_LOW', dtype=DT_CHAR, repeat='#TAGS', order=44)
        self.putdef('PlotDef', 'LIMIT_HIGH', dtype=DT_CHAR, repeat='#TAGS', order=45)
        self.putdef('PlotDef', 'SCALE_GROUP', dtype=DT_CHAR, repeat='#TAGS', order=46)
        self.putdef('PlotDef', 'PLOT_NUMBER', dtype=DT_INTEGER, repeat='#TAGS', order=47)
        self.putdef('PlotDef', '#SCOOTERS', dtype=DT_LIST, order=48)
        self.putdef('PlotDef', 'SCOOTER_START', dtype=DT_TIMESTAMP, repeat='#SCOOTERS', order=49)
        self.putdef('PlotDef', 'SCOOTER_END', dtype=DT_TIMESTAMP, repeat='#SCOOTERS', order=50)
        self.putdef('PlotDef', 'SCOOTER_TAGS', dtype=DT_RECORD, repeat='#SCOOTERS', order=51)
        self.putdef('PlotDef', 'SCOOTER_FUNCTIONS', dtype=DT_CHAR, repeat='#SCOOTERS', order=52)
        self.putdef('PlotDef', 'CATEGORY', dtype=DT_INTEGER, repeat='#SCOOTERS', format='LOGBOOK-CATEGORIES', order=53)
        self.putdef('PlotDef', 'ANNOTATION_TEXT', dtype=DT_CHAR, repeat='#SCOOTERS', order=54)
        self.putdef('PlotDef', '#PLOTS', dtype=DT_LIST, order=55)
        self.putdef('PlotDef', 'PLOT_TITLE', dtype=DT_CHAR, repeat='#PLOTS', order=56)
        x = [ self.put(p, 'SCOOTER_START', t, i + 1) for p in self.getlist('PlotDef') for i, t in enumerate(self.getlist(p, 'TIME')) ]
        self.deldef('PlotDef', 'TIME')
        if saved_tags:
            for t, values in saved_tags.iteritems():
                self.putlist((t, 'TAG'), [ v + ' VALUE' for v in values ], notify=True)

        self.add('ViewDef', DEFINITION_DEF)
        self.putdef('ViewDef', 'DESCRIPTION', dtype=DT_CHAR, order=1)
        self.deldef('ViewDef', 'DATA_SOURCE')
        self.putdef('ViewDef', 'RECORD', dtype=DT_RECORD, order=3)
        self.putdef('ViewDef', '#COLUMNS', dtype=DT_LIST, order=4)
        self.putdef('ViewDef', 'COLUMN_FIELD', dtype=DT_RECORD, repeat='#COLUMNS', order=5)
        self.putdef('ViewDef', '#SEARCHES', dtype=DT_LIST, order=6)
        self.putdef('ViewDef', 'SEARCH_FIELD', dtype=DT_RECORD, repeat='#SEARCHES', order=7)
        self.putdef('ViewDef', 'SEARCH_OPERATOR', dtype=DT_CHAR, repeat='#SEARCHES', order=8)
        self.putdef('ViewDef', 'SEARCH_VALUE', dtype=DT_CHAR, repeat='#SEARCHES', order=9)
        self.putdef('ViewDef', '#SORTS', dtype=DT_LIST, order=10)
        self.putdef('ViewDef', 'SORT_FIELD', dtype=DT_RECORD, repeat='#SORTS', order=11)
        self.putdef('ViewDef', 'SORT_DIRECTION', dtype=DT_INTEGER, repeat='#SORTS', order=12)
        if self.add('AnalogView', 'ViewDef'):
            self.put('AnalogView', 'DESCRIPTION', 'Analogs tabular view')
            self.put('AnalogView', 'RECORD', 'AnalogDef')
            self.put('AnalogView', '#COLUMNS', 2)
            self.put('AnalogView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('AnalogView', 'COLUMN_FIELD', 'ENG_UNITS', 2)
        if self.add('DigitalView', 'ViewDef'):
            self.put('DigitalView', 'DESCRIPTION', 'Digitals tabular view')
            self.put('DigitalView', 'RECORD', 'DiscreteDef')
            self.put('DigitalView', '#COLUMNS', 1)
            self.put('DigitalView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
        if self.add('CalcView', 'ViewDef'):
            self.put('CalcView', 'DESCRIPTION', 'Calculations tabular view')
            self.put('CalcView', 'RECORD', 'CalculationDef')
            self.put('CalcView', '#COLUMNS', 3)
            self.put('CalcView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('CalcView', 'COLUMN_FIELD', 'ENG_UNITS', 2)
            self.put('CalcView', 'COLUMN_FIELD', 'CODE', 3)
        if self.add('FunctionView', 'ViewDef'):
            self.put('FunctionView', 'DESCRIPTION', 'Functions tabular view')
            self.put('FunctionView', 'RECORD', 'FunctionDef')
            self.put('FunctionView', '#COLUMNS', 1)
            self.put('FunctionView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
        if self.add('ModelView', 'ViewDef'):
            self.put('ModelView', 'DESCRIPTION', 'DMC Models tabular view')
            self.put('ModelView', 'RECORD', 'DmcModelDef')
            self.put('ModelView', '#COLUMNS', 3)
            self.put('ModelView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('ModelView', 'COLUMN_FIELD', 'SS_TIME', 2)
            self.put('ModelView', 'COLUMN_FIELD', '#COEFFICIENTS', 3)
        if self.add('ModelViewView', 'ViewDef'):
            self.put('ModelViewView', 'DESCRIPTION', '')
            self.put('ModelViewView', 'RECORD', 'ModelViewDef')
            self.put('ModelViewView', '#COLUMNS', 1)
            self.put('ModelViewView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
        if self.add('SliceSetView', 'ViewDef'):
            self.put('SliceSetView', 'DESCRIPTION', '')
            self.put('SliceSetView', 'RECORD', 'SliceSetDef')
            self.put('SliceSetView', '#COLUMNS', 2)
            self.put('SliceSetView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('SliceSetView', 'COLUMN_FIELD', '#SLICES', 2)
        if self.add('PlotView', 'ViewDef'):
            self.put('PlotView', 'DESCRIPTION', 'Plots tabular view')
            self.put('PlotView', 'RECORD', 'PlotDef')
            self.put('PlotView', '#COLUMNS', 4)
            self.put('PlotView', 'COLUMN_FIELD', 'SAVE_TIME', 1)
            self.put('PlotView', 'COLUMN_FIELD', 'CHART_TYPE', 2)
            self.put('PlotView', 'COLUMN_FIELD', '#TAGS', 3)
            self.put('PlotView', 'COLUMN_FIELD', 'DESCRIPTION', 4)
        if self.add('MyPlotView', 'ViewDef'):
            self.put('MyPlotView', 'DESCRIPTION', 'Personal plots view')
            self.put('MyPlotView', 'RECORD', 'PlotDef')
            self.put('MyPlotView', '#SEARCHES', 1)
            self.put('MyPlotView', 'SEARCH_FIELD', 'OWNER', 1)
            self.put('MyPlotView', 'SEARCH_OPERATOR', '=', 1)
            self.put('MyPlotView', 'SEARCH_VALUE', '{login}', 1)
        if self.add('MyGraphicView', 'ViewDef'):
            self.put('MyGraphicView', 'DESCRIPTION', 'Personal graphics view')
            self.put('MyGraphicView', 'RECORD', 'GraphicDef')
            self.put('MyGraphicView', '#SEARCHES', 1)
            self.put('MyGraphicView', 'SEARCH_FIELD', 'OWNER', 1)
            self.put('MyGraphicView', 'SEARCH_OPERATOR', '=', 1)
            self.put('MyGraphicView', 'SEARCH_VALUE', '{login}', 1)
        if self.add('MatplotlibView', 'ViewDef'):
            self.put('MatplotlibView', 'DESCRIPTION', 'Matplotlib tabular view')
            self.put('MatplotlibView', 'RECORD', 'MatplotlibDef')
        if self.add('GraphicView', 'ViewDef'):
            self.put('GraphicView', 'DESCRIPTION', 'Graphics tabular view')
            self.put('GraphicView', 'RECORD', 'GraphicDef')
            self.put('GraphicView', '#COLUMNS', 2)
            self.put('GraphicView', 'COLUMN_FIELD', 'SAVE_TIME', 1)
            self.put('GraphicView', 'COLUMN_FIELD', 'DESCRIPTION', 2)
        if self.add('SymbolView', 'ViewDef'):
            self.put('SymbolView', 'DESCRIPTION', 'Graphic symbols view')
            self.put('SymbolView', 'RECORD', 'SymbolDef')
            self.put('SymbolView', '#COLUMNS', 1)
            self.put('SymbolView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
        if self.add('ViewView', 'ViewDef'):
            self.put('ViewView', 'DESCRIPTION', 'Views tabular view')
            self.put('ViewView', 'RECORD', 'ViewDef')
            self.put('ViewView', '#COLUMNS', 2)
            self.put('ViewView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('ViewView', 'COLUMN_FIELD', 'RECORD', 2)
        if self.add('WebLinkView', 'ViewDef'):
            self.put('WebLinkView', 'RECORD', 'WebLinkDef')
            self.put('WebLinkView', '#COLUMNS', 2)
            self.put('WebLinkView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('WebLinkView', 'COLUMN_FIELD', 'URL', 2)
        if self.add('WebPageView', 'ViewDef'):
            self.put('WebPageView', 'RECORD', 'WebPageDef')
            self.put('WebPageView', '#COLUMNS', 1)
            self.put('WebPageView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
        if self.add('ScriptView', 'ViewDef'):
            self.put('ScriptView', 'RECORD', 'ScriptDef')
            self.put('ScriptView', '#COLUMNS', 5)
            self.put('ScriptView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('ScriptView', 'COLUMN_FIELD', 'TASK_TAG', 2)
            self.put('ScriptView', 'COLUMN_FIELD', 'PROCESSING', 3)
            self.put('ScriptView', 'COLUMN_FIELD', 'TIME', 4)
            self.put('ScriptView', 'COLUMN_FIELD', 'MESSAGE', 5)
        if self.add('OpcDeviceView', 'ViewDef'):
            self.put('OpcDeviceView', 'RECORD', 'OpcDeviceDef')
            self.put('OpcDeviceView', '#COLUMNS', 3)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'DEVICE_PROCESSING', 1)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'TIME', 2)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'MESSAGE', 3)
        if self.add('OpcDeviceView', 'ViewDef'):
            self.put('OpcDeviceView', 'RECORD', 'OpcDeviceDef')
            self.put('OpcDeviceView', '#COLUMNS', 3)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'DEVICE_PROCESSING', 1)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'TIME', 2)
            self.put('OpcDeviceView', 'COLUMN_FIELD', 'MESSAGE', 3)
        if self.add('OpcGetView', 'ViewDef'):
            self.put('OpcGetView', 'RECORD', 'OpcGetDef')
            self.put('OpcGetView', '#COLUMNS', 5)
            self.put('OpcGetView', 'COLUMN_FIELD', 'GROUP_PROCESSING', 1)
            self.put('OpcGetView', 'COLUMN_FIELD', '#TAGS', 2)
            self.put('OpcGetView', 'COLUMN_FIELD', 'GROUP_STATUS', 3)
            self.put('OpcGetView', 'COLUMN_FIELD', 'GROUP_TIME', 4)
            self.put('OpcGetView', 'COLUMN_FIELD', 'OPC_READ_TIME', 5)
        if self.add('OpcPutView', 'ViewDef'):
            self.put('OpcPutView', 'RECORD', 'OpcPutDef')
            self.put('OpcPutView', '#COLUMNS', 5)
            self.put('OpcPutView', 'COLUMN_FIELD', 'GROUP_PROCESSING', 1)
            self.put('OpcPutView', 'COLUMN_FIELD', '#TAGS', 2)
            self.put('OpcPutView', 'COLUMN_FIELD', 'GROUP_STATUS', 3)
            self.put('OpcPutView', 'COLUMN_FIELD', 'GROUP_TIME', 4)
            self.put('OpcPutView', 'COLUMN_FIELD', 'OPC_WRITE_TIME', 5)
        if self.add('InvalidTags', 'ViewDef'):
            self.put('InvalidTags', 'RECORD', 'OpcGetDef')
            self.put('InvalidTags', '#COLUMNS', 3)
            self.put('InvalidTags', 'COLUMN_FIELD', 'REMOTE_TAG', 1)
            self.put('InvalidTags', 'COLUMN_FIELD', 'LOCAL_TAG', 2)
            self.put('InvalidTags', 'COLUMN_FIELD', 'STATUS', 3)
            self.put('InvalidTags', '#SEARCHES', 1)
            self.put('InvalidTags', 'SEARCH_FIELD', 'STATUS', 1)
            self.put('InvalidTags', 'SEARCH_OPERATOR', '=', 1)
            self.put('InvalidTags', 'SEARCH_VALUE', 'Error', 1)
        if self.add('FirIdView', 'ViewDef'):
            self.put('FirIdView', 'DESCRIPTION', '')
            self.put('FirIdView', 'RECORD', 'FirIdDef')
            self.put('FirIdView', '#COLUMNS', 2)
            self.put('FirIdView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('FirIdView', 'COLUMN_FIELD', 'LAST_RUN', 2)
        if self.add('IoDeviceView', 'ViewDef'):
            self.put('IoDeviceView', 'RECORD', 'IoDeviceDef')
            self.put('IoDeviceView', '#COLUMNS', 3)
            self.put('IoDeviceView', 'COLUMN_FIELD', 'DEVICE_PROCESSING', 1)
            self.put('IoDeviceView', 'COLUMN_FIELD', 'TIME', 2)
            self.put('IoDeviceView', 'COLUMN_FIELD', 'MESSAGE', 3)
        if self.add('IoGetView', 'ViewDef'):
            self.put('IoGetView', 'RECORD', 'IoGetDef')
            self.put('IoGetView', '#COLUMNS', 5)
            self.put('IoGetView', 'COLUMN_FIELD', 'GROUP_PROCESSING', 1)
            self.put('IoGetView', 'COLUMN_FIELD', '#TAGS', 2)
            self.put('IoGetView', 'COLUMN_FIELD', 'GROUP_STATUS', 3)
            self.put('IoGetView', 'COLUMN_FIELD', 'GROUP_TIME', 4)
            self.put('IoGetView', 'COLUMN_FIELD', 'IO_READ_TIME', 5)
        if self.add('PredictionView', 'ViewDef'):
            self.put('PredictionView', 'RECORD', 'PredictionDef')
            self.put('PredictionView', '#COLUMNS', 2)
            self.put('PredictionView', 'COLUMN_FIELD', 'DEP_NAME', 1)
            self.put('PredictionView', 'COLUMN_FIELD', 'MODEL_NAME', 2)
        if self.add('HistoryFileView', 'ViewDef'):
            self.put('HistoryFileView', 'RECORD', 'HistoryFileDef')
            self.put('HistoryFileView', '#COLUMNS', 5)
            self.put('HistoryFileView', 'COLUMN_FIELD', 'SCHEDULE_TIME', 1)
            self.put('HistoryFileView', 'COLUMN_FIELD', 'SCHEDULE_FREQ', 2)
            self.put('HistoryFileView', 'COLUMN_FIELD', 'TRIM_DELAY', 3)
            self.put('HistoryFileView', 'COLUMN_FIELD', 'TIME', 4)
            self.put('HistoryFileView', 'COLUMN_FIELD', 'MESSAGE', 5)
        if self.add('NotifyRuleView', 'ViewDef'):
            self.put('NotifyRuleView', 'RECORD', 'NotifyRuleDef')
        if self.add('UserGroupView', 'ViewDef'):
            self.put('UserGroupView', 'RECORD', 'UserGroupDef')
        if self.add('UserView', 'ViewDef'):
            self.put('UserView', 'RECORD', 'UserDef')
            self.put('UserView', '#COLUMNS', 2)
            self.put('UserView', 'COLUMN_FIELD', 'FULL_NAME', 1)
            self.put('UserView', 'COLUMN_FIELD', 'BASE_ROLE', 2)
        if self.add('UserRoleView', 'ViewDef'):
            self.put('UserRoleView', 'RECORD', 'UserRoleDef')
            self.put('UserRoleView', '#COLUMNS', 3)
            self.put('UserRoleView', 'COLUMN_FIELD', 'DESCRIPTION', 1)
            self.put('UserRoleView', 'COLUMN_FIELD', 'MENU_TREE', 2)
            self.put('UserRoleView', 'COLUMN_FIELD', 'BASE_POLICY', 3)
        if self.add('MyGraphicView', 'ViewDef'):
            self.put('MyGraphicView', 'RECORD', 'GraphicDef')
            self.put('MyGraphicView', '#SEARCHES', 1)
            self.put('MyGraphicView', 'SEARCH_FIELD', 'OWNER', 1)
            self.put('MyGraphicView', 'SEARCH_OPERATOR', '=', 1)
            self.put('MyGraphicView', 'SEARCH_VALUE', '{login}', 1)
        if self.add('MyPlotView', 'ViewDef'):
            self.put('MyPlotView', 'RECORD', 'PlotDef')
            self.put('MyPlotView', '#SEARCHES', 1)
            self.put('MyPlotView', 'SEARCH_FIELD', 'OWNER', 1)
            self.put('MyPlotView', 'SEARCH_OPERATOR', '=', 1)
            self.put('MyPlotView', 'SEARCH_VALUE', '{login}', 1)
        if self.add('ReplicationView', 'ViewDef'):
            self.put('ReplicationView', 'RECORD', 'ReplicationDef')
        self.add('My Groups', 'FolderDef')
        self.add('Shared Plots', 'FolderDef')
        self.add('Shared Graphics', 'FolderDef')
        if self.add('Plots', 'FolderViewDef'):
            self.put('Plots', 'VIEW_RECORD', 'PlotView')
        if self.add('Matplotlib', 'FolderViewDef'):
            self.put('Matplotlib', 'VIEW_RECORD', 'MatplotlibView')
        if self.add('Graphics', 'FolderViewDef'):
            self.put('Graphics', 'VIEW_RECORD', 'GraphicView')
        if self.add('Symbols', 'FolderViewDef'):
            self.put('Symbols', 'VIEW_RECORD', 'SymbolView')
        if self.add('Analogs', 'FolderViewDef'):
            self.put('Analogs', 'VIEW_RECORD', 'AnalogView')
        if self.add('Digitals', 'FolderViewDef'):
            self.put('Digitals', 'VIEW_RECORD', 'DigitalView')
        if self.add('Calculations', 'FolderViewDef'):
            self.put('Calculations', 'VIEW_RECORD', 'CalcView')
        if self.add('Functions', 'FolderViewDef'):
            self.put('Functions', 'VIEW_RECORD', 'FunctionView')
        if self.add('Models', 'FolderViewDef'):
            self.put('Models', 'VIEW_RECORD', 'ModelView')
        if self.add('Model Views', 'FolderViewDef'):
            self.put('Model Views', 'VIEW_RECORD', 'ModelViewView')
        if self.add('Slice Sets', 'FolderViewDef'):
            self.put('Slice Sets', 'VIEW_RECORD', 'SliceSetView')
        if self.add('Views', 'FolderViewDef'):
            self.put('Views', 'VIEW_RECORD', 'ViewView')
        if self.add('Web Links', 'FolderViewDef'):
            self.put('Web Links', 'VIEW_RECORD', 'WebLinkView')
        if self.add('Web Pages', 'FolderViewDef'):
            self.put('Web Pages', 'VIEW_RECORD', 'WebPageView')
        if self.add('Scripts', 'FolderViewDef'):
            self.put('Scripts', 'VIEW_RECORD', 'ScriptView')
        if self.add('OPC Servers', 'FolderViewDef'):
            self.put('OPC Servers', 'VIEW_RECORD', 'OpcDeviceView')
        if self.add('Read Groups', 'FolderViewDef'):
            self.put('Read Groups', 'VIEW_RECORD', 'OpcGetView')
        if self.add('Write Groups', 'FolderViewDef'):
            self.put('Write Groups', 'VIEW_RECORD', 'OpcPutView')
        if self.add('IO Servers', 'FolderViewDef'):
            self.put('IO Servers', 'VIEW_RECORD', 'IoDeviceView')
        if self.add('IO Groups', 'FolderViewDef'):
            self.put('IO Groups', 'VIEW_RECORD', 'IoGetView')
        if self.add('Predictions', 'FolderViewDef'):
            self.put('Predictions', 'VIEW_RECORD', 'PredictionView')
        self.put(('History Files', 'NAME'), 'History Groups')
        if self.add('History Groups', 'FolderViewDef'):
            self.put('History Groups', 'VIEW_RECORD', 'HistoryFileView')
        if self.add('Users', 'FolderViewDef'):
            self.put('Users', 'VIEW_RECORD', 'UserView')
        if self.add('Notifications', 'FolderViewDef'):
            self.put('Notifications', 'VIEW_RECORD', 'NotifyRuleView')
        if self.add('User Groups', 'FolderViewDef'):
            self.put('User Groups', 'VIEW_RECORD', 'UserGroupView')
        if self.add('User Roles', 'FolderViewDef'):
            self.put('User Roles', 'VIEW_RECORD', 'UserRoleView')
        if self.add('Replication', 'FolderViewDef'):
            self.put('Replication', 'VIEW_RECORD', 'ReplicationView')
        if self.add('My Graphics', 'FolderViewDef'):
            self.put('My Graphics', 'VIEW_RECORD', 'MyGraphicView')
        if self.add('My Plots', 'FolderViewDef'):
            self.put('My Plots', 'VIEW_RECORD', 'MyPlotView')
        self.add('OPC', 'FolderDef')
        self.put('OPC', '#RECORDS', 3)
        self.put('OPC', 'RECORD_NAME', 'OPC Servers', 1)
        self.put('OPC', 'RECORD_NAME', 'Read Groups', 2)
        self.put('OPC', 'RECORD_NAME', 'Write Groups', 3)
        self.add('IO', 'FolderDef')
        self.put('IO', '#RECORDS', 2)
        self.put('IO', 'RECORD_NAME', 'IO Servers', 1)
        self.put('IO', 'RECORD_NAME', 'IO Groups', 2)
        self.add('DMC', 'FolderDef')
        self.put('RootFolder', '#RECORDS', 25)
        self.put('RootFolder', 'RECORD_NAME', 'My Groups', 1)
        self.put('RootFolder', 'RECORD_NAME', 'Analogs', 2)
        self.put('RootFolder', 'RECORD_NAME', 'Digitals', 3)
        self.put('RootFolder', 'RECORD_NAME', 'Calculations', 4)
        self.put('RootFolder', 'RECORD_NAME', 'Functions', 5)
        self.put('RootFolder', 'RECORD_NAME', 'Models', 6)
        self.put('RootFolder', 'RECORD_NAME', 'Model Views', 7)
        self.put('RootFolder', 'RECORD_NAME', 'Predictions', 8)
        self.put('RootFolder', 'RECORD_NAME', 'Slice Sets', 9)
        self.put('RootFolder', 'RECORD_NAME', 'Matplotlib', 10)
        self.put('RootFolder', 'RECORD_NAME', 'Symbols', 11)
        self.put('RootFolder', 'RECORD_NAME', 'Graphics', 12)
        self.put('RootFolder', 'RECORD_NAME', 'Plots', 13)
        self.put('RootFolder', 'RECORD_NAME', 'Views', 14)
        self.put('RootFolder', 'RECORD_NAME', 'Web Links', 15)
        self.put('RootFolder', 'RECORD_NAME', 'Web Pages', 16)
        self.put('RootFolder', 'RECORD_NAME', 'Notifications', 17)
        self.put('RootFolder', 'RECORD_NAME', 'History Groups', 18)
        self.put('RootFolder', 'RECORD_NAME', 'Replication', 19)
        self.put('RootFolder', 'RECORD_NAME', 'User Roles', 20)
        self.put('RootFolder', 'RECORD_NAME', 'Users', 21)
        self.put('RootFolder', 'RECORD_NAME', 'Scripts', 22)
        self.put('RootFolder', 'RECORD_NAME', 'OPC', 23)
        self.put('RootFolder', 'RECORD_NAME', 'IO', 24)
        self.put('RootFolder', 'RECORD_NAME', 'DMC', 25)
        if user_folder_ok:
            self.put('UserFolder', '#RECORDS', 9)
            self.put('UserFolder', 'RECORD_NAME', 'Analogs', 1)
            self.put('UserFolder', 'RECORD_NAME', 'Digitals', 2)
            self.put('UserFolder', 'RECORD_NAME', 'Calculations', 3)
            self.put('UserFolder', 'RECORD_NAME', 'Functions', 4)
            self.put('UserFolder', 'RECORD_NAME', 'Symbols', 5)
            self.put('UserFolder', 'RECORD_NAME', 'My Plots', 6)
            self.put('UserFolder', 'RECORD_NAME', 'My Graphics', 7)
            self.put('UserFolder', 'RECORD_NAME', 'Shared Plots', 8)
            self.put('UserFolder', 'RECORD_NAME', 'Shared Graphics', 9)
        if self.add('GuestRole', 'UserRoleDef'):
            self.put(('GuestRole', 'DESCRIPTION'), 'Guest user role')
            self.put(('GuestRole', 'MENU_TREE'), 'RootFolder')
            self.put(('GuestRole', 'BASE_POLICY'), 0)
        if self.add('AdminRole', 'UserRoleDef'):
            self.put(('AdminRole', 'DESCRIPTION'), 'Administrator user role')
            self.put(('AdminRole', 'MENU_TREE'), 'RootFolder')
            self.put(('AdminRole', 'BASE_POLICY'), 1)
        if self.add('UserRole', 'UserRoleDef'):
            self.put(('UserRole', 'DESCRIPTION'), 'Standard user role')
            self.put(('UserRole', 'MENU_TREE'), 'UserFolder')
            self.put(('UserRole', 'BASE_POLICY'), 0)
            self.put(('UserRole', '#RULES'), 2)
            self.put(('UserRole', 'TAG', 1), 'PlotDef')
            self.put(('UserRole', 'SCOPE', 1), 0)
            self.put(('UserRole', 'READ', 1), 1)
            self.put(('UserRole', 'WRITE', 1), 1)
            self.put(('UserRole', 'CREATE', 1), 1)
            self.put(('UserRole', 'DELETE', 1), 1)
            self.put(('UserRole', 'TAG', 2), 'GraphicDef')
            self.put(('UserRole', 'SCOPE', 2), 0)
            self.put(('UserRole', 'READ', 2), 1)
            self.put(('UserRole', 'WRITE', 2), 1)
            self.put(('UserRole', 'CREATE', 2), 1)
            self.put(('UserRole', 'DELETE', 2), 1)
        if self.add('admin', 'UserDef'):
            self.put(('admin', 'FULL_NAME'), 'Database administrator')
            self.put(('admin', 'PASSWORD'), 'admin')
            self.put(('admin', 'BASE_ROLE'), 'AdminRole')
        if self.add('guest', 'UserDef'):
            self.put(('guest', 'FULL_NAME'), 'Non-authenticated user')
            self.put(('guest', 'PASSWORD'), '')
            self.put(('guest', 'BASE_ROLE'), 'GuestRole')
        code = 'def lowpass2(X, T = 6, Ts = 1):\n    """ \n        Kent\'s example low pass filter\n        X - list containing data\n        T - filter time constant (minutes)\n        Ts - sample time of data (minutes)\t\n    """\n\n    xlen = len(X)\n    if T>0:\n        a = exp(-float(Ts)/float(T))\n    else:\n        a = 0\n\n    Y = zeros(xlen)\n    Y[0] = X[0]\n\n    for k in range(1,xlen):\n        if (not isnan(X[k])) and (not isnan(Y[k-1])):\n            Y[k] = a*Y[k-1] + (1-a)*X[k]\n        else:\n            Y[k] = X[k]\n\n    return Y\n'
        if self.add('lowpass2', 'FunctionDef'):
            self.put('lowpass2', 'DESCRIPTION', 'Low-pass filter function')
            self.put('lowpass2', 'CODE', code)
        code = 'def lowpass(x, Tf = 6, Ts = 1):\n    """\n        X  - list containing data\n        Tf - filter time constant (minutes)\n        Ts - sample time of data (minutes)  \n    """\n    p = -exp(-float(Ts)/float(Tf))\n    b = array([0, 1+p])\n    a = array([1, p])\n    y = scipy.signal.lfilter(b,a,x)\n    return y\n'
        self.add('lowpass', 'FunctionDef')
        self.put('lowpass', 'DESCRIPTION', 'Low-pass filter function')
        self.put('lowpass', 'CODE', code)
        code = 'def diff(X):\n    """ \n        Example diff high pass filter\n        X - list containing data\n        returns list\n    """\n\n    xlen = len(X)\n    Y = zeros(xlen)\n\n    for k in range(1,xlen):\n        if isnan(X[k]) or isnan(X[k-1]):\n            Y[k] = NaN\n        else:\n            Y[k] = X[k] - X[k-1]\n\n    return Y\n\n'
        if self.add('diff', 'FunctionDef'):
            self.put('diff', 'DESCRIPTION', 'Differencing (high pass filter)')
            self.put('diff', 'CODE', code)
        code = 'def analyzer_spline(X, low, high):\n    D = fabs(diff(X))\n\n    X[ D > high ] = nan\n    X[ D < low ] = nan\n\n    return interpolate_bad(X)\n'
        if self.add('analyzer_spline', 'FunctionDef'):
            self.put('analyzer_spline', 'DESCRIPTION', '')
            self.put('analyzer_spline', 'CODE', code)
        code = 'def interpolate_bad(X):\n    if isnan(X[0]): X[0] = X[isfinite(X)][0]\n    if isnan(X[-1]): X[-1] = X[isfinite(X)][-1]\n\n    t = arange(len(X), dtype=float)\n    t1 = t[isfinite(X)]\n    v1 = X[isfinite(X)]\n    t2 = t[isnan(X)]\n\n    ifunc = scipy.interpolate.interp1d(t1, v1)\n    v2 = array(ifunc(t2), X.dtype)\n    X[isnan(X)] = v2\n\n    return X\n'
        self.add('interpolate_bad', 'FunctionDef')
        self.put('interpolate_bad', 'DESCRIPTION', 'Replace NaN with interpolated values')
        self.put('interpolate_bad', 'CODE', code)
        code = 'def xform_linear(X, alpha, low=0.0, high=100.0):\n    X = maximum(X, low)\n    X = minimum(X, high)\n    frac = (X - low) / (high - low)\n\n    Y = maximum( 0.0 , minimum( 100.0, 100.0 * frac / sqrt(alpha + (1 - alpha) * (frac ** 2))))\n        \n    return Y\n'
        if self.add('xform_linear', 'FunctionDef'):
            self.put('xform_linear', 'DESCRIPTION', 'Linear transform')
            self.put('xform_linear', 'CODE', code)
        code = 'def pw_linear(v,X=[0,1],Y=[0,1]):\n    """ \n        Fast Piece-wise Linear Xform\n        v -    vector data\n        X -    X-axis data points\n        Y -    Y-axis data points\n        returns vector\n    """\n\n    coeff = []\n    for i in range(len(X)-1):\n        a = float(Y[i+1]-Y[i])/float(X[i+1]-X[i])  # slope\n        b = Y[i] - a*X[i] # intersect\n        coeff.append((a,b))\n    coeff.append((a,b))\n    return numpy.piecewise(v, [v >= b for b in X], [lambda x=v, (a,b)=c: a*x+b for c in coeff])\n'
        if self.add('pw_linear', 'FunctionDef'):
            self.put('pw_linear', 'DESCRIPTION', 'Piecewise linear transform')
            self.put('pw_linear', 'CODE', code)
        code = 'def multi_regress_exp(V1, V2=0.0, V3=0.0, V4=0.0, V5=0.0, V6=0.0, C0=0.0, C1=0.0, C2=0.0, C3=0.0, C4=0, C5=0.0, C6=0.0, D0=0.0, D1=0.0):\n    return exp(C0*(C1*V1 + C2*V2 + C3*V3 + C4*V4 + C5*V5 + C6*V6 + D1)) + D0\n'
        if self.add('multi_regress_exp', 'FunctionDef'):
            self.put('multi_regress_exp', 'DESCRIPTION', '')
            self.put('multi_regress_exp', 'CODE', code)
        code = 'def xform_parabolic(X, alpha, low=0.0, high=100.0):\n    X = maximum(X, low)\n    X = minimum(X, high)\n    frac = (X - low) / (high - low)\n\n    Y = maximum( 0.0 , minimum( 100.0, 100.0 * frac ** 2 / sqrt(alpha + (1 - alpha) * (frac ** 4))))\n        \n    return Y\n\n'
        if self.add('xform_parabolic', 'FunctionDef'):
            self.put('xform_parabolic', 'DESCRIPTION', 'Parabolic transform')
            self.put('xform_parabolic', 'CODE', code)
        code = 'def pct_antoine(Pact, Patm, Pbase,  Tact, B, C, C18=1.0, C32=0.0):\n    """\n        Pact    Actual pressure (gauge) \n        Patm    Atmospheric pressure constant \n        Pbase   Base pressure (average P) \n        Tact    Temperature to be corrected \n        B       Antoine coefficient \n        C       Antoine coefficient \n        C18     1.0 for degF, 1.8 for degC \n        C32     0.0 for degF, 32.0 for degC \n    """\n\n    return (1.0 / (log10((Pact + Patm) / (Pbase + Patm)) / B + 1.0 / (C18 * Tact + C32 + C))- C - C32) / C18\n'
        if self.add('pct_antoine', 'FunctionDef'):
            self.put('pct_antoine', 'DESCRIPTION', 'PCT - Antoine')
            self.put('pct_antoine', 'CODE', code)
        code = 'def pct_linear(Pact, Pbase, T, slope):\n    return slope * (Pact - Pbase) + T\n'
        if self.add('pct_linear', 'FunctionDef'):
            self.put('pct_linear', 'DESCRIPTION', 'PCT - Linear')
            self.put('pct_linear', 'CODE', code)
        self.put('SystemSettings', 'VALUE', __version__, 'SchemaVersion', add_keys=True)
        self.put('SystemSettings', 'VALUE', ','.join(compatible_versions), 'CompatibleVersions', add_keys=True)
        self.select_cache = {}
        code = 'def shift(X, n):\n    """\n        X   Vector\n        n   Number samples to shift left/right\n    """\n\n    n = int(n)\n    X = roll(X, n)\n\n    if n < 0:\n        X[...,n:] = nan\n    else:\n        X[...,:n] = nan\n        \n    return X\n\n'
        if self.add('shift', 'FunctionDef'):
            self.put('shift', 'DESCRIPTION', 'Shift samples left or right')
            self.put('shift', 'CODE', code)
        code = 'def sopdt_dyn_comp(vector, tau1, tau2, deadtime):\n    return shift(lowpass(lowpass(vector, exp(-1/tau1)), exp(-1/tau2)), deadtime)\n'
        if self.add('sopdt_dyn_comp', 'FunctionDef'):
            self.put('sopdt_dyn_comp', 'DESCRIPTION', '')
            self.put('sopdt_dyn_comp', 'CODE', code)
        code = 'def xform_piecewise(Vec,X1,Y1,X2,Y2,X3,Y3,X4=None,Y4=None,X5=None,Y5=None,X6=None,Y6=None,X7=None,Y7=None,X8=None,Y8=None,X9=None,Y9=None,X10=None,Y10=None):\n    """ \n        Mike\'s Piece-wise Linear Xform\n        Vec -   vector data\n        X1 -    #1 X-axis data point\n        Y1 -    #1 Y-axis data point\n        returns vector\n    """\n    if X4 == None:\n        X4 = X3 * 1.001\n        Y4 = Y3 * 1.001\n        X5 = X4\n        Y5 = Y4\n        X6 = X4\n        Y6 = Y4\n        X7 = X4\n        Y7 = Y4\n        X8 = X4\n        Y8 = Y4\n        X9 = X4\n        Y9 = Y4\n        X10 = X4\n        Y10 = Y4\n    elif X5 == None:\n        X5 = X4 * 1.001\n        Y5 = Y4 * 1.001\n        X6 = X5\n        Y6 = Y5\n        X7 = X5\n        Y7 = Y5\n        X8 = X5\n        Y8 = Y5\n        X9 = X5\n        Y9 = Y5\n        X10 = X5\n        Y10 = Y5\n    elif X6 == None:\n        X6 = X5 * 1.001\n        Y6 = Y5 * 1.001\n        X7 = X6\n        Y7 = Y6\n        X8 = X6\n        Y8 = Y6\n        X9 = X6\n        Y9 = Y6\n        X10 = X6\n        Y10 = Y6\n    elif X7 == None:\n        X7 = X6 * 1.001\n        Y7 = Y6 * 1.001\n        X8 = X7\n        Y8 = Y7\n        X9 = X7\n        Y9 = Y7\n        X10 = X7\n        Y10 = Y7\n    elif X8 == None:\n        X8 = X7 * 1.001\n        Y8 = Y7 * 1.001\n        X9 = X8\n        Y9 = Y8\n        X10 = X8\n        Y10 = Y8\n    elif X9 == None:\n        X9 = X8 * 1.001\n        Y9 = Y8 * 1.001\n        X10 = X9\n        Y10 = Y9\n    elif X10 == None:\n        X10 = X9 * 1.001\n        Y10 = Y9 * 1.001\n\n    xlen = len(Vec)\n    Y = zeros(xlen)\n\n    for k in range(1,xlen):\n        if isnan(Vec[k]):\n            Y[k] = NaN\n        elif Vec[k] < X1:\n            Y[k] = NaN\n        elif Vec[k] <= X2:\n            Y[k] = (Vec[k]-X1) * (Y2-Y1)/(X2-X1) + Y1\n        elif Vec[k] <= X3:\n            Y[k] = (Vec[k]-X2) * (Y3-Y2)/(X3-X2) + Y2\n        elif Vec[k] <= X4:\n            Y[k] = (Vec[k]-X3) * (Y4-Y3)/(X4-X3) + Y3\n        elif Vec[k] <= X5:\n            Y[k] = (Vec[k]-X4) * (Y5-Y4)/(X5-X4) + Y4\n        elif Vec[k] <= X6:\n            Y[k] = (Vec[k]-X5) * (Y6-Y5)/(X6-X5) + Y5\n        elif Vec[k] <= X7:\n            Y[k] = (Vec[k]-X6) * (Y7-Y6)/(X7-X6) + Y6\n        elif Vec[k] <= X8:\n            Y[k] = (Vec[k]-X7) * (Y8-Y7)/(X8-X7) + Y7\n        elif Vec[k] <= X9:\n            Y[k] = (Vec[k]-X8) * (Y9-Y8)/(X9-X8) + Y8\n        elif Vec[k] <= X10:\n            Y[k] = (Vec[k]-X9) * (Y10-Y9)/(X10-X9) + Y9\n        elif Vec[k] > X10:\n            Y[k] = NaN\n\n    return Y'
        if self.add('xform_piecewise', 'FunctionDef'):
            self.put('xform_piecewise', 'DESCRIPTION', 'Piecewise linear transform')
            self.put('xform_piecewise', 'CODE', code)
        code = 'def pct_true(times, values):\n    return float(sum(values == 1)) / sum(~isnan(values)) * 100.0\n'
        self.add('pct_true', 'AggFunctionDef')
        self.put('pct_true', 'DESCRIPTION', 'Percent of values equal to 1')
        self.put('pct_true', 'AGGREGATE_ID', -2)
        self.put('pct_true', 'CODE', code)
        code = 'def pct_false(times, values):\n    return float(sum(values == 0)) / sum(~isnan(values)) * 100.0\n'
        self.add('pct_false', 'AggFunctionDef')
        self.put('pct_false', 'DESCRIPTION', 'Percent of values equal to 0')
        self.put('pct_false', 'AGGREGATE_ID', -3)
        self.put('pct_false', 'CODE', code)
        code = 'def mode(times, values):\n    values = array(values[values > 0], dtype=int)\n    if len(values) == 0:\n        return nan\n    else:\n        return bincount(values).argmax()\n'
        self.add('mode', 'AggFunctionDef')
        self.put('mode', 'DESCRIPTION', 'Mode')
        self.put('mode', 'AGGREGATE_ID', -1)
        self.put('mode', 'CODE', code)
        self.put('SystemSettings', 'VALUE', __version__, 'SchemaVersion', add_keys=True)
        self.select_cache = {}
        self.CALCULATION_DEF = self.name2id('CalculationDef')
        self.update_name2()
        self.update_desc_db()
        return True

    def update_desc_db(self, init = False):

        def update(def_name):
            did = self.name2id(def_name)
            tags = self.lsname_alt(did)
            if self.DESCRIPTION_FT == None:
                return
            else:
                descriptions = self.mget(tags, self.DESCRIPTION_FT, ascii=True)
                pipe = self.rdb.pipeline(transaction=False)
                for tag, desc in zip(tags, descriptions):
                    pipe.hset(pkey('desc', did), '%s\x00%s' % (tag, desc), tag)

                pipe.execute()
                return

        keys = self.rdb.keys('desc*')
        if len(keys) > 0:
            if init:
                self.rdb.delete(*keys)
            else:
                return
        update('AnalogDef')
        update('DiscreteDef')
        update('CalculationDef')

    def _add_desc_key(self, record, description):
        did = self.get_defid(record)
        name = self.get(record, NAME)
        description = decode_u_str(description)
        self.rdb.hset(pkey('desc', did), '%s\x00%s' % (name, description), name)

    def _del_desc_key(self, record):
        did = self.get_defid(record)
        name = self.get(record, NAME)
        description = self.get(record, self.DESCRIPTION_FT)
        description = decode_u_str(description)
        self.rdb.hdel(pkey('desc', did), '%s\x00%s' % (name, description))

    def _del_desc_key_scan(self, record):
        did = self.get_defid(record)
        k = pkey('desc', did)
        search = self.get(record, NAME) + '\x00*'
        cur = 0
        keys = []
        while True:
            cur, hdict = self.rdb.hscan(k, cursor=cur, match=search)
            keys += hdict.keys()
            if cur == 0:
                break

        if len(keys) > 0:
            self.rdb.hdel(k, *keys)

    def update_sdef_db(self):
        keys = self.rdb.keys('sdef*')
        if len(keys) > 0:
            self.rdb.delete(*keys)
        for tag in self.lsname_alt():
            if tag == None:
                continue
            rid = self.name2id(tag)
            did = self.get_defid(rid)
            self.rdb.hset(pkey('sdef', did), tag, pack('>I', rid))

        return

    def update_name2(self):
        if self.rdb.hlen('name') > self.rdb.hlen('name2'):
            self.rdb.delete('name2')
            id_list = self.rdb.hvals('name')
            pipe = self.rdb.pipeline(transaction=False)
            for id in id_list:
                pipe.hget('rec' + id, pfld(NAME))

            name_list = pipe.execute()
            pipe = self.rdb.pipeline(transaction=False)
            for name, id in zip(name_list, id_list):
                pipe.hset('name2', name, id)

            pipe.execute()

    def get_calc(self, tag):
        all_funcs = self.getlist('FunctionDef')
        all_funcs_re = '|'.join(all_funcs)
        all_funcs_re = '(?<![A-Za-z0-9_])(' + all_funcs_re + ')\\('
        match_funcs = re.findall(all_funcs_re, tag)
        f_code = ''
        for f in match_funcs:
            f_code += self.get(f, 'CODE') + '\n'

        exec (f_code)
        value = eval(tag)
        return value

    def get(self, tag, field = None, occ = 0, text = False, ascii = False, ascii_errors = False, definition = None, has_history = False, excel = False, unicode_raw = False):
        if text:
            ascii = True
        if field == None:
            uid = self.tag2uid(tag)
            if uid == None:
                if ascii:
                    if ascii_errors:
                        return 'ERROR'
                    else:
                        return ''
                else:
                    return
            rid, fid, occ = uid
        else:
            if isinstance(tag, tuple):
                if ascii:
                    return ''
                else:
                    return
            rid = self.name2id(tag)
            fid = self.name2id(field)
            if occ == '':
                occ = 0
            else:
                occ = self.key2idx(occ)
            if rid == None or fid == None or occ == None:
                if ascii:
                    if ascii_errors:
                        return 'ERROR'
                    else:
                        return ''
                else:
                    return
        if not self._pps_query(None, P_WRITE) and fid == self.PASSWORD_FT:
            if ascii:
                return ''
            else:
                return
        if definition:
            did = definition
        else:
            did = self.get_defid(rid)
            if did == None:
                return
        dtype = self.getdef(did, fid, DEF_DTYPE)
        if dtype == None:
            if ascii:
                return ''
            else:
                return
        elif dtype == DT_DICTIONARY:
            fid = self.list(did, fid)[0]
            n = len(self.list_keys(rid, fid))
            if ascii:
                return str(n)
            else:
                return n
        format = self.getdef(did, fid, DEF_FORMAT)
        if self.get_defid(format) == FIELD_DEF:
            format = self.get(rid, format)
            if format == 0 and dtype == DT_INTEGER:
                format = None
        if excel and (dtype == DT_INTEGER and format != None or dtype in (DT_TIMESTAMP,
         DT_SCHEDULE,
         DT_RECORD,
         DT_FIELD)):
            ascii = True
        if has_history or did in (self.ANALOG_DEF, self.DISCRETE_DEF) and fid == self.VALUE_FT or fid in self.extra_history_fields or (did, fid) in self.custom_history_fields:
            hid = self.tag2hid((rid, fid, occ))
            if hid:
                value = self.last_h_value(hid)
                if ascii:
                    if value == None:
                        value = ''
                    elif did == self.ANALOG_DEF:
                        value = self.format_value_hist(value, format)
                    elif self.get_defid(format) in (self.SELECT_DEF, self.SELECT_DICT_DEF):
                        value = self.int2str(value, format)
                    else:
                        value = str(value)
            else:
                data = self.rdb.hget(pkey('rec', rid), pfld(fid, int(occ)))
                value = self.unpack_field(data, dtype, format=format, ascii=ascii)
        elif (did in (self.ANALOG_DEF, self.DISCRETE_DEF) or (did, self.VALUE_FT) in self.custom_history_fields) and fid == self.TIME_FT:
            hid = self.tag2hid((rid, self.VALUE_FT))
            value = self.last_h_time(hid)
            if value == None:
                value = 0.0
            if ascii:
                value = self.format_value(value, dtype, format)
        else:
            data = self.rdb.hget(pkey('rec', rid), pfld(fid, int(occ)))
            value = self.unpack_field(data, dtype, format=format, ascii=ascii)
        if self.unicode_mode and fid in self.unicode_fields and not unicode_raw:
            value = decode_u_str(value)
        if excel:
            if isinstance(value, numpy.string_):
                value = str(value)
            elif type(value) in (float,
             numpy.float16,
             numpy.float32,
             numpy.float64) and numpy.isnan(value):
                value = None
        return value

    def format_value_hist(self, value, format):
        if not hasattr(value, 'dtype') or format in (None, ''):
            value = str(value)
        elif issubdtype(value.dtype, numpy.float):
            if format == None or format < 0:
                value = float2str(value)
            else:
                fmt = '%%.%df' % format
                value = fmt % value
        elif issubdtype(value.dtype, numpy.int) and self.type(format) in (self.SELECT_DEF, self.SELECT_DICT_DEF):
            value = self.int2str(value, format)
        else:
            value = str(value)
        return value

    def format_value(self, value, dtype, format):
        if dtype == DT_FLOAT:
            if value is None:
                value = ''
            elif numpy.isnan(value):
                value = 'nan'
            elif format == None or format < 0:
                value = float2str(value)
            else:
                fmt = '%%.%df' % format
                value = fmt % value
            return value
        elif dtype == DT_TIMESTAMP:
            return self.time2ascii(value)
        else:
            return str(value)
            return

    def first_q_time(self, tags, ascii = False):
        if not isinstance(tags, list):
            tags = [tags]
            single = True
        else:
            single = False
        hids = [ self.tag2hid(t) for t in tags ]
        pipe = self.rdb.pipeline(transaction=False)
        for hid in hids:
            if hid == None:
                h = 4294967295
            else:
                h = hid.hid
            pipe.lindex(pkey('hq', h), 0)

        rows = pipe.execute()
        time_list = []
        for row in rows:
            if row is None:
                time_list.append(None)
            else:
                start_time = self.unpack_h_key(row)
                time_list.append(start_time)

        if ascii:
            time_list = self.times2ascii(time_list)
        if single:
            return time_list[0]
        else:
            return time_list
            return

    def first_h_time(self, tags, ascii = False):
        if not isinstance(tags, list):
            tags = [tags]
            single = True
        else:
            single = False
        if (isinstance(tags[0], tuple) or isinstance(tags[0], str)) and self.is_calc(tags[0]):
            start_time, end_time = self.get_calc_times(tags[0], ascii=ascii)
            return start_time
        else:
            hids = [ self.tag2hid(t) for t in tags ]
            pipe = self.rdb.pipeline(transaction=False)
            for hid in hids:
                if hid == None:
                    h = 4294967295
                else:
                    h = hid.hid
                pipe.zrange(pkey('hd', h), 0, 0)

            rows = pipe.execute()
            time_list = []
            for row in rows:
                if row in (None, []):
                    time_list.append(None)
                else:
                    row = row[0]
                    start_time = self.unpack_h_key(row)
                    time_list.append(start_time)

            if time_list.count(None) > 0:
                time_list2 = self.first_q_time(hids)
                time_list = [ (qt if dt == None else dt) for dt, qt in zip(time_list, time_list2) ]
            if ascii:
                time_list = self.times2ascii(time_list)
            if single:
                return time_list[0]
            return time_list
            return

    def last_h_time(self, tags, ascii = False):
        if not isinstance(tags, list):
            tags = [tags]
            single = True
        else:
            single = False
        if len(tags) == 1 and (isinstance(tags[0], tuple) or isinstance(tags[0], str)) and self.is_calc(tags[0]):
            start_time, end_time = self.get_calc_times(tags[0], ascii=ascii)
            return end_time
        else:
            hids = [ self.tag2hid(t) for t in tags ]
            pipe = self.rdb.pipeline(transaction=False)
            for hid in hids:
                if hid == None:
                    h = 4294967295
                else:
                    h = hid.hid
                pipe.lindex(pkey('hq', h), -1)

            rows = pipe.execute()
            time_list = []
            for row in rows:
                if row in (None, []):
                    time_list.append(None)
                    continue
                times, values = self.unpack_h_block(row)
                if len(times) == 0:
                    time_list.append(None)
                else:
                    time_list.append(times[-1])

            if ascii:
                time_list = self.times2ascii(time_list)
            if single:
                return time_list[0]
            return time_list
            return

    def last_h_value(self, tags):
        if not isinstance(tags, list):
            tags = [tags]
            single = True
        else:
            single = False
        hids = self.tags2hids(tags)
        if hids == None:
            return
        else:
            pipe = self.rdb.pipeline(transaction=False)
            for hid in hids:
                if hid == None:
                    h = 4294967295
                else:
                    h = hid.hid
                pipe.lindex(pkey('hq', h), -1)
            rows = pipe.execute()
            value_list = []
            for row in rows:
                if row in (None, []):
                    value_list.append(None)
                    continue
                times, values = self.unpack_h_block(row)
                if len(values) == 0:
                    value_list.append(None)
                else:
                    value_list.append(values[-1])

            if single:
                return value_list[0]
            return value_list
            return

    def last_h_tuple(self, tags, ascii = False):
        if not isinstance(tags, list):
            tags = [tags]
            single = True
        else:
            single = False
        hids = self.tags2hids(tags)
        pipe = self.rdb.pipeline(transaction=False)
        for hid in hids:
            if hid == None:
                h = 4294967295
            else:
                h = hid.hid
            pipe.lindex(pkey('hq', h), -1)

        rows = pipe.execute()
        time_list = []
        value_list = []
        for row in rows:
            if row in (None, []):
                value_list.append(None)
                continue
            times, values = self.unpack_h_block(row)
            time_list.append(times[-1])
            value_list.append(values[-1])

        if ascii:
            time_list = self.times2ascii(time_list)
        tuple_list = zip(time_list, value_list)
        if single:
            return tuple_list[0]
        else:
            return tuple_list
            return

    def get_calc_times(self, record, ascii = False):
        if isinstance(record, tuple):
            record = record[0]
        rid = self.name2id(record)
        if rid == None or self.type(rid) != self.CALCULATION_DEF:
            return
        else:
            name = self.id2name(rid)
            agg_times = None
            calc_start = None
            calc_end = None
            calc_start = self.get(rid, 'CALC_START')
            time_tag = self.get(rid, 'TIME_TAG', ascii=True)
            freq = self.get(rid, 'CALC_INTERVAL')
            if time_tag:
                time_hid = self.tag2hid(time_tag)
                if time_hid != None:
                    agg_times, agg_values = self.gethis(time_tag)
                    if len(agg_times) > 0:
                        calc_start = agg_times[0]
                        calc_end = agg_times[-1]
                    else:
                        return (None, None)
                else:
                    return (None, None)
                if ascii:
                    calc_start = self.time2ascii(calc_start)
                    calc_end = self.time2ascii(calc_end)
                return (calc_start, calc_end)
            if not calc_start:
                calc_start = self.get('SystemSettings', 'VALUE', 'CalcStartDefault')
                if isinstance(calc_start, str):
                    calc_start = self.ascii2time(calc_start.strip())
            if not freq:
                freq = self.get('SystemSettings', 'VALUE', 'CalcFreqDefault')
                try:
                    freq = int(freq)
                except TypeError:
                    freq = 60

                if freq < 0:
                    freq = abs(freq)
            if self.get(rid, 'SAVE_TIME') > self.get(rid, 'COMPILED_TIME'):
                code = self.get(rid, 'CODE', ascii=True)
                all_tags = [ t.upper() for t in self.lsname('AnalogDef') + self.lsname('CalculationDef') + self.lsname('PredictionDef') + self.lsname('DiscreteDef') ]
                input_tags = self.list_keys(rid, 'input_description', ascii=True)
                if len(input_tags) > 0:
                    input_tags_re = '|'.join(input_tags)
                    now_tags_re = '(?<![A-Za-z0-9_:\\."\'])(' + input_tags_re + ')(?![\\(A-Za-z0-9_:\\.])'
                    now_match_tags = re.findall(now_tags_re, code)
                    if len(now_match_tags) > 0:
                        sub_dict = dict([ (t, self.get(rid, 'input_tag', t, ascii=True)) for t in now_match_tags ])
                        if len(sub_dict) > 0:
                            code = multiple_replace(sub_dict, code, pre='(?<![A-Za-z0-9_:\\."\'])', post='(?![\\(A-Za-z0-9_:\\.])')
                now_tags_re = '{(.+?)}'
                now_match_tags = re.findall(now_tags_re, code)
                if len(now_match_tags) > 0:
                    sub_dict = dict([ ('{%s}' % t, '_a[%d]' % i) for i, t in enumerate(now_match_tags) ])
                    if len(sub_dict) > 0:
                        code = multiple_replace(sub_dict, code)
                match_tags = [ t for t in now_match_tags if t.upper() in all_tags ]
                now_tags_re = '(?<![A-Za-z0-9_:\\."\'])([A-Za-z0-9_:\\.]+)(?![\\(A-Za-z0-9_:\\.])'
                now_match_tags = re.findall(now_tags_re, code)
                if len(now_match_tags) > 0:
                    now_match_tags = [ t for t in now_match_tags if t.upper() in all_tags ]
                match_tags += now_match_tags
                match_tags = unique(match_tags)
                self.putlist((rid, 'TAG'), match_tags, notify=True)
            else:
                match_tags = self.getlist(rid, 'TAG')
            if len(match_tags) == 0:
                return (None, None)
            if not calc_start:
                start_times = [ self.first_h_time(t) for t in match_tags ]
                start_times = [ t for t in start_times if t != None ]
                start_times.sort()
                if len(start_times) > 0:
                    calc_start = start_times[0]
            if not calc_end:
                end_times = [ self.last_h_time(t) for t in match_tags ]
                end_times = [ t for t in end_times if t != None ]
                end_times.sort()
                if len(end_times) > 0:
                    calc_end = end_times[-1]
            if not calc_start or not calc_end:
                return (None, None)
            new_start = self.ms2time(self.time2ms(calc_end) - int(freq * 1000) * (MAX_VALUES - 1))
            if new_start > calc_start:
                calc_start = new_start
            if ascii:
                calc_start = self.time2ascii(calc_start)
                calc_end = self.time2ascii(calc_end)
            return (calc_start, calc_end)

    def gethis_nan(self, start_time, end_time, freq, max_len = -MAX_VALUES):
        max_len = abs(max_len)
        times = self.trange(start_time, end_time, freq)[-max_len:]
        values = array([nan] * len(times), dtype=float32)
        return (times, values)

    def tag_expression_replace(self, tag_expression, path):
        if path and tag_expression:
            for m in re.finditer('{((../)*)([A-Za-z_]+)}', tag_expression):
                up_count = m.groups()[0].count('../')
                if up_count < len(path):
                    up_tag = str(path[up_count])
                    up_field = str(m.groups()[2])
                    if up_field.upper() == 'NAME':
                        value = up_tag
                    elif self.is_field(up_tag, 'VALUE', up_field):
                        value = self.get(up_tag, 'VALUE', up_field)
                        value = self.tag_expression_replace(value, path[up_count:])
                    else:
                        value = self.get(up_tag, up_field)
                        value = self.tag_expression_replace(value, path[up_count:])
                    if value != None:
                        tag_expression = tag_expression.replace(m.group(), value)

        return tag_expression

    def gethis_calc(self, record, start_time = None, end_time = None, freq = None, agg_fn = None, agg_times = None, max_len = -MAX_VALUES, ascii = False, fill = None, adhoc_base = None, time_sync = False, item_path = None):
        if isinstance(record, tuple):
            record = record[0]
        if start_time not in (None, 0) or end_time not in (None, MAX_TIME):
            override_time = True
        else:
            override_time = False
        if isinstance(agg_fn, str):
            agg_id = self.get(agg_fn, 'AGGREGATE_ID')
            if agg_id <= 0 or agg_id == None:
                agg_fn = self.get_function(agg_fn)
            else:
                agg_fn = agg_id
            if agg_fn == None:
                return self.empty_h_tuple()
        freq2 = freq
        agg_fn2 = agg_fn
        agg_times2 = agg_times
        asset_vars = {}
        if agg_times2 is not None and len(agg_times2) == 0:
            return self.empty_h_tuple()
        else:
            calc_start = None
            calc_end = None
            self.calc_err = None
            self.calc_err_list = None
            if override_time:
                lookback_time = self.get('SystemSettings', 'VALUE', 'CalcLookbackDefault')
                try:
                    lookback_time = self.sec2time(int(lookback_time))
                except TypeError:
                    lookback_time = 0

            else:
                lookback_time = 0
            adhoc_calc = self.is_adhoc_calc(record)
            if adhoc_calc:
                code = record[1:]
                agg_fn = None
                if start_time in (None, 0):
                    calc_start = self.get('SystemSettings', 'VALUE', 'CalcStartDefault')
                else:
                    calc_start = start_time - lookback_time
                if end_time in (None, MAX_TIME):
                    pass
                else:
                    calc_end = end_time
                if isinstance(calc_start, str):
                    calc_start = self.ascii2time(calc_start.strip())
                freq = self.get('SystemSettings', 'VALUE', 'CalcFreqDefault')
                try:
                    freq = int(freq)
                except TypeError:
                    freq = 60

            else:
                rid = self.name2id(record)
                did = self.get_defid(rid)
                name = self.id2name(rid)
                code = self.get(rid, 'CODE', ascii=True)
                if code is None:
                    code = ''
                agg_fn = self.get(rid, 'AGG_FUNCTION')
                if agg_fn:
                    agg_id = self.get(agg_fn, 'AGGREGATE_ID')
                    if agg_id == None or agg_id <= 0:
                        agg_fn = self.get_function(agg_fn)
                    else:
                        agg_fn = agg_id
                if override_time:
                    calc_start = start_time - lookback_time
                    calc_end = end_time
                time_tag = self.get(rid, 'TIME_TAG', ascii=True)
                if time_tag:
                    ok = False
                    time_hid = self.tag2hid(time_tag)
                    if time_hid != None:
                        agg_times, agg_values = self.gethis(time_tag, calc_start, calc_end, max_len=max_len)
                        if len(agg_times) > 0:
                            over_read_sec = self.get(rid, 'CALC_INTERVAL')
                            if not over_read_sec:
                                over_read_sec = self.get('SystemSettings', 'VALUE', 'CalcFreqDefault')
                                try:
                                    over_read_sec = int(over_read_sec)
                                except TypeError:
                                    over_read_sec = 60

                            calc_start = agg_times[0]
                            calc_end = agg_times[-1] + self.sec2time(over_read_sec)
                            ok = True
                    if not ok:
                        self.calc_err = 'The TIME_TAG contains no history values.'
                        self.calc_err_list = [self.calc_err]
                        self.calc_code = ''
                        return self.empty_h_tuple()
                else:
                    if not calc_start:
                        calc_start = self.get(rid, 'CALC_START')
                    if not calc_start:
                        calc_start = self.get('SystemSettings', 'VALUE', 'CalcStartDefault')
                        if isinstance(calc_start, str):
                            calc_start = self.ascii2time(calc_start.strip())
                    freq = self.get(rid, 'CALC_INTERVAL')
                    if not freq:
                        freq = self.get('SystemSettings', 'VALUE', 'CalcFreqDefault')
                        try:
                            freq = int(freq)
                        except TypeError:
                            freq = 60

            if freq2 is None:
                freq2 = freq
            if adhoc_calc or self.get(rid, 'SAVE_TIME') > self.get(rid, 'COMPILED_TIME'):
                all_tags = [ t.upper() for t in self.lsname('AnalogDef') + self.lsname('CalculationDef') + self.lsname('PredictionDef') + self.lsname('DiscreteDef') ]
                all_tags2 = [ t.upper() for t in self.lsname('SliceSetDef') ]
                now_match_tags = []
                now_match_tags2 = []
                if not adhoc_calc:
                    constant_tags = self.list_keys(record, 'constant_description', ascii=True)
                    if len(constant_tags) > 0:
                        constant_tags_re = '|'.join(constant_tags)
                        now_tags_re = '(?<![A-Za-z0-9_:\\."\'])(' + constant_tags_re + ')(?![\\(A-Za-z0-9_:\\.])'
                        now_match_tags = re.findall(now_tags_re, code)
                        if len(now_match_tags) > 0:
                            sub_dict = dict([ (t, str(self.get(name, 'constant_value', t))) for t in now_match_tags ])
                            if len(sub_dict) > 0:
                                code = multiple_replace(sub_dict, code, pre='(?<![A-Za-z0-9_:\\."\'])', post='(?![\\(A-Za-z0-9_:\\.])')
                if not adhoc_calc:
                    input_tags = self.list_keys(record, 'input_description', ascii=True)
                    if len(input_tags) > 0:
                        input_tags_re = '|'.join(input_tags)
                        now_tags_re = '(?<![A-Za-z0-9_:\\."\'])(' + input_tags_re + ')(?![\\(A-Za-z0-9_:\\.])'
                        now_match_tags = re.findall(now_tags_re, code)
                        if len(now_match_tags) > 0:
                            sub_dict = dict([ (t, '{%s}' % self.get(record, 'input_tag', t, ascii=True)) for t in now_match_tags ])
                            if len(sub_dict) > 0:
                                code = multiple_replace(sub_dict, code, pre='(?<![A-Za-z0-9_:\\."\'])', post='(?![\\(A-Za-z0-9_:\\.])')
                now_tags_re = '{(.+?)}'
                now_match_tags = re.findall(now_tags_re, code)
                sub_dict = {}
                if len(now_match_tags) > 0:
                    now_match_tags2 = unique([ t for t in now_match_tags if t.upper() in all_tags2 ])
                    sub_dict2 = dict([ ('{%s}' % t, '_s[%d]' % i) for i, t in enumerate(now_match_tags2) ])
                    if len(sub_dict2) > 0:
                        code = re.sub(': *\n', ' :\n', code)
                        code = multiple_replace(sub_dict2, code)
                    now_match_tags = unique([ t for t in now_match_tags if t.upper() in all_tags ])
                    sub_dict = dict([ ('{%s}' % t, '_a[%d]' % i) for i, t in enumerate(now_match_tags) ])
                    if len(sub_dict) > 0:
                        code = re.sub(': *\n', ' :\n', code)
                        code = multiple_replace(sub_dict, code)
                match_tags = [ t for t in now_match_tags ]
                slice_tags = [ t for t in now_match_tags2 ]
                curly_count = len(match_tags)
                now_tags_re = '(?<![A-Za-z0-9_:\\."\'])([A-Za-z0-9_:\\.]+)(?![\\(A-Za-z0-9_:\\.])'
                now_match_tags = re.findall(now_tags_re, code)
                sub_dict = {}
                if len(now_match_tags) > 0:
                    now_match_tags2 = unique([ t for t in now_match_tags if t.upper() in all_tags2 ])
                    sub_dict2 = dict([ (t, '_s[%d]' % i) for i, t in enumerate(now_match_tags2) ])
                    if len(sub_dict2) > 0:
                        code = re.sub(': *\n', ' :\n', code)
                        code = multiple_replace(sub_dict2, code, pre='(?<![A-Za-z0-9_:\\."\'])', post='(?![\\(A-Za-z0-9_:\\.])')
                    now_match_tags = unique([ t for t in now_match_tags if t.upper() in all_tags ])
                    sub_dict = dict([ (t, '_a[%d]' % (i + curly_count)) for i, t in enumerate(now_match_tags) ])
                    if len(sub_dict) > 0:
                        code = re.sub(': *\n', ' :\n', code)
                        code = multiple_replace(sub_dict, code, pre='(?<![A-Za-z0-9_:\\."\'])', post='(?![\\(A-Za-z0-9_:\\.])')
                match_tags += [ t for t in now_match_tags if t in sub_dict.keys() ]
                match_tags = unique(match_tags)
                slice_tags += [ t for t in now_match_tags2 if t in sub_dict2.keys() ]
                slice_tags = unique(slice_tags)
                if not adhoc_calc and len(match_tags) == 0:
                    if override_time:
                        return self.gethis_nan(start_time, end_time, freq2, max_len=max_len)
                    self.calc_err = 'The calculation code contains no valid tag names.'
                    self.calc_err_list = [self.calc_err]
                    self.calc_code = code
                    return self.empty_h_tuple()
                all_funcs = self.lsname('FunctionDef')
                all_funcs_re = '|'.join(all_funcs)
                all_funcs_re = '(?<![A-Za-z0-9_])(' + all_funcs_re + ')\\('
                match_funcs = re.findall(all_funcs_re, code)
                f_code = ''
                f_code_dict = {}
                for f in match_funcs:
                    f_code += self.get(f, 'CODE') + '\n'
                    f_code_dict[f] = f_code

                f_code_top = ''
                for f in match_funcs:
                    match_funcs = re.findall(all_funcs_re, f_code_dict[f])
                    for f in match_funcs:
                        f_code_top += self.get(f, 'CODE') + '\n'

                f_code = f_code_top + '\n' + f_code
                if len(f_code) > 0:
                    f_code = re.sub('^|\n', '\n\t', f_code)
                ftext = ''
                for i, t in enumerate(slice_tags):
                    ftext += '# _s[%d] = %s\n' % (i, t)

                for i, t in enumerate(match_tags):
                    ftext += '# _a[%d] = %s\n' % (i, t)

                if len(ftext) > 0:
                    ftext += '\n'
                if adhoc_calc:
                    ftext += 'def _f(_a,_s,_v,db):\n%s\n\treturn %s\n' % (f_code, code)
                else:
                    code = re.sub('\n', '\n\t', code)
                    if len(f_code) > 3:
                        ftext += 'def _f(_a,_s,_v,db):\n\t%s\n\t%s\n' % (f_code, code)
                    else:
                        ftext += 'def _f(_a,_s,_v,db):\n\t%s\n' % code
                if not adhoc_calc:
                    self.put(rid, 'COMPILED_CODE', ftext)
                    tags = slice_tags + match_tags
                    self.putlist((rid, 'TAG'), tags, notify=True)
                    fill_default = self.get(('SystemSettings', 'VALUE', 'CalcFillDefault'), text=True).strip()
                    if fill_default == '1':
                        self.putlist((rid, 'TAG_FILL'), [1] * len(tags), notify=True)
                        self.putlist((rid, 'TAG_NULL'), [0] * len(tags), notify=True)
                    else:
                        tag_fills = []
                        tag_nulls = []
                        for t in tags:
                            hcfg = self.get_h_cfg(t)
                            if hcfg != None:
                                h, btype, c = hcfg
                                dtype = HISTORY_BTYPES[btype]
                                if dtype in (float16, float32, float64):
                                    tag_fills.append(0)
                                    tag_nulls.append(0)
                                else:
                                    tag_fills.append(1)
                                    tag_nulls.append(0)
                            else:
                                tag_fills.append(0)
                                tag_nulls.append(0)

                        self.putlist((rid, 'TAG_FILL'), tag_fills, notify=True)
                        self.putlist((rid, 'TAG_NULL'), tag_nulls, notify=True)
                match_tags = [ self.id2name(t) for t in match_tags ]
            else:
                match_tags = self.getlist(rid, 'TAG')
                slice_tags = [ t for t in match_tags if self.type(t, ascii=True) == 'SliceSetDef' ]
                match_tags = [ t for t in match_tags if self.type(t, ascii=True) != 'SliceSetDef' ]
                ftext = self.get(rid, 'COMPILED_CODE')
            if not adhoc_calc and item_path and ftext.find('{') != -1:
                ftext = self.tag_expression_replace(ftext, item_path)
            if not adhoc_calc:
                tag_fills = []
                tag_nulls = []
                tag_functions = []
                for tag, tag_fn, tag_fill, tag_null in self.getlist(rid, ('TAG', 'TAG_FUNCTION', 'TAG_FILL', 'TAG_NULL')):
                    if tag in match_tags:
                        tag_fills.append(tag_fill == 'YES')
                        if tag_null in (None, ''):
                            tag_null = 0
                        tag_nulls.append(int(tag_null))
                        if tag_fn:
                            agg_id = self.get(tag_fn, 'AGGREGATE_ID')
                            if agg_id == None or agg_id <= 0:
                                tag_fn = self.get_function(tag_fn)
                            else:
                                tag_fn = agg_id
                        else:
                            tag_fn = agg_fn
                        tag_functions.append(tag_fn)

            if adhoc_calc and len(match_tags) == 0 and adhoc_base:
                t = self.name2id(adhoc_base)
                if t:
                    calc_start = self.first_h_time(adhoc_base)
                    calc_end = self.last_h_time(adhoc_base)
            if not calc_start:
                start_times = [ self.first_h_time(t) for t in match_tags ]
                start_times = [ t for t in start_times if t != None ]
                start_times.sort()
                if len(start_times) > 0:
                    calc_start = start_times[0]
            if not calc_end:
                end_times = [ self.last_h_time(t) for t in match_tags ]
                end_times = [ t for t in end_times if t != None ]
                end_times.sort()
                if len(end_times) > 0:
                    calc_end = end_times[-1] + self.sec2time(freq) + 10 * MSEC
            if not calc_start or not calc_end:
                self.calc_err = 'None of the tags in the calculation contain any data.'
                self.calc_err_list = [self.calc_err]
                self.calc_code = code
                return self.empty_h_tuple()
            if freq and freq > 0:
                new_start = self.ms2time(self.time2ms(calc_end) - int(freq * 1000) * (abs(max_len) - 1))
                if new_start > calc_start:
                    calc_start = new_start
            if adhoc_calc and len(match_tags) == 0:
                agg_times = self.trange(calc_start, calc_end, freq)
                values = numpy.zeros(len(agg_times), dtype=float32)
                data = array([values])
                slice_data = []
                ftext = ftext.replace('return ', 'return _a[0]+')
            elif adhoc_calc and len(match_tags) == 1:
                agg_times, values = self.gethis(match_tags[0], calc_start, calc_end)
                data = array([values])
                slice_data = []
            else:
                data = [0] * len(match_tags)
                for i, t in enumerate(match_tags):
                    if adhoc_calc:
                        tag_fill = fill
                        tag_null = 0
                        tag_fn = agg_fn
                    else:
                        tag_fill = tag_fills[i]
                        tag_null = tag_nulls[i]
                        tag_fn = tag_functions[i]
                    times, values = self.gethis(t, calc_start, calc_end, agg_fill=True)
                    if len(times) == 0:
                        self.calc_err = 'The tag %s returned no data.' % t
                        self.calc_err_list = [self.calc_err]
                        self.calc_code = code
                        return self.empty_h_tuple()
                    if agg_times is None:
                        if time_sync:
                            calc_start = times[0]
                        agg_times = self.trange(calc_start, calc_end, freq)
                    try:
                        data[i] = self.timealign(times, values, agg_times, tag_fn, fill=tag_fill, null=tag_null)
                    except:
                        import traceback
                        etype, value, tb = sys.exc_info()
                        self.calc_err_list = traceback.format_exception(etype, value, tb.tb_next)
                        self.calc_err = str(value)
                        self.calc_code = self.get(self.get(rid, 'AGG_FUNCTION'), 'CODE')
                        return self.empty_h_tuple()

                slice_data = numpy.empty((len(slice_tags), len(agg_times)), dtype=numpy.bool)
                for i, t in enumerate(slice_tags):
                    slice_data[i] = self.slice2bools(t, agg_times)

            sys.stdout = PrintLogger(self, self.name2id(record))
            try:
                exec (ftext in globals(), locals())
                values = _f(data, slice_data, None, self)
            except Exception as e:
                import traceback
                etype, value, tb = sys.exc_info()
                self.calc_err_list = traceback.format_exception(etype, value, tb.tb_next)
                self.calc_err = str(value)
                agg_times, values = self.empty_h_tuple()
                value = None
                time = None
            else:
                if not isinstance(values, numpy.ndarray):
                    if override_time:
                        return self.gethis_nan(start_time, end_time, freq2, max_len=max_len)
                    self.calc_err = 'The calculation does not return an array of values.'
                    self.calc_err_list = [self.calc_err]
                    self.calc_code = ftext
                    agg_times, values = self.empty_h_tuple()
                    time = None
                    value = None
                elif len(values) > 0:
                    self.calc_err = None
                    self.calc_err_list = None
                    time = agg_times[-1]
                    value = values[-1]
                    if not ascii:
                        if isgood(value):
                            value = float(value)
                        else:
                            value = None
                else:
                    if override_time:
                        if end_time is not None:
                            return self.gethis_nan(start_time, end_time, freq2, max_len=max_len)
                        else:
                            return self.empty_h_tuple()
                    self.calc_err = 'The calculation contains no tags which produce historical values.'
                    self.calc_err_list = [self.calc_err]
                    self.calc_code = ftext
                    time = None
                    value = None
            finally:
                self.calc_code = ftext

            sys.stdout = sys.__stdout__
            if freq2 and not time_sync:
                agg_times2 = self.trange(start_time, end_time, freq2)
                if len(agg_times) == 0:
                    return self.empty_h_tuple()
            if agg_times2 is not None:
                if agg_fn2 in (None, 1):
                    values = self.timealign(agg_times, values, agg_times2, 1, 0, 0)
                else:
                    if isinstance(agg_fn2, str):
                        agg_fn2 = self.get_function(agg_fn2)
                        if agg_fn2 == None:
                            return self.empty_h_tuple()
                    try:
                        values = self.timealign(agg_times, values, agg_times2, agg_fn2, 0, 0)
                    except:
                        return self.empty_h_tuple()

                if len(values) > 0:
                    value = values[-1]
                else:
                    value = None
                agg_times = agg_times2
            self.put(record, self.VALUE_FT, value, notify=False)
            if len(agg_times) > 0:
                self.put(record, self.TIME_FT, agg_times[-1])
            else:
                self.put(record, self.TIME_FT, 0)
            if lookback_time > 0:
                i = agg_times >= start_time
                agg_times = agg_times[i]
                values = values[i]
            if ascii:
                agg_times = self.times2ascii(agg_times)
            if not isinstance(values, numpy.ndarray):
                values = numpy.array(values)
            if values.dtype in (float16, float32, float64):
                values[isinf(values)] = nan
            return (agg_times, values)

    def gethis_pred(self, tag, ascii = False):
        SELF = tag
        linenum = 0
        t1 = self.now()
        result = [(t1, 0)]

        def logtxt(linenum, variable):
            linenum = linenum + 1
            self.put(SELF, '#OUTPUT_LINES', linenum)
            self.put(SELF, 'OUTPUT_LINE', variable, linenum)
            return linenum

        def interpol(X):
            if isnan(X[0]):
                X[0] = X[isfinite(X)][0]
            if isnan(X[-1]):
                X[-1] = X[isfinite(X)][-1]
            t = arange(len(X), dtype=float)
            t1 = t[isfinite(X)]
            v1 = X[isfinite(X)]
            t2 = t[isnan(X)]
            ifunc = interp1d(t1, v1)
            v2 = ifunc([t2])
            X[isnan(X)] = v2
            return X

        def mdif(step):
            ncof = len(step)
            imp = [0.0] * ncof
            imp[0] = step[0]
            for i in range(1, ncof):
                imp[i] = step[i] - step[i - 1]

            return imp

        msgtxt = 'Prediction: %s  - started at %s' % (self.get(SELF, 'NAME', ascii=True), self.time2ascii(t1))
        linenum = logtxt(linenum, msgtxt)
        mdlname = self.get(SELF, 'MODEL_NAME', ascii=True)
        if len(mdlname) == 0:
            linenum = logtxt(linenum, 'Error - no model specified')
            return result
        ttss = float(self.get(mdlname, 'SS_TIME'))
        ncof = int(self.get(mdlname, '#COEFFICIENTS'))
        nind = int(self.get(mdlname, '#INDEPENDENTS'))
        ndep = int(self.get(mdlname, '#DEPENDENTS'))
        resp = self.getlist(mdlname, 'MOD_RESPONSE')
        mdl_indinfo = self.getlist(mdlname, ['IND_NAME', 'IND_DESCRIPTION', 'IND_UNITS'])
        mdl_depinfo = self.getlist(mdlname, ['DEP_NAME',
         'DEP_DESCRIPTION',
         'DEP_UNITS',
         'RAMP_INDICATOR'])
        tsamp = 60.0 * ttss / ncof
        depindex = int(self.get(SELF, 'DEP_INDEX'))
        if depindex < 1 or depindex > ndep:
            msgtxt = 'DEP_INDEX must in range 1 to %d' % ndep
            linenum = logtxt(linenum, msgtxt)
            return result
        depname = self.get(SELF, 'DEP_NAME', ascii=True)
        if len(depname) == 0:
            linenum = logtxt(linenum, 'Error - no dependent variable specified')
            return result
        nindpred = int(self.get(SELF, '#INDEPENDENTS'))
        if nindpred < 1 or nindpred > nind:
            msgtxt = '#INDEPENDENTS must in range 1 to %d' % nind
            linenum = logtxt(linenum, msgtxt)
            return result
        indinfo = self.getlist(SELF, ['IND_NAME', 'IND_INDEX', 'IND_ACTIVE'])
        for info in indinfo:
            k = int(info[1])
            if k < 1 or k > nind:
                msgtxt = 'IND_INDEX must in range 1 to %d (%s)' % (nind, info[0])
                linenum = logtxt(linenum, msgtxt)
                return result

        msgtxt = 'Modelname used: %s' % mdlname
        linenum = logtxt(linenum, '')
        linenum = logtxt(linenum, msgtxt)
        msgtxt = '    TTSS=%f   NCOEF=%d  NIND=%d  NDEP=%d   (TSAMP=%f)' % (ttss,
         ncof,
         nind,
         ndep,
         tsamp)
        linenum = logtxt(linenum, msgtxt)
        info = mdl_depinfo[depindex - 1][0]
        ramp = int(mdl_depinfo[depindex - 1][3])
        msgtxt = '  DEP VEC name: %s (%s/%s)   - Name in MDL: %s   (mdl-index=%d) RAMP=%d' % (depname,
         self.get(depname, 'DESCRIPTION'),
         self.get(depname, 'ENG_UNITS'),
         info,
         depindex,
         ramp)
        linenum = logtxt(linenum, '')
        linenum = logtxt(linenum, 'Vectors used in Prediction')
        linenum = logtxt(linenum, msgtxt)
        tags = [depname]
        nindactive = 0
        for i in range(nindpred):
            indname = indinfo[i][0]
            indindex = int(indinfo[i][1])
            indactive = indinfo[i][2]
            if indactive == 'ON':
                tags.append(indname)
                nindactive = nindactive + 1
            info = mdl_indinfo[indindex - 1]
            msgtxt = '  IND VEC name: %s  (%s/%s) - Name in MDL: %s  (mdl-index=%d)  Active=%s' % (indname,
             self.get(indname, 'DESCRIPTION'),
             self.get(indname, 'ENG_UNITS'),
             info[0],
             indindex,
             indactive)
            linenum = logtxt(linenum, msgtxt)

        self.put(SELF, 'CALC_INTERVAL', tsamp)
        starttime = self.get(SELF, 'CALC_START')
        npred = self.get(SELF, 'FUTURE_SAMPLES')
        if npred < 0:
            npred = 0
        linenum = logtxt(linenum, '')
        linenum = logtxt(linenum, 'History call results:')
        linenum = logtxt(linenum, tags)
        times, values = self.gethis(depname)
        starttime = times[0]
        endtime = times[-1]
        timedata = []
        vecdata = []
        for tag in tags:
            timedata, values = self.gethis(tag, start_time=starttime, end_time=endtime, freq=tsamp)
            vecdata.append(values)

        t = timedata[-1]
        timedata = list(timedata)
        vecdata = [ [ vecdata[j][i] for j in range(len(tags)) ] for i in range(len(timedata)) ]
        datalength = len(timedata)
        if datalength < ncof + 2:
            msgtxt = 'Error: not enough data returned (len=%d).  Is start time set correctly?' % datalength
            linenum = logtxt(linenum, msgtxt)
            return result
        msgtxt = '  First Value at: %s   Last Value at: %s    Data Length: %d' % (self.time2ascii(timedata[0]), self.time2ascii(timedata[-1]), datalength)
        linenum = logtxt(linenum, msgtxt)
        t2 = self.now()
        msgtxt = '  History Retrival Complete at: %s    - duration: %f sec' % (self.time2ascii(t2), t2 - t1)
        linenum = logtxt(linenum, msgtxt)
        dlen = datalength + npred
        initval = vecdata[0][0]
        deppred = zeros(dlen) + initval
        for k in range(npred):
            t = timedata[-1] + self.sec2time(tsamp)
            timedata.append(t)
            vecdata.append(vecdata[-1][:])

        dataarray = numpy.array(vecdata, float)
        cvraw = interpol(dataarray[:, 0])
        cvval = cvraw[0]
        if ramp > 0:
            cvraw = lfilter([1, -1], [1, 0], cvraw - cvval)
            lastslope = cvraw[-npred - 1]
            for k in range(npred):
                cvraw[-npred + k] = lastslope

            cvraw = cvraw + cvval
        linenum = logtxt(linenum, '')
        msgtxt = 'Processing %d Independent Contributions' % nindactive
        linenum = logtxt(linenum, msgtxt)
        idata = 0
        for k in range(nindpred):
            indactive = indinfo[k][2]
            if indactive == 'ON':
                mv = interpol(dataarray[:, idata + 1])
                mvval = mv[0]
                mvdel = mv - mvval
                cvdel = zeros(dlen)
                mvindex = int(indinfo[k][1])
                mvname = indinfo[k][0]
                step = resp[mvindex - 1][depindex - 1][:]
                imp = mdif(step)
                if ramp > 0:
                    imp = mdif(imp)
                qsum = sum(abs(array(step)))
                msgtxt = '  k=%d   len=%d  init-val=%f  mdl-index=%d   finalval=%f  name=%s  qsum=%f ' % (k,
                 len(mvdel),
                 mvval,
                 mvindex,
                 step[-1],
                 mvname,
                 qsum)
                linenum = logtxt(linenum, msgtxt)
                if qsum > 1e-12:
                    b = numpy.array(imp)
                    a = numpy.zeros(ncof)
                    a[0] = 1
                    mvdel = hstack((zeros(ncof), mvdel))
                    cvdel = lfilter(b, a, mvdel)
                    cvdel = cvdel[ncof:]
                    deppred = deppred + cvdel
                idata = idata + 1

        prederrfilt = 0.0 * deppred
        tfilt = self.get(SELF, 'PRED_ERR_FILTER')
        if tfilt <= 0:
            frac = 0
        else:
            frac = exp(-(tsamp / 60) / tfilt)
            msgtxt = 'Applying Prediction Error filtering.  Filter Factor = %f ' % frac
            linenum = logtxt(linenum, msgtxt)
        if frac > 0:
            prederr = cvraw - deppred
            if npred > 0:
                prederr[-npred:] = prederr[-npred - 1]
                a = [1.0, -frac]
                b = [1 - frac, 0.0]
                prederrfilt = lfilter(b, a, prederr)
        deppred = deppred + prederrfilt
        if ramp > 0:
            inival = deppred[0]
            nlen = len(deppred)
            deppred = deppred - inival
            temp = zeros(nlen)
            temp[0] = deppred[0]
            for k in range(1, nlen):
                temp[k] = temp[k - 1] + deppred[k]

            deppred = temp + inival
        t2 = self.now()
        msgtxt = 'Prediction: first=%f  last=%f  - vector length = %d ' % (deppred[0], deppred[-1], len(deppred))
        linenum = logtxt(linenum, msgtxt)
        msgtxt = 'Prediction complete at %s  -   %f seconds  ' % (self.time2ascii(t2), t2 - t1)
        linenum = logtxt(linenum, '')
        linenum = logtxt(linenum, msgtxt)
        return (timedata, deppred)

    def get_calc_err(self):
        return self.calc_err

    def get_calc_err_list(self):
        return self.calc_err_list

    def get_calc_code(self):
        return self.calc_code

    def is_calc(self, tag):
        if isinstance(tag, tuple):
            if tag[1] not in ('VALUE', self.VALUE_FT):
                return False
            tag = tag[0]
        if tag in (None, ''):
            return False
        elif self.is_adhoc_calc(tag):
            return True
        else:
            return self.get_defid(tag) == self.CALCULATION_DEF

    def is_adhoc_calc(self, tag):
        if not isinstance(tag, str) or len(tag) == 0:
            return False
        return tag[0] in ('=', '@')

    def is_adhoc_constant(self, tag):
        if adhoc_constant_pattern.match(tag):
            return True
        else:
            return False

    def is_pred(self, tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        if tag in (None, ''):
            return False
        else:
            if type(tag) == types.IntType:
                tag = self.id2name(tag)
            return self.get_defid(tag, True) == 'PredictionDef'

    def put(self, tag, value, oldv = None, occ = 0, idx = 0, add_keys = False, activate = True, notify = True, key_order = None, unicode_raw = False, has_history = False):
        try:
            if oldv is None:
                if add_keys and len(tag) > 2 and isinstance(tag[2], str):
                    self.key2idx(tag[2], add_keys=True)
                uid = self.tag2uid(tag)
                if uid == None:
                    return False
                rid, fid, occ = uid
                tag = uid
            else:
                rid = self.name2id(tag)
                fid = self.name2id(value)
                if idx != 0:
                    occ = idx
                if isinstance(occ, str):
                    occ = self.key2idx(occ, add_keys)
                if rid == None or fid == None or occ == None:
                    return False
                value = oldv
                tag = (rid, fid, occ)
            if isinstance(value, str) and not unicode_raw:
                if self.unicode_mode and fid in self.unicode_fields:
                    value = '\\u' + value.encode('utf-16')
                else:
                    value = cast_str(value)
            did = self.get_defid(rid)
            if did == None:
                return False
            if not self._pps_query(did, P_WRITE, rid):
                return False
            if type(value) in (numpy.float16, numpy.float32, numpy.float64):
                value = float(value)
            if did in (self.ANALOG_DEF, self.DISCRETE_DEF) and fid != self.VALUE_FT and not has_history:
                hcfg = None
            else:
                hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg != None:
                hid, btype, cos = hcfg
                if cos:
                    old_value = self.get(rid, fid, occ)
            tfld = None
            dtype = self.getdef(did, fid, DEF_DTYPE)
            format = self.getdef(did, fid, DEF_FORMAT, dref=rid)
            repeat = self.getdef(did, fid, DEF_REPEAT)
            if repeat:
                repeat_type = self.getdef(did, repeat, DEF_DTYPE)
            else:
                repeat_type = None
            chain = self.getdef(did, fid, DEF_CHAIN)
            if dtype == DT_FLOAT and value == None:
                value = nan
            if dtype == None:
                return False
            if repeat != None and repeat_type not in (DT_DICTIONARY, DT_SPREADSHEET):
                if occ == 0:
                    return False
                num_occ = self.get(rid, repeat)
                if occ > num_occ:
                    return False
            if repeat == None and occ != 0:
                return False
            if dtype == DT_LIST:
                num_occ = self.get(rid, fid)
            if fid == NAME:
                if not isinstance(value, str) or value.strip() == '':
                    return False
                old_name = self.get(rid, NAME)
                if self.name2id(value) != None and value.upper() != old_name.upper():
                    return False
                if did in (self.ANALOG_DEF, self.DISCRETE_DEF, self.CALCULATION_DEF):
                    self._del_desc_key(rid)
                self.rdb.hdel('name', old_name.upper())
                self.rdb.hset('name', value.upper(), pack('>I', rid))
                self.rdb.hdel('name2', old_name)
                self.rdb.hset('name2', value, pack('>I', rid))
                self.rdb.hdel(pkey('sdef', did), old_name)
                self.rdb.hset(pkey('sdef', did), value, pack('>I', rid))
                if self.id_cache.has_key(old_name.upper()):
                    del self.id_cache[old_name.upper()]
            if fid == self.DESCRIPTION_FT and did in (self.ANALOG_DEF, self.DISCRETE_DEF, self.CALCULATION_DEF):
                self._del_desc_key(rid)
                self._add_desc_key(rid, value)
            if hcfg == None:
                data = self.pack_field(value, dtype, format)
                if data == None:
                    return False
                self.rdb.hset(pkey('rec', rid), pfld(fid, occ), data)
                if fid == NAME and did in (self.ANALOG_DEF, self.DISCRETE_DEF, self.CALCULATION_DEF):
                    if self.DESCRIPTION_FT != None:
                        self._add_desc_key(rid, self.get(rid, self.DESCRIPTION_FT))
                if dtype == DT_LIST:
                    repeat_fids = self.list(did, repeat=fid)
                    if num_occ == None:
                        num_occ = 0
                    value = int(value)
                    if value > num_occ:
                        default_values = []
                        for f in repeat_fids:
                            default = self.getdef(did, f, DEF_DEFAULT)
                            dtype = self.getdef(did, f, DEF_DTYPE)
                            if default == None:
                                default_values.append(self.default_value(dtype))
                            else:
                                default_values.append(self.pack_field(default, dtype))
                        for new_occ in range(num_occ + 1, int(value) + 1):
                            for i, f in enumerate(repeat_fids):
                                self.rdb.hset(pkey('rec', rid), pfld(f, new_occ), default_values[i])

                    elif value < num_occ:
                        for old_occ in range(value + 1, num_occ + 1):
                            for f in repeat_fids:
                                f_dtype = self.getdef(did, f, DEF_DTYPE)
                                if f_dtype in (DT_RECORD, DT_FIELD):
                                    self.putref((rid, f, old_occ), None)
                                self.rdb.hdel(pkey('rec', rid), pfld(f, old_occ))
                                if f_dtype == DT_SCHEDULE:
                                    self.rdb.hdel('sched', self.uid(rid, f, old_occ))
                                    self.rdb.publish('del_sched', self.uid(rid, f, old_occ))

                elif dtype == DT_HISTORY:
                    pass
                elif dtype == DT_SCHEDULE:
                    self.rdb.hset('sched', self.uid(rid, fid, occ), data)
                    self.rdb.sadd(pkey('sched', rid), self.uid(rid, fid, occ))
                    self.rdb.publish('put_sched', self.uid(rid, fid, occ) + data)
                elif dtype == DT_INTEGER and fid == self.SCHEDULE_FREQ_FT:
                    self.rdb.publish('put_freq', self.uid(rid, fid, occ) + data)
                elif dtype == DT_RECORD:
                    ref = self.unpack_field(data, dtype)
                    self.putref((rid, fid, occ), ref)
                    if self.h_meta_cache.has_key(did):
                        del self.h_meta_cache[did]
                elif dtype == DT_FIELD:
                    ref = self.unpack_field(data, dtype)
                    self.putref((rid, fid, occ), ref)
                if repeat != None and repeat_type == DT_DICTIONARY:
                    self.putref((rid, fid, occ), occ)
                if (key_order or add_keys) and repeat_type == DT_SPREADSHEET:
                    if key_order == None:
                        key_order = 9999
                    self.rdb.hset(pkey('order', rid), pfld(repeat, occ), pack('>I', key_order))
            if activate:
                self.activate(rid, chain, occ)
                if hcfg != None:
                    ts = self.now()
                    times = numpy.array([ts], dtype=float64)
                    h_dtype = HISTORY_BTYPES[btype]
                    try:
                        values = numpy.array([value], dtype=h_dtype)
                    except ValueError:
                        if value == '?':
                            values = numpy.array([numpy.nan])
                            self.puthis(tag, times, values, verify=False)
                    else:
                        self.puthis(tag, times, values, verify=False)

            if notify:
                self.send_event((rid, fid, occ), (did, fid, occ))
                if fid in (self.VALUE_FORMAT_FT, self.FORMAT_RECORD_FT):
                    self.send_event((rid, self.VALUE_FT, 0), (did, self.VALUE_FT, 0))
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def allocate_hid(self):
        data = self.rdb.lpop('free_hid')
        hid, = unpack('>I', data)
        return hid

    def allocate_hids(self, count):
        pipe = self.rdb.pipeline(transaction=False)
        for i in range(count):
            pipe.lpop('free_hid')

        rows = pipe.execute()
        hid_list = []
        for row in rows:
            hid, = unpack('>I', row)
            hid_list.append(hid)

        return hid_list

    def deallocate_hid(self, hid):
        self.rdb.rpush('free_hid', pack('>I', hid))

    def put_h_cfg(self, tag, hfile = None, dtype = None, complib = None):
        if not self._pps_query(None, P_WRITE):
            return False
        elif dtype != None and self.dtype2btype(dtype) == None:
            return
        else:
            if isinstance(dtype, str):
                if HISTORY_CUSTOM_DTYPES.has_key(dtype):
                    dtype = HISTORY_CUSTOM_DTYPES[dtype]
                else:
                    dtype = numpy.dtype(dtype).type
            if dtype == numpy.bool:
                dtype = numpy.bool8
            if hfile == None or dtype == None or complib == None:
                hfile_default = 'HistoryFile1'
                dtype_default = numpy.float32
                complib_default = None
                hcfg = self.get_h_cfg(tag)
                if hcfg:
                    hid, btype, complib_default = hcfg
                    dtype_default = HISTORY_BTYPES[btype]
                    hfile_default = hid.hfile
                if hfile == None:
                    hfile = hfile_default
                if dtype == None:
                    dtype = dtype_default
                if complib == None:
                    complib = complib_default
            uid = self.tag2uid(tag)
            if uid == None:
                return
            rid, fid, kid = uid
            hfile = self.name2id(hfile)
            if hfile == None:
                return
            complib = self.name2id(complib)
            if complib == None:
                complib = 0
            if dtype in HISTORY_DTYPES:
                btype = HISTORY_DTYPES[dtype]
            else:
                return
            key = pack('>III', rid, fid, kid)
            if self.rdb.hexists('hr', key):
                p = self.get_h_cfg((rid, fid, kid))
                hid = p[0].hid
                if self.hid_reverse_cache.has_key(hid):
                    keys = self.hid_reverse_cache[hid].keys()
                    self.hid_reverse_cache.pop(hid)
                    map(self.hid_cache.pop, keys)
            else:
                hid = self.allocate_hid()
            pvalue = pack('>IIBI', hfile, hid, btype, complib)
            self.rdb.hset('hr', key, pvalue)
            self.rdb.zadd('zhr', key, 0)
            self.hcfg_cache[tag] = (HID(hfile, hid), btype, complib)
            return HID(hfile, hid)

    def get_h_cfg(self, tag, text = False, ascii = False, cached = False):
        if text:
            ascii = True
        if cached and tag in self.hcfg_cache:
            return self.hcfg_cache[tag]
        else:
            uid = self.tag2uid(tag)
            if uid == None:
                return
            rid, fid, kid = uid
            pkey = pack('>III', rid, fid, kid)
            pvalue = self.rdb.hget('hr', pkey)
            if pvalue == None:
                return
            if len(pvalue) == 10:
                hfile, hid, btype, complib = unpack('>IIBB', pvalue)
            else:
                hfile, hid, btype, complib = unpack('>IIBI', pvalue)
            self.hcfg_cache[tag] = (HID(hfile, hid), btype, complib)
            if ascii:
                if complib == 0:
                    complib = ''
                else:
                    complib = self.id2name(complib)
                return (self.id2name(hfile), self.get_btype_name(btype), complib)
            return (HID(hfile, hid), btype, complib)
            return

    def mget_h_cfg(self, tags, field = None):
        if field == None:
            field = 'VALUE'
        rids = self.names2ids(tags)
        fid = self.name2id(field)
        uids = [ ((rid, fid, 0) if rid != None else None) for rid in rids ]
        pipe = self.rdb.pipeline(transaction=False)
        for uid in uids:
            if uid == None:
                rid = 4294967295
                fid = 0
                kid = 0
            else:
                rid, fid, kid = uid
            pkey = pack('>III', rid, fid, kid)
            pipe.hget('hr', pkey)

        rows = pipe.execute()
        rule_list = []
        for i, row in enumerate(rows):
            if row == None:
                rule_list.append(None)
            else:
                hfile, hid, btype, complib = unpack('>IIBI', row)
                rule_list.append((HID(hfile, hid), btype, complib))
                self.hcfg_cache[tags[i]] = (HID(hfile, hid), btype, complib)

        return rule_list

    def del_h_cfg(self, tag):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            uid = self.tag2uid(tag)
            if uid == None:
                return
            rid, fid, kid = uid
            hid = self.tag2hid((rid, fid, kid))
            if hid == None:
                return
            self.delhis(tag)
            key = pack('>III', rid, fid, kid)
            self.rdb.hdel('hr', key)
            self.rdb.zrem('zhr', key)
            self.deallocate_hid(hid.hid)
            if self.hid_reverse_cache.has_key(hid.hid):
                keys = self.hid_reverse_cache[hid.hid].keys()
                self.hid_reverse_cache.pop(hid.hid)
                map(self.hid_cache.pop, keys)
            if self.hcfg_cache.has_key(tag):
                del self.hcfg_cache[tag]
            return

    def list_h_cfg(self, record = 0, field = 0, key = 0, text = False, ascii = False, hfile = None, hids = False, include_def = True):
        if text:
            ascii = True
        rid = self.name2id(record)
        fid = self.name2id(field)
        kid = self.name2id(key)
        hfile = self.name2id(hfile)
        if rid == None:
            return []
        else:
            start, end = self.zrange_keys(rid, fid, kid)
            ulist = []
            xlist = []
            for u in self.rdb.zrangebylex('zhr', start, end):
                if len(u) != 12:
                    continue
                found_rid, found_fid, found_kid = unpack('>III', u)
                if not include_def and self.type(found_rid) == 0:
                    continue
                ulist.append(u)
                xlist.append((found_rid, found_fid, found_kid))

            if hids or hfile:
                pipe = self.rdb.pipeline(transaction=False)
                for u in ulist:
                    pipe.hget('hr', u)

                hrules = pipe.execute()
                hlist = []
                for uid, hr in zip(xlist, hrules):
                    found_hfile, hid, btype, complib = unpack('>IIBI', hr)
                    if hfile in (None, found_hfile):
                        if hids:
                            hlist.append(HID(found_hfile, hid))
                        else:
                            hlist.append(uid)

            else:
                hlist = xlist
            if ascii:
                rids = [ h[0] for h in hlist ]
                fids = [ h[1] for h in hlist ]
                kids = [ h[2] for h in hlist ]
                records = self.ids2names(rids)
                fields = self.ids2names(fids)
                keys = self.ids2names(kids)
                keys = [ ('' if k == 'DefinitionDef' else k) for k in keys ]
                hlist = zip(records, fields, keys)
            return hlist

    def mlist_h_cfg(self, records, field = 0, key = 0, ascii = False, hids = False, all_data = False):
        if not isinstance(records, list):
            return
        rids = self.names2ids(records)
        fid = self.name2id(field)
        kid = self.name2id(key)
        keys = [ self.zrange_keys(rid, fid, kid) for rid in rids ]
        pipe = self.rdb.pipeline(transaction=False)
        for start, end in keys:
            pipe.zrangebylex('zhr', start, end)

        rows = pipe.execute()
        pipe = self.rdb.pipeline(transaction=False)
        for row in rows:
            for u in row:
                pipe.hget('hr', u)

        hrules = pipe.execute()
        i = 0
        hlist = []
        for row in rows:
            for u in row:
                found_rid, found_fid, found_kid = unpack('>III', u)
                hr = hrules[i]
                i += 1
                if all_data:
                    found_hfile, hid, btype, complib = unpack('>IIBI', hr)
                    hlist.append((found_rid,
                     found_fid,
                     found_kid,
                     HID(found_hfile, hid),
                     btype,
                     complib))
                elif hids:
                    found_hfile, hid, btype, cos = unpack('>IIBI', hr)
                    hlist.append(HID(found_hfile, hid))
                else:
                    hlist.append((found_rid, found_fid, found_kid))

        if ascii:
            rids = [ h[0] for h in hlist ]
            fids = [ h[1] for h in hlist ]
            kids = [ h[2] for h in hlist ]
            records = self.ids2names(rids)
            fields = self.ids2names(fids)
            keys = self.ids2names(kids)
            keys = [ ('' if k == 'DefinitionDef' else k) for k in keys ]
            hlist = zip(records, fields, keys)
        return hlist

    def verifyhis(self, times, values):
        sorted_times = numpy.sort(times)
        if len(times) == 0 or len(times) != len(values) or len(times) != len(numpy.unique(times)) or not numpy.array_equal(times, sorted_times) or sorted_times[0] < MIN_TIME or sorted_times[-1] > MAX_TIME:
            return False
        else:
            return True

    def put_history(self, tag, times, values, verify = True):
        try:
            if not self._pps_query(None, P_WRITE):
                return False
            hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg == None:
                return False
            hid, btype, complib = hcfg
            dtype = HISTORY_BTYPES.get(btype)
            if dtype == None:
                return False
            if not isinstance(times, numpy.ndarray) or times.dtype != float64:
                # times = [self.self.str2time(i) for i in times]
                times = numpy.array(times, dtype=float64)
            if not isinstance(values, numpy.ndarray) or values.dtype != dtype:
                try:
                    values = numpy.array(values, dtype=dtype)
                except ValueError:
                    return False

            if verify:
                if not self.verifyhis(times, values):
                    return False
            elif len(times) == 0 or len(times) != len(values):
                return False
            if times[-1] > self._tix / self._mtix:
                return False
            if self.pg_found:
                data = self.rdb.hget('atime', pack('>I', hid.hid))
                if data != None:
                    arc_time, = unpack('d', data)
                    if times[0] <= arc_time:
                        return False
            bsize = self.max_block_size(values.dtype)
            hkey = pkey('hd', hid.hid)
            qkey = pkey('hq', hid.hid)
            append = False
            qlen = self.rdb.llen(qkey)
            if qlen > 1:
                qfirst_block = self.rdb.lindex(qkey, 0)
                if qfirst_block != None:
                    qfirst_time = self.unpack_h_key(qfirst_block)
                    if times[-1] < qfirst_time:
                        append = False
                    else:
                        self.process_queue(tag)
                        append = True
                        middle = False
            elif qlen == 1:
                qlast_block = self.rdb.lindex(qkey, -1)
                if qlast_block != None:
                    qlast_time = self.unpack_h_key(qlast_block)
                    if qlast_time < times[0]:
                        append = True
                        middle = False
                    elif qlast_time < times[-1] or abs(qlast_time - times[-1]) < self.sec2time(0.01) or abs(qlast_time - times[0]) < self.sec2time(0.01):
                        append = True
                        middle = True
                    else:
                        append = False
            else:
                append = False
                self.rdb.rpush(qkey, self.pack_h_block(times[-1:], values[-1:], btype=btype))
            if append:
                rows = self.rdb.zrange(hkey, -1, -1)
                if len(rows) > 0:
                    block_times, block_values = self.unpack_h_block(rows[0])
                    if middle:
                        if block_times[0] - self.sec2time(0.01) < times[0]:
                            search_time = times[0] + self.sec2time(0.01)
                            i = len(block_times) - numpy.argmax(block_times[::-1] < search_time) - 1
                            times = numpy.append(block_times[:i], times)
                            values = numpy.append(block_values[:i], values)
                        else:
                            self.delhis(tag, times[0], times[-1])
                    else:
                        times = numpy.append(block_times, times)
                        values = numpy.append(block_values, values)
                    self.rdb.zrem(hkey, rows[0])
                data = self.pack_h_block(times[-1:], values[-1:], btype=btype)
                if data is not None:
                    try:
                        self.rdb.lset(qkey, -1, data)
                    except redis.ResponseError:
                        self.rdb.rpush(qkey, data)

            elif qlen != 0:
                self.delhis(tag, times[0], times[-1])
            self.put_h_block(hid, times, values, bsize=bsize, btype=btype)
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def get_queue(self, tags, start_time = None, end_time = None, text = False):
        hids = self.tags2hids(tags)
        if hids.count(None) > 0:
            return
        else:
            if isinstance(start_time, str):
                start_time = self.str2time(start_time)
                if start_time == None:
                    return
            if isinstance(end_time, str):
                end_time = self.str2time(end_time)
                if end_time == None:
                    return
            pipe = self.rdb.pipeline(transaction=False)
            for hid in hids:
                key = pkey('hq', hid.hid)
                pipe.lrange(key, 0, -1)

            rows = pipe.execute()
            results = []
            for row in rows:
                btype_list = []
                time_list = []
                value_list = []
                for data in row:
                    btime, btype, time_data, value_data = self.extract_h_block(data)
                    btype_list.append(btype)
                    time_list.append(time_data)
                    value_list.append(value_data)

                i = 0
                n = len(btype_list)
                while True:
                    j = not_index(btype_list[i:], btype_list[i]) + i
                    time_data = ''.join(time_list[i:j])
                    value_data = ''.join(value_list[i:j])
                    utimes, uvalues = self.unpack_h_data(time_data, value_data, btype_list[i])
                    if i == 0:
                        times = utimes
                        values = uvalues
                    else:
                        times = numpy.append(times, utimes)
                        values = numpy.append(values, uvalues)
                    if j == n:
                        break
                    i = j

                if start_time != None and len(times) > 0 and times[0] < start_time:
                    b = times >= start_time
                    times = times[b]
                    values = values[b]
                if end_time != None and len(times) > 0 and times[-1] > end_time:
                    b = times < end_time
                    times = times[b]
                    values = values[b]
                if text:
                    times = self.times2str(times)
                results.append((times, values))

            return results

    def put_queue(self, tags, times, values, notify = True):
        try:
            if not self._pps_query(None, P_WRITE):
                return False
            if self.now() > self._tix / self._mtix:
                return False
            if not len(tags) == len(times) == len(values):
                return False
            n = 0
            ok = []
            pipe = self.rdb.pipeline(transaction=False)
            for tag, time, value in zip(tags, times, values):
                hcfg = self.get_h_cfg(tag, cached=True)
                if hcfg is None:
                    ok.append(False)
                    continue
                hid, btype, complib = hcfg
                dtype = HISTORY_BTYPES.get(btype)
                if dtype is None:
                    ok.append(False)
                    continue
                if type(time) not in (list, tuple) and not hasattr(time, 'dtype'):
                    time = [time]
                    value = [value]
                if time[0] is None:
                    ok.append(False)
                    continue
                key = pkey('hq', hid.hid)
                btime = self.time2ms(time[0])
                times = array(time, dtype=float64)
                values = cast_array(value, dtype)
                if values is None:
                    ok.append(False)
                    continue
                ptimes = times.tostring()
                pvalues = values.tostring()
                compress = 0
                data = pack('>QBBI', btime, btype, compress, len(ptimes)) + ptimes + pvalues
                pipe.rpush(key, data)
                ok.append(True)

            pipe.execute()
            if notify:
                uids = [ self.tag2uid(t) for t in tags ]
                uids = [ u for u in uids if u is not None ]
                uids += [ (u[0], self.TIME_FT, u[2]) for u in uids if u[1] == self.VALUE_FT ]
                self.send_events(uids)
            return ok
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def max_block_size(self, dtype):
        tsize = 1.0
        vsize = numpy.dtype(dtype).itemsize / 2.0
        bsize = int(64800 / (tsize + vsize)) * 4
        return bsize

    def dtype2btype(self, dtype):
        if isinstance(dtype, str):
            try:
                dtype = HISTORY_CUSTOM_DTYPES[dtype]
            except KeyError:
                try:
                    dtype = numpy.dtype(dtype).type
                except TypeError:
                    return

        if dtype == numpy.bool:
            dtype = numpy.bool8
        try:
            btype = HISTORY_DTYPES[dtype]
        except KeyError:
            return

        return btype

    def btype2dtype(self, btype):
        try:
            return HISTORY_BTYPES[btype]
        except KeyError:
            return

    def get_btype_name(self, btype):
        try:
            return HISTORY_DTYPE_NAMES[btype]
        except KeyError:
            if btype == 0:
                return 'noopt'
            else:
                return btype

    def deadband_compress(self, times, values, deadband, max_time):
        max_time = self.sec2time(max_time)
        b = cci.deadband_compress(times, values, deadband, max_time)
        return (times[b], values[b])

    def process_queue(self, tag, keep = 1, store_only_changes = False):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg == None:
                return
            hid, btype, complib = hcfg
            dtype = HISTORY_BTYPES[btype]
            bsize = self.max_block_size(dtype)
            hkey = pkey('hd', hid.hid)
            qkey = pkey('hq', hid.hid)
            btype_list = []
            time_list = []
            value_list = []
            for row in self.rdb.lrange(qkey, 0, -(keep + 1)):
                btime, btype, time_data, value_data = self.extract_h_block(row)
                btype_list.append(btype)
                time_list.append(time_data)
                value_list.append(value_data)

            i = 0
            n = len(btype_list)
            if n == 0:
                return 0
            while True:
                j = not_index(btype_list[i:], btype_list[i]) + i
                time_data = ''.join(time_list[i:j])
                value_data = ''.join(value_list[i:j])
                utimes, uvalues = self.unpack_h_data(time_data, value_data, btype_list[i], dtype)
                if i == 0:
                    times = utimes
                    values = uvalues
                else:
                    times = numpy.append(times, utimes)
                    values = numpy.append(values, uvalues)
                if j == n:
                    break
                i = j

            rows = self.rdb.zrange(hkey, -1, -1)
            if len(rows) > 0:
                block_times, block_values = self.unpack_h_block(rows[0])
                times = numpy.append(block_times, times)
                values = numpy.append(block_values, values)
                self.rdb.zrem(hkey, rows[0])
            self.rdb.ltrim(qkey, n, -1)
            if store_only_changes:
                selection = numpy.ones(len(values), dtype=bool)
                selection[1:] = values[1:] != values[:-1]
                times = times[selection]
                values = values[selection]
            self.put_h_block(hid, times, values, bsize=bsize, btype=btype)
            return n

    def add_months(self, ts, num_months):
        dt = self.time2dt(ts)
        for i in range(num_months):
            days = calendar.monthrange(dt.year, dt.month)[1]
            dt += timedelta(days=days)

        return self.dt2time(dt)

    def mktimes(self, start_time, freq, num, format = None, text = False, ascii = False):
        if text:
            ascii = True
        if format is None:
            format = self.time_format
        if isinstance(start_time, str):
            start_time = self.ascii2time(start_time)
        if isinstance(freq, str):
            freq = self.delta2sec(freq)
        if start_time == None or freq == None:
            return
        else:
            if freq < 0:
                dt = self.time2dt(start_time)
                month_step = abs(int(freq))
                times = []
                times.append(self.dt2time(dt))
                for i in range(num - 1):
                    for j in range(month_step):
                        days = calendar.monthrange(dt.year, dt.month)[1]
                        dt += timedelta(days=days)

                    times.append(self.dt2time(dt))

                times = numpy.array(times)
            else:
                freq /= 86400.0
                start_time = round_time(start_time)
                end_time = round_time(start_time + (num - 1) * freq)
                times = linspace(start_time, end_time, num)
            if ascii:
                times = self.times2ascii(times, format)
            return times

    def trange(self, start_time, end_time, freq, format = None, text = False, ascii = False):
        if text:
            ascii = True
        if format is None:
            format = self.time_format
        if isinstance(start_time, str):
            start_time = self.ascii2time(start_time)
        if isinstance(end_time, str):
            end_time = self.ascii2time(end_time)
        if isinstance(freq, str):
            freq = self.delta2sec(freq)
        if start_time == None or end_time == None or freq == None:
            return
        elif start_time > end_time:
            return numpy.array([], dtype=float64)
        else:
            if freq < 0:
                dt = self.time2dt(start_time)
                end_dt = self.time2dt(end_time)
                month_step = abs(int(freq))
                times = []
                times.append(self.dt2time(dt))
                while dt < end_dt:
                    for j in range(month_step):
                        days = calendar.monthrange(dt.year, dt.month)[1]
                        dt += datetime.timedelta(days=days)
                    times.append(self.dt2time(dt))

                times = [ t for t in times if t < end_time ]
                times = numpy.array(times)
            else:
                freq /= 86400.0
                start_time = round_time(start_time)
                end_time = round_time(end_time - freq)
                num = int(round((end_time - start_time) / freq)) + 1
                end_time = round_time(start_time + (num - 1) * freq)
                times = linspace(start_time, end_time, num)
            if ascii:
                times = self.times2ascii(times, format)
            return times

    def unpack_h_key(self, data):
        btime, = unpack('>Q', data[:8])
        btime = self.ms2time(btime)
        return btime

    def pack_h_key(self, btime):
        btime = self.time2ms(btime)
        return pack('>Q', btime)

    def put_h_block(self, hid, times, values, bsize = 4000, btype = HISTORY_DTYPES[numpy.float32]):
        if len(values) > bsize:
            split_idxs = numpy.arange(bsize, len(values), step=bsize)
            time_groups = numpy.split(times, split_idxs)
            value_groups = numpy.split(values, split_idxs)
        else:
            time_groups = [times]
            value_groups = [values]
        for i, values in enumerate(value_groups):
            times = time_groups[i]
            if len(times) == 0:
                continue
            data = self.pack_h_block(times, values, btype=btype)
            if data is not None:

                x = self.rdb.zadd(pkey('hd', hid.hid), data, 0)
        return

    def split_h_block(self, hid, block_id, left_time = None, right_time = None, btype = HISTORY_DTYPES[numpy.float32]):
        times, values = self.unpack_h_block(block_id)
        if left_time:
            i = bisect.bisect_left(times, left_time)
        if right_time:
            j = bisect.bisect_right(times, right_time)
        if left_time and right_time and i == j == len(times):
            return 0
        self.rdb.zrem(pkey('hd', hid.hid), block_id)
        bsize = self.max_block_size(values.dtype)
        if left_time and len(times[:i]) > 0:
            self.put_h_block(hid, times[:i], values[:i], btype=btype, bsize=bsize)
        if right_time and len(times[j:]) > 0:
            self.put_h_block(hid, times[j:], values[j:], btype=btype, bsize=bsize)
        return 1

    # decode 변환 작업
    def extract_h_block(self, data):
        btime, btype, compress, n = unpack('>QBBI', data[:14])
        data = data[14:]
        if compress:
            times = blosc.decompress(data[:n])
            values = blosc.decompress(data[n:])
            self.ratio.append(float(len(data)) / len(values))
        else:
            # try:
            times = data[:n]
                # times = data[:n].decode('unicode-escape')
            values = data[n:]
                # values = data[n:].decode('unicode-escape')
            # except UnicodeDecodeError as e:
            #
            #     times = data[:n].decode('utf-8', 'backslashreplace')
            #     values = data[n:].decode('utf-8', 'backslashreplace')

        return (btime,
         btype,
         times,
         values)

    # encode 변환 작업
    def unpack_h_data(self, time_data, value_data, btype, cast_dtype = None):
        dtype = HISTORY_BTYPES.get(btype)
        if dtype == None:
            return self.empty_h_tuple()
        else:
            d_l = len(time_data)
            n = len(time_data) / 8
            if n > 0:
                # time_data, value_data는 현재 str 인데 frombuffer에는 bytes로 변환하여 들어가야 함
                # bytes --> ValueError: buffer size must be a multiple of element size 에러 발생
                # ISO-8859-1 방식으로 인코드 하여 작업
                if type(time_data) != bytes:
                    time_data = time_data.encode('ISO-8859-1')
                    value_data = value_data.encode('ISO-8859-1')
                times = numpy.frombuffer(time_data, dtype=float64)
                values = numpy.frombuffer(value_data, dtype=dtype)
            else:
                times, values = self.empty_h_tuple()
            if cast_dtype != None and cast_dtype != HISTORY_BTYPES[btype]:
                try:
                    values = numpy.array(values, dtype=cast_dtype)
                except ValueError:
                    self.hcfg_cache = {}
                    times, values = self.empty_h_tuple()

            if len(times) == len(values):
                return (times, values)
            return self.empty_h_tuple()
            return

    def unpack_h_block(self, data):
        btime, btype, time_data, value_data = self.extract_h_block(data)
        return self.unpack_h_data(time_data, value_data, btype)

    def unpack_h_block_tdf(self, data):
        btype, time_data, value_data = self.extract_h_block_tdf(data)
        return self.unpack_h_data_tdf(time_data, value_data, btype)

    def extract_h_block_tdf(self, data):
        btype, = unpack('>B', data[0])
        data = data[1:]
        if btype == 0:
            btype, = unpack('>B', data[:1])
            data = data[1:]
            times = data[:8]
            values = data[8:]
            return (btype, times, values)
        elif btype == 1:
            n = len(data) / 3 * 2
            times = data[:n]
            values = data[n:]
            return (btype, times, values)
        elif btype > 11:
            n, = unpack('>I', data[:4])
            data = data[4:]
            times = blosc.decompress(data[:n])
            values = blosc.decompress(data[n:])
            return (btype, times, values)
        elif btype == 10:
            data = blosc.decompress(data)
            times = data[:24]
            values = data[24:]
            return (btype, times, values)
        elif btype == 11:
            data = blosc.decompress(data)
            n = len(data) / 3 * 2
            times = data[:n]
            values = data[n:]
            return (btype, times, values)
        elif btype == 9:
            data = zlib.decompress(data)
            times = data[:24]
            values = data[24:]
            return (btype, times, values)
        elif btype == 2:
            data = zlib.decompress(data)
            n = len(data) / 3 * 2
            times = data[:n]
            values = data[n:]
            return (btype, times, values)
        else:
            return (btype, '', '')

    def unpack_h_data_tdf(self, time_data, value_data, btype, cast_dtype = None):
        if btype == 0:
            dtype = HISTORY_BTYPES[btype]
            n = len(time_data) / 8
            if n > 0:
                times = numpy.frombuffer(time_data, dtype=float64)
                values = numpy.frombuffer(value_data, dtype=dtype)
            else:
                times, values = self.empty_h_tuple()
        elif btype == 1:
            n = len(time_data) / 8
            if n > 0:
                times = numpy.frombuffer(time_data, dtype=float64)
                values = numpy.frombuffer(value_data, dtype=float32)
            else:
                times, values = self.empty_h_tuple()
        elif btype > 11:
            dtype = HISTORY_BTYPES[btype]
            n = len(time_data) / 8
            if n > 0:
                times = numpy.frombuffer(time_data, dtype=float64)
                values = numpy.frombuffer(value_data, dtype=dtype)
            else:
                times, values = self.empty_h_tuple()
        elif btype == 10:
            num_blocks = len(time_data) / 24
            n = num_blocks * 3
            time_headers = unpack('>%dd' % n, time_data)
            num_values = len(value_data) / 4
            if num_values > 0:
                times = numpy.empty(num_values)
                k = 0
                for i in range(num_blocks):
                    j = i * 3
                    start_time = time_headers[j]
                    freq = time_headers[j + 1]
                    n = int(time_headers[j + 2])
                    block_times = self.mktimes(start_time, freq, n)
                    m = k + len(block_times)
                    times[k:m] = block_times
                    k = m

                values = numpy.frombuffer(value_data, dtype=float32)
            else:
                times, values = self.empty_gehis_tuple()
        elif btype == 11:
            n = len(time_data) / 8
            if n > 0:
                times = numpy.frombuffer(time_data, dtype=float64)
                values = numpy.frombuffer(value_data, dtype=float32)
            else:
                times, values = self.empty_h_tuple()
        elif btype == 2:
            n = len(time_data) / 8
            if n > 0:
                times = numpy.frombuffer(time_data, '>d')
                values = numpy.frombuffer(value_data, '>f')
                times = times.byteswap().newbyteorder()
                values = values.byteswap().newbyteorder()
            else:
                times, values = self.empty_h_tuple()
        elif btype == 9:
            num_blocks = len(time_data) / 24
            n = num_blocks * 3
            time_headers = unpack('>%dd' % n, time_data)
            num_values = len(value_data) / 4
            if num_values > 0:
                times = numpy.empty(num_values)
                k = 0
                for i in range(num_blocks):
                    j = i * 3
                    start_time = time_headers[j]
                    freq = time_headers[j + 1]
                    n = int(time_headers[j + 2])
                    block_times = self.mktimes(start_time, freq, n)
                    m = k + len(block_times)
                    times[k:m] = block_times
                    k = m

                values = numpy.frombuffer(value_data, '>f')
                values = values.byteswap().newbyteorder()
            else:
                times, values = self.empty_gehis_tuple()
        else:
            times, values = self.empty_h_tuple()
        if cast_dtype != None and cast_dtype != HISTORY_BTYPES[btype]:
            values = numpy.array(values, dtype=cast_dtype)
        return (times, values)

    def pack_h_block(self, times, values, btype = HISTORY_DTYPES[numpy.float32]):
        block_dtype = HISTORY_BTYPES[btype]
        if values.dtype != block_dtype:
            try:
                values = array(values, dtype=block_dtype)
            except ValueError:
                return

        btime = self.time2ms(times[0])
        if len(times) > 15:
            ptimes = blosc.compress(times.tostring(), times.dtype.itemsize)
            pvalues = blosc.compress(values.tostring(), values.dtype.itemsize)
            compress = 1
        else:
            ptimes = times.tostring()
            pvalues = values.tostring()
            compress = 0

        return pack('>QBBI', btime, btype, compress, len(ptimes)) + ptimes + pvalues

    def pack_h_block_tdf(self, times, values, btype = HISTORY_DTYPES[numpy.float32]):
        n = len(times)
        if btype == 1:
            ptimes = times.tostring()
            pvalues = values.tostring()
            zdata = blosc.compress(ptimes + pvalues, 4)
            return pack('>B', btype) + zdata
        elif btype > 11:
            ztimes = blosc.compress(times.tostring(), times.dtype.itemsize)
            zvalues = blosc.compress(values.tostring(), values.dtype.itemsize)
            return pack('>BI', btype, len(ztimes)) + ztimes + zvalues
        else:
            if btype == 10:
                if n == 1:
                    freq = 0.0
                else:
                    freq = self.get_h_freq(times)
                if freq != None:
                    ptime = pack('>ddd', round_time(times[0]), freq, float(n))
                    pvalues = values.tostring()
                    zdata = blosc.compress(ptime + pvalues, 4)
                    return pack('>B', btype) + zdata
                else:
                    return self.pack_h_block_tdf(times, values, btype=11)
            else:
                if btype == 11:
                    ptimes = times.tostring()
                    pvalues = values.tostring()
                    zdata = blosc.compress(ptimes + pvalues, 4)
                    return pack('>B', btype) + zdata
                if btype == 9:
                    if n == 1:
                        freq = 0.0
                    else:
                        freq = self.get_h_freq(times)
                    freq = self.get_h_freq(times)
                    if freq != None:
                        ptime = pack('>ddd', round_time(times[0]), freq, float(n))
                        pvalues = pack(('>%df' % n), *values)
                        zdata = zlib.compress(ptime + pvalues)
                        return pack('>B', btype) + zdata
                    else:
                        return self.pack_h_block_tdf(times, values, btype=2)
                else:
                    if btype == 2:
                        ptimes = pack(('>%dd' % n), *times)
                        pvalues = pack(('>%df' % n), *values)
                        zdata = zlib.compress(ptimes + pvalues)
                        return pack('>B', btype) + zdata
                    if btype == 7:
                        return ''
                    return ''
            return

    def get_h_freq(self, times):
        n = len(times)
        if n > 2:
            start = self.time2ms(times[0])
            end = self.time2ms(times[-1])
            freq1 = self.time2ms(times[1]) - start
            freq2 = end - self.time2ms(times[-2])
            if freq1 == freq2 and start + freq1 * (n - 1) == end:
                return freq1 / 1000.0
            else:
                return None
        else:
            return None
        return None

    def start_h_block(self, data):
        btype, tdata, vdata = self.extract_h_block(data)
        if btype >= 10 or btype == 0 or btype == 1:
            start, = unpack('d', tdata[:8])
        else:
            start, = unpack('>d', tdata[:8])
        return start

    def end_h_block(self, data):
        btime, btype, time_data, value_data = self.extract_h_block(data)
        i = len(time_data)
        end_time, = unpack('d', time_data[i - 8:i])
        return end_time

    def len_h_block(self, data):
        btype, = unpack('>B', data[8])
        compress, = unpack('>B', data[9])
        data = data[10:]
        n, = unpack('>I', data[:4])
        data = data[4:]
        if compress:
            data = blosc.decompress(data[n:])
        else:
            data = data[n:]
        dtype = HISTORY_BTYPES[btype]
        dt_size = numpy.dtype(dtype).itemsize
        n = len(data) / dt_size
        return n

    def type_h_block(self, data):
        btype, = unpack('>B', data[0])
        return btype

    def tag2hid(self, tag):
        if isinstance(tag, HID):
            return tag
        else:
            if isinstance(tag, str):
                if tag.count(' ') > 0 and self.name2id(tag) == None:
                    tag = tuple(tag.split(' '))
                    if len(tag) == 3:
                        tag = (tag[0], tag[2], tag[1])
                else:
                    tag = (tag, self.VALUE_FT)
            elif isinstance(tag, int):
                tag = (tag, self.VALUE_FT)
            if isinstance(tag, tuple):
                if tag in self.hid_cache:
                    return self.hid_cache[tag]
                else:
                    hcfg = self.get_h_cfg(tag)
                    if hcfg == None:
                        return
                    hid, btype, cos = hcfg
                    self.hid_cache[tag] = hid
                    if not hid.hid in self.hid_reverse_cache:
                        self.hid_reverse_cache[hid.hid] = {}
                    self.hid_reverse_cache[hid.hid][tag] = None
                    return hid
            else:
                return
            return

    def tags2hids(self, tags):
        if not isinstance(tags, list) or len(tags) == 0:
            return
        elif isinstance(tags[0], HID):
            return tags
        else:
            if isinstance(tags[0], str) or isinstance(tags[0], int):
                tags = [ (t, self.VALUE_FT) for t in tags ]
            if isinstance(tags[0], tuple):
                hids = [ (self.hid_cache[t] if t in self.hid_cache else None) for t in tags ]
                if hids.count(None) == 0:
                    return hids
                simple_tags = [ t[0] for t in tags ]
                field = tags[0][1]
                rules = self.mget_h_cfg(simple_tags, field)
                hids = [ (r[0] if r else None) for r in rules ]
                for tag, hid in zip(tags, hids):
                    if hid != None:
                        self.hid_cache[tag] = hid
                        if not hid.hid in self.hid_reverse_cache:
                            self.hid_reverse_cache[hid.hid] = {}
                        self.hid_reverse_cache[hid.hid][tag] = None

                return hids
            return
            return

    def hid2tag(self, hid, text = False):
        if isinstance(hid, int):
            hid = HID(0, hid)
        rid = None
        fid = None
        kid = None
        for row in self.rdb.hgetall('hr').items():
            if len(row[1]) == 10:
                hfile, found_hid, btype, cos = unpack('>IIBB', row[1])
            else:
                hfile, found_hid, btype, cos = unpack('>IIBI', row[1])
            if found_hid == hid.hid:
                rid, fid, kid = unpack('>III', row[0])
                break

        if text:
            rid = self.id2name(rid)
            fid = self.id2name(fid)
            if kid == 0:
                kid = ''
            else:
                kid = self.id2name(kid)
        return (rid, fid, kid)

    def get_q_len(self, hid):
        hid = self.tag2hid(hid)
        if hid == None:
            return
        else:
            return self.rdb.llen(pkey('hq', hid.hid))

    def list_q_blocks(self, hid, text = False, ascii = False):
        if text:
            ascii = True
        hid = self.tag2hid(hid)
        if hid == None:
            return
        else:
            block_list = []
            for row in self.rdb.lrange(pkey('hq', hid.hid), 0, -1):
                block_time = self.unpack_h_key(row)
                btype, = unpack('>B', row[8])
                size = self.len_h_block(row)
                if ascii:
                    block_list.append((self.time2ascii(block_time), self.get_btype_name(btype), size))
                else:
                    block_list.append((block_time, btype, size))

            return block_list

    def list_h_blocks(self, hid, start_time = 0, end_time = MAX_TIME, hfile = None, text = False, ascii = False, bytes = False):
        if text:
            ascii = True
        hid = self.tag2hid(hid)
        if hid == None:
            return
        else:
            if hfile != None:
                hfile = self.name2id(hfile)
                if hfile == None:
                    return
                hid = HID(hfile, hid.hid)
            start_time = self.ascii2time(start_time)
            end_time = self.ascii2time(end_time)
            if start_time == None or end_time == None:
                return
            start = '[' + self.pack_h_key(start_time)
            end = '[' + self.pack_h_key(end_time)
            block_list = []
            for row in self.rdb.zrangebylex(pkey('hd', hid.hid), start, end):
                block_time = self.unpack_h_key(row)
                btype, = unpack('>B', row[8])
                if bytes:
                    size = len(row)
                else:
                    size = self.len_h_block(row)
                if ascii:
                    block_list.append((self.time2ascii(block_time), self.get_btype_name(btype), size))
                else:
                    block_list.append((block_time, btype, size))

            return block_list

    def list_a_blocks(self, hid, start_time = None, end_time = None, text = False, ascii = False, bytes = False):
        if not self.pg_found:
            return
        else:
            if text:
                ascii = True
            hid = self.tag2hid(hid)
            if hid == None:
                return
            if start_time != None:
                start_time = self.ascii2time(start_time)
                if start_time == None:
                    return
            if end_time != None:
                end_time = self.ascii2time(end_time)
                if end_time == None:
                    return
            if start_time == None and end_time == None:
                sql = 'SELECT data FROM arc_%d WHERE hid=%d ORDER BY ts' % (hid.hfile, hid.hid)
            elif end_time == None:
                pg_start_time = self.time2dt(start_time).pydatetime()
                sql = "SELECT data FROM arc_%d WHERE hid=%d AND ts>='%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_start_time)
            elif start_time == None:
                pg_end_time = self.time2dt(end_time).pydatetime()
                sql = "SELECT data FROM arc_%d WHERE hid=%d AND ts<'%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_end_time)
            else:
                pg_start_time = self.time2dt(start_time).pydatetime()
                pg_end_time = self.time2dt(end_time).pydatetime()
                sql = "SELECT data FROM arc_%d WHERE hid=%d AND ts>='%s' AND ts<'%s' ORDER BY ts" % (hid.hfile,
                 hid.hid,
                 pg_start_time,
                 pg_end_time)
            block_list = []
            for row, in self.pg_get(sql):
                block_time = self.unpack_h_key(row)
                btype, = unpack('>B', row[8])
                if bytes:
                    size = len(row)
                else:
                    size = self.len_h_block(row)
                if ascii:
                    block_list.append((self.time2ascii(block_time), self.get_btype_name(btype), size))
                else:
                    block_list.append((block_time, btype, size))

            return block_list

    def delete_history(self, tag, start_time = None, end_time = None):
        try:
            if not self._pps_query(None, P_WRITE):
                return False
            hcfg = self.get_h_cfg(tag)
            if hcfg == None:
                return
            hid, btype, complib = hcfg
            n = 0
            if start_time == None and end_time == None:
                n += self.rdb.zcard(pkey('hd', hid.hid))
                n += self.rdb.llen(pkey('hq', hid.hid))
                self.rdb.delete(pkey('hd', hid.hid), pkey('hq', hid.hid))
                self.rdb.hdel('rsample', pack('>I', hid.hid))
                self.rdb.hdel('atime', pack('>I', hid.hid))
                if self.pg_found:
                    try:
                        status = self.pg_put('DELETE FROM arc_%d WHERE hid=%d' % (hid.hfile, hid.hid))
                    except psycopg2.ProgrammingError:
                        pass
                    else:
                        host, count = status[0]
                        if count is not None:
                            n += count
                return n
            start_time = self.ascii2time(start_time)
            end_time = self.ascii2time(end_time)
            if start_time == None or end_time == None or start_time > end_time:
                return
            self.process_queue(tag)
            key = pkey('hd', hid.hid)
            min = b'(' + pack('>Q', self.time2ms(start_time) - 1)
            max = b'(' + pack('>Q', self.time2ms(end_time) + 1)
            rows = self.rdb.zrevrangebylex(key, min, '-', 0, 1)
            if len(rows) > 0:
                head_block = rows[0]
                head_time, = unpack('>Q', head_block[:8])
                head_time += 1
                found_head_block = True
            else:
                head_time = self.time2ms(start_time)
                found_head_block = False
            rows = self.rdb.zrevrangebylex(key, max, '-', 0, 1)
            if len(rows) > 0:
                tail_block = rows[0]
                tail_time, = unpack('>Q', tail_block[:8])
                tail_time -= 1
                found_tail_block = True
            else:
                tail_time = self.time2ms(end_time)
                found_tail_block = False
            if not found_head_block and not found_tail_block:
                return n
            if found_head_block and found_tail_block and head_block[:8] == tail_block[:8]:
                n += self.split_h_block(hid, head_block, left_time=start_time, right_time=end_time, btype=btype)
            else:
                min = b'(' + pack('>Q', head_time)
                max = b'(' + pack('>Q', tail_time)
                n += self.rdb.zremrangebylex(key, min, max)
                if found_head_block:
                    n += self.split_h_block(hid, head_block, left_time=start_time, btype=btype)
                if found_tail_block:
                    n += self.split_h_block(hid, tail_block, right_time=end_time, btype=btype)
            return n
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def resample_h_blocks(self, tag, start_time, freq, agg_fn = None):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg == None:
                return
            hid, btype, complib = hcfg
            dtype = HISTORY_BTYPES[btype]
            bsize = self.max_block_size(dtype)
            start_time = self.ascii2time(start_time)
            if start_time == None:
                return
            key = pkey('hd', hid.hid)
            max = '(' + pack('>Q', self.time2ms(start_time) + 1)
            rows = self.rdb.zrevrangebylex(key, max, '-', 1, 2)
            if len(rows) == 0:
                return 0
            tail_block = rows[0]
            tail_time, = unpack('>Q', tail_block[:8])
            data = self.rdb.hget('rsample', pack('>I', hid.hid))
            if data != None:
                end_time_ms, = unpack('>Q', data)
                incomplete_min = '(' + pack('>Q', end_time_ms - 1)
                rows = self.rdb.zrangebylex(key, incomplete_min, '+', 0, 1)
                found_incomplete_block = True
            else:
                rows = self.rdb.zrange(key, 0, 0)
                found_incomplete_block = False
            if len(rows) == 0:
                return 0
            head_block = rows[0]
            head_time, = unpack('>Q', head_block[:8])
            if head_time > tail_time:
                return 0
            start_time = self.ms2time(head_time)
            btime, btype, time_data, value_data = self.extract_h_block(tail_block)
            i = len(time_data)
            end_time, = unpack('d', time_data[i - 8:i])
            min = '(' + pack('>Q', self.time2ms(end_time) - 1)
            rows = self.rdb.zrangebylex(key, min, '+', 0, 1)
            if len(rows) > 0:
                next_block_time, = unpack('>Q', rows[0][:8])
            else:
                next_block_time = None
            times, values = self.gethis(tag, start_time, end_time, freq, agg_fn)
            if found_incomplete_block:
                rows = self.rdb.zrevrangebylex(key, incomplete_min, '-', 0, 1)
                if len(rows) > 0:
                    incomplete_block = rows[0]
                    block_times, block_values = self.unpack_h_block(incomplete_block)
                    times = numpy.append(block_times, times)
                    values = numpy.append(block_values, values)
                else:
                    found_incomplete_block = False
            if len(values) > bsize:
                split_idxs = numpy.arange(bsize, len(values), step=bsize)
                time_groups = numpy.split(times, split_idxs)
                value_groups = numpy.split(values, split_idxs)
            else:
                time_groups = [times]
                value_groups = [values]
            pipe = self.rdb.pipeline(transaction=True)
            if found_incomplete_block:
                pipe.zrem(key, incomplete_block)
            min = '(' + pack('>Q', head_time - 1)
            max = '(' + pack('>Q', tail_time + 1)
            pipe.zremrangebylex(key, min, max)
            for i, values in enumerate(value_groups):
                times = time_groups[i]
                if len(times) == 0:
                    continue
                data = self.pack_h_block(times, values, btype=btype)
                if data is not None:
                    pipe.zadd(key, data, 0)

            if next_block_time != None:
                pipe.hset('rsample', pack('>I', hid.hid), pack('>Q', next_block_time))
            pipe.execute()
            return len(value_groups)

    def trim_h_blocks(self, tag, start_time):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg == None:
                return
            hid, btype, complib = hcfg
            n = 0
            start_time = self.ascii2time(start_time)
            if start_time == None:
                return
            key = pkey('hd', hid.hid)
            max = '(' + pack('>Q', self.time2ms(start_time) + 1)
            rows = self.rdb.zrevrangebylex(key, max, '-', 0, 1)
            if len(rows) == 0:
                return 0
            tail_block = rows[0]
            tail_time, = unpack('>Q', tail_block[:8])
            tail_time -= 1
            max = '(' + pack('>Q', tail_time)
            n = self.rdb.zremrangebylex(key, '-', max)
            return n

    def pg_backlog_replay(self, hfile, host, max_count = None):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            n = 0
            dst_host = host
            src_host = None
            for h in self.pg_real_hosts:
                if h != dst_host:
                    src_host = h
                    break

            if src_host == None:
                return
            while True:
                row = self.pg_backlog_head(hfile, host)
                if row is None:
                    return 0
                hid, time_data = row
                block_time, = unpack('>Q', time_data)
                block_time = self.time2dt(self.ms2time(block_time)).pydatetime()
                rows = self.pg_get("SELECT data FROM arc_%d WHERE hid=%d and ts='%s'" % (hfile, hid, block_time), host=src_host, ret_errors=True)
                if rows is None:
                    return
                if len(rows) > 0:
                    data = rows[0][0]
                    try:
                        status = self.pg_put("INSERT INTO arc_%d (ts,hid,data) VALUES ('%s',%d,%s)" % (hfile,
                         block_time,
                         hid,
                         psycopg2.Binary(data)), host=dst_host)
                    except psycopg2.IntegrityError:
                        pass
                    else:
                        host, count = status[0]
                        if count is None:
                            self.pg_failed_slaves.add(host)
                            return

                    n += 1
                self.pg_backlog_pop(hfile, host)
                if max_count and n >= max_count:
                    break

            return n

    def archive_h_blocks(self, tag, start_time):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            hcfg = self.get_h_cfg(tag, cached=True)
            if hcfg == None:
                return
            hid, btype, complib = hcfg
            start_time = self.ascii2time(start_time)
            if start_time == None:
                return
            status = [ (h, 0) for h in self.pg_hosts ]
            key = pkey('hd', hid.hid)
            max = '(' + pack('>Q', self.time2ms(start_time) + 1)
            rows = self.rdb.zrevrangebylex(key, max, '-', 0, 1)
            if len(rows) == 0:
                return status
            tail_block = rows[0]
            tail_time, = unpack('>Q', tail_block[:8])
            tail_time -= 1
            max = '(' + pack('>Q', tail_time)
            rows = self.rdb.zrangebylex(key, '-', max)
            if len(rows) == 0:
                return status
            for data in rows:
                time_data = data[:8]
                block_time, = unpack('>Q', time_data)
                block_dt = self.time2dt(self.ms2time(block_time))
                try:
                    status = self.pg_put("INSERT INTO arc_%d (ts,hid,data) VALUES ('%s',%d,%s)" % (hid.hfile,
                     block_dt.pydatetime(),
                     hid.hid,
                     psycopg2.Binary(data)))
                except psycopg2.IntegrityError:
                    pass
                else:
                    host, count = status[0]
                    if count is None:
                        return status
                    failed_slaves = [ host for host, count in status[1:] if count is None ]
                    for host in failed_slaves:
                        self.pg_failed_slaves.add(host)
                        self.pg_backlog_push(hid.hfile, host, hid.hid, time_data)

            end_time = self.end_h_block(data)
            self.rdb.hset('atime', pack('>I', hid.hid), pack('d', end_time))
            self.rdb.zremrangebylex(key, '-', max)
            return status

    def times2dt64(self, times, utc = False):
        if self.utc_mode and not utc:
            offset = self.utc_offset
        elif not self.utc_mode and utc:
            offset = -self.utc_offset
        else:
            offset = 0
        times64 = cci.times2dt64(times, offset)
        times64.dtype = 'datetime64[us]'

        return times64

    def downsample(self, times, values, n):
        freq = self.time2sec((times[-1] - times[0]) / n)
        new_times = self.trange(times[0], times[-1], freq)
        min_values = self.timealign(times, values, new_times, agg_fn=7, fill=True)
        max_values = self.timealign(times, values, new_times, agg_fn=8, fill=True)
        new_values = np.ravel(np.column_stack((min_values, max_values)))
        new_times = np.ravel(np.column_stack((new_times, new_times)))
        return (new_times, new_values)

    def get_series(self, tag, start_time = None, end_time = None, freq = None, agg_fn = None, agg_times = None, fill = None, null = None, agg_fill = False, maxlen = -MAX_VALUES, ascii = False, utc = False):
        data = self.gethis(tag, start_time, end_time, freq=freq, agg_fn=agg_fn, agg_times=agg_times, fill=fill, null=null, agg_fill=agg_fill, maxlen=maxlen, ascii_values=ascii, utc=utc)
        if data == None:
            return
        else:
            times, values = data
            if len(times) != 0:
                times = self.times2dt64(times, utc=utc)
            if values.dtype.fields is not None:
                return pandas.DataFrame(values, index=times)
            return pandas.Series(values, index=times)
            return

    def get_dataframe(self, tags, start_time, end_time, freq, agg_fn = None, agg_times = None, fill = None, null = None, agg_fill = False, maxlen = -MAX_VALUES, ascii = False, utc = False):
        values_list = []
        for tag in tags:
            data = self.gethis(tag, start_time, end_time, freq=freq, agg_fn=agg_fn, agg_times=agg_times, fill=fill, null=null, agg_fill=agg_fill, maxlen=maxlen, ascii_values=ascii, utc=utc)
            if data == None:
                return
            times, values = data
            values_list.append(values)

        print(values)
        if len(times) != 0:
            # times = self.times2dt64(times, utc=utc)
            times = self.times2str(times)
        print(times)
        values_array = numpy.array(values_list)
        return pandas.DataFrame(values_array.transpose(), index=times, columns=tags)

    def get_history(self, tag, start_time = None, end_time = None, freq = None, agg_fn = None, agg_times = None, fill = None, null = None, agg_fill = False, max_len = -MAX_VALUES, maxlen = None, text = False, ascii = False, text_values = False, ascii_values = False, force_array = False, utc = False, time_sync = False, item_path = None):

        if text:
            ascii = True
        if text_values:
            ascii_values = True
        self.last_fill = False
        self.h_more = False
        if start_time == 0:
            start_time = None
        if end_time == MAX_TIME:
            end_time = None
        if isinstance(start_time, str):
            start_time = self.ascii2time(start_time, utc=utc)
            if start_time == None:
                return
        if isinstance(end_time, str):
            end_time = self.ascii2time(end_time, utc=utc)
            if end_time == None:
                return
        if freq != None:
            freq = self.delta2sec(freq)
            if freq == None:
                return
        if maxlen not in (None, 0):
            max_len = maxlen
        hcfg = self.get_h_cfg(tag, cached=True)
        if hcfg == None:
            if self.is_calc(tag):
                return self.gethis_calc(tag, start_time, end_time, freq, agg_fn=agg_fn, agg_times=agg_times, max_len=max_len, ascii=ascii, time_sync=time_sync, item_path=item_path)
            elif force_array:
                return self.empty_h_tuple()
            else:
                return
        hid, btype, c = hcfg
        dtype = HISTORY_BTYPES.get(btype)
        if dtype == None:
            return self.empty_h_tuple()
        else:
            dt_size = numpy.dtype(dtype).itemsize
            if fill == None:
                fill = False
            self.last_fill = fill
            if null == None:
                if dtype in (float16, float32, float64):
                    null = nan
                else:
                    null = 0
            self.last_null = null
            if freq:
                return self.gethis_agg(tag, start_time, end_time, freq=freq, agg_fn=agg_fn, fill=fill, null=null, max_len=max_len, ascii=ascii)
            if agg_times is not None:
                return self.gethis_agg(tag, agg_times=agg_times, agg_fn=agg_fn, fill=fill, null=null, max_len=max_len, ascii=ascii)
            if start_time not in (None, 0):
                start_time -= MSEC
            if end_time not in (None, MAX_TIME):
                end_time -= MSEC
            if max_len < 0:
                reverse = True
            else:
                reverse = False
            get_archive = True
            agg_fill_stop = False
            time_list = []
            value_list = []
            btype_list = []
            n = 0
            key = pkey('hd', hid.hid)
            qkey = pkey('hq', hid.hid)
            if start_time == None:
                min = '-'
            else:
                min = '('.encode() + pack('>Q', self.time2ms(start_time) - 1)
                rows = self.rdb.zrevrangebylex(key, min, '-', 0, 1)
                if len(rows) > 0:
                    min = '['.encode() + rows[0]
                    if self.pg_found:
                        block_start = self.unpack_h_key(rows[0])
                        if start_time >= block_start:
                            get_archive = False
            if end_time == None:
                max = '+'
                get_queue = True
            else:
                max = '('.encode() + pack('>Q', self.time2ms(end_time) + 1)
                row = self.rdb.lindex(qkey, 0)
                if row != None:
                    queue_start = self.unpack_h_key(row)
                    if end_time < queue_start:
                        get_queue = False
                    else:
                        get_queue = True
                else:
                    get_queue = False
            if get_queue:
                queue_rows = self.rdb.lrange(qkey, 0, -1)
            else:
                queue_rows = []
            if self.pg_found and get_archive:
                if start_time != None:
                    pg_start_time = self.time2dt(start_time, utc=self.utc_mode).pydatetime()
                    rows = self.pg_get("SELECT ts FROM arc_%d WHERE hid=%d AND ts<'%s' ORDER BY ts DESC LIMIT 1" % (hid.hfile, hid.hid, pg_start_time))
                    if len(rows) > 0:
                        pg_start_time = rows[0][0]
                if end_time != None:
                    pg_end_time = self.time2dt(end_time, utc=self.utc_mode).pydatetime()
                if start_time == None and end_time == None:
                    rows = self.pg_get('SELECT data FROM arc_%d WHERE hid=%d ORDER BY ts' % (hid.hfile, hid.hid))
                elif start_time == None:
                    rows = self.pg_get("SELECT data FROM arc_%d WHERE hid=%d AND ts<'%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_end_time))
                elif end_time == None:
                    rows = self.pg_get("SELECT data FROM arc_%d WHERE hid=%d AND ts>='%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_start_time))
                else:
                    rows = self.pg_get("SELECT data dROM arc_%d WHERE hid=%d AND ts>='%s' AND ts<'%s'" % (hid.hfile,hid.hid,pg_start_time,pg_end_time))
                archive_rows = [ r[0] for r in rows ]
            else:
                archive_rows = []
            for row in archive_rows + self.rdb.zrangebylex(key, min, max) + queue_rows:
                btime, btype, time_data, value_data = self.extract_h_block(row)
                btype_list.append(btype)
                time_list.append(time_data)
                value_list.append(value_data)

                n += len(time_data) / 8
                if not reverse and len(btype_list) > 1 and n > abs(max_len):
                    self.h_more = True
                    break

            if len(btype_list) == 0:
                return self.empty_h_tuple(dtype)
            i = 0
            n = len(btype_list)
            while True:
                j = not_index(btype_list[i:], btype_list[i]) + i
                time_data = b''.join(time_list[i:j])
                value_data = b''.join(value_list[i:j])
                utimes, uvalues = self.unpack_h_data(time_data, value_data, btype_list[i], dtype)
                if i == 0:
                    times = utimes
                    values = uvalues
                else:
                    times = numpy.append(times, utimes)
                    values = numpy.append(values, uvalues)
                if j == n:
                    break
                i = j

            if len(queue_rows) == 1 and len(times) > 1 and times[-1] == times[-2]:
                times = times[:-1]
                values = values[:-1]
            if True:
                if start_time != None and len(times) > 0 and times[0] < start_time:
                    b = times >= start_time
                    times = times[b]
                    values = values[b]
                if end_time != None and len(times) > 0 and times[-1] > end_time:
                    b = times < end_time
                    times = times[b]
                    values = values[b]
            if len(times) > abs(max_len):
                if reverse:
                    times = times[max_len:]
                    values = values[max_len:]
                else:
                    times = times[:max_len]
                    values = values[:max_len]
            if ascii:
                times = self.times2ascii(times, utc=utc)
            if ascii or ascii_values:
                rid, fid, kid = self.tag2uid(tag)
                did = self.get_defid(rid)
                fmt_fld = self.getdef(did, fid, DEF_FORMAT)
                if fmt_fld:
                    dtype = self.getdef(did, fmt_fld, DEF_DTYPE)
                    if dtype == DT_RECORD:
                        format_rec = self.get(rid, fmt_fld)
                        if format_rec:
                            if self.get_defid(format_rec) == self.SELECT_DICT_DEF:
                                states = self.getdict(format_rec, 'SELECT_DESCRIPTION')
                                values = [ (states[str(v)] if states.has_key(str(v)) else str(v)) for v in values ]
                            else:
                                states = self.getlist(format_rec, 'SELECT_DESCRIPTION')
                                n = len(states)
                                values = numpy.array([ (states[int(v)] if int(v) < n else str(v)) for v in values ])
            # times = self.times2str(times)
            return [times, values]

    def gethist(self, tag, start_time = None, end_time = None, freq = None, agg_fn = None, agg_times = None, fill = None, null = None, agg_fill = False, max_len = -MAX_VALUES, maxlen = None, text = False, ascii = False, text_values = False, ascii_values = False, force_array = False, utc = False, time_sync = False, item_path = None):

        if text:
            ascii = True
        if text_values:
            ascii_values = True
        self.last_fill = False
        self.h_more = False
        if start_time == 0:
            start_time = None
        if end_time == MAX_TIME:
            end_time = None
        if isinstance(start_time, str):
            start_time = self.ascii2time(start_time, utc=utc)
            if start_time == None:
                return
        if isinstance(end_time, str):
            end_time = self.ascii2time(end_time, utc=utc)
            if end_time == None:
                return
        if freq != None:
            freq = self.delta2sec(freq)
            if freq == None:
                return
        if maxlen not in (None, 0):
            max_len = maxlen
        hcfg = self.get_h_cfg(tag, cached=True)
        if hcfg == None:
            if self.is_calc(tag):
                return self.gethis_calc(tag, start_time, end_time, freq, agg_fn=agg_fn, agg_times=agg_times, max_len=max_len, ascii=ascii, time_sync=time_sync, item_path=item_path)
            elif force_array:
                return self.empty_h_tuple()
            else:
                return
        hid, btype, c = hcfg
        dtype = HISTORY_BTYPES.get(btype)
        if dtype == None:
            return self.empty_h_tuple()
        else:
            dt_size = numpy.dtype(dtype).itemsize
            if fill == None:
                fill = False
            self.last_fill = fill
            if null == None:
                if dtype in (float16, float32, float64):
                    null = nan
                else:
                    null = 0
            self.last_null = null
            if freq:
                return self.gethis_agg(tag, start_time, end_time, freq=freq, agg_fn=agg_fn, fill=fill, null=null, max_len=max_len, ascii=ascii)
            if agg_times is not None:
                return self.gethis_agg(tag, agg_times=agg_times, agg_fn=agg_fn, fill=fill, null=null, max_len=max_len, ascii=ascii)
            if start_time not in (None, 0):
                start_time -= MSEC
            if end_time not in (None, MAX_TIME):
                end_time -= MSEC
            if max_len < 0:
                reverse = True
            else:
                reverse = False
            get_archive = True
            agg_fill_stop = False
            time_list = []
            value_list = []
            btype_list = []
            n = 0
            key = pkey('hd', hid.hid)
            qkey = pkey('hq', hid.hid)
            if start_time == None:
                min = '-'
            else:
                min = '('.encode() + pack('>Q', self.time2ms(start_time) - 1)
                rows = self.rdb.zrevrangebylex(key, min, '-', 0, 1)
                if len(rows) > 0:
                    min = '['.encode() + rows[0]
                    if self.pg_found:
                        block_start = self.unpack_h_key(rows[0])
                        if start_time >= block_start:
                            get_archive = False
            if end_time == None:
                max = '+'
                get_queue = True
            else:
                max = '('.encode() + pack('>Q', self.time2ms(end_time) + 1)
                row = self.rdb.lindex(qkey, 0)
                if row != None:
                    queue_start = self.unpack_h_key(row)
                    if end_time < queue_start:
                        get_queue = False
                    else:
                        get_queue = True
                else:
                    get_queue = False
            if get_queue:
                queue_rows = self.rdb.lrange(qkey, 0, -1)
            else:
                queue_rows = []
            if self.pg_found and get_archive:
                if start_time != None:
                    pg_start_time = self.time2dt(start_time, utc=self.utc_mode).pydatetime()
                    rows = self.pg_get("SELECT ts FROM arc_%d WHERE hid=%d AND ts<'%s' ORDER BY ts DESC LIMIT 1" % (hid.hfile, hid.hid, pg_start_time))
                    if len(rows) > 0:
                        pg_start_time = rows[0][0]
                if end_time != None:
                    pg_end_time = self.time2dt(end_time, utc=self.utc_mode).pydatetime()
                if start_time == None and end_time == None:
                    rows = self.pg_get('SELECT data FROM arc_%d WHERE hid=%d ORDER BY ts' % (hid.hfile, hid.hid))
                elif start_time == None:
                    rows = self.pg_get("SELECT data FROM arc_%d WHERE hid=%d AND ts<'%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_end_time))
                elif end_time == None:
                    rows = self.pg_get("SELECT data FROM arc_%d WHERE hid=%d AND ts>='%s' ORDER BY ts" % (hid.hfile, hid.hid, pg_start_time))
                else:
                    rows = self.pg_get("SELECT data dROM arc_%d WHERE hid=%d AND ts>='%s' AND ts<'%s'" % (hid.hfile,hid.hid,pg_start_time,pg_end_time))
                archive_rows = [ r[0] for r in rows ]
            else:
                archive_rows = []
            for row in archive_rows + self.rdb.zrangebylex(key, min, max) + queue_rows:
                btime, btype, time_data, value_data = self.extract_h_block(row)
                btype_list.append(btype)
                time_list.append(time_data)
                value_list.append(value_data)

                n += len(time_data) / 8
                if not reverse and len(btype_list) > 1 and n > abs(max_len):
                    self.h_more = True
                    break

            if len(btype_list) == 0:
                return self.empty_h_tuple(dtype)
            i = 0
            n = len(btype_list)
            while True:
                j = not_index(btype_list[i:], btype_list[i]) + i
                time_data = b''.join(time_list[i:j])
                value_data = b''.join(value_list[i:j])
                utimes, uvalues = self.unpack_h_data(time_data, value_data, btype_list[i], dtype)
                if i == 0:
                    times = utimes
                    values = uvalues
                else:
                    times = numpy.append(times, utimes)
                    values = numpy.append(values, uvalues)
                if j == n:
                    break
                i = j

            if len(queue_rows) == 1 and len(times) > 1 and times[-1] == times[-2]:
                times = times[:-1]
                values = values[:-1]
            if True:
                if start_time != None and len(times) > 0 and times[0] < start_time:
                    b = times >= start_time
                    times = times[b]
                    values = values[b]
                if end_time != None and len(times) > 0 and times[-1] > end_time:
                    b = times < end_time
                    times = times[b]
                    values = values[b]
            if len(times) > abs(max_len):
                if reverse:
                    times = times[max_len:]
                    values = values[max_len:]
                else:
                    times = times[:max_len]
                    values = values[:max_len]
            if ascii:
                times = self.times2ascii(times, utc=utc)
            if ascii or ascii_values:
                rid, fid, kid = self.tag2uid(tag)
                did = self.get_defid(rid)
                fmt_fld = self.getdef(did, fid, DEF_FORMAT)
                if fmt_fld:
                    dtype = self.getdef(did, fmt_fld, DEF_DTYPE)
                    if dtype == DT_RECORD:
                        format_rec = self.get(rid, fmt_fld)
                        if format_rec:
                            if self.get_defid(format_rec) == self.SELECT_DICT_DEF:
                                states = self.getdict(format_rec, 'SELECT_DESCRIPTION')
                                values = [ (states[str(v)] if states.has_key(str(v)) else str(v)) for v in values ]
                            else:
                                states = self.getlist(format_rec, 'SELECT_DESCRIPTION')
                                n = len(states)
                                values = numpy.array([ (states[int(v)] if int(v) < n else str(v)) for v in values ])
            # times = [self.time2dt(i).astimezone().strftime("%Y-%m-%d %H:%M:%S") for i in times]
            times = self.times2str(times)
            return (times, values)

    def gethis_agg(self, tag, start_time = None, end_time = None, freq = 60, agg_times = None, agg_fn = None, fill = False, null = 0, max_len = -MAX_VALUES, ascii = False):
        if agg_times is not None:
            if len(agg_times) > 0:
                start_time = agg_times[0]
                end_time = agg_times[-1]
            else:
                return self.empty_h_tuple()
        elif end_time not in (None, MAX_TIME) and freq > 0:
            new_start = self.ms2time(self.time2ms(end_time) - int(freq * 1000) * (abs(max_len) - 1))
            if new_start > start_time:
                start_time = new_start
        if agg_times is not None:
            times, values = self.gethis(tag, start_time, end_time + 2 * MSEC, agg_fill=True, max_len=max_len)
        else:
            times, values = self.gethis(tag, start_time, end_time, agg_fill=True, max_len=max_len)
        if agg_times is None:
            if start_time in (None, 0):
                if len(times) > 0:
                    start_time = times[0]
                else:
                    return self.empty_h_tuple()
            if end_time in (None, MAX_TIME):
                if len(times) > 0:
                    end_time = times[-1]
                else:
                    return self.empty_h_tuple()
            agg_times = self.trange(start_time, end_time, freq)
        if agg_fn in (None, 1):
            agg_values = self.timealign(times, values, agg_times, 1, fill, null)
        else:
            if isinstance(agg_fn, str):
                agg_id = self.get(agg_fn, 'AGGREGATE_ID')
                if agg_id == None or agg_id <= 0:
                    agg_fn = self.get_function(agg_fn)
                else:
                    agg_fn = agg_id
                if agg_fn == None:
                    return
            try:
                agg_values = self.timealign(times, values, agg_times, agg_fn, fill, null)
            except:
                return self.empty_h_tuple()

        if ascii:
            agg_times = self.times2ascii(agg_times)
        return (agg_times, agg_values)

    def timealign(self, times, values, new_times, agg_fn = 1, fill = False, null = 0):
        if not isinstance(times, ndarray) or times.dtype != float64:
            times = array(times, dtype=float64)
        if not isinstance(values, ndarray):
            values = array(values)
        if not isinstance(new_times, ndarray) or new_times != float64:
            new_times = array(new_times, dtype=float64)
        if agg_fn in (None, 0):
            agg_fn = 1
        # if issubdtype(values.dtype, np.float) or issubdtype(values.dtype, np.integer):
        #     return cci.timealign_agg(times, values, new_times, agg_fn, bool(fill), null)
        # else:
        return self.timealign_cdt(times, values, new_times)
        return None

    def timealign_cdt(self, times, values, new_times):
        n = len(new_times)
        m = len(times)
        agg_values = numpy.zeros(n, dtype=values.dtype)
        ms = 10 * MSEC
        j = 0
        for i in range(n):
            while j < m:
                if i < n - 1 and times[j] >= new_times[i + 1] - ms:
                    break
                elif times[j] >= new_times[i] - ms:
                    agg_values[i] = values[j]
                    j += 1
                    break
                else:
                    j += 1

        return agg_values

    def empty_h_tuple(self, dtype = numpy.float32):
        return (array([], dtype=float64), array([], dtype=dtype))

    def set_key_order(self, record, repeat, key, pos):
        rid = self.name2id(record)
        rfid = self.name2id(repeat)
        kid = self.name2id(key)
        if rid == None or rfid == None or kid == None:
            return
        else:
            self.rdb.hset(pkey('order', rid), pfld(rfid, kid), pack('>I', pos))
            return

    def cast_values(self, values, dtypes):
        values2 = []
        for i, dt in enumerate(dtypes):
            try:
                v = dt(values[i])
            except ValueError:
                if dt in (float16, float32, float64):
                    v = dt(nan)
                else:
                    v = dt(0)

            values2.append(v.tostring())

        return values2

    def group_worker(self, group, tags, stop_event):
        n = len(tags)
        hids = [0] * n
        btypes = [0] * n
        mput_hfiles = [0] * n
        mput_dtypes = [numpy.float32] * n
        mput_is_hfield = [False] * n
        complib_list = [0] * n
        for i, t in enumerate(tags):
            hid = self.tag2hid(t)
            if hid:
                mput_is_hfield[i] = True
                hids[i] = hid.hid
                hid, btype, complib = self.get_h_cfg(t)
                btypes[i] = btype
                mput_hfiles[i] = hid.hfile
                mput_dtypes[i] = HISTORY_BTYPES[btype]
                complib_list[i] = complib

        mput_phids = pack(('>%dI' % n), *hids)
        mput_pbtypes = pack(('>%dB' % n), *btypes)
        mput_tags = tags
        complib_dict = {}
        for c in unique(complib_list):
            if c != 0:
                complib_dict[c] = self.tag2dict(c)

        mput_complib_dev = [0] * n
        mput_complib_max = [0] * n
        mput_complib_badval = [None] * n
        for i, c in enumerate(complib_list):
            if c != 0:
                mput_complib_dev[i] = complib_dict[c]['DEV_VALUE']
                mput_complib_max[i] = self.sec2time(complib_dict[c]['DEV_MAX_TIME'])
                if complib_dict[c]['STORE_BAD']:
                    mput_complib_badval[i] = complib_dict[c]['BAD_VALUE']

        mput_last_value = [None] * n
        mput_last_time = [None] * n
        fresh_rebuild = True
        mput_uids = [ self.tag2uid(t) for t in tags ]
        time_uids = []
        for u in mput_uids:
            if u[1] == self.VALUE_FT:
                time_uids.append((u[0], self.TIME_FT, u[2]))

        mput_uids += time_uids
        mput_uids = [ self.uid2(u) for u in mput_uids ]
        while True:
            try:
                time_list = []
                values_list = []
                while True:
                    if stop_event.isSet():
                        return
                    try:
                        ts, values = self._group_queue[group].get_nowait()
                        time_list.append(ts)
                        values_list.append(values)
                    except Queue.Empty:
                        if len(time_list) > 0:
                            break
                        else:
                            time.sleep(0.1)

                n = len(mput_tags)
                pzero = pack('>B', 0)
                times = array(time_list, dtype=float64)
                ptimes = times.tostring()
                itime = self.time2ms(times[0])
                pitime = pack('>Q', itime)
                values_list = zip(*values_list)
                plen = pack('>I', len(ptimes))
                pipe = self.rdb.pipeline(transaction=False)
                for i in range(n):
                    values = cast_array(values_list[i], mput_dtypes[i], badval=mput_complib_badval[i])
                    if values is not None:
                        j = i * 4
                        key = 'hq' + mput_phids[j:j + 4]
                        data = pitime + mput_pbtypes[i] + pzero + plen + ptimes + values.tostring()
                        pipe.rpush(key, data)

                pipe.execute()
                self.send_events(mput_uids)
            except redis.exceptions.ReadOnlyError:
                continue

        return

    def put_group(self, tags, time, values, group = None, notify = True, rebuild = False):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            time = self.ascii2time(time)
            if time == None:
                return False
            if time > self._tix / self._mtix:
                return False
            if not self._group_queue.has_key(group) or tags != self._group_tags[group] or rebuild:
                if group in self._group_thread:
                    self._group_event[group].set()
                    self._group_thread[group].join()
                self._group_tags[group] = tags
                self._group_queue[group] = Queue.Queue()
                e = threading.Event()
                t = threading.Thread(target=self.group_worker, args=(group, tags, e))
                self._group_event[group] = e
                self._group_thread[group] = t
                t.daemon = True
                t.start()
            self._group_queue[group].put((time, values))
            return True

    def insocc(self, record, field, start_idx, ins_count):
        rid = self.name2id(record)
        fid = self.name2id(field)
        if rid == None or fid == None:
            return False
        else:
            did = self.get_defid(rid)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            field_list = self.list(rid, fid)
            total_count = self.get(rid, fid)
            did = self.get_defid(rid)
            self.put(rid, fid, total_count + ins_count)
            change_list = [ (i, i + ins_count) for i in range(start_idx + 1, total_count + 1) ]
            change_list.reverse()
            for old_idx, new_idx in change_list:
                for f in field_list:
                    value = self.get(rid, f, old_idx)
                    self.put(rid, f, value, new_idx)
                    dtype = self.getdef(did, f, DEF_DTYPE)
                    success = self.put(rid, f, self.unpack_field(self.default_value(dtype), dtype), old_idx)

            return True

    def append_rows(self, record, field, new_rows, notify = True):
        try:
            rid = self.name2id(record)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return False
            did = self.get_defid(rid)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            if not isinstance(new_rows, list):
                return False
            if len(new_rows) > 0 and type(new_rows[0]) not in (list, tuple):
                return False
            field_list = self.list(rid, fid)
            dtype_list = [ self.getdef(did, f, DEF_DTYPE) for f in field_list ]
            format_list = [ self.getdef(did, f, DEF_FORMAT) for f in field_list ]
            ref_list = []
            old_count = self.get(rid, fid)
            if old_count is None:
                old_count = 0
            new_count = old_count + len(new_rows)
            pipe = self.rdb.pipeline(transaction=False)
            for i, idx in enumerate(range(old_count + 1, new_count + 1)):
                for j, (f, dt, format) in enumerate(zip(field_list, dtype_list, format_list)):
                    if j < len(new_rows[i]):
                        value = new_rows[i][j]
                        data = self.pack_field(value, dt, format)
                    else:
                        value = ''
                        data = self.default_value(dt)
                    pipe.hset(pkey('rec', rid), pfld(f, idx), data)
                    if dt in (DT_RECORD, DT_FIELD):
                        ref_list.append(((rid, f, idx), self.tag2uid(value)))
                    elif dt == DT_SCHEDULE:
                        pipe.hset('sched', self.uid(rid, f, idx), data)
                        pipe.sadd(pkey('sched', rid), self.uid(rid, f, idx))
                        pipe.publish('put_sched', self.uid(rid, f, idx) + data)
                    elif dt == DT_INTEGER and f == self.SCHEDULE_FREQ_FT:
                        pipe.publish('put_freq', self.uid(rid, f, idx) + data)

            pipe.hset(pkey('rec', rid), pfld(fid, 0), self.pack_field(new_count, DT_INTEGER))
            pipe.execute()
            self.putrefs(ref_list)
            if notify:
                self.send_event((rid, fid, 0))
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def insert_rows(self, record, field, start_idx, new_rows, notify = True):
        try:
            rid = self.name2id(record)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return False
            did = self.get_defid(rid)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            if not isinstance(new_rows, list):
                return False
            if len(new_rows) > 0 and type(new_rows[0]) not in (list, tuple):
                return False
            field_list = self.list(rid, fid)
            dtype_list = [ self.getdef(did, f, DEF_DTYPE) for f in field_list ]
            ref_list = []
            ins_count = len(new_rows)
            old_count = self.get(rid, fid)
            new_count = old_count + ins_count
            if start_idx < 1 or start_idx > old_count + 1:
                return False
            reindex_list = [ i for i in range(start_idx, old_count + 1) ]
            if len(reindex_list) > 0:
                pipe = self.rdb.pipeline(transaction=False)
                for i in reindex_list:
                    for f in field_list:
                        pipe.hget(pkey('rec', rid), pfld(f, i))

                rows = pipe.execute()
            pipe = self.rdb.pipeline(transaction=False)
            if len(reindex_list) > 0:
                for i in reindex_list:
                    for f, dt in zip(field_list, dtype_list):
                        pipe.hdel(pkey('rec', rid), pfld(f, i))
                        if dt in (DT_RECORD, DT_FIELD):
                            ref_list.append(((rid, f, i), None))
                        elif dt == DT_SCHEDULE:
                            pipe.hdel('sched', self.uid(rid, f, i))
                            pipe.publish('del_sched', self.uid(rid, f, i))

            pipe.hset(pkey('rec', rid), pfld(fid, 0), self.pack_field(new_count, DT_INTEGER))
            for i, idx in enumerate(range(start_idx, start_idx + ins_count)):
                for j, (f, dt) in enumerate(zip(field_list, dtype_list)):
                    if j < len(new_rows[i]):
                        value = new_rows[i][j]
                        data = self.pack_field(value, dt)
                    else:
                        value = ''
                        data = self.default_value(dt)
                    pipe.hset(pkey('rec', rid), pfld(f, idx), data)
                    if dt in (DT_RECORD, DT_FIELD):
                        ref_list.append(((rid, f, idx), self.tag2uid(value)))
                    elif dt == DT_SCHEDULE:
                        pipe.hset('sched', self.uid(rid, f, idx), data)
                        pipe.sadd(pkey('sched', rid), self.uid(rid, f, idx))
                        pipe.publish('put_sched', self.uid(rid, f, idx) + data)
                    elif dt == DT_INTEGER and f == self.SCHEDULE_FREQ_FT:
                        pipe.publish('put_freq', self.uid(rid, f, idx) + data)

            if len(reindex_list) > 0:
                j = 0
                for i in range(start_idx + ins_count, old_count + ins_count + 1):
                    for f, dt in zip(field_list, dtype_list):
                        data = rows[j]
                        if data is not None:
                            pipe.hset(pkey('rec', rid), pfld(f, i), data)
                        if dt in (DT_RECORD, DT_FIELD):
                            ref = self.unpack_field(data, dt)
                            ref_list.append(((rid, f, i), ref))
                        elif dt == DT_SCHEDULE:
                            pipe.hset('sched', self.uid(rid, f, i), data)
                            pipe.sadd(pkey('sched', rid), self.uid(rid, f, i))
                            pipe.publish('put_sched', self.uid(rid, f, i) + data)
                        elif dt == DT_INTEGER and f == self.SCHEDULE_FREQ_FT:
                            pipe.publish('put_freq', self.uid(rid, f, i) + data)
                        j += 1

            pipe.execute()
            self.putrefs(ref_list)
            if notify:
                self.send_event((rid, fid, 0))
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def delete_rows(self, record, field, indexes, notify = True):
        try:
            rid = self.name2id(record)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return False
            did = self.get_defid(rid)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            indexes = unique(indexes)
            indexes.sort()
            if len(indexes) == 0:
                return True
            field_list = self.list(rid, fid)
            dtype_list = [ self.getdef(did, f, DEF_DTYPE) for f in field_list ]
            ref_list = []
            old_count = self.get(rid, fid)
            new_count = old_count - len(indexes)
            if indexes[0] < 1 or indexes[-1] > old_count:
                return False
            reindex_list = [ i for i in range(indexes[0] + 1, old_count + 1) if i not in indexes ]
            if len(reindex_list) > 0:
                pipe = self.rdb.pipeline(transaction=False)
                for i in reindex_list:
                    for f in field_list:
                        pipe.hget(pkey('rec', rid), pfld(f, i))

                rows = pipe.execute()
            pipe = self.rdb.pipeline(transaction=False)
            for i in range(indexes[0], old_count + 1):
                for f, dt in zip(field_list, dtype_list):
                    pipe.hdel(pkey('rec', rid), pfld(f, i))
                    if dt in (DT_RECORD, DT_FIELD):
                        ref_list.append(((rid, f, i), None))
                    elif dt == DT_SCHEDULE:
                        pipe.hdel('sched', self.uid(rid, f, i))
                        pipe.publish('del_sched', self.uid(rid, f, i))

            pipe.hset(pkey('rec', rid), pfld(fid, 0), self.pack_field(new_count, DT_INTEGER))
            if len(reindex_list) > 0:
                j = 0
                for i in range(indexes[0], new_count + 1):
                    for f, dt in zip(field_list, dtype_list):
                        data = rows[j]
                        if data is not None:
                            pipe.hset(pkey('rec', rid), pfld(f, i), data)
                        if dt in (DT_RECORD, DT_FIELD):
                            ref = self.unpack_field(data, dt)
                            ref_list.append(((rid, f, i), ref))
                        elif dt == DT_SCHEDULE:
                            pipe.hset('sched', self.uid(rid, f, i), data)
                            pipe.sadd(pkey('sched', rid), self.uid(rid, f, i))
                            pipe.publish('put_sched', self.uid(rid, f, i) + data)
                        elif dt == DT_INTEGER and f == self.SCHEDULE_FREQ_FT:
                            pipe.publish('put_freq', self.uid(rid, f, i) + data)
                        j += 1

            pipe.execute()
            self.putrefs(ref_list)
            if notify:
                self.send_event((rid, fid, 0))
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def delocc(self, record, field, indexes):
        rid = self.name2id(record)
        fid = self.name2id(field)
        if rid == None or fid == None:
            return False
        else:
            did = self.get_defid(rid)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            if len(indexes) == 0:
                return True
            field_list = self.list(rid, fid)
            total_count = self.get(rid, fid)
            pipe = self.rdb.pipeline(transaction=False)
            for i in indexes:
                for f in field_list:
                    pipe.hdel(pkey('rec', rid), pfld(f, i))

            pipe.execute()
            index_set = set(range(1, total_count + 1))
            del_set = set(indexes)
            index_set -= del_set
            index_list = list(index_set)
            index_list.sort()
            change_list = [ (old, new + 1) for new, old in enumerate(index_list) if old != new + 1 ]
            for old_index, new_index in change_list:
                for f in field_list:
                    value = self.get(rid, f, old_index)
                    self.put(rid, f, value, new_index)

            ok = self.put(rid, fid, len(index_list))
            return ok

    def process_schedule(self):
        if not hasattr(self, 'schedule_ts_dict'):
            self.schedule_ts_dict = {}
            self.schedule_rfld_dict = {}
            self.schedule_freq_dict = {}
            self.schedule_did_dict = {}
            for row in self.rdb.hgetall('sched').items():
                uid = self.xuid(row[0])
                ts = self.time2ms(self.get(uid))
                rid, fid, idx = uid
                did = self.get_defid(rid)
                rsfid = self.getdef(did, fid, DEF_RESCHEDULE)
                if rsfid:
                    freq = self.get(rid, rsfid, idx)
                    if freq == None:
                        freq = 0
                else:
                    freq = 0
                self.schedule_ts_dict[uid] = ts
                self.schedule_rfld_dict[uid] = (rid, rsfid, idx)
                self.schedule_freq_dict[uid] = freq
                self.schedule_did_dict[uid] = did

        if not hasattr(self, 'schedule_ps'):
            self.schedule_ps = self.rdb.pubsub(ignore_subscribe_messages=True)
            self.schedule_ps.subscribe('put_sched')
            self.schedule_ps.subscribe('put_freq')
            self.schedule_ps.subscribe('del_sched')
        while True:
            msg = self.schedule_ps.get_message()
            if msg == None:
                break
            if msg['channel'] == 'put_sched':
                uid = self.xuid(msg['data'][:12])
                ts, = unpack('>d', msg['data'][12:])
                self.schedule_ts_dict[uid] = self.time2ms(ts)
                if uid not in self.schedule_rfld_dict:
                    rid, fid, idx = uid
                    did = self.get_defid(rid)
                    rsfid = self.getdef(did, fid, DEF_RESCHEDULE)
                    if rsfid:
                        freq = self.get(rid, rsfid, idx)
                        if freq == None:
                            freq = 0
                    else:
                        freq = 0
                    self.schedule_rfld_dict[uid] = (rid, rsfid, idx)
                    self.schedule_freq_dict[uid] = freq
                    self.schedule_did_dict[uid] = did
            elif msg['channel'] == 'put_freq':
                uid = self.xuid(msg['data'][:12])
                freq, = unpack('>l', msg['data'][12:])
                rev_dict = {v:k for k, v in self.schedule_rfld_dict.items()}
                if uid in rev_dict:
                    uid = rev_dict[uid]
                    self.schedule_freq_dict[uid] = freq
            elif msg['channel'] == 'del_sched':
                uid = self.xuid(msg['data'])
                try:
                    del self.schedule_ts_dict[uid]
                    del self.schedule_freq_dict[uid]
                    del self.schedule_rfld_dict[uid]
                    del self.schedule_did_dict[uid]
                except KeyError:
                    pass

        if self.is_local:
            if self.utc_mode:
                now = self.time2ms(self.dt2time(datetime.utcnow(), utc=True))
            else:
                now = self.time2ms(self.dt2time(datetime.now()))
        else:
            now = self.time2ms(self.now())
        update_list = []
        for uid, ts in self.schedule_ts_dict.items():
            if ts <= now and ts != 0:
                freq = self.schedule_freq_dict[uid]
                if freq > 0:
                    freq *= self.schedule_freq_base
                    new_ts = ts + freq
                    if new_ts < now:
                        n = int((now - new_ts) / freq) + 2
                        new_ts = ts + n * freq
                    new_ts_ms = new_ts
                    new_ts = self.ms2time(new_ts)
                elif freq < 0:
                    freq = abs(freq)
                    new_ts = self.ms2time(ts)
                    while new_ts < self.now():
                        new_ts = self.add_months(new_ts, freq)

                    new_ts_ms = self.time2ms(new_ts)
                else:
                    new_ts = 0.0
                    new_ts_ms = 0
                self.schedule_ts_dict[uid] = new_ts_ms
                did = self.schedule_did_dict[uid]
                def_uid = (did, uid[1], uid[2])
                update_list.append((uid, def_uid, new_ts))

        if len(update_list) > 0:
            pipe = self.rdb.pipeline(transaction=False)
            for uid, def_uid, new_ts in update_list:
                data = self.pack_field(new_ts, DT_SCHEDULE)
                pipe.hset(pkey('rec', uid[0]), pfld(uid[1], uid[2]), data)
                pipe.publish(self.uid2(uid), self.uid2(uid) + data)
                pipe.publish(self.uid2(def_uid), self.uid2(uid) + data)

            pipe.execute()
        return

    def pack_history(self, rid, did, rfid):
        if not self.hpack_cache.has_key(did):
            self.hpack_cache[did] = [ (f, self.getdef(did, f, DEF_SOURCE)) for f in self.list(did, rfid) ]
        data_list = []
        for f_id, f_meta in self.get_h_meta(did, rfid):
            data = self.rdb.hget(pkey('rec', self.uid(rid)), pfld(f_meta['source'], 0))
            if f_meta['dtype'] == DT_CHAR:
                if len(data) < f_meta['length']:
                    data = data.ljust(f_meta['length'])
                else:
                    data = data[:f_meta['length']]
            data_list.append(data)

        h_data = ''.join(data_list)
        return h_data

    def pack_history2(self, did, rfid, data_fields):
        if not self.hpack_cache.has_key(did):
            self.hpack_cache[did] = [ (f, self.getdef(did, f, DEF_SOURCE)) for f in self.list(did, rfid) ]
        data_list = []
        for i, (f_id, f_meta) in enumerate(self.get_h_meta(did, rfid)):
            data = self.pack_field(data_fields[i], f_meta['dtype'], f_meta['format'])
            if f_meta['dtype'] == DT_CHAR:
                if len(data) < f_meta['length']:
                    data = data.ljust(f_meta['length'])
                else:
                    data = data[:f_meta['length']]
            if data == None:
                return
            data_list.append(data)

        h_data = ''.join(data_list)
        return h_data

    def unpack_history(self, did, rfid, data, fids, ascii = False, dref = None):
        h_values = []
        value = {}
        start_idx = 0
        for f_id, f_meta in self.get_h_meta(did, rfid, dref):
            end_idx = start_idx + f_meta['length']
            if start_idx == 0:
                h_time = self.unpack_field(data[start_idx:end_idx], f_meta['dtype'], format=f_meta['format'], ascii=False)
            value[f_id] = self.unpack_field(data[start_idx:end_idx], f_meta['dtype'], format=f_meta['format'], ascii=ascii, record=dref)
            start_idx += f_meta['length']

        for f in fids:
            h_values.append(value[f])

        return (h_time, h_values)

    def unpack_history_pv(self, data):
        values = self.pack_obj_AnalogDef.unpack(data)
        return (values[0], values)

    def get_h_meta(self, did, rfid, dref = None):
        if not self.h_meta_cache.has_key(did):
            self.h_meta_cache[did] = [ (fid, {'dtype': self.getdef(did, fid, DEF_DTYPE),
              'length': self.getdef(did, fid, DEF_LENGTH),
              'format': self.getdef(did, fid, DEF_FORMAT, dref),
              'source': self.getdef(did, fid, DEF_SOURCE),
              'order': self.getdef(did, fid, DEF_ORDER)}) for fid in self.list(did, rfid) ]
        return self.h_meta_cache[did]

    def activate(self, record, field, occ):
        rid = self.name2id(record)
        fid = self.name2id(field)
        if rid == None or fid == None:
            return False
        else:
            did = self.get_defid(rid)
            dtype = self.getdef(did, fid, DEF_DTYPE)
            if dtype == DT_TIMESTAMP:
                ok = self.put(rid, fid, self.now(), occ)
                if not ok:
                    self.put(rid, fid, self.now())
            elif dtype == DT_INTEGER:
                self.put(rid, fid, 1)
            return

    def count(self, definition = None):
        if definition is None:
            return self.rdb.hlen('name')
        else:
            did = self.name2id(definition)
            if did is None:
                return
            return self.rdb.hlen(pkey('sdef', did))
            return

    def mem(self, text = False):
        if text:
            return self.rdb.info()['used_memory_human']
        else:
            return self.rdb.info()['used_memory']

    def role(self):
        return self.rdb.info('replication')['role']

    def master(self):
        if self.sentinel:
            return self.sentinel.discover_master(self.sentinel_service)

    def pg_master(self):
        if self.sentinel:
            master = self.master()
            master_host, master_port = master
            hosts = [ (host, port) for host, port in self.pg_hosts if host == master_host ]
            if len(hosts) > 0:
                return hosts[0]

    def pg_slaves(self):
        if self.sentinel:
            master = self.master()
            master_host, master_port = master
            hosts = [ (host, port) for host, port in self.pg_hosts if host != master_host ]
            return hosts

    def slaves(self):
        if self.sentinel:
            return self.sentinel.discover_slaves(self.sentinel_service)

    def sentinels(self):
        if not self.sentinel:
            return
        hosts = []
        for host, s in zip(self.sentinel_hosts, self.sentinel.sentinels):
            try:
                s.ping()
            except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError, redis.exceptions.TimeoutError):
                continue

            hosts.append(host)

        return hosts

    def failover(self):
        if not self._pps_query(None, P_WRITE):
            return False
        elif not self.sentinel:
            return
        else:
            for s in self.sentinel.sentinels:
                try:
                    ok = s.execute_command('SENTINEL failover', self.sentinel_service)
                except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError, redis.exceptions.TimeoutError):
                    continue

                return ok

            return

    def check_quorum(self):
        if not self.sentinel:
            return
        for s in self.sentinel.sentinels:
            try:
                msg = s.execute_command('SENTINEL ckquorum', self.sentinel_service)
            except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
                continue
            except redis.exceptions.ResponseError:
                return str(sys.exc_info()[1])

            return msg

    def getdef(self, definition, field, pid, dref = None):
        did = self.name2id(definition)
        fid = self.name2id(field)
        if did == None or fid == None:
            return
        elif (did, fid, pid) in self.getdef_cache:
            return self.getdef_cache[did, fid, pid]
        else:
            data = self.rdb.hget(pkey('def', did), pfld(fid, pid))
            if data != None:
                if pid == DEF_DEFAULT:
                    dtype = self.getdef(did, fid, DEF_DTYPE)
                    value = self.unpack_field(data, dtype)
                elif pid == DEF_FORMAT:
                    dtype = self.getdef(did, fid, DEF_DTYPE)
                    value, = unpack('>I', data)
                    if dref and self.get_defid(value) == FIELD_DEF and dtype not in (DT_FLOAT, DT_DOUBLE):
                        value = self.get(dref, value)
                        if value == 0:
                            value = None
                else:
                    value, = unpack('>I', data)
                    if dref and self.get_defid(value) == FIELD_DEF:
                        value = self.get(dref, value)
                        if value == 0:
                            value = None
            elif pid == DEF_LENGTH:
                dtype = self.getdef(did, fid, DEF_DTYPE)
                value = len(self.default_value(dtype))
            else:
                value = None
            self.getdef_cache[did, fid, pid] = value
            return value

    def mgetdef(self, definition, fields, pids):
        did = self.name2id(definition)
        fids = self.names2ids(fields)
        if did == None or fids.count(None) > 0:
            return
        elif (did, tuple(fids), tuple(pids)) in self._mgetdef_cache:
            return self._mgetdef_cache[did, tuple(fids), tuple(pids)]
        else:
            pipe = self.rdb.pipeline(transaction=False)
            for pid in pids:
                for fid in fids:
                    pipe.hget(pkey('def', did), pfld(fid, pid))

            rows = pipe.execute()
            value_dict = {}
            i = 0
            for pid in pids:
                for field, fid in zip(fields, fids):
                    data = rows[i]
                    if data != None:
                        if pid == DEF_DEFAULT:
                            dtype = self.getdef(did, fid, DEF_DTYPE)
                            value = self.unpack_field(data, dtype)
                        else:
                            value, = unpack('>I', data)
                    elif pid == DEF_LENGTH:
                        dtype = self.getdef(did, fid, DEF_DTYPE)
                        value = len(self.default_value(dtype))
                    else:
                        value = None
                    if field not in value_dict:
                        value_dict[field] = {}
                    value_dict[field][pid] = value
                    i += 1

            self._mgetdef_cache[did, tuple(fids), tuple(pids)] = value_dict
            return value_dict

    def putdef(self, definition, field, dtype = None, length = None, order = None, repeat = None, format = None, chain = None, source = None, reschedule = None, default = None, quality = None, dhistory = None, skey = None, time = None, readonly = None, hidden = None):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            did = self.name2id(definition)
            fid = self.name2id(field)
            if did == None or fid == None:
                return False
            if dtype != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_DTYPE), pack('>I', dtype))
                if self.getdef_cache.has_key((did, fid, DEF_DTYPE)):
                    del self.getdef_cache[did, fid, DEF_DTYPE]
            if length != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_LENGTH), pack('>I', length))
                if self.getdef_cache.has_key((did, fid, DEF_LENGTH)):
                    del self.getdef_cache[did, fid, DEF_LENGTH]
            if order != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_ORDER), pack('>I', order))
                if self.getdef_cache.has_key((did, fid, DEF_ORDER)):
                    del self.getdef_cache[did, fid, DEF_ORDER]
            if repeat != None:
                repeat = self.name2id(repeat)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_REPEAT), pack('>I', repeat))
                if self.getdef_cache.has_key((did, fid, DEF_REPEAT)):
                    del self.getdef_cache[did, fid, DEF_REPEAT]
            if format != None:
                format = self.name2id(format)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_FORMAT), pack('>I', format))
                self.putref((did, fid, DEF_FORMAT), (format, 0, 0))
                if self.getdef_cache.has_key((did, fid, DEF_FORMAT)):
                    del self.getdef_cache[did, fid, DEF_FORMAT]
            if chain != None:
                chain = self.name2id(chain)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_CHAIN), pack('>I', chain))
                if self.getdef_cache.has_key((did, fid, DEF_CHAIN)):
                    del self.getdef_cache[did, fid, DEF_CHAIN]
            if source != None:
                source = self.name2id(source)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_SOURCE), pack('>I', source))
                if self.getdef_cache.has_key((did, fid, DEF_SOURCE)):
                    del self.getdef_cache[did, fid, DEF_SOURCE]
            if reschedule != None:
                reschedule = self.name2id(reschedule)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_RESCHEDULE), pack('>I', reschedule))
                if self.getdef_cache.has_key((did, fid, DEF_RESCHEDULE)):
                    del self.getdef_cache[did, fid, DEF_RESCHEDULE]
            if quality != None:
                quality = self.name2id(quality)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_QUALITY), pack('>I', quality))
                if self.getdef_cache.has_key((did, fid, DEF_QUALITY)):
                    del self.getdef_cache[did, fid, DEF_QUALITY]
            if time != None:
                time = self.name2id(time)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_TIME), pack('>I', time))
                if self.getdef_cache.has_key((did, fid, DEF_TIME)):
                    del self.getdef_cache[did, fid, DEF_TIME]
            if dhistory != None:
                dhistory = self.name2id(dhistory)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_DHISTORY), pack('>I', dhistory))
                if self.getdef_cache.has_key((did, fid, DEF_DHISTORY)):
                    del self.getdef_cache[did, fid, DEF_DHISTORY]
            if skey != None:
                skey = self.name2id(skey)
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_SKEY), pack('>I', skey))
                if self.getdef_cache.has_key((did, fid, DEF_SKEY)):
                    del self.getdef_cache[did, fid, DEF_SKEY]
            if default != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_DEFAULT), self.pack_field(default, dtype))
                if self.getdef_cache.has_key((did, fid, DEF_DEFAULT)):
                    del self.getdef_cache[did, fid, DEF_DEFAULT]
            if readonly != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_READONLY), pack('>I', int(readonly)))
                if self.getdef_cache.has_key((did, fid, DEF_READONLY)):
                    del self.getdef_cache[did, fid, DEF_READONLY]
            if hidden != None:
                self.rdb.hset(pkey('def', did), pfld(fid, DEF_HIDDEN), pack('>I', int(hidden)))
                if self.getdef_cache.has_key((did, fid, DEF_HIDDEN)):
                    del self.getdef_cache[did, fid, DEF_HIDDEN]
            self.putref((did, fid, 0), (fid, 0, 0))
            self._list_fields_cache = {}
            self._mgetdef_cache = {}
            return True

    def deldef(self, definition, field, pid = None):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            did = self.name2id(definition)
            fid = self.name2id(field)
            if did == None or fid == None:
                return False
            if pid != None:
                ok = self.rdb.hdel(pkey('def', did), pfld(fid, pid))
                return bool(ok)
            found_flds = []
            for k in self.rdb.hkeys(pkey('def', did)):
                found_fid, found_pid = ufld(k)
                if found_fid == fid:
                    found_flds.append(k)

            if len(found_flds) == 0:
                return False
            self.rdb.hdel(pkey('def', did), *found_flds)
            self.putref((did, fid, 0), None)
            for rid in self.lsname(did, ascii=False):
                self.rdb.hdel(pkey('rec', rid), pfld(fid, 0))

            self.getdef_cache = {}
            self._mgetdef_cache = {}
            self._list_fields_cache = {}
            return True
            return

    def set_property(self, definition, field, property, value):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            did = self.name2id(definition)
            fid = self.name2id(field)
            if did == None or fid == None:
                return False
            if isinstance(value, str):
                value = self.name2id(value)
                if value == None:
                    return False
            if property == DEF_DEFAULT:
                dtype = self.get_property(did, fid, DEF_DTYPE)
                if dtype == None:
                    return False
                value = self.pack_field(value, dtype)
            else:
                value = pack('>I', value)
            self.rdb.hset(pkey('def', did), pfld(fid, property), value)
            return True

    def get_property(self, definition, field, property, text = False, ascii = False):
        if text:
            ascii = True
        val = self.getdef(definition, field, property)
        if ascii:
            if property == DEF_DTYPE:
                val = DEF_DTYPES[val]
            elif property not in (DEF_ORDER,
             DEF_READONLY,
             DEF_DEFAULT,
             DEF_LENGTH):
                val = self.id2name(val)
        return val

    def get_defid(self, record, ascii = False):

        rid = self.name2id(record)
        if rid == None:
            return
        else:
            if  rid in self.did_cache:
                did = self.did_cache[rid]
            else:
                data = self.rdb.hget(pkey('rec', rid), pfld(0, 0))
                if data == None:
                    return
                did, = unpack('>I', data)
                self.did_cache[rid] = did
            if ascii:
                return self.id2name(did)
            return did
            return

    def types(self, rids, text = False, ascii = False):
        if text:
            ascii = True
        if len(rids) == 0:
            return []
        else:
            if isinstance(rids[0], str):
                rids = self.names2ids(rids)
            pipe = self.rdb.pipeline(transaction=False)
            for rid in rids:
                if rid == None:
                    rid = 4294967295
                pipe.hget(pkey('rec', rid), pfld(0, 0))

            type_list = []
            for row in pipe.execute():
                if row == None:
                    type_list.append(None)
                else:
                    did, = unpack('>I', row)
                    type_list.append(did)

            if ascii:
                type_list = self.ids2names(type_list)
                type_list = [ ('' if t == None else t) for t in type_list ]
            return type_list

    def dtype(self, tag, cached = False):
        h = self.get_h_cfg(tag, cached=cached)
        if h is None:
            return
        else:
            return self.btype2dtype(h[1])

    def dtypes(self, tags, field = None):
        if field == None:
            field = 'VALUE'
        return [ (self.btype2dtype(h[1]) if h is not None else None) for h in self.mget_h_cfg(tags, field) ]

    def uid(self, rid, fid, idx):
        if type(idx) == str:
            return pack('>III', rid, fid, 0) + idx
        else:
            return pack('>III', rid, fid, idx)

    def uid2(self, in_uid):
        if type(in_uid) in (list, tuple):
            if len(in_uid) == 3:
                rid, fid, occ = in_uid
            elif len(in_uid):
                rid, fid = in_uid
                occ = 0
        else:
            rid = in_uid
            fid = 0
            occ = 0
        return pack('>III', rid, fid, occ)

    def xuid(self, uid):
        return unpack('>III', uid)

    def type(self, tag, field = None, text = False, ascii = False):
        if text:
            ascii = True
        rid = self.name2id(tag)
        if rid == None or rid < 0:
            return
        elif field != None:
            fid = self.name2id(field)
            if fid == None:
                return
            did = self.get_defid(rid)
            if did == 0:
                did = rid
            dtype = self.getdef(did, fid, DEF_DTYPE)
            if ascii:
                dtype = DEF_DTYPES[dtype]
            return dtype
        else:
            dtype = self.get_defid(rid, ascii)
            return dtype
            return

    def add(self, names, definition = None):
        if definition == None:
            definition = self.ANALOG_DEF
        if type(names) in (list, tuple):
            status = []
            for name in names:
                status.append(self._add(name, definition))

        else:
            status = self._add(names, definition)
        return status

    def _add(self, name, definition):
        try:
            if not is_ascii(name):
                return False
            name = str(name)
            if name.strip() == '':
                return False
            if self.name2id(name, use_cache=False) != None:
                return False
            defid = self.name2id(definition)
            parent_id = self.get_defid(definition)
            if defid == None or parent_id != 0:
                return False
            if not self._pps_query(defid, P_ADD):
                return False
            recid = self.allocate_id()
            if defid == DEFINITION_DEF:
                self.putdef(recid, NAME, dtype=DT_CHAR, order=0)
            self.rdb.hset(pkey('rec', recid), pfld(0, 0), pack('>I', defid))
            for fid in self.list(defid):
                if fid == NAME:
                    self.rdb.hset(pkey('rec', recid), pfld(fid, 0), name)
                else:
                    dtype = self.getdef(defid, fid, DEF_DTYPE)
                    repeat = self.getdef(defid, fid, DEF_REPEAT)
                    default = self.getdef(defid, fid, DEF_DEFAULT)
                    if repeat == None:
                        if fid == self.OWNER_FT:
                            value = self.pack_field(self.user, DT_RECORD)
                            self.putref((recid, fid, 0), self.name2id(self.user))
                        elif default == None:
                            value = self.default_value(dtype)
                        else:
                            value = self.pack_field(default, dtype)
                        self.rdb.hset(pkey('rec', recid), pfld(fid, 0), value)

            if defid != DEFINITION_DEF:
                for r, f, k in self.list_h_cfg(defid):
                    hid, btype, cos = self.get_h_cfg((r, f, k))
                    self.put_h_cfg((recid, f, k), hfile=hid.hfile, dtype=HISTORY_BTYPES[btype], complib=cos)

            self.rdb.hset('name', name.upper(), pack('>I', recid))
            self.rdb.hset('name2', name, pack('>I', recid))
            self.rdb.hset(pkey('sdef', defid), name, pack('>I', recid))
            self.did_cache[recid] = defid
            self.id_cache[name.upper()] = recid
            return True
        except redis.exceptions.ReadOnlyError:
            return False
        return

    def madd(self, names, definition = None):
        if not self._pps_query(None, P_ADD):
            return False
        else:
            if not isinstance(names, list):
                names = [names]
            if len(names) == 0:
                return False
            ids = self.names2ids(names)
            if ids.count(None) != len(names):
                return False
            if definition is None:
                definition = self.ANALOG_DEF
            did = self.name2id(definition)
            parent_id = self.get_defid(definition)
            if did == None or parent_id != 0:
                return False
            id_list = self.allocate_ids(len(names))
            fid_list = self.list(did)
            repeat_dict = {}
            value_dict = {}
            for fid in fid_list:
                if fid == NAME:
                    pass
                else:
                    dtype = self.getdef(did, fid, DEF_DTYPE)
                    repeat = self.getdef(did, fid, DEF_REPEAT)
                    default = self.getdef(did, fid, DEF_DEFAULT)
                    repeat_dict[fid] = repeat
                    if repeat == None:
                        if default == None:
                            value = self.default_value(dtype)
                        else:
                            value = self.pack_field(default, dtype)
                        value_dict[fid] = value

            if did == DEFINITION_DEF:
                for rid in id_list:
                    self.putdef(rid, NAME, dtype=DT_CHAR, order=0)

            pipe = self.rdb.pipeline(transaction=False)
            for i, rid in enumerate(id_list):
                key = pkey('rec', rid)
                pipe.hset(key, pfld(0, 0), pack('>I', did))
                for fid in fid_list:
                    if fid == NAME:
                        pipe.hset(key, pfld(fid, 0), names[i])
                    elif repeat_dict[fid] == None:
                        pipe.hset(key, pfld(fid, 0), value_dict[fid])

                pipe.hset('redi', names[i].upper(), pack('>I', rid))
                pipe.hset('name2', names[i], pack('>I', rid))
                pipe.hset(pkey('sdef', did), names[i], pack('>I', rid))
                self.did_cache[rid] = did

            pipe.execute()
            if did != DEFINITION_DEF:
                hist_rules = []
                for r, f, k in self.list_h_cfg(did):
                    hid, btype, complib = self.get_h_cfg((r, f, k))
                    hist_rules.append((hid.hfile,
                     f,
                     k,
                     btype,
                     complib))

                n = len(id_list) * len(hist_rules)
                hids = self.allocate_hids(n)
                pipe = self.rdb.pipeline(transaction=False)
                i = 0
                for rid in id_list:
                    for hfile, fid, kid, btype, complib in hist_rules:
                        key = pack('>III', rid, fid, kid)
                        pvalue = pack('>IIBI', hfile, hids[i], btype, complib)
                        pipe.hset('hr', key, pvalue)
                        pipe.zadd('zhr', key, 0)
                        i += 1

                pipe.execute()
            return True

    def delete(self, records, delref = False):
        if type(records) in (list, tuple):
            status = []
            for record in records:
                status.append(self._delete(record, delref))

        else:
            status = self._delete(records, delref)
        return status

    def _delete(self, record, delref = False):
        try:
            recid = self.name2id(record)
            if recid == None:
                return False
            did = self.get_defid(recid)
            if not self._pps_query(did, P_DELETE, recid):
                return False
            if did == DEFINITION_DEF and self.count(recid) > 0:
                return False
            ref_list = self.getref((recid, 0, 0))
            if delref:
                def_list = [ r for r, f, o in ref_list if self.get_defid(r) == DEFINITION_DEF ]
                if len(def_list) > 0:
                    return False
                for ref in ref_list:
                    self.put(ref, None)
                    if ref[2] != 0 and self.type(ref[0]) == self.DICTIONARY_DEF:
                        self.del_key(ref)

                self.delref_outer(recid)
            elif len(ref_list) > 0:
                return False
            self.delref_inner(recid)
            for r, f, k in self.list_h_cfg(recid):
                self.del_h_cfg((r, f, k))

            if type(record) == types.int:
                record = self.id2name(recid)
            if did in (self.ANALOG_DEF, self.DISCRETE_DEF, self.CALCULATION_DEF):
                self._del_desc_key(recid)
            self.rdb.hdel('name', record.upper())
            self.rdb.hdel('name2', record)
            self.rdb.hdel(pkey('sdef', did), record)
            sched_uids = self.rdb.smembers(pkey('sched', recid))
            for u in sched_uids:
                self.rdb.publish('del_sched', u)

            if len(sched_uids) > 0:
                self.rdb.hdel('sched', *sched_uids)
                self.rdb.delete(pkey('sched', recid))
            self.rdb.delete(pkey('rec', recid))
            self.deallocate_id(recid)
            if self.did_cache.has_key(recid):
                del self.did_cache[recid]
            if self.id_cache.has_key(record.upper()):
                del self.id_cache[record.upper()]
            if self.hcfg_cache.has_key(recid):
                del self.hcfg_cache[recid]
            if self.hcfg_cache.has_key((recid, self.VALUE_FT)):
                del self.hcfg_cache[recid, self.VALUE_FT]
            if self.hcfg_cache.has_key(record.upper()):
                del self.hcfg_cache[record.upper()]
            if self.hcfg_cache.has_key((record.upper(), 'VALUE')):
                del self.hcfg_cache[record.upper(), 'VALUE']
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def copy(self, src_record, dst_record):
        src_rid = self.name2id(src_record)
        dst_rid = self.name2id(dst_record)
        if src_rid == None or dst_rid != None:
            return False
        elif not self._pps_query(src_rid, P_ADD):
            return False
        else:
            did = self.get_defid(src_rid)
            ok = self.add(dst_record, did)
            if not ok:
                return False
            dst_rid = self.name2id(dst_record)
            for field, idx, value, dtype, fmt in self.lsrec(src_rid):
                if field == 'NAME':
                    continue
                self.put(dst_rid, field, value, activate=False, notify=False)
                if dtype in (DT_LIST, DT_DICTIONARY, DT_SPREADSHEET):
                    for field, idx, value, dtype, fmt in self.lsrec(src_rid, field):
                        self.put(dst_rid, field, value, idx)

                elif dtype == DT_HISTORY:
                    hfields = self.list(src_rid, field)
                    for data_list in self.gethis(src_rid, hfields):
                        self.puthis(dst_rid, field, data_list)

            return True

    def checkpoint(self):
        return self.save()

    def save(self, sync = False):
        if not self._pps_query(None, P_WRITE):
            return False
        else:
            try:
                if sync:
                    self.rdb.save()
                else:
                    self.rdb.bgsave()
            except redis.ResponseError:
                return

            return True
            return

    def last_save_time(self, text = False):
        d = self.rdb.lastsave()
        t = self.dt2time(d)
        if text:
            return self.time2ascii(t)
        else:
            return t

    def last_save_ok(self):
        return self.rdb.info()['rdb_last_bgsave_status'] == 'ok'

    def close(self):
        if self.redis_process:
            self.rdb.shutdown()
            self.redis_process.terminate()
            self.redis_process.wait()
        elif self.is_open():
            self.ps.close()
            self.rdb.connection_pool.disconnect()
        if self.pg_found:
            for host in self.pg_hosts:
                try:
                    self.pg_cur[host].close()
                    self.pg_con[host].close()
                except:
                    pass

        self.port = None
        self.id_cache = {}
        self.getdef_cache = {}
        self._mgetdef_cache = {}
        self._list_fields_cache = {}
        self.hpack_cache = {}
        self.h_meta_cache = {}
        self.select_cache = {}
        return

    def is_open(self):
        try:
            self.rdb.ping()
        except (AttributeError, redis.ConnectionError):
            return False

        return True

    def allocate_id(self):
        data = self.rdb.lpop('free')
        rid, = unpack('>I', data)
        return rid

    def allocate_ids(self, count):
        pipe = self.rdb.pipeline(transaction=False)
        for i in range(count):
            pipe.lpop('free')

        rows = pipe.execute()
        id_list = []
        for row in rows:
            id, = unpack('>I', row)
            id_list.append(id)

        return id_list

    def deallocate_id(self, rid):
        self.rdb.rpush('free', pack('>I', rid))

    def default_value(self, datatype, length = 0):
        if datatype == DT_CHAR:
            return ''
        if datatype == DT_INTEGER:
            return pack('>l', 0)
        if datatype == DT_FLOAT:
            return pack('>d', 0.0)
        if datatype == DT_DOUBLE:
            return pack('>d', 0.0)
        if datatype == DT_TIMESTAMP:
            return pack('>d', 0.0)
        if datatype == DT_SCHEDULE:
            return pack('>d', 0.0)
        if datatype == DT_RECORD:
            return pack('>I', 0)
        if datatype == DT_FIELD:
            return pack('>II', 0, 0)
        if datatype == DT_LIST:
            return pack('>I', 0)
        if datatype == DT_DICTIONARY:
            return pack('>I', 0)
        if datatype == DT_SPREADSHEET:
            return pack('>I', 0)
        if datatype == DT_HISTORY:
            return pack('>L', 0)
        if datatype == DT_CHISTORY:
            return pack('>L', 0)
        if datatype == DT_MATRIX:
            return pack('>LL', 0, 0)

    def default_value_unpacked(self, datatype):
        if datatype == DT_CHAR:
            return ''
        if datatype == DT_INTEGER:
            return 0
        if datatype == DT_FLOAT:
            return 0.0
        if datatype == DT_DOUBLE:
            return 0.0
        if datatype == DT_TIMESTAMP:
            return 0.0
        if datatype == DT_SCHEDULE:
            return 0.0
        if datatype == DT_RECORD:
            return 0
        if datatype == DT_FIELD:
            return (0, 0)
        if datatype == DT_LIST:
            return 0
        if datatype == DT_DICTIONARY:
            return 0
        if datatype == DT_SPREADSHEET:
            return 0
        if datatype == DT_HISTORY:
            return 0
        if datatype == DT_CHISTORY:
            return 0
        if datatype == DT_MATRIX:
            return (0, 0)

    def get_function(self, tag):
        name = self.get(tag, 'NAME')
        code = self.get(tag, 'CODE')
        try:
            exec (code)
            f = eval(name)
        except:
            f = None

        return f

    def get_current_time(self):
        return self.now()

    def now_local(self, text = False, ascii = False):
        if text:
            ascii = True
        dt = datetime.now()
        t = self.dt2time(dt)
        if ascii:
            t = self.time2ascii(t)
        return t

    def now(self, text = False, ascii = False):
        if text:
            ascii = True
        t, ms = self.rdb.time()
        t = self.unix2time(t) + self.ms2time(ms / 1000.0)
        if ascii:
            t = self.time2ascii(t)
        return t

    def time2ms(self, value):
        return int(round(value * 86400000.0))
    def ms2time(self, value):
        return float(value) / 86400000.0

    def time2sec(self, value):
        return value * 86400.0

    def sec2time(self, value):
        return float(value) / 86400.0

    def time2dt(self, value, utc = False):
        if value == None:
            return
        else:
            if self.utc_mode and not utc:
                offset = self.utc_offset
            else:
                offset = 0

            days, secs = divmod(value, 1)

            # days, secs = cci.time2dt(value)
            days = int(days)

            dt = datetime.datetime.fromordinal(days).replace(tzinfo=UTC)

            musec_prec = 20
            remainder_musec = int(round(secs * MUSECONDS_PER_DAY / musec_prec)
                                  * musec_prec)+(offset*1000000)

            if days < 30 * 365:
                remainder_musec = int(round(remainder * MUSECONDS_PER_DAY))+(offset*1000000)
            dt += datetime.timedelta(microseconds=remainder_musec)


            return dt
    def dt2time(self, dt, utc = False):
        # dt = datetime.fromtimestamp(dt)
        base = float(dt.toordinal())

        if hasattr(dt, 'hour'):
            base += dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0 + dt.microsecond / 86400000000.0
        if self.utc_mode and not utc:
            base -= self.utc_offset / 86400.0

        return base

    def is_dst(self, value):
        if isinstance(value, str):
            value = self.str2time(value)
        if value is None:
            return
        else:
            dt = datetime.fromtimestamp(self.time2unix(value))
            dt = self.tz.localize(dt)
            return bool(dt.dst())

    def str2time(self, value, format = None, utc = False):
        if not isinstance(value, str):
            return value
        else:
            if format != None:
                strict_mode = True
            else:
                strict_mode = False
                format = self.time_format
            try:
                if value.count(':') == 1:
                    value += ':00'
                dt = datetime.datetime.strptime(value, format)
            except ValueError:
                if strict_mode:
                    return
                value = value.replace('this month', 'last month + 1 month')
                value = value.replace('current month', 'last month + 1 month')
                value = value.replace('this year', 'last year + 1 year')
                value = value.replace('current year', 'last year + 1 year')
                source_time = self.time2dt(self.now())
                dt, parse_status = self._cal.parseDT(value, source_time)
                if parse_status == 0:
                    return

            return self.dt2time(dt, utc=utc)

    def str2time_fast(self, value, format = 1, utc = False):
        fast_int = cci.fast_int
        if format == 3:
            m = time_pattern_iso.match(value)
        else:
            m = time_pattern.match(value)
        if m != None:
            if format == 1:
                month = fast_int(m.group(1))
                day = fast_int(m.group(2))
                year = fast_int(m.group(3))
            elif format == 2:
                day = fast_int(m.group(1))
                month = fast_int(m.group(2))
                year = fast_int(m.group(3))
            elif format == 3:
                year = fast_int(m.group(1))
                month = fast_int(m.group(2))
                day = fast_int(m.group(3))
            else:
                return
            if 0 <= year <= 68:
                year += 2000
            elif 69 <= year <= 99:
                year += 1900
            hour = fast_int(m.group(4))
            minute = fast_int(m.group(5))
            sec = fast_int(m.group(6))
            micro = fast_int(m.group(7))
            if micro != 0:
                micro *= 10 ** (6 - len(m.group(7)))
            try:
                dt = datetime(year, month, day, hour, minute, sec, micro)
            except ValueError:
                return

            return self.dt2time(dt, utc=utc)
        else:
            return
        return

    def times2str(self, times, format = None, utc = False):
        if format is None:
            format = self.time_format
        times = [ self.time2dt(t, utc=utc) for t in times ]
        if self.iso_time_enabled:
            if self.time_decimal > 2:
                return [ ('' if t is None else cci.mx2iso(t.year, t.month, t.day, t.hour, t.minute, t.second)) for t in times ]
            else:
                return [ ('' if t is None else str(t)[:20 + self.time_decimal]) for t in times ]
        else:
            return [ ('' if t is None else t.strftime(format)) for t in times ]
        return

    def time2str(self, value, format = None, utc = False):
        if format is None:
            format = self.time_format
        if value in (0.0, None):
            value = ''
        else:
            d = self.time2dt(value, utc)
            if d is None:
                return
            if self.iso_time_enabled:
                if self.time_decimal > 2:
                    value = cci.mx2iso(d.year, d.month, d.day, d.hour, d.minute, d.second)
                else:
                    value = str(d)[:20 + self.time_decimal]
            else:
                value = d.strftime(format)
        return value

    def sec2delta(self, value):
        return format_timespan(value)

    def delta2sec(self, value):
        if not isinstance(value, str):
            return value
        else:
            match = re.match('([0-9]+) {0,1}(mo)(nth|nths){0,1}$', value)
            if match:
                return -int(match.group(1))
            try:
                return parse_timespan(value)
            except:
                return None

            return None

    def delta2time(self, value):
        if isinstance(value, str):
            try:
                sec = parse_timespan(value)
            except:
                return

            return self.sec2time(sec)
        else:
            return

    def unix2time(self, value):
        if self.utc_mode:
            d = datetime.datetime.utcfromtimestamp(value)
            return self.dt2time(d, utc=True)
        else:
            d = datetime.datetime.fromtimestamp(value)
            return self.dt2time(d)

    def time2unix(self, value):
        if self.utc_mode:
            d = self.time2dt(value, utc=True)
            return calendar.timegm(d.timetuple())
        else:
            d = self.time2dt(value)
            return time.mktime(d.timetuple())

    def local2utc(self, value):
        if self.utc_mode:
            return value - self.utc_offset / 86400.0
        else:
            return value

    def utc2local(self, value):
        if self.utc_mode:
            return value + self.utc_offset / 86400.0
        else:
            return value

    def local2utc_unix(self, value):
        if self.utc_mode:
            return value - self.utc_offset
        else:
            return value

    def utc2local_unix(self, value):
        if self.utc_mode:
            return value + self.utc_offset
        else:
            return value

    def int2str(self, int_value, select_tag):
        if isinstance(int_value, str):
            return int_value
        rid = self.name2id(select_tag)
        if not rid:
            return ''
        did = self.get_defid(rid)
        if did == self.SELECT_DICT_DEF:
            states = self.getdict(rid, 'SELECT_DESCRIPTION')
            if states.has_key(str(int_value)):
                return states[str(int_value)]
            else:
                return ''
        else:
            state_list = self.getlist(rid, 'SELECT_DESCRIPTION')
            try:
                return state_list[int(int_value)]
            except (IndexError, ValueError):
                return ''

    def unpack_field(self, fld_data, datatype, format = None, ascii = False, columns = 1, record = None):
        # rid, fid = unpack('>d', "\x00\x00\x00\x02")
        if fld_data in (None, ''):
            if ascii:
                return ''
            else:
                return
        elif datatype == DT_TIMESTAMP:
            if len(fld_data) == 8:
                value, = unpack('>d', fld_data)
            else:
                value = 0.0
            if ascii:
                value = self.time2ascii(value)


        elif datatype == DT_FLOAT:
            if len(fld_data) == 8:
                value, = unpack('>d', fld_data)
            elif len(fld_data) == 4:
                value, = unpack('>f', fld_data)
            else:
                value = nan
            if ascii:
                if numpy.isnan(value):
                    value = 'nan'
                else:
                    if record:
                        format = self.get(record, format)
                    if format == None or format < 0:
                        value = float2str(value)
                    else:
                        fmt = '%%.%df' % format
                        value = fmt % value
        elif datatype == DT_INTEGER:
            if len(fld_data) == 4:
                # str , bytes 변환 과정
                if isinstance(fld_data,str):
                    fld_data = fld_data.encode()
                value, = unpack('>l', fld_data)
            else:
                value = 0
            if ascii:
                if format != None:
                    if self.get_defid(format) == self.name2id('SelectDef'):
                        if not self.select_cache.has_key(format):
                            self.select_cache[format] = self.getlist(format, 'SELECT_DESCRIPTION')
                        try:
                            value = self.select_cache[format][value]
                        except (KeyError, IndexError):
                            value = ''

                else:
                    value = str(value)
        elif datatype == DT_CHAR:
            value = fld_data
        elif datatype == DT_SCHEDULE:
            if len(fld_data) == 8:
                value, = unpack('>d', fld_data)
            else:
                value = 0.0
            if ascii:
                value = self.time2ascii(value)
        elif datatype == DT_DOUBLE:
            if len(fld_data) == 8:
                value, = unpack('>d', fld_data)
            else:
                value = nan
            if ascii:
                if numpy.isnan(value):
                    value = 'nan'
                elif format == None or format < 0:
                    value = float2str(value)
                else:
                    fmt = '%%.%df' % format
                    value = fmt % value
        elif datatype == DT_RECORD:
            if len(fld_data) == 4:
                rid, = unpack('>I', fld_data)
            else:
                rid = 0
            if ascii:
                if rid == 0:
                    value = ''
                else:
                    value = self.rdb.hget(pkey('rec', rid), pfld(NAME))
                    if value is None:
                        value = ''
            else:
                value = rid
        elif datatype == DT_FIELD:
            if len(fld_data) == 8:
                rid, fid = unpack('>II', fld_data)
                idx = 0
            elif len(fld_data) == 12:
                rid, fid, idx = unpack('>III', fld_data)
            else:
                rid = 0
                fid = 0
                idx = 0
            if ascii:
                if rid == 0:
                    value = ''
                else:
                    rvalue = self.rdb.hget(pkey('rec', rid), pfld(NAME))
                    if rvalue is None:
                        return ''
                    if fid == self.VALUE_FT:
                        fvalue = 'VALUE'
                    else:
                        fvalue = self.rdb.hget(pkey('rec', fid), pfld(NAME))
                    if idx == 0:
                        value = '%s   %s' % (rvalue, fvalue)
                    else:
                        ivalue = self.rdb.hget(pkey('rec', idx), pfld(NAME))
                        value = '%s   %s   %s' % (rvalue, ivalue, fvalue)
            elif idx == 0:
                value = (rid, fid)
            else:
                value = (rid, fid, idx)
        elif datatype == DT_LIST:
            if len(fld_data) == 4:
                value, = unpack('>I', fld_data)
            else:
                value = 0
            if ascii:
                value = str(value)
        elif datatype == DT_DICTIONARY:
            if len(fld_data) == 4:
                value, = unpack('>I', fld_data)
            else:
                value = 0
            if ascii:
                value = str(value)
        elif datatype == DT_SPREADSHEET:
            if len(fld_data) == 4:
                value, = unpack('>I', fld_data)
            else:
                value = 0
            if ascii:
                value = str(value)
        elif datatype == DT_HISTORY:
            value, = unpack('>L', fld_data)
            if ascii:
                value = str(value)
        elif datatype == DT_CHISTORY:
            value = 0
            if ascii:
                value = str(value)
        elif datatype == DT_MATRIX:
            n = len(fld_data[2:]) / 8
            a = unpack('>LL%dd' % n, fld_data)
            if a[1] > 0:
                value = array(a[2:]).reshape(-1, a[1])
            else:
                return [[]]
        else:
            value = None
        return value

    def unpack_field_old(self, fld_data, datatype, format = None, ascii = False, columns = 1, record = None):
        if fld_data in (None, ''):
            if ascii:
                return ''
            else:
                return
        elif datatype == DT_TIMESTAMP:
            value, = unpack('>d', fld_data)
            if value != 0.0:
                value = self.unix2time(value)
            if ascii:
                value = self.time2ascii(value)
        elif datatype == DT_FLOAT:
            if len(fld_data) == 8:
                value, = unpack('>d', fld_data)
            else:
                value, = unpack('>f', fld_data)
            if ascii:
                if numpy.isnan(value):
                    value = '??????'
                else:
                    if record:
                        format = self.get(record, format)
                    if format == None or format < 0:
                        value = float2str(value)
                    else:
                        fmt = '%%.%df' % format
                        value = fmt % value
        elif datatype == DT_INTEGER:
            value, = unpack('>l', fld_data)
            if ascii:
                if format != None:
                    if self.get_defid(format) == self.name2id('SelectDef'):
                        if not self.select_cache.has_key(format):
                            self.select_cache[format] = self.getlist(format, 'SELECT_DESCRIPTION')
                        try:
                            value = self.select_cache[format][value]
                        except (KeyError, IndexError):
                            value = ''

                else:
                    value = str(value)
        elif datatype == DT_CHAR:
            value = fld_data
        elif datatype == DT_SCHEDULE:
            value, = unpack('>d', fld_data)
            if value != 0.0:
                value = self.unix2time(value)
            value = self.unix2time(value)
            if ascii:
                value = self.time2ascii(value)
        elif datatype == DT_DOUBLE:
            value, = unpack('>d', fld_data)
            if ascii:
                if numpy.isnan(value):
                    value = '??????'
                elif format == None or format < 0:
                    value = float2str(value)
                else:
                    fmt = '%%.%df' % format
                    value = fmt % value
        elif datatype == DT_RECORD:
            rid, = unpack('>H', fld_data)
            if ascii:
                if rid == 0:
                    value = ''
                else:
                    value = self.rdb.hget(pkey('rec', rid), pfld(NAME))
            else:
                value = rid
        elif datatype == DT_FIELD:
            if len(fld_data) == 8:
                rid, fid = unpack('>HH', fld_data)
                idx = 0
            else:
                rid, fid, idx = unpack('>HHH', fld_data)
            if ascii:
                if rid == 0:
                    value = ''
                else:
                    rvalue = self.rdb.hget(pkey('rec', rid), pfld(NAME))
                    fvalue = self.rdb.hget(pkey('rec', fid), pfld(NAME))
                    if idx == 0:
                        value = '%s   %s' % (rvalue, fvalue)
                    else:
                        ivalue = self.rdb.hget(pkey('rec', idx), pfld(NAME))
                        value = '%s   %s   %s' % (rvalue, ivalue, fvalue)
            elif idx == 0:
                value = (rid, fid)
            else:
                value = (rid, fid, idx)
        elif datatype == DT_LIST:
            value, = unpack('>H', fld_data)
            if ascii:
                value = str(value)
        elif datatype == DT_DICTIONARY:
            value, = unpack('>H', fld_data)
            if ascii:
                value = str(value)
        elif datatype == DT_SPREADSHEET:
            value, = unpack('>H', fld_data)
            if ascii:
                value = str(value)
        elif datatype == DT_HISTORY:
            value, = unpack('>L', fld_data)
            if ascii:
                value = str(value)
        elif datatype == DT_CHISTORY:
            value = 0
            if ascii:
                value = str(value)
        elif datatype == DT_MATRIX:
            n = len(fld_data[2:]) / 8
            a = unpack('>LL%dd' % n, fld_data)
            if a[1] > 0:
                value = array(a[2:]).reshape(-1, a[1])
                value = value.tolist()
            else:
                return [[]]
        else:
            value = None
        return value

    def pack_field(self, fld_data, datatype, format = None):
        if datatype == DT_FLOAT:
            if fld_data in (None, '', '?', '??????'):
                fld_data = numpy.nan
            if type(fld_data) == float:
                value = pack('>d', fld_data)
            elif type(fld_data) in (numpy.float32, numpy.float64):
                value = pack('>d', float(fld_data))
            elif type(fld_data) == int:
                value = pack('>d', float(fld_data))
            elif type(fld_data) == bool:
                value = pack('>d', float(fld_data))
            else:
                try:
                    fld_data = locale.atof(fld_data)
                except:
                    value = None
                else:
                    value = pack('>d', fld_data)

        elif datatype == DT_TIMESTAMP or datatype == DT_SCHEDULE:
            if type(fld_data) == str:
                if len(fld_data.replace(' ', '')) == 0:
                    fld_data = 0.0
                    value = pack('>d', fld_data)
                else:
                    fld_data = self.ascii2time(fld_data)
                    if fld_data == None:
                        value = None
                    else:
                        value = pack('>d', fld_data)
            else:
                if fld_data == None or numpy.isnan(fld_data):
                    fld_data = 0.0
                value = pack('>d', fld_data)
        elif datatype == DT_INTEGER:
            if type(fld_data) == str:
                if format != None and self.get_defid(format) == self.name2id('SelectDef'):
                    n = 1
                    value = 0
                    while True:
                        value = self.get(format, 'SELECT_DESCRIPTION', n)
                        if value == None:
                            fld_data = None
                            break
                        if value.lower() == fld_data.lower():
                            fld_data = n - 1
                            break
                        n += 1

                else:
                    try:
                        fld_data = int(fld_data)
                    except:
                        fld_data = None

            if fld_data != None:
                value = pack('>l', int(fld_data))
            else:
                value = None
        elif datatype == DT_CHAR:
            if fld_data == None:
                fld_data = ''
            value = str(fld_data)
        elif datatype == DT_DOUBLE:
            if fld_data == None:
                fld_data = numpy.nan
            if type(fld_data) == types.FloatType:
                value = pack('>d', fld_data)
            elif type(fld_data) == types.IntType:
                value = pack('>d', float(fld_data))
            else:
                try:
                    fld_data = locale.atof(fld_data)
                except:
                    value = None
                else:
                    value = pack('>d', fld_data)

        elif datatype == DT_RECORD:
            if type(fld_data) == types.StringType:
                if len(fld_data.replace(' ', '')) == 0:
                    rid = 0
                else:
                    rid = self.name2id(fld_data)
                if rid != None:
                    value = pack('>I', rid)
                else:
                    value = None
            elif fld_data == None:
                rid = 0
                value = pack('>I', rid)
            else:
                value = pack('>I', fld_data)
        elif datatype == DT_FIELD:
            if type(fld_data) == types.StringType:
                if len(fld_data.replace(' ', '')) == 0:
                    rid = 0
                    fid = 0
                    idx = 0
                    dtype = 1
                else:
                    parts = re.sub(' +', ' ', fld_data).split(' ')
                    if len(parts) == 3:
                        record = parts[0]
                        index = parts[1]
                        field = parts[2]
                        rid = self.name2id(record)
                        idx = self.name2id(index)
                        fid = self.name2id(field)
                    elif len(parts) == 2:
                        record = parts[0]
                        field = parts[1]
                        rid = self.name2id(record)
                        fid = self.name2id(field)
                        idx = 0
                    else:
                        rid = None
                        fid = None
                        idx = None
                    if rid != None:
                        did = self.get_defid(rid)
                        dtype = self.getdef(did, fid, DEF_DTYPE)
                    else:
                        dtype = None
                if rid != None and fid != None and idx != None and (dtype != None or did == 0):
                    if idx == 0:
                        value = pack('>II', rid, fid)
                    else:
                        value = pack('>III', rid, fid, idx)
                else:
                    value = None
            elif fld_data == None:
                rid = 0
                fid = 0
                value = pack('>II', rid, fid)
            elif len(fld_data) == 2:
                value = pack('>II', *fld_data)
            else:
                value = pack('>III', *fld_data)
        elif datatype == DT_LIST:
            if fld_data == None:
                fld_data = 0
            try:
                fld_data = int(fld_data)
            except:
                value = None
            else:
                value = pack('>I', fld_data)

        elif datatype == DT_DICTIONARY:
            if fld_data == None:
                fld_data = 0
            value = pack('>I', int(fld_data))
        elif datatype == DT_SPREADSHEET:
            if fld_data == None:
                fld_data = 0
            value = pack('>I', int(fld_data))
        elif datatype == DT_HISTORY:
            if fld_data == None:
                fld_data = 0
            value = pack('>L', int(fld_data))
        elif datatype == DT_CHISTORY:
            value = pack('>L', 0)
        elif datatype == DT_MATRIX:
            try:
                a = array(fld_data)
            except ValueError:
                value = None
            else:
                if len(a.shape) == 2:
                    value = pack(('>LL%dd' % a.size), *concatenate((a.shape, a.flatten())))
                else:
                    value = None
        return value

    def id2name(self, rid):
        if rid == self.VALUE_FT:
            return 'VALUE'
        return self.get(rid, NAME)

    def ids2names(self, rids):
        pipe = self.rdb.pipeline(transaction=False)
        for rid in rids:
            if rid == None:
                rid = 4294967295
            pipe.hget(pkey('rec', rid), pfld(self.NAME_FT))

        names = pipe.execute()
        return names

    def uid2name(self, uid):
        if len(uid) == 2:
            r, f = uid
            i = 0
        else:
            r, f, i = uid
        r = self.id2name(r)
        f = self.id2name(f)
        d = self.get_defid(r)
        if i == 0:
            i = ''
        else:
            repeat = self.getdef(d, f, DEF_REPEAT)
            if repeat != None:
                repeat_type = self.getdef(d, repeat, DEF_DTYPE)
                if repeat_type == DT_DICTIONARY:
                    i = self.id2name(i)
        return (r, f, i)

    def uid2tag(self, uid):
        if len(uid) == 2 or len(uid) == 3 and uid[2] == 0:
            r = self.id2name(uid[0])
            f = self.id2name(uid[1])
            if r != None and f != None:
                if f == 'VALUE':
                    return r
                else:
                    return '%s %s' % (r, f)
            else:
                return ''
        elif len(uid) == 3:
            r = self.id2name(uid[0])
            f = self.id2name(uid[1])
            k = self.id2name(uid[2])
            if r != None and f != None and k != None:
                if f == 'VALUE':
                    return '%s %s' % (r, k)
                else:
                    return '%s %s %s' % (r, f, k)
            else:
                return ''
        else:
            return ''
        return

    def tag2uid(self, tag):
        if isinstance(tag, tuple):
            parts = tag
        elif isinstance(tag, int):
            parts = [tag]
        else:
            parts = re.sub('  +', '~', tag).strip().split('~')
        if len(parts) == 1:
            r = self.name2id(parts[0])
            if r != None and self.is_field(r, self.VALUE_FT):
                return (r, self.VALUE_FT, 0)
            else:
                return
        elif len(parts) == 2:
            r = self.name2id(parts[0])
            if isinstance(parts[1], str) and parts[1].upper() == 'VALUE' and self.VALUE_FT != None:
                f = self.VALUE_FT
            else:
                f = self.name2id(parts[1])
            if r != None and f != None:
                return (r, f, 0)
            else:
                return
        elif len(parts) == 3:
            r = self.name2id(parts[0])
            f = self.name2id(parts[1])
            if r != parts[0] and isinstance(parts[2], int):
                k = int(parts[2])
            elif parts[2] == '':
                k = 0
            else:
                k = self.name2id(parts[2])
            if r != None and f != None and k != None:
                return (r, f, k)
            else:
                return
        else:
            return
        return

    def is_field(self, record, field, key = None):
        did = self.type(record)
        if did != None:
            if key != None:
                if isinstance(key, str):
                    dict_keys = [ k.upper() for k in self.list_keys(record, field, ascii=True) ]
                    key = key.upper()
                else:
                    dict_keys = self.list_keys(record, field)
                if key not in dict_keys:
                    return False
            return bool(self.getdef(did, field, DEF_DTYPE))
        else:
            return False
            return

    def exists(self, tag):
        if isinstance(tag, str):
            return self.name2id(tag) != None
        elif isinstance(tag, int):
            return self.id2name(tag) != None
        else:
            return False
            return None

    def name2id(self, name, use_cache = True):
        if isinstance(name, int):
            return name
        else:
            if type(name) == bytes:
                name = name.decode()
            if isinstance(name, str):
                name = name.upper()
                if use_cache:
                    if name in self.id_dict:
                        return self.id_dict[name]
                    if name in self.id_cache:
                        return self.id_cache[name]
                row = self.rdb.hget('name', name)
                if row:
                    recid, = unpack('>I', row)
                    self.id_cache[name] = recid
                    return recid
                else:
                    return
            elif isinstance(name, tuple):
                r, f, o = name
                r = self.name2id(r)
                f = self.name2id(f)
                if r == None or f == None:
                    return
                else:
                    return (r, f, o)
            else:
                return
            return

    def names2ids(self, names):
        if len(names) > 0 and isinstance(names[0], int):
            return names
        else:
            names = [ (name.upper() if isinstance(name, str) else name) for name in names ]
            try:
                return [ self.id_cache[n] for n in names ]
            except KeyError:
                pass

            pipe = self.rdb.pipeline(transaction=False)
            for name in names:
                pipe.hget('name', name)

            rows = pipe.execute()
            id_list = []
            for i, row in enumerate(rows):
                if row == None:
                    id_list.append(None)
                else:
                    rid, = unpack('>I', row)
                    id_list.append(rid)
                    self.id_cache[names[i]] = rid

            return id_list

    def mget(self, tags, field = None, text = False, ascii = False):
        if text:
            ascii = True
        if isinstance(field, list):
            return self.mget2(tags, field, ascii)
        elif type(tags) not in (list, tuple):
            return
        elif len(tags) == 0:
            return []
        else:
            if field == None:
                field = self.VALUE_FT
            if isinstance(tags[0], str):
                rids = self.names2ids(tags)
            else:
                rids = tags
            if isinstance(field, str):
                fid = self.name2id(field)
                if fid == None:
                    return
            else:
                fid = field
            if not self._pps_query(None, P_WRITE) and fid == self.PASSWORD_FT:
                if ascii:
                    return [''] * len(tags)
                else:
                    return [None] * len(tags)
            if fid == self.VALUE_FT:
                values = self.last_h_value(rids)
                if ascii:
                    values = [ (float2str(v) if type(v) in (float,
                     float16,
                     float32,
                     float64) else (str(v) if v != None else '')) for v in values ]
                return values
            did = self.get_defid(rids[0])
            if fid == self.TIME_FT and (did in (self.ANALOG_DEF, self.DISCRETE_DEF) or (did, self.VALUE_FT) in self.custom_history_fields):
                return self.last_h_time(rids, ascii=ascii)
            elif fid in self.extra_history_fields or (did, fid) in self.custom_history_fields:
                tags = [ (r, fid) for r in rids ]
                values = self.last_h_value(tags)
                if ascii:
                    values = [ (float2str(v) if type(v) in (float,
                     float16,
                     float32,
                     float64) else (str(v) if v != None else '')) for v in values ]
                return values
            dtype = self.getdef(did, fid, DEF_DTYPE)
            format = self.getdef(did, fid, DEF_FORMAT)
            pipe = self.rdb.pipeline(transaction=False)
            for rid in rids:
                if rid == None:
                    rid = 4294967295
                pipe.hget(pkey('rec', rid), pfld(fid, 0))

            rows = pipe.execute()
            value_list = []
            for row in rows:
                value = self.unpack_field(row, dtype, format=format, ascii=ascii)
                value_list.append(value)

            if self.unicode_mode and fid in self.unicode_fields:
                value_list = [ decode_u_str(v) for v in value_list ]
            return value_list

    def mget_sql(self, rids, fids):
        return self.mget2(rids, fids, sql=True)

    def mget2(self, rids, fids, ascii = False, sql = False):
        if len(rids) == 0:
            return []
        else:
            if type(rids[0]) == bytes:
                rids = [rids[0].decode()]
            if isinstance(rids[0], str):
                rids = self.names2ids(rids)
            if isinstance(fids[0], str):
                fids = self.names2ids(fids)
            fids = [ (4294967295 if f is None else f) for f in fids ]
            did = self.get_defid(rids[0])
            hids = {}
            dtypes = {}
            formats = {}
            for fid in fids:
                if fid in self.history_fields or fid == self.TIME_FT or (did, fid) in self.custom_history_fields:
                    if fid == self.TIME_FT:
                        uids = [ (r, self.VALUE_FT, 0) for r in rids ]
                    else:
                        uids = [ (r, fid, 0) for r in rids ]
                    hids[fid] = self.tags2hids(uids)
                    hids[fid] = [ (4294967295 if h is None else h.hid) for h in hids[fid] ]
                else:
                    dtypes[fid] = self.getdef(did, fid, DEF_DTYPE)
                    formats[fid] = self.getdef(did, fid, DEF_FORMAT)
            pipe = self.rdb.pipeline(transaction=False)
            for i, rid in enumerate(rids):
                for fid in fids:
                    if fid in self.history_fields or fid == self.TIME_FT or (did, fid) in self.custom_history_fields:
                        pipe.lindex(pkey('hq', hids[fid][i]), -1)
                    else:

                        pipe.hget(pkey('rec', rid), pfld(fid, 0))
            datas = []
            data = pipe.execute()
            for i,d in enumerate(data):
                if d != None:
                    datas.append(d.decode())
                else:
                    datas.append(d)
            rows = iter(datas)
            values = []
            values_list = []
            for rid in rids:
                values = []
                for fid in fids:
                    # next() --> __next__() renamed
                    row = rows.__next__()
                    if row == None:
                        val = '' if ascii or sql else None
                    elif fid in self.history_fields or (did, fid) in self.custom_history_fields:
                        ts, vs = self.unpack_h_block(row)
                        if len(vs) > 0:
                            val = vs[-1]
                    elif fid == self.TIME_FT:
                        ts, vs = self.unpack_h_block(row)
                        if len(ts) > 0:
                            val = ts[-1]
                        else:
                            val = None
                        if sql or ascii:
                            val = self.time2ascii(val)
                    else:
                        if sql:
                            ascii = False if dtypes[fid] in (DT_FLOAT,
                             DT_DOUBLE,
                             DT_INTEGER,
                             DT_LIST,
                             DT_DICTIONARY) and formats[fid] == None else True
                        val = self.unpack_field(row, dtypes[fid], format=formats[fid], ascii=ascii)
                    values.append(val)

                values_list.append(values)

            if not self._pps_query(None, P_WRITE) and self.PASSWORD_FT in fids:
                j = fids.index(self.PASSWORD_FT)
                blank = '' if ascii else None
                for i in range(len(values_list)):
                    values_list[i][j] = blank

            return values_list

    def mget3(self, rid, fids, h_fids = [], text = False):
        if isinstance(rid, str):
            rid = self.name2id(rid)
        if rid == None:
            return
        else:
            if isinstance(fids[0], str):
                fids = self.names2ids(fids)
            if len(h_fids) > 0:
                if isinstance(h_fids[0], str):
                    h_fids = self.names2ids(h_fids)
                if self.VALUE_FT in h_fids:
                    h_fids.append(self.TIME_FT)
            h_uids = [ (rid, fid, 0) for fid in fids if fid in h_fids ]
            hids = []
            for uid in h_uids:
                if uid[1] == self.TIME_FT:
                    hid = self.tag2hid((uid[0], self.VALUE_FT, 0))
                else:
                    hid = self.tag2hid(uid)
                hids.append(hid)

            did = self.type(rid)
            def_dict = self.mgetdef(did, fids, [DEF_DTYPE, DEF_FORMAT])
            pipe = self.rdb.pipeline(transaction=False)
            i = 0
            for fid in fids:
                if fid in h_fids:
                    pipe.lindex(pkey('hq', hids[i].hid), -1)
                    i += 1
                else:
                    pipe.hget(pkey('rec', rid), pfld(fid, 0))

            rows = pipe.execute()
            values = []
            for fid, row in zip(fids, rows):
                if row == None:
                    val = '' if text else None
                elif fid in h_fids:
                    if fid == self.TIME_FT:
                        ts, vs = self.unpack_h_block(row)
                        if len(ts) > 0:
                            val = ts[-1]
                        else:
                            val = None
                        if text:
                            val = self.time2str(val)
                    else:
                        ts, vs = self.unpack_h_block(row)
                        if len(vs) > 0:
                            val = vs[-1]
                        if text:
                            if issubdtype(val.dtype, numpy.float) or issubdtype(val.dtype, numpy.int):
                                format = def_dict[fid][DEF_FORMAT]
                                if did == self.ANALOG_DEF and issubdtype(val.dtype, numpy.float) or did == self.DISCRETE_DEF and issubdtype(val.dtype, numpy.int):
                                    if format:
                                        format = self.get(rid, format)
                                    else:
                                        format = None
                                else:
                                    format = None
                                val = self.format_value_hist(val, format)
                            else:
                                val = str(val)
                else:
                    dtype = def_dict[fid][DEF_DTYPE]
                    format = def_dict[fid][DEF_FORMAT]
                    val = self.unpack_field(row, dtype, format=format, ascii=text)
                if self.unicode_mode and fid in self.unicode_fields:
                    val = decode_u_str(val)
                values.append(val)

            if not self._pps_query(None, P_WRITE) and self.PASSWORD_FT in fids:
                i = fids.index(self.PASSWORD_FT)
                blank = '' if text else None
                values[i] = blank
            return values

    def key2idx(self, key, add_keys = False):
        if isinstance(key, str):
            idx = self.name2id(key)
            if idx == None and add_keys:
                self.add(key, FIELD_DEF)
                idx = self.name2id(key)
            return idx
        else:
            return key
            return

    def del_key(self, tag, field = None, key = None):
        try:
            if not self._pps_query(None, P_WRITE):
                return False
            if field == None:
                uid = self.tag2uid(tag)
                if uid == None:
                    return
                rid, fid, kid = uid
            else:
                rid = self.name2id(tag)
                fid = self.name2id(field)
                kid = self.key2idx(key)
                if rid == None or fid == None or kid == None:
                    return
            ok = self.rdb.hdel(pkey('rec', rid), pfld(fid, kid))
            self.putref((rid, fid, kid), None)
            return ok
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def list_keys(self, tag, field = None, text = False, ascii = False):
        if text:
            ascii = True
        if field == None:
            uid = self.tag2uid(tag)
            if uid == None:
                return
            rid, fid, kid = uid
        else:
            rid = self.name2id(tag)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return []
        did = self.get_defid(rid)
        rfid = self.getdef(did, fid, DEF_REPEAT)
        repeat_type = self.getdef(did, rfid, DEF_DTYPE)
        found_keys = []
        for k in self.rdb.hkeys(pkey('rec', rid)):
            f, o = ufld(k)
            if f == fid and o != 0:
                found_keys.append(o)

        if ascii:
            found_keys = self.ids2names(found_keys)
        if repeat_type == DT_SPREADSHEET:
            order_dict = {}
            for k in found_keys:
                kid = self.name2id(k)
                data = self.rdb.hget(pkey('order', rid), pfld(rfid, kid))
                if data != None:
                    order, = unpack('>I', data)
                else:
                    order = 9999
                order_dict[k] = order

            found_keys = sorted(order_dict, key=order_dict.__getitem__)
        else:
            found_keys.sort()
            found_keys = [ k for k in found_keys if k != None ]
        return found_keys

    def list_fields(self, definition, repeat = None, text = False, ascii = False):
        if text:
            ascii = True
        if repeat not in (None, 0):
            repeat = self.name2id(repeat)
        did = self.name2id(definition)
        if did == None:
            return
        else:
            if self.get_defid(did) != DEFINITION_DEF:
                did = self.get_defid(did)
            if (did, repeat) in self._list_fields_cache:
                fields = self._list_fields_cache[did, repeat]
                if ascii:
                    fields = self.ids2names(fields)
                return fields
            rows = []
            fids = []
            for k in self.rdb.hkeys(pkey('def', did)):
                fid, pid = ufld(k)
                rows.append((fid, pid))
                fids.append(fid)

            def_dict = self.mgetdef(did, fids, [DEF_ORDER, DEF_REPEAT])
            fields = []
            for fid, pid in rows:
                if pid == DEF_DTYPE:
                    order = def_dict[fid][DEF_ORDER]
                    found_repeat = def_dict[fid][DEF_REPEAT]
                    if repeat == 0 and found_repeat != None:
                        continue
                    if repeat in (None, 0) or found_repeat == repeat:
                        fields.append((fid, order))

            fields.sort(key=operator.itemgetter(1))
            fields = [ i for i, j in fields ]
            self._list_fields_cache[did, repeat] = fields
            if ascii:
                fields = self.ids2names(fields)
            return fields

    def lsname_alt(self, definition = None, ascii = True):
        if definition != None:
            did = self.name2id(definition)
        else:
            did = 0
        name_list = []
        for v in self.rdb.hvals('name'):
            rid, = unpack('>I', v)
            if did != 0:
                if self.get_defid(rid) != did:
                    continue
            if ascii:
                name = self.id2name(rid)
                name_list.append(name)
            else:
                name_list.append(rid)

        return name_list

    def _lsname(self, definition = None, search = None, desc_search = None, ascii = True):
        if definition != None:
            did = self.name2id(definition)
            if did == None:
                return []
        else:
            did = 0
        if definition == None:
            k = 'name2'
        else:
            k = pkey('sdef', did)
        if ascii:
            if search and desc_search:
                k = pkey('desc', did)
                cur = 0
                tag_list = []
                if search.count('*') == 0:
                    search = '*' + search + '*'
                if desc_search.count('*') == 0:
                    desc_search = '*' + desc_search + '*'
                search = no_case_pattern(search) + '\x00' + no_case_pattern(desc_search)
                while True:
                    cur, hdict = self.rdb.hscan(k, cursor=cur, match=search, count=10000)
                    tag_list += hdict.values()
                    if cur == 0:
                        break

                tag_list.sort()
            elif search:
                cur = 0
                tag_list = []
                if search.count('*') == 0:
                    search = '*' + search + '*'
                search = no_case_pattern(search)
                while True:
                    cur, hdict = self.rdb.hscan(k, cursor=cur, match=search, count=10000)
                    tag_list += hdict.keys()
                    if cur == 0:
                        break

                tag_list.sort()
            elif desc_search:
                k = pkey('desc', did)
                cur = 0
                tag_list = []
                if desc_search.count('*') == 0:
                    desc_search = '*' + desc_search + '*'
                search = '*\x00' + no_case_pattern(desc_search)
                while True:
                    cur, hdict = self.rdb.hscan(k, cursor=cur, match=search, count=10000)
                    tag_list += hdict.values()
                    if cur == 0:
                        break

                tag_list.sort()
            else:
                tag_list = self.rdb.hkeys(k)
                tag_list.sort()
        else:
            tag_list = []
            for v in self.rdb.hvals(k):
                rid, = unpack('>I', v)
                tag_list.append(rid)

        return tag_list

    def lsname(self, definition = None, search = None, desc_search = None, ascii = True):
        if definition != None:
            did = self.name2id(definition)
            if did == None:
                return []
        if definition == None or self.get_defid(did) == DEFINITION_DEF:
            return self._lsname(definition, search, desc_search, ascii=ascii)
        elif self.get_defid(did) == self.FOLDER_DEF:
            name_list = []
            num_tags = self.get(did, '#RECORDS')
            for i in range(num_tags):
                name = self.get(did, 'RECORD_NAME', i + 1, ascii=ascii)
                if name == None or name == '':
                    continue
                name_list.append(name)

            return name_list
        elif self.get_defid(did) == self.name2id('ViewDef'):
            return self._gen_view_data(definition, search=search, desc_search=desc_search)
        elif self.get_defid(did) == self.name2id('FolderViewDef'):
            view_rec = self.get(definition, 'view_record')
            return self._gen_view_data(view_rec, search=search, desc_search=desc_search)
        else:
            return []
            return

    list_tags = lsname

    def mput(self, tags, fields, rows, notify = True):
        try:
            if not isinstance(tags, list) or not isinstance(fields, list) or not isinstance(rows, list):
                return False
            if len(rows) > 0 and type(rows[0]) not in (list, tuple):
                return False
            if len(tags) != len(rows) or len(fields) != len(rows[0]):
                return False
            rids = self.names2ids(tags)
            fids = self.names2ids(fields)
            if rids.count(None) > 0 or fids.count(None) > 0:
                return False
            did = self.type(rids[0])
            def_dict = self.mgetdef(did, fids, [DEF_DTYPE, DEF_FORMAT])
            if not self._pps_query(did, P_WRITE, rids[0]):
                return False
            uid_list = []
            in_list = []
            ref_list = []
            pipe = self.rdb.pipeline(transaction=False)
            for rid, row in zip(rids, rows):
                key = pkey('rec', rid)
                for fid, value in zip(fids, row):
                    dtype = def_dict[fid][DEF_DTYPE]
                    if dtype == None:
                        continue
                    format = def_dict[fid][DEF_FORMAT]
                    data = self.pack_field(value, dtype, format)
                    pipe.hset(key, pfld(fid, 0), data)
                    uid_list.append((rid, fid, 0))
                    if dtype in (DT_RECORD, DT_FIELD):
                        in_list.append((rid, fid, 0))
                        ref_list.append(value)

            n = pipe.execute()
            if notify:
                self.send_events(uid_list)
            if len(ref_list) > 0:
                if isinstance(ref_list[0], str):
                    ref_list = self.names2ids(ref_list)
                ref_tuples = zip(in_list, ref_list)
                self.putrefs(ref_tuples)
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def get_all(self, tag, area = 0, text = False):
        rid = self.name2id(tag)
        if rid == None:
            return
        else:
            fids = self.list_fields(tag, area)
            fields = self.ids2names(fids)
            did = self.type(rid)
            dtype_dict = self.mgetdef(did, fids, [DEF_DTYPE])
            format = None
            k = pkey('rec', rid)
            if area:
                count = self.get(rid, area)
                if count == 0:
                    return []
                flds = [ pfld(fid, i + 1) for i in range(count) for fid in fids ]
                rows = self.rdb.hmget(k, flds)
                values = []
                i = 0
                for idx in range(count):
                    row_dict = {}
                    for field, fid in zip(fields, fids):
                        data = rows[i]
                        dtype = dtype_dict[fid][DEF_DTYPE]
                        value = self.unpack_field(data, dtype, format=format, ascii=text)
                        row_dict[field] = value
                        i += 1

                    values.append(row_dict)

            else:
                flds = [ pfld(fid, 0) for fid in fids ]
                rows = self.rdb.hmget(k, flds)
                values = {}
                for field, fid, data in zip(fields, fids, rows):
                    dtype = dtype_dict[fid][DEF_DTYPE]
                    value = self.unpack_field(data, dtype, format=format, ascii=text)
                    values[field] = value

            return values

    def get_dict_old(self, tag, field = None, text = True, ascii = True):
        if not text:
            ascii = False
        if isinstance(tag, tuple):
            return dict([ (k, self.get((tag[0], tag[1], k), ascii=ascii)) for k in self.list_keys(tag, ascii=ascii) ])
        elif field != None:
            return dict([ (k, self.get(tag, field, k, ascii=ascii)) for k in self.list_keys(tag, field, ascii=ascii) ])
        else:
            return self.rec2dict(tag, ascii=ascii)
            return

    def get_dict(self, tag, field = None, text = True, ascii = True):
        if not text:
            ascii = False
        if field == None:
            return self.rec2dict(tag, ascii=ascii)
        else:
            rid = self.name2id(tag)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return
            did = self.get_defid(rid)
            dtype = self.getdef(did, fid, DEF_DTYPE)
            format = self.getdef(did, fid, DEF_FORMAT)
            kid_list = self.list_keys(rid, fid, ascii=False)
            if ascii:
                keys = self.ids2names(kid_list)
            else:
                keys = kid_list
            pipe = self.rdb.pipeline(transaction=False)
            for kid in kid_list:
                pipe.hget(pkey('rec', rid), pfld(fid, kid))

            rows = pipe.execute()
            value_dict = {}
            for k, row in zip(keys, rows):
                value = self.unpack_field(row, dtype, format=format, ascii=ascii)
                value_dict[k] = value

            if self.unicode_mode and fid in self.unicode_fields:
                value_dict = {k:decode_u_str(v) for k, v in value_dict}
            return value_dict

    def select(self, tag, ascii = True):
        return [ Tag(self, t, ascii) for t in self.getlist(tag) ]

    def select2(self, tag, fields = [], ascii = True):
        tags = self.getlist(tag, ascii)
        if len(fields) > 0:
            rows = []
            for t in tags:
                row = []
                for f in fields:
                    v = self.get(t, f)
                    row.append(v)

                rows.append(row)

            return rows
        else:
            return tags

    def dselect(self, tag, fields = [], ascii = True):
        tags = self.getlist(tag, ascii)
        if len(fields) > 0:
            rows = []
            for t in tags:
                row = {}
                for f in fields:
                    v = self.get(t, f)
                    row[f] = v

                rows.append(row)

        else:
            rows = []
            for t in tags:
                d = self.rec2dict(t)
                rows.append(d)

        return rows

    def get_list(self, record = None, field = None, search = None, desc_search = None, regex_search = None, text = True, ascii = True, sql = False):
        if not text:
            ascii = False
        if search is not None and search.strip() in ('*', ''):
            search = None
        values = []
        if isinstance(record, tuple):
            uid = self.tag2uid(record)
            if uid == None:
                return
            record, field, idx = uid
            if idx != 0:
                return

        definition = self.get_defid(record, True)

        if definition != None:
            definition = definition.decode()
        if definition == 'DefinitionDef' or record == None:
            values = self.lsname(record, search=search, desc_search=desc_search, ascii=ascii)
        elif definition == 'AssetDef':
            record = self.get(record, 'ASSET_TEMPLATE')
            if record is None:
                return []
            values = self.list_keys(record, ascii=True)
        elif definition == 'AssetTemplateDef':
            values = self.list_keys(record, ascii=True)
        elif definition == 'FolderViewDef':
            view = self.get(record, 'view_record')
            values = self._gen_view_data(view, search=search, desc_search=desc_search, ascii=ascii)
        elif definition == 'ViewDef' and field == None:
            values = self._gen_view_data(record, search=search, desc_search=desc_search, ascii=ascii)
        elif definition == 'FolderDef' and field == None:
            field = 'RECORD_NAME'
        if isinstance(field, list) or isinstance(field, tuple):
            rows = []
            for f in field:
                values = self.getlist(record, f, search=search, desc_search=desc_search, ascii=ascii)
                rows.append(values)

            values = zip(*rows)
        else:
            did = self.name2id(definition)
            repeat = self.getdef(did, field, DEF_REPEAT)
            if repeat != None:
                dtype = self.getdef(did, repeat, DEF_DTYPE)
                if dtype == DT_LIST:
                    n = self.get(record, repeat)
                    if n == None:
                        n = 0
                    rid = self.name2id(record)
                    fid = self.name2id(field)
                    dtype = self.getdef(did, fid, DEF_DTYPE)
                    format = self.getdef(did, fid, DEF_FORMAT)
                    pipe = self.rdb.pipeline(transaction=False)
                    for i in range(1, n + 1):
                        pipe.hget(pkey('rec', rid), pfld(fid, i))

                    rows = pipe.execute()
                    for row in rows:
                        if sql:
                            ascii = False if dtype in (DT_FLOAT,
                             DT_DOUBLE,
                             DT_INTEGER,
                             DT_LIST,
                             DT_DICTIONARY) and format == None else True
                        value = self.unpack_field(row, dtype, format=format, ascii=ascii)
                        values.append(value)

                    if self.unicode_mode and fid in self.unicode_fields:
                        values = [ decode_u_str(v) for v in values ]
                elif dtype == DT_DICTIONARY:
                    values = sorted(self.get_dict(record, field).items())
        if search or regex_search:
            if ascii:
                if regex_search:
                    try:
                        values = [ t for t in values if regex(t, regex_search) ]
                    except:
                        values = []

                else:
                    values = [ t for t in values if wildcard_match(t, search, sql) ]
            else:
                values = []
        # values = [i.decode() for i in values if type(i) == bytes]
        return values

    def getlist2(self, record, field = None, ascii = True):
        if isinstance(record, list):
            definition = self.get_defid(record[0])
            records = record
        else:
            definition = self.get_defid(record, True)
            if definition == 'DefinitionDef':
                records = self.lsname(record, ascii=ascii)
            elif definition == 'FolderViewDef':
                view = self.get(record, 'view_record')
                records = self._gen_view_data(view)
            elif definition == 'ViewDef' and field == None:
                records = self._gen_view_data(record)
            elif definition == 'FolderDef':
                records = [record]
                field = 'RECORD_NAME'
            elif self.name2id(record):
                records = [record]
            else:
                return []
            if len(records) > 0:
                definition = self.get_defid(records[0])
            else:
                return []
        if field == None:
            return records
        else:
            if isinstance(field, list):
                fields = field
            else:
                fields = [field]
            repeat_fields = [ self.name2id(f) for f in fields if self.getdef(definition, f, DEF_REPEAT) ]
            if len(repeat_fields) > 0:
                repeat = self.getdef(definition, repeat_fields[0], DEF_REPEAT)
                rows = []
                for r in records:
                    n = self.get(r, repeat)
                    for i in range(1, n + 1):
                        values = []
                        for f in fields:
                            if self.name2id(f) in repeat_fields:
                                v = self.get(r, f, i, ascii=ascii)
                            else:
                                v = self.get(r, f, ascii=ascii)
                            if isinstance(field, list):
                                values.append(v)
                            else:
                                values = v

                        rows.append(values)

                return rows
            if isinstance(field, list):
                return [ [ self.get(r, f, ascii=ascii) for f in field ] for r in records ]
            return [ self.get(r, field, ascii=ascii) for r in records ]
            return

    def put_list(self, tag, value_list, notify = False):
        try:
            if isinstance(tag, str):
                if self.get_defid(tag) == self.FOLDER_DEF:
                    tag = (tag, 'RECORD_NAME')
            uid = self.tag2uid(tag)
            if uid == None:
                return False
            rid, fid, idx = uid
            if idx != 0:
                return False
            did = self.get_defid(rid)
            repeat = self.getdef(did, fid, DEF_REPEAT)
            if repeat == None:
                return False
            if not self._pps_query(did, P_WRITE, rid):
                return False
            key = pkey('rec', rid)
            dtype = self.getdef(did, fid, DEF_DTYPE)
            format = self.getdef(did, fid, DEF_FORMAT)
            old_count = self.get(rid, repeat)
            new_count = len(value_list)
            self.put(rid, repeat, new_count, notify=notify)
            in_list = []
            ref_list = []
            put_uids = []
            pipe = self.rdb.pipeline(transaction=False)
            for i, value in enumerate(value_list):
                data = self.pack_field(value, dtype, format)
                pipe.hset(key, pfld(fid, i + 1), data)
                if dtype in (DT_RECORD, DT_FIELD):
                    in_list.append((rid, fid, i + 1))
                    ref_list.append(value)
                put_uids.append((rid, fid, i + 1))

            pipe.execute()
            if notify:
                self.send_events(put_uids)
                if new_count < old_count:
                    del_uids = [ (rid, fid, i) for i in range(new_count + 1, old_count + 1) ]
                    self.send_events(del_uids)
            if len(ref_list) > 0:
                if isinstance(ref_list[0], str):
                    ref_list = self.names2ids(ref_list)
                ref_tuples = zip(in_list, ref_list)
                self.putrefs(ref_tuples)
            return True
        except redis.exceptions.ReadOnlyError:
            return False

        return

    def put_dict(self, record, field, value_dict):
        rid = self.name2id(record)
        fid = self.name2id(field)
        if rid == None or fid == None or not isinstance(value_dict, dict):
            return False
        else:
            did = self.type(rid)
            dtype = self.getdef(did, fid, DEF_DTYPE)
            format = self.getdef(did, fid, DEF_FORMAT)
            if not self._pps_query(did, P_WRITE, rid):
                return False
            repeat = self.getdef(did, fid, DEF_REPEAT)
            if repeat == None:
                return False
            repeat_type = self.getdef(did, repeat, DEF_DTYPE)
            if repeat_type != DT_DICTIONARY:
                return False
            keys = value_dict.keys()
            values = value_dict.values()
            idxs = self.names2ids(keys)
            new_keys = [ key for key, idx in zip(keys, idxs) if idx == None ]
            self.add(new_keys, FIELD_DEF)
            idxs = self.names2ids(keys)
            pipe = self.rdb.pipeline(transaction=False)
            key = pkey('rec', rid)
            for idx in self.list_keys(rid, fid):
                pipe.hdel(key, pfld(fid, idx))

            key_refs = []
            in_list = []
            ref_list = []
            for idx, value in zip(idxs, values):
                data = self.pack_field(value, dtype, format)
                if data == None:
                    return False
                pipe.hset(key, pfld(fid, idx), data)
                key_refs.append(((rid, fid, idx), idx))
                if dtype in (DT_RECORD, DT_FIELD):
                    in_list.append((rid, fid, idx))
                    ref_list.append(value)

            pipe.execute()
            self.putrefs(key_refs)
            if len(ref_list) > 0:
                if isinstance(ref_list[0], str):
                    ref_list = self.names2ids(ref_list)
                ref_tuples = zip(in_list, ref_list)
                self.putrefs(ref_tuples)
            return True

    def lsrec(self, record, area = 0, ascii = False):
        if area != 0:
            area = self.name2id(area)
        rid = self.name2id(record)
        if rid == None:
            return []
        did = self.get_defid(rid)
        if did == None:
            return []
        if did == DEFINITION_DEF:
            did = rid
        fields = []
        for k in self.rdb.hkeys(pkey('def', did)):
            fid, pid = ufld(k)
            if pid == DEF_DTYPE:
                order = self.getdef(did, fid, DEF_ORDER)
                found_repeat = self.getdef(did, fid, DEF_REPEAT)
                if found_repeat == None:
                    found_repeat = 0
                if found_repeat == area:
                    fields.append((fid, order))

        fields.sort(key=operator.itemgetter(1))
        fields = [ i for i, j in fields ]
        values = self.mget2([rid], fields, ascii=ascii)[0]
        names = self.ids2names(fields)
        fdata = []
        for i, f in enumerate(fields):
            name = names[i]
            dtype = self.getdef(did, f, DEF_DTYPE)
            fmt = self.getdef(did, f, DEF_FORMAT)
            skey = self.getdef(did, f, DEF_SKEY)
            if fmt != None and dtype == DT_INTEGER:
                states = self.get_states(rid, f)
            elif skey != None:
                states = None
            else:
                states = None
            if area == 0:
                value = values[i]
            else:
                value = None
            fdata.append((name,
             0,
             value,
             dtype,
             states))

        if area != 0:
            repeat_type = self.getdef(did, area, DEF_DTYPE)
            if repeat_type in (DT_DICTIONARY, DT_SPREADSHEET):
                occ_list = self.list_keys(rid, fdata[0][0], ascii=True)
            else:
                if repeat_type == DT_HISTORY:
                    return fdata
                n = self.get(rid, area)
                if n == None:
                    n = 0
                occ_list = range(1, n + 1)
            rdata = []
            for name, occ, value, dtype, states in fdata:
                n = self.get(rid, area)
                for occ in occ_list:
                    value = self.get(rid, name, occ, ascii)
                    rdata.append((name,
                     occ,
                     value,
                     dtype,
                     states))

            return rdata
        else:
            return fdata

    def tag2dict(self, tag, area = 0, ascii = False):
        return self.rec2dict(tag, area, ascii)

    def rec2dict(self, record, area = 0, ascii = False):
        rid = self.name2id(record)
        if rid == None:
            return {}
        elif area == 0:
            return dict([ (x[0], x[2]) for x in self.lsrec(rid, area, ascii) ])
        else:
            values_dict = {}
            fields = self.list_fields(rid, area, ascii=True)
            if len(fields) == 0:
                return []
            for f in fields:
                values_dict[f] = self.getlist(record, f, ascii=ascii)

            n = len(values_dict[fields[0]])
            return [ dict([ (f, values_dict[f][i]) for f in fields ]) for i in range(n) ]
            return

    def show(self, tag, area = None, search = None):
        rid = self.name2id(tag)
        if rid == None:
            return
        else:
            if area == None:
                did = self.get_defid(rid)
                if did in (self.FOLDER_DEF,
                 self.USER_FOLDER_DEF,
                 self.FOLDER_VIEW_DEF,
                 DEFINITION_DEF):
                    print ('\n'.join(self.getlist(rid, search=search)))
                else:
                    for f in self.lsrec(rid, ascii=True):
                        fname = f[0]
                        value = f[2]
                        ftype = f[3]
                        fid = self.name2id(fname)
                        if self.getdef(did, fid, DEF_HIDDEN) == 1:
                            continue
                        if ftype == DT_DICTIONARY:
                            value = self.get(rid, fid)
                        has_history = self.get_h_cfg((rid, fid)) or did == self.CALCULATION_DEF and fid == self.VALUE_FT
                        if has_history or did in (self.ANALOG_DEF, self.DISCRETE_DEF) and fid == self.TIME_FT:
                            value = self.get(rid, fid, ascii=True)
                        if search != None and not glob.fnmatch.fnmatch(fname, search):
                            continue
                        if has_history or ftype in (DT_LIST, DT_DICTIONARY):
                            print ('%-20s -> %s' % (fname, value))
                        elif fname == 'CODE':
                            print ('%s\n%s' % (fname, value))
                        else:
                            print ('%-20s    %s' % (fname, value))

            else:
                aid = self.name2id(area)
                if aid == None:
                    return
                did = self.get_defid(rid)
                hid = self.tag2hid((rid, aid))
                area_type = self.type(rid, aid)
                if hid or did == self.CALCULATION_DEF and aid == self.VALUE_FT:
                    print (self.get_series((rid, aid), maxlen=-20))
                elif area_type == DT_LIST:
                    fields = self.list_fields(rid, aid, ascii=True)
                    widths = []
                    for f in fields:
                        values = self.get_list(rid, f, ascii=True)
                        values = [f] + values
                        w = max([ len(v) for v in values ])
                        widths.append(w + 2)

                    line = 'INDEX  '
                    for f, w in zip(fields, widths):
                        line += '%-*s' % (w, f)

                    line = '-----  '
                    for w in widths:
                        line += '%-*s' % (w, '-' * (w - 2))

                    for i, row in enumerate(self.get_list(rid, fields)):
                        if search != None and not glob.fnmatch.fnmatch(row[0], search):
                            continue
                        line = '%-7s' % str(i + 1)
                        for j, value in enumerate(row):
                            line += '%-*s' % (widths[j], value)


                elif area_type == DT_DICTIONARY:
                    fields = self.list_fields(did, aid, ascii=True)
                    column_dict = {}
                    widths = []
                    keys = []
                    k_width = 0
                    for i, f in enumerate(fields):
                        d = self.get_dict(rid, f, ascii=True)
                        if i == 0:
                            keys = d.keys()
                            k_width = max([ len(k) for k in d.keys() ]) + 2
                        w = max([ len(v) for v in d.values() + [f] ])
                        column_dict[f] = d
                        widths.append(w + 2)

                    line = '%-*s' % (k_width, 'KEY')
                    for i, f in enumerate(fields):
                        line += '%-*s' % (widths[i], f)

                    line = '%-*s' % (k_width, '-' * (k_width - 2))
                    for w in widths:
                        line += '%-*s' % (w, '-' * (w - 2))

                    for i, k in enumerate(sorted(keys, key=str.upper)):
                        if search != None and not glob.fnmatch.fnmatch(k, search):
                            continue
                        line = '%-*s' % (k_width, k)
                        for j, f in enumerate(fields):
                            line += '%-*s' % (widths[j], column_dict[f][k])

            return

    def slice2bools(self, record, times):
        rid = self.name2id(record)
        if rid == None:
            return
        else:
            bools = numpy.zeros(len(times), dtype=numpy.bool)
            for start, end in self.getlist(rid, ['START_TIME', 'END_TIME'], ascii=False):
                bools |= (start <= times) & (times <= end)

            return bools

    def get_states(self, record, field = None):
        if field == None:
            uid = self.tag2uid(record)
            if uid == None:
                return
            rid, fid, idx = uid
        else:
            rid = self.name2id(record)
            fid = self.name2id(field)
            if rid == None or fid == None:
                return
        did = self.get_defid(rid)
        if did == 0:
            did = rid
        fid = self.getdef(did, fid, DEF_FORMAT)
        if fid and self.get_defid(fid) == FIELD_DEF:
            if self.getdef(did, fid, DEF_DTYPE) != DT_RECORD:
                return
            fid = self.get(rid, fid)
            if fid == 0:
                fid = None
        if fid == None:
            return
        else:
            states = self.getlist(fid, 'SELECT_DESCRIPTION')
            return states
            return

    def format_selector(self, value, format):
        if not self.select_cache.has_key(format):
            self.select_cache[format] = self.getlist(format, 'SELECT_DESCRIPTION')
        try:
            value = self.select_cache[format][value]
        except (KeyError, IndexError):
            value = ''

        return value

    def expand_tags(self, tlist, folder = None, search = '', desc_search = None, expand_plots = True, plottable_only = True, max_tags = None, tag_descriptions = {}):
        DefinitionDef = 0
        AnalogDef = self.name2id('AnalogDef')
        DiscreteDef = self.name2id('DiscreteDef')
        PlotDef = self.name2id('PlotDef')
        GraphicDef = self.name2id('GraphicDef')
        FolderDef = self.name2id('FolderDef')
        FolderViewDef = self.name2id('FolderViewDef')
        ViewDef = self.name2id('ViewDef')
        CalculationDef = self.name2id('CalculationDef')
        PredictionDef = self.name2id('PredictionDef')
        tags = [ (t[0] if isinstance(t, tuple) else t) for t in tlist if t is not None ]
        dtype_list = self.types(tags)
        tags = []
        for i, t in enumerate(tlist):
            if max_tags:
                if len(tags) >= max_tags:
                    break
            if isinstance(t, tuple):
                if self.tag2hid(t):
                    if self.type(t[0]) in (AnalogDef,
                     DiscreteDef,
                     CalculationDef,
                     PredictionDef) and t[1] in ('VALUE', self.VALUE_FT):
                        tags.append(t[0])
                    else:
                        tags.append(t)
                    continue
                else:
                    t = t[0]
            dtype = dtype_list[i]
            if dtype == DefinitionDef:
                view_tags = self.getlist(t, search=search, desc_search=desc_search)
                tags += self.expand_tags(view_tags, folder=t, plottable_only=plottable_only, expand_plots=expand_plots, max_tags=max_tags, tag_descriptions=tag_descriptions)
            elif dtype == PlotDef:
                if expand_plots:
                    plot_tags = [ x[0] for x in self.getlist(t, 'TAG', ascii=False) ]
                    plot_tags = self.ids2names(plot_tags)
                    search = ''
                    tags += plot_tags
                else:
                    tags.append(t)
            elif dtype == GraphicDef:
                if expand_plots:
                    plot_tags = self.getlist(t, 'TAG')
                    plot_tags = [ t2 for t2 in plot_tags if t2 != t ]
                    search = ''
                    tags += self.expand_tags(plot_tags, search=search, desc_search=desc_search, folder=t, plottable_only=plottable_only, tag_descriptions=tag_descriptions)
                else:
                    tags.append(t)
            elif dtype == FolderDef:
                f = Record(self, t, True)
                tags += self.expand_tags([ t2 for t2 in f.record_name if t2 != t ], search=search, desc_search=desc_search, folder=t, plottable_only=plottable_only, expand_plots=expand_plots, max_tags=max_tags, tag_descriptions=tag_descriptions)
            elif dtype == FolderViewDef:
                view_record = self.get(t, 'VIEW_RECORD')
                view_tags = self._gen_view_data(view_record, search=search, desc_search=desc_search)
                tags += self.expand_tags(view_tags, search=search, desc_search=desc_search, folder=t, plottable_only=plottable_only, expand_plots=expand_plots, max_tags=max_tags, tag_descriptions=tag_descriptions)
            elif dtype == ViewDef:
                if self.get(t, 'RECORD') != ViewDef:
                    tags += self.expand_tags(self._gen_view_data(t), search=search, desc_search=desc_search, folder=t, max_tags=max_tags, tag_descriptions=tag_descriptions)
            elif not plottable_only or plottable_only and (dtype in (AnalogDef, DiscreteDef) or self.get_h_cfg(t) != None) or plottable_only and dtype in (CalculationDef, PredictionDef):
                if not search and not desc_search or search and wildcard_match(t, search) or (desc_search and wildcard_match(tag_descriptions[t], desc_search) if t in tag_descriptions else False):
                    tags.append(t)

        return unique(tags)

    def _gen_view_data(self, record, include_fields = False, search = None, desc_search = None, ascii = True):
        view = Record(self, record, ascii=True)
        definition = view.record
        fields = view.column_field
        search_rules = zip(view.search_field, view.search_operator, view.search_value)
        sort_fields = zip(view.sort_field, map(int, view.sort_direction))
        sort_fields = [ ((f,), d) for f, d in sort_fields ]

        def get_field_paths(sfields, path = []):
            field_paths = []
            for field, checked, children in sfields:
                if checked:
                    field_paths.append(path + [field])
                field_paths += get_field_paths(children, path + [field])

            return field_paths

        # bytes --> str 로 변환하여 에러 해결
        for i ,t in enumerate(fields):
            if isinstance(t,bytes):
                fields[i] =t.decode()

        if len(fields) > 0 and type(fields[0]) == str:
            fields = [ [f, True, []] for f in fields ]
        field_paths = get_field_paths(fields)
        record_list = self.lsname(definition, search=search, desc_search=desc_search, ascii=ascii)
        num_recs = len(record_list)
        matched_records = []
        field_value_dict = {}
        p = re.compile('\\{(.+?)\\}')
        for field, operator, value in search_rules:
            dtype = self.type(definition, field)
            format = self.getdef(definition, field, DEF_FORMAT)
            if dtype == DT_INTEGER and format is not None or dtype in (DT_RECORD, DT_FIELD):
                ascii = True
            else:
                ascii = False
            field_value_dict[field] = self.mget(record_list, field, ascii)

        for i, name in enumerate(record_list):
            rules_match = True
            for field, operator, value in search_rules:
                op_function = [ op_func for op_name, op_func in SEARCH_OPERATORS if op_name == operator ][0]
                m = p.match(value)
                if m:
                    tag = m.group(1)
                    if tag.lower() == 'login':
                        value = self.user
                    elif definition in ('DmcIndDef', 'DmcDepDef') and field != 'NAME':
                        value = self.get(name, 'VALUE', tag, ascii=True)
                    else:
                        db_value = field_value_dict[field][i]
                    if value == None:
                        value = ''
                if is_float(value):
                    ascii = False
                elif value.count('/') == 2:
                    value = self.ascii2time(value)
                    ascii = False
                else:
                    ascii = True
                if definition in ('DmcIndDef', 'DmcDepDef') and field != 'NAME':
                    db_value = self.get(name, 'VALUE', field, ascii=ascii)
                else:
                    db_value = field_value_dict[field][i]
                if db_value == None:
                    db_value = ''
                if not ascii and is_float(db_value):
                    value = float(value)
                    db_value = float(db_value)
                else:
                    value = value.upper()
                    db_value = db_value.upper()
                if not op_function(db_value, value):
                    rules_match = False
                    break

            if rules_match:
                matched_records.append(name)

        if len(sort_fields) > 0:

            def record_compare(rec1, rec2):
                for path, reverse in sort_fields:
                    field = path[0]
                    if len(path) > 1:
                        sub_field = path[1]
                    else:
                        sub_field = 'VALUE'
                    if definition in ('DmcIndDef', 'DmcDepDef') and field != 'NAME':
                        value1 = self.get(rec1, sub_field, field)
                        value2 = self.get(rec2, sub_field, field)
                        if is_float(value1) and is_float(value2):
                            value1 = float(value1)
                            value2 = float(value2)
                    else:
                        value1 = self.get(rec1, field)
                        value2 = self.get(rec2, field)
                    if type(value1) == types.StringType:
                        value1 = value1.upper()
                    if type(value2) == types.StringType:
                        value2 = value2.upper()
                    if value1 == None and value2 != None:
                        return 1
                    if value1 != None and value2 == None:
                        return -1
                    if not reverse and value1 > value2 or reverse and value1 < value2:
                        return 1
                    if value1 == value2:
                        continue
                    else:
                        return -1

                return 0

            matched_records.sort(record_compare)
        if include_fields:
            fields = [ self.name2id(f[0]) for f in fields ]
            output_list = []
            for t in matched_records:
                fvalues = [ self.get(t, f, ascii=True) for f in fields ]
                output_list.append([t] + fvalues)

            matched_records = output_list
        return matched_records

    def _gen_view_data2(self, definition, fields = None, search = None, desc_search = None, search_rules = [], sort_fields = [], max_tags = 5000):

        def get_field_paths(sfields, path = []):
            field_paths = []
            for field, checked, children in sfields:
                if checked:
                    field_paths.append(path + [field])
                field_paths += get_field_paths(children, path + [field])
            return field_paths
        if len(fields) > 0 and type(fields[0]) == types.StringType:
            fields = [ [f, True, []] for f in fields ]
        field_paths = get_field_paths(fields)
        if search == None:
            search = ''
        if len(fields) > 1 and len(fields[0]) > 1 and self.getdef(definition, fields[0][0], DEF_REPEAT) != None:
            is_repeat_area = True
            field_names = [ f[0] for f in fields ]
            repeat_area_rows = []
            for t in self.lsname(definition, search=search, desc_search=desc_search):
                for row in self.getlist(t, field_names):
                    repeat_area_rows.append([t] + list(row))

            record_list = [ t[0] for t in repeat_area_rows ]
        else:
            is_repeat_area = False
            record_list = self.lsname(definition, search=search, desc_search=desc_search)
        num_recs = len(record_list)
        matched_records = []
        matched_repeat_data = []
        field_value_dict = {}
        p = re.compile('\\{(.+?)\\}')
        for field, operator, value in search_rules:
            dtype = self.type(definition, field)
            format = self.getdef(definition, field, DEF_FORMAT)
            if dtype == DT_INTEGER and format is not None or dtype in (DT_RECORD, DT_FIELD):
                ascii = True
            else:
                ascii = False
            field_value_dict[field] = self.mget(record_list, field, ascii)

        for i, name in enumerate(record_list):
            if search:
                if not wildcard_match(name, search):
                    continue
            rules_match = True
            for field, operator, value in search_rules:
                try:
                    op_function = [ op_func for op_name, op_func in SEARCH_OPERATORS if op_name == operator ][0]
                except IndexError:
                    continue

                m = p.match(value)
                if m:
                    tag = m.group(1)
                    if tag.lower() == 'login':
                        value = self.user
                    elif definition in ('DmcIndDef', 'DmcDepDef', 'DmcControlDef') and field != 'NAME':
                        value = self.get(name, 'VALUE', tag, ascii=True)
                    else:
                        value = self.get(name, tag, ascii=True)
                    if value == None:
                        value = ''
                if is_float(value):
                    ascii = False
                elif value.count('/') == 2:
                    value = self.ascii2time(value)
                    ascii = False
                else:
                    ascii = True
                if definition in ('DmcIndDef', 'DmcDepDef', 'DmcControlDef') and field != 'NAME':
                    db_value = self.get(name, 'VALUE', field, ascii=ascii)
                elif is_repeat_area:
                    field_idx = field_names.index(field) + 1
                    db_value = repeat_area_rows[i][field_idx]
                else:
                    db_value = field_value_dict[field][i]
                if db_value is None:
                    db_value = ''
                if not ascii and is_float(db_value) and not isnan(db_value):
                    value = float(value)
                    db_value = float(db_value)
                else:
                    value = value.strip().upper()
                    db_value = str(db_value).strip().upper()
                    (value, db_value)
                if not op_function(db_value, value):
                    rules_match = False
                    break

            if rules_match:
                matched_records.append(name)
                if is_repeat_area:
                    matched_repeat_data.append(repeat_area_rows[i])

        if len(sort_fields) > 0:

            def record_compare(rec1, rec2):
                for path, reverse in sort_fields:
                    field = path[0]
                    if len(path) > 1:
                        sub_field = path[1]
                    else:
                        sub_field = 'VALUE'
                    if definition in ('DmcIndDef', 'DmcDepDef', 'DmcControlDef') and field != 'NAME':
                        value1 = self.get(rec1, sub_field, field)
                        value2 = self.get(rec2, sub_field, field)
                        if is_float(value1) and is_float(value2):
                            value1 = float(value1)
                            value2 = float(value2)
                    else:
                        value1 = self.get(rec1, field)
                        value2 = self.get(rec2, field)
                    if type(value1) == types.StringType:
                        value1 = value1.upper()
                    if type(value2) == types.StringType:
                        value2 = value2.upper()
                    if value1 == None and value2 != None:
                        return 1
                    if value1 != None and value2 == None:
                        return -1
                    if not reverse and value1 > value2 or reverse and value1 < value2:
                        return 1
                    if value1 == value2:
                        continue
                    else:
                        return -1

                return 0

            matched_records.sort(record_compare)
        return matched_records[:max_tags]

    def register_event(self, uid):
        if uid == None:
            return
        else:
            record, field, idx = uid
            if record == None:
                return
            record = self.name2id(record)
            field = self.name2id(field)
            idx = self.key2idx(idx)
            if None in (record, field, idx):
                return
            channel = self.uid(record, field, idx)
            if self._sub_count.has_key(channel):
                self._sub_count[channel] += 1
            else:
                self.ps.subscribe(channel)
                self._sub_count[channel] = 1
            return

    def register_events(self, uids):
        if len(uids) == 0:
            return
        records = [ u[0] for u in uids ]
        fields = [ u[1] for u in uids ]
        idxs = [ u[2] for u in uids ]
        if isinstance(records[0], str):
            records = self.names2ids(records)
        if isinstance(fields[0], str):
            fields = self.names2ids(fields)
        channels = [ self.uid(r, f, i) for r, f, i in zip(records, fields, idxs) ]
        new_channels = [ c for c in channels if not self._sub_count.has_key(c) ]
        if len(new_channels) > 0:
            self.ps.subscribe(*new_channels)
        for channel in channels:
            if self._sub_count.has_key(channel):
                self._sub_count[channel] += 1
            else:
                self._sub_count[channel] = 1

    def unregister_event(self, uid = None):
        if uid not in (None, (0, 0, 0)):
            record, field, idx = uid
            record = self.name2id(record)
            field = self.name2id(field)
            channel = self.uid(record, field, idx)
            if self._sub_count.has_key(channel):
                if self._sub_count[channel] > 1:
                    self._sub_count[channel] -= 1
                else:
                    self.ps.unsubscribe(channel)
                    del self._sub_count[channel]
        return

    def unregister_events(self, uids):
        if len(uids) == 0:
            return
        records = [ u[0] for u in uids ]
        fields = [ u[1] for u in uids ]
        idxs = [ u[2] for u in uids ]
        if isinstance(records[0], str):
            records = self.names2ids(records)
        if isinstance(fields[0], str):
            fields = self.names2ids(fields)
        channels = [ self.uid(r, f, i) for r, f, i in zip(records, fields, idxs) ]
        done_channels = []
        for channel in channels:
            if self._sub_count.has_key(channel):
                if self._sub_count[channel] > 1:
                    self._sub_count[channel] -= 1
                else:
                    done_channels.append(channel)
                    del self._sub_count[channel]

        if len(done_channels) > 0:
            self.ps.unsubscribe(*done_channels)

    def get_thread_id(self):
        return threading._get_ident()

    def wait_event(self, timeout = None):
        start = time.time()
        while True:
            if self.ps.connection:
                msg = self.ps.get_message()
            else:
                msg = None
            if msg:
                if len(msg['data']) == 20:
                    uid = self.xuid(msg['data'][:12])
                    next_ts = self.unpack_field(msg['data'][12:], DT_SCHEDULE)
                    if self.now() < next_ts or next_ts in (0, nan):
                        return uid
                    continue
                elif len(msg['data']) == 12:
                    return self.xuid(msg['data'])
                else:
                    return self.xuid(msg['channel'])

            else:
                if timeout == 0:
                    return
                time.sleep(0.001)
            if timeout != None and time.time() - start > timeout:
                break

        return

    wait_event2 = wait_event

    def send_event(self, uid, def_uid = None):
        uid = self.uid2(uid)
        if def_uid:
            def_uid = self.uid2(def_uid)
            n = self.rdb.execute_command('PUBSUB', 'NUMSUB', uid, def_uid)
            if n[3] > 0:
                self.rdb.publish(def_uid, uid)
        else:
            n = self.rdb.execute_command('PUBSUB', 'NUMSUB', uid)
        if n[1] > 0:
            self.rdb.publish(uid, '')

    def send_events(self, uids):
        uids = self.get_event_uids(uids)
        if len(uids) == 0:
            return
        pipe = self.rdb.pipeline(transaction=False)
        for uid in uids:
            pipe.publish(uid, '')

        pipe.execute()

    def send_schedule_event(self, uid):
        uid = self.tag2uid(uid)
        if uid == None:
            return
        else:
            did = self.get_defid(uid[0])
            def_uid = (did, uid[1], uid[2])
            data = self.pack_field(0.0, DT_SCHEDULE)
            self.rdb.publish(self.uid2(uid), self.uid2(uid) + data)
            self.rdb.publish(self.uid2(def_uid), self.uid2(uid) + data)
            return

    def get_event_uids(self, uids):
        if len(uids) > 0 and isinstance(uids[0], tuple):
            uids = [ self.uid2(u) for u in uids ]
        channels = self.rdb.execute_command('PUBSUB CHANNELS')
        return set(channels).intersection(uids)

    def send_code(self, code):
        pass

    def send_event_end(self, no_db = False, end_type = 0):
        self.rdb.publish(pack('>III', 0, end_type, 0), '')

    def pid_exists(self, pid):
        if os.name == 'posix':
            try:
                os.kill(pid, 0)
            except OSError as e:
                if e.errno == 3:
                    return False

            return True
        else:
            try:
                import win32api
                import win32con
                import pywintypes
                try:
                    win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, pid)
                except pywintypes.error as e:
                    if e[0] == 87:
                        return False

            except ImportError:
                pass

            return True

    def zrange_keys(self, rid, fid, kid):
        start = b'[' + pack('>III', rid, fid, kid)
        if rid == 0:
            end = '+'
        elif fid == 0:
            end = b'(' + pack('>III', rid + 1, 0, 0)
        elif kid == 0:
            end = b'(' + pack('>III', rid, fid + 1, 0)
        else:
            end = b'(' + pack('>III', rid, fid, kid + 1)
        return (start, end)

    def delref_inner(self, recid):
        found_uids1 = []
        found_uids2 = []
        start, end = self.zrange_keys(recid, 0, 0)
        for k in self.rdb.zrangebylex('zref', start, end):
            v = self.rdb.hget('ref', k)
            found_uids1.append(k)
            found_uids2.append(v + k)

        if len(found_uids1) > 0:
            self.rdb.hdel('ref', *found_uids1)
            self.rdb.zrem('zref', *found_uids1)
            self.rdb.zrem('sref', *found_uids2)

    def delref_outer(self, recid):
        found_uids1 = []
        found_uids2 = []
        start, end = self.zrange_keys(recid, 0, 0)
        for row in self.rdb.zrangebylex('sref', start, end):
            found_uids1.append(row)
            found_uids2.append(row[12:])

        if len(found_uids1) > 0:
            self.rdb.zrem('sref', *found_uids1)
            self.rdb.hdel('ref', *found_uids2)
            self.rdb.zrem('zref', *found_uids2)

    def putref(self, in_uid, ref_uid):
        ref = self.rdb.hget('ref', self.uid2(in_uid))
        pipe = self.rdb.pipeline(transaction=False)
        if ref != None:
            pipe.zrem('sref', ref + self.uid2(in_uid))
        if ref_uid == None:
            pipe.hdel('ref', self.uid2(in_uid))
            pipe.zrem('zref', self.uid2(in_uid))
        else:
            pipe.hset('ref', self.uid2(in_uid), self.uid2(ref_uid))
            pipe.zadd('zref', self.uid2(in_uid), 0)
            pipe.zadd('sref', self.uid2(ref_uid) + self.uid2(in_uid), 0)
        pipe.execute()
        return

    def putrefs(self, ref_tuples):
        if len(ref_tuples) == 0:
            return
        else:
            pipe = self.rdb.pipeline(transaction=False)
            for in_uid, ref_uid in ref_tuples:
                pipe.hget('ref', self.uid2(in_uid))

            refs = pipe.execute()
            pipe = self.rdb.pipeline(transaction=False)
            for i, (in_uid, ref_uid) in enumerate(ref_tuples):
                ref = refs[i]
                if ref != None:
                    pipe.zrem('sref', ref + self.uid2(in_uid))
                if ref_uid == None:
                    pipe.hdel('ref', self.uid2(in_uid))
                    pipe.zrem('zref', self.uid2(in_uid))
                else:
                    pipe.hset('ref', self.uid2(in_uid), self.uid2(ref_uid))
                    pipe.zadd('zref', self.uid2(in_uid), 0)
                    pipe.zadd('sref', self.uid2(ref_uid) + self.uid2(in_uid), 0)

            pipe.execute()
            return

    def getref(self, ref_uid, ascii = False):
        if isinstance(ref_uid, str) or isinstance(ref_uid, int):
            ref_uid = (self.name2id(ref_uid), 0, 0)
        if ascii:
            ref_uid = (self.name2id(ref_uid[0]), self.name2id(ref_uid[1]), 0)
        rid, fid, kid = ref_uid
        if rid == None or fid == None:
            return []
        else:
            start, end = self.zrange_keys(rid, fid, kid)
            ref_list = []
            for row in self.rdb.zrangebylex('sref', start, end):
                ref_list.append(self.xuid(row[12:]))

            if ascii:
                ref_list = [ self.uid2name(uid) for uid in ref_list ]
            return ref_list

    def get_repeat(self, record, field, ascii = False, text = False):
        if text:
            ascii = True
        rid = self.name2id(record)
        fid = self.name2id(field)
        if rid == None or fid == None:
            return
        else:
            did = self.get_defid(record)
            rfid = self.getdef(did, fid, DEF_REPEAT)
            if rfid == None:
                return
            if ascii:
                return self.id2name(rfid)
            return rfid
            return

    def __getitem__(self, key):
        if type(key) in (types.ListType, types.TupleType):
            return key
        tokens = key.split(' ')
        n = len(tokens)
        if n == 1:
            did = self.get_defid(key)
            if did == DEFINITION_DEF:
                return map(self.Record, self.lsname(key))
            else:
                return self.Record(key)
        else:
            if n in (2, 3):
                if n == 2:
                    rec = tokens[0]
                    field = tokens[1]
                    occ = 0
                elif n == 3:
                    rec = tokens[0]
                    field = tokens[1]
                    try:
                        occ = int(tokens[2])
                    except ValueError:
                        occ = str(tokens[2])

                return self.get(rec, field, occ)
            return

    def __setitem__(self, key, value):
        tokens = key.split(' ')
        n = len(tokens)
        if n in (2, 3):
            if n == 2:
                rec = tokens[0]
                field = tokens[1]
                occ = 0
            elif n == 3:
                rec = tokens[0]
                field = tokens[1]
                try:
                    occ = int(tokens[2])
                except ValueError:
                    occ = str(tokens[2])

            self.put(rec, field, value, occ)

    def Record(self, name, ascii = False):
        x = Record(self, name, ascii)
        return x


class Tag():

    def __init__(self, db, tag, ascii = False):
        self.db = db
        for f in db.list_fields(tag, ascii=True):
            setattr(self, f, db.get(tag, f))


class Record():

    def __init__(self, db, name, ascii = False):
        self.db = db
        self.name = name
        self.ascii = ascii

    def __getattr__(self, name):
        repeat = self.db.get_repeat(self.name, name)
        if repeat:
            values = []
            n = self.db.get(self.name, repeat)
            for i in range(1, n + 1):
                v = self.db.get(self.name, name, i, ascii=self.ascii)
                values.append(v)

            return values
        else:
            return self.db.get(self.name, name, ascii=self.ascii)

class HID():
    def __init__(self, hfile, hid):
        self.hfile = hfile
        self.hid = hid