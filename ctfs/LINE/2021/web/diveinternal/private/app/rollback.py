import subprocess,time,os, sys
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('KillCoinapi') 

subprocess.SW_HIDE = 1

def RunRollbackDB(dbhash):
    try:
        if os.environ['ENV'] == 'LOCAL':
            return
        if dbhash is None:
            return "dbhash is None"
        dbhash = ''.join(e for e in dbhash if e.isalnum())
        if os.path.isfile('backup/'+dbhash):
            with open('FLAG', 'r') as f:
                flag = f.read()
                return flag
        else:
            return "Where is file?"
        

        
    except Exception as e :
        logger.error('Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno))
        return "exception!!"
        pass

def RunbackupDB(remove, dbhash):
    try:
        if os.environ['ENV'] == 'LOCAL':
            return
        subprocess.Popen(r'rm backup/*' , shell=True).wait()
        
        subprocess.Popen(r'cp ' + os.environ['DBFILE'] + ' backup/' + dbhash, shell=True).wait() # for low memory.
        
        return dbhash
    except Exception as e :
        logger.error('Error On  {f} : {c}, Message, {m}, Error on line {l}'.format(f = sys._getframe().f_code.co_name ,c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno))
        pass
