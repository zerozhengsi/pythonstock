#coding=utf-8
'''
Created on 2016年7月4日

@author: zeroz
'''
from log import LoggerFactory
import urllib2
from datetime import date
from datetime import datetime
from dbconn.DBOperator import *
import threading
import time
import uuid

class StockTencent(object):
    
    __stockTables = {'cash':'stock_cash_tencent','quotation':'stock_quotation_tencent'}
    __sleepTime = 1

    def __init__(self):
        self.__logger = LoggerFactory.getLogger('StockTencent')
        self.__dbOperatorCash = DBOperator()
        self.__dbOperatorQuotation = DBOperator()
        self.__tmpCashData = ""
        self.__tmpQuotationData = ""
        self.__tmpUUID = ""
        
    def main(self):
        self.__dbOperatorCash.connDB()
        self.__dbOperatorQuotation.connDB()
        while True:
            self.getStockTencentByCodes("sz",[300352])    
#             cashThread = threading.Thread(target = self.getStockCashByCodes,args=("sz",[300352]))
#             cashThread.start()
#     #         threading.Thread(target = self.getStockQuotation()).start() 
#             cashThread.join()
            
        self.__dbOperatorCash.closeDB()
        self.__dbOperatorQuotation.closeDB()
        
    def __isStockExitsInDate(self, table, stock, date):
        sql = "select * from " + table + " where code = '%s' and date='%s'" % (stock, date)
        n = self.__dbOperator.execute(sql) 
        if n >= 1:
            return True
        
    def __getStockCashDetail(self, dataUrl):
        tempData = self.__getDataFromUrl(dataUrl)
         
        if tempData == None or tempData == self.__tmpCashData:
            time.sleep(self.__sleepTime)
            return False
                
        self.__tmpCashData = tempData
        stockCash = {} 
        stockInfo = tempData.split('~')
        if len(stockInfo) < 13: 
            time.sleep(self.__sleepTime)
            return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') == -1:
            self.__tmpUUID = uuid.uuid4()
            table = self.__stockTables['cash']
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
            stockCash['uuid']             = self.__tmpUUID
            stockCash['createtime']       = datetime.now()    
            self.__dbOperatorCash.insertIntoDB(table, stockCash)
            time.sleep(self.__sleepTime)
            
    def chgStr(self,oldStr,inx):
        if oldStr == None or oldStr == "":
            return ""
        
        oldStrs = oldStr.split('~')
        for i in inx:
            oldStrs[i] = ""
        newStr = '~'.join(oldStrs)
        return newStr
            
    def getStockQuotationDetail(self, dataUrl):
        tempData = self.__getDataFromUrl(dataUrl)
         
        if tempData == None or self.chgStr(tempData, (29,30,35,40,41)) == self.chgStr(self.__tmpQuotationData, (29,30,35,40,41)):
            time.sleep(self.__sleepTime)
            return False 
        
        self.__tmpQuotationData = tempData
        stockQuotation = {} 
        stockInfo = tempData.split('~')
        if len(stockInfo) < 45: 
            time.sleep(self.__sleepTime)
            return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') ==-1 and stockInfo[3].find('0.00') == -1:
            table = self.__stockTables['quotation']
            stockQuotation['code']  = stockInfo[2]
            stockQuotation['name']  = stockInfo[1].decode('utf8')
            stockQuotation['price'] = stockInfo[3]
            stockQuotation['yesterday_close']   = stockInfo[4]
            stockQuotation['today_open']        = stockInfo[5]
            stockQuotation['volume']            = stockInfo[6]
            stockQuotation['outer_sell']        = stockInfo[7]
            stockQuotation['inner_buy']         = stockInfo[8]
            stockQuotation['buy_one']           = stockInfo[9]
            stockQuotation['buy_one_volume']    = stockInfo[10]
            stockQuotation['buy_two']           = stockInfo[11]
            stockQuotation['buy_two_volume']    = stockInfo[12]
            stockQuotation['buy_three']         = stockInfo[13]
            stockQuotation['buy_three_volume']  = stockInfo[14]
            stockQuotation['buy_four']          = stockInfo[15]
            stockQuotation['buy_four_volume']   = stockInfo[16]
            stockQuotation['buy_five']          = stockInfo[17]
            stockQuotation['buy_five_volume']   = stockInfo[18]
            stockQuotation['sell_one']          = stockInfo[19]
            stockQuotation['sell_one_volume']   = stockInfo[20]
            stockQuotation['sell_two']          = stockInfo[22]
            stockQuotation['sell_two_volume']   = stockInfo[22]
            stockQuotation['sell_three']        = stockInfo[23]
            stockQuotation['sell_three_volume'] = stockInfo[24]
            stockQuotation['sell_four']         = stockInfo[25]
            stockQuotation['sell_four_volume']  = stockInfo[26]
            stockQuotation['sell_five']         = stockInfo[27]
            stockQuotation['sell_five_volume']  = stockInfo[28]
            stockQuotation['datetime']          = stockInfo[30]
            stockQuotation['updown']            = stockInfo[31]
            stockQuotation['updown_rate']       = stockInfo[32]
            stockQuotation['heighest_price']    = stockInfo[33]
            stockQuotation['lowest_price']      = stockInfo[34]
            stockQuotation['volume_amout']      = stockInfo[35].split('/')[2]
            stockQuotation['turnover_rate']     = stockInfo[38]
            stockQuotation['pe_rate']           = stockInfo[39]
            stockQuotation['viberation_rate']   = stockInfo[42]
            stockQuotation['circulated_stock']  = stockInfo[43]
            stockQuotation['total_stock']       = stockInfo[44]
            stockQuotation['pb_rate']           = stockInfo[45]
            stockQuotation['uuid']              = self.__tmpUUID
            stockQuotation['createtime']        = datetime.now()  
            self.__dbOperatorQuotation.insertIntoDB(table, stockQuotation)
            time.sleep(self.__sleepTime)
                
    def __getDataFromUrl(self, dataUrl):
        r = urllib2.Request(dataUrl)
        try:
            stdout = urllib2.urlopen(r, data=None, timeout=3)
        except Exception,e:
            self.__logger.error(">>>>>> Exception: " +str(e))   
            return None
         
        stdoutInfo = stdout.read().decode('gbk').encode('utf-8') 
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
        
    def getStockTencentByCodes(self,stockmark,codes):
        for code in codes:
            dataUrl = ""
            if "sh"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=ff_sh%d" % code
            elif "sz"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
            elif "zx"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
            elif "cy"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%d" % code
            
            cashThread = threading.Thread(target = self.__getStockCashDetail,args=(dataUrl,))
            cashThread.start()
            
            
            if "sh"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=sh%d" % code
            elif "sz"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
            elif "zx"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
            elif "cy"==stockmark:
                dataUrl = "http://qt.gtimg.cn/q=sz%d" % code
            
            quotationThread = threading.Thread(target = self.getStockQuotationDetail,args=(dataUrl,))
            quotationThread.start()  
              
            cashThread.join(5)
            quotationThread.join(5);
            
    def getStockQuotation(self):
        self.__logger.debug("start stock quotation") 
        try:
            #sh
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=sh%d" % code
                self.getStockQuotationDetail(dataUrl)   
        
            #sz
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)  
          
            #zx
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)     
             
            #  cy
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=sz%d" % code
                self.getStockQuotationDetail(dataUrl)     
         
        except Exception as err:
            self.__logger.error(">>>>>> Exception: " +str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("end stock quotation")
        
if __name__ == '__main__':
    StockTencent().main() 
