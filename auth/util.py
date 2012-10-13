from struct import pack, unpack
from hashlib import sha256 as password_hash
import random,string
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def random_char(maxlength=6):
	a = list(string.ascii_letters)
	random.shuffle(a)
	return ''.join(a[:maxlength])

def hash_password(id,password):
	return password_hash("%s%s"%(password, pack('Q', int(id)))).digest()