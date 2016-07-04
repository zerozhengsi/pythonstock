#coding=utf-8
'''
Created on 2016年7月4日

@author: zeroz
'''
from log import LoggerFactory
import urllib2
from datetime import date
from db import *
from setting import *
from dbconn import DBOperator
import threading
import time
from stockextractor import StockTencent

class MyClass(object):
    
    __stockTables = {'cash':'stock_cash_tencent','quotation':'stock_quotation_tencent'}

    def __init__(self, params):
        self.__logger = LoggerFactory.getLogger('StockTencent')
        self.__dbOperator = DBOperator()
        
    def main(self):
        self.__dbOperator.connDB()
        threading.Thread(target = self.getStockCashByCodes,args=("sz",["300352"])).start() 
#         threading.Thread(target = self.getStockQuotation()).start() 
        self.__dbOperator.closeDB()
        
    def __isStockExitsInDate(self, table, stock, date):
        sql = "select * from " + table + " where code = '%s' and date='%s'" % (stock, date)
        n = self.__dbOperator.execute(sql) 
        if n >= 1:
            return True
        
    def __getStockCashDetail(self, dataUrl):
        tempData = self.__getDataFromUrl(dataUrl)
         
        if tempData == None:
            time.sleep(10)
            tempData = self.__getDataFromUrl(dataUrl)
            return False
                
        stockCash = {} 
        stockInfo = tempData.split('~')
        if len(stockInfo) < 13: return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') == -1:
            table = self.__stockTables['cash']
            code = stockInfo[0].split('=')[1][2:]
            date = stockInfo[13]
            if not self.__isStockExitsInDate(table, code, date):
                stockCash['code'] = stockInfo[0].split('=')[1][2:]
                stockCash['main_in_cash']     = stockInfo[1]
                stockCash['main_out_cash']    = stockInfo[2]
                stockCash['main_net_cash']    = stockInfo[3]
                stockCash['main_net_rate']    = stockInfo[4]
                stockCash['private_in_cash']  = stockInfo[5]
                stockCash['private_out_cash'] = stockInfo[6]
                stockCash['private_net_cash'] = stockInfo[7]
                stockCash['private_net_rate'] = stockInfo[8]
                stockCash['total_cash']       = stockInfo[9]
                stockCash['name']             = stockInfo[12].decode('utf8')
                stockCash['date']             = stockInfo[13]    
                self.__dbOperator.insertIntoDB(table, stockCash)
                
    def __getDataFromUrl(self, dataUrl):
        r = urllib2.Request(dataUrl)
        try:
            stdout = urllib2.urlopen(r, data=None, timeout=3)
        except Exception,e:
            self.__logger.error(">>>>>> Exception: " +str(e))   
            return None
         
        stdoutInfo = stdout.read().decode().encode('utf-8') 
        tempData = stdoutInfo.replace('"', '')
        self.__logger.debug(tempData) 
        return tempData
    
    def getStockCash(self):
        self.__logger.debug("start stock cache")
        try:
            #sh
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=ff_sh%d" % code
                self.__getStockCashDetail(dataUrl) 
                 
            #sz
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)  
                    
            #zx
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)      
             
            #cy
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%d" % code
                self.__getStockCashDetail(dataUrl)    
         
        except Exception as err:
            self.__logger.error(">>>>>> Exception: " +str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("end stock cache")   
        
    def getStockCashByCodes(self,stockmark,codes):
        dataUrl = ""
        if "sh"==stockmark:
            dataUrl = "http://qt.gtimg.cn/q=ff_sh%d"
        elif "sz"==stockmark:
            dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d"
        elif "zx"==stockmark:
            dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d"
        elif "cy"==stockmark:
            dataUrl = "http://qt.gtimg.cn/q=ff_sz%d"
            
        for i in codes:
            dataUrl = dataUrl % codes[i]
            self.__getStockCashDetail(dataUrl)
        
if __name__ == '__main__':
    StockTencent().main() 