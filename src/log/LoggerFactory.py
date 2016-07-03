#coding=utf-8
'''
Created on 2016年7月2日

@author: zeroz
'''
import logging
import time

def getLogger(name):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
          
        logging.basicConfig(
            level    = logging.DEBUG,
            format   = now +" : " + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',
            datefmt  = '%m-%d %H:%M',
            filename =  "F:\\python\\log\\stock.log",
            filemode = 'w');
                      
        console = logging.StreamHandler();
        console.setLevel(logging.DEBUG);
        formatter = logging.Formatter(name + ': LINE %(lineno)-4d : %(levelname)-8s %(message)s');
        console.setFormatter(formatter);
          
        logger = logging.getLogger(name)
        logger.addHandler(console); 
        return logger
      
if __name__ == '__main__':
    getLogger("www").debug("www")
