#encoding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import os
import json
import logging

class NSC_Structure(object):
    global option

    def __init__(self):
        global logger
        logger = logging.getLogger('NSCRun')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('D:\\temp\\log\\IVR.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.info('Service init')
        global option
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-gpu')
        option.add_argument('--hide-scrollbars')
        option.add_argument('--no-sandbox')
        #option.add_argument('--headless')
        option.add_argument('--window-size=800x1000')
        option.add_argument("--proxy-server='direct://'");
        option.add_argument("--proxy-bypass-list=*");
        #option.add_argument('blink-settings=imagesEnabled=false')
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\temp\\'}
        option.add_experimental_option('prefs', prefs) 

    def every_downloads_chrome(self,driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var items = downloads.Manager.get().items_;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.file_url);
            """)

    def Read_Script(self,infile):
        global logger
        logger.info('Load script')
        f=open(infile,'r')
        sourceInLine=f.readlines()
        dataset=[]
        for line in sourceInLine:
            temp1=line.strip('\n')
            temp2=temp1.split()
            for data in temp2:
                dataset.append(data)
        return dataset

    def NSC_Run(self):
        global option,driver,logger
        step=0
        pwd=os.getcwd()
        scrfile=pwd+'\\script.txt'
        script=self.Read_Script(scrfile)
        steplen=len(script)
        logger.info('Script len ='+str(steplen))
        print(str(script))

        #init driver
        driver = webdriver.Chrome(chrome_options = option)  # Optional argument, if not specified will search path.
        driver.implicitly_wait(90)
        
        while(step<steplen):
            print('Current command:',script[step])
            if(script[step]=='id'):
                #element=driver.find_element_by_id(script[step+1])
                element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id(script[step+1]))
                step+=2
            elif(script[step]=='name'):
                #element=driver.find_element_by_name(script[step+1])
                element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name(script[step+1]))
                step+=2
            elif(script[step]=='rem'):
                laststep=script[step+1]
                step+=2
            elif(script[step]=='click'):
                element.click()
                step+=1
            elif(script[step]=='open'):
                driver.get(script[step+1])
                step+=2
            elif(script[step]=='input'):
                exec("element.send_keys(script[step+1])")
                step+=2
            elif(script[step]=='sleep'):
                exec("time.sleep(int(script[step+1]))")
                step+=2
            elif(script[step]=='waitfordownload'):
                WebDriverWait(driver, 120, 0.2).until(self.every_downloads_chrome)
                step+=1
            elif(script[step]=='transationstart'):
                transationname=script[step+1]
                transationstarttime=int(round(time.time() * 1000))
                transationstatus=0
                step+=2
            elif(script[step]=='transationend'):
                transationname=script[step+1]
                transationendtime=int(round(time.time() * 1000))
                transationfinalstatus=transationstatus
                #self.postdata(bpmname,transationname,transationfinalstatus,
                #         transationendtime-transationstarttime)
                print(transationname+' '+str(transationfinalstatus)+' '+str(transationendtime-transationstarttime))
                step+=2
            elif(script[step]=='enter'):
                element.send_keys(Keys.ENTER)
                step+=1
            elif(script[step]=='check'):
                try:
                    time.sleep(2)
                    assert(script[step+1] in driver.page_source),'Cannot find keyword in page'
                except AssertionError as msg:
                    print(msg)
                    transationstatus=1
                step+=2
            else:
                print('Step [',script[step],'] in count',step,'cannot analys')
                step+=1

        #self.postdata(bpmname,transationname,transationfinalstatus,
        #                transationendtime-transationstarttime)

        #data = {'agentname' : bpmname, 'transation': transationname,  'status': transationfinalstatus,'runtime': transationendtime-transationstarttime}
        
        #url = 'http://trgame.ddns.net:22880/nsserver/receiver.php'
        #ret = urllib.request.urlopen(url=url, data=json.dumps(data).encode(encoding='UTF8'))
        

        print('Script ',script,' finished. Result posted.')
        #time.sleep(5)
        driver.quit()
        return 0


if __name__=='__main__':
    print("start")
    nsc=NSC_Structure()
    nsc.NSC_Run()




        
