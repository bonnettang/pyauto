# Module     : winGuiAuto.py
# Synopsis   : Windows GUI automation utilities
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 25 June 2003
# Version    : 1.0 pre-alpha 2
# Copyright  : Released to the public domain. Provided as-is, with no warranty.
# Notes      : Requires Python 2.3, win32all and ctypes 
'''Windows GUI automation utilities.

Until I get around to writing some docs and examples, the tests at the foot of
this module should serve to get you started.
'''
import time
import sqlite3
import re

def initDb():
    conn = sqlite3.connect('autotrade.db')
    cu = conn.cursor()
    sql="SELECT name FROM sqlite_master WHERE type='table'"
    cu.execute(sql)
    out=str(cu.fetchall())
    #print(out)
    if not re.search('stock_positions',out):
        sql='CREATE TABLE stock_positions( \
                    security CHAR(50),  \
                    count    INT, \
                    price    FLOAT,\
                    time     TEXT)'
        cu.execute(sql)   
    if not re.search('stock_monitor',out):
        sql='CREATE TABLE stock_monitor( \
                    security CHAR(50),  \
                    high     FLOAT, \
                    low     FLOAT, \
                    vol     FLOAT, \
                    avg     FLOAT, \
                    ma5     FLOAT,\
                    ma10     FLOAT, \
                    ma20     FLOAT, \
                    price    FLOAT,\
                    time     TEXT)'
        cu.execute(sql)
    conn.commit()
    return [conn,cu]
    
def get_local_price(security):
    conn,cu = initDb()    
    sql='select * from stock_monitor where security="'+security+'"'
    cu.execute(sql)
    out=cu.fetchall()
    
    if not re.search(security,str(out)):
        return [security,0,0]
    else:
        return [security,out[0][1],out[0][2] ]
    conn.close()
def set_local_price(security,high=0,low=0):
    conn,cu = initDb()
    sql='select * from stock_monitor where security="'+security+'"'
    print('%s,%f,%f'%(security,high,low))
    cu.execute(sql)
    out=str(cu.fetchall())
    #print(out)
    if not re.search(security,out):
        sql= 'insert into stock_monitor (security) values("'+security+'")'
        #print(sql)
        cu.execute(sql)
    if high >0 :
        sql='update stock_monitor set high='+str(high) + ' where security="'+security+'"'
        cu.execute(sql)
    if low >0 :
        sql='update stock_monitor set low='+str(low) + ' where security="'+security+'"'
        cu.execute(sql)
    print(sql)
    conn.commit()    
    conn.close()

def del_local_security(security):
    conn,cu = initDb()
    sql='select * from stock_monitor where security="'+security+'"'
    cu.execute(sql)
    out=str(cu.fetchall())
    if not re.search(security,out):
        return True
    sql='delete  from stock_monitor where security="'+security+'"'
    cu.execute(sql)  
    conn.commit()    
    conn.close()
    
if __name__ == '__main__': 
    set_local_price('000485',high=6.55)
    print(get_local_price('000485'))
    del_local_security('000485')
    print(get_local_price('000485'))