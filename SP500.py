#! -*- coding:utf-8 -*-


import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    Price = selector.xpath('/html/body/div[1]/div[2]/div[1]/div/div/table/tbody/tr/td[5]/text()')
    f_price = RemoveDot(remove_block(Price))
    f_tup = tuple(f_price)
    big_list.append((f_tup))
    return big_list



def RemoveDot(item):
    f_l = []
    for it in item:

        f_str = "".join(it.split(","))
        f_l.append(f_str)

    return f_l




def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items






def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='SP500_Nas100',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        sp500 = 'MSFT,AAPL,AMZN,FB,BRK_B,GOOGL,GOOG,JPM,JNJ,V,PG,MA,T,INTC,BAC,UNH,HD,VZ,DIS,XOM,KO,MRK,CMCSA,PEP,CVX,PFE,CSCO,WFC,ADBE,BA,NVDA,CRM,WMT,NFLX,MCD,C,BMY,ABT,MDT,COST,ABBV,PYPL,NEE,PM,ACN,IBM,TMO,AMGN,HON,UNP,NKE,UTX,LLY,AVGO,ORCL,TXN,LIN,AMT,LMT,GE,DHR,SBUX,QCOM,LOW,FIS,GILD,CVS,MMM,AXP,MDLZ,CHTR,MO,ADP,USB,BKNG,CME,TJX,CI,DUK,INTU,D,CAT,CB,TFC,GS,SPGI,SO,PLD,ANTM,SYK,UPS,CCI,BDX,ISRG,FISV,ZTS,PNC,AGN,CL,NOW,BLK,COP,MS,VRTX,MU,CSX,GPN,RTN,BIIB,TGT,AMD,MMC,BSX,NOC,AMAT,EQIX,APD,DE,ITW,NSC,AON,ICE,ECL,SCHW,AEP,LHX,WM,KMB,ATVI,PGR,EXC,EW,SHW,HUM,COF,BAX,EL,ROST,SRE,LRCX,ADI,MCO,SPG,GD,SLB,ADSK,EMR,KMI,ETN,DG,GM,ILMN,NEM,EOG,AIG,ALL_,ROP,SYY,MET,PSX,DD,HCA,FDX,CTSH,XEL,WBA,MAR,MPC,BK,AFL,PRU,OXY,WELL,TRV,CNC,DOW,IR,REGN,PSA,STZ,SBAC,HPQ,GIS,JCI,VLO,WEC,ZBH,AVB,DAL,EA,MSI,INFO,TROW,OKE,ES,YUM,TMUS,EQR,MCK,TDG,PEG,TEL,F,ED,HLT,ORLY,APH,IQV,EBAY,DLR,PAYX,TWTR,FE,EIX,VRSK,PPG,STT,VFC,O,WLTW,MNST,PH,ETR,LUV,FLT,DTE,MSCI,PPL,AZO,PCAR,BLL,CMI,A,AWK,WMB,KLAC,RMD,KR,MCHP,CTAS,ADM,ANSS,HSY,ROK,VTR,IDXX,CERN,DFS,CTVA,SWK,CMG,PXD,TSN,ALXN,WY,SNPS,MTB,AME,XLNX,DLTR,APTV,FAST,FTV,ESS,LVS,CLX,VRSN,RSG,AMP,GLW,BXP,AEE,LYB,NTRS,HIG,DHI,CBRE,FITB,CDNS,MKC,AJG,BBY,LEN,CMS,FRC,SYF,ARE,CPRT,SWKS,CDW,EFX,KEY_,WDC,CHD,LH,PEAK,HPE,MTD,HAL,ALGN,VMC,CAH,COO,KEYS_,KSU,DOV,TFX,OMC,MAA,RCL,KHC,UAL,EVRG,ULTA,CINF,FCX,IP,KMX,AMCR,MXIM,K,AKAM,CFG,HES,MLM,EXPE,MGM,XYL,FTNT,LDOS,RF,CCL,DGX,CXO,UDR,PAYC,VIAC,ABC,NUE,DRI,TIF,STE,CAG,HBAN,INCY,GPC,LW,ATO,DRE,NVR,LNT,J,EXR,GRMN,CTXS,ODFL,HOLX,IFF,L,CBOE,WAT,WAB,FMC,PFG,AES,BR,NDAQ,IT,GWW,MAS,MKTX,ARNC,JKHY,IEX,BKR,TTWO,CE,SIVB,CNP,CTL,EXPD,SJM,BF_B,VAR,ZBRA,XRAY,FOXA,HRL,STX,HST,ALLE,ANET,PHM,FANG,RJF,WYNN,TSCO,UHS,NTAP,ETFC,RE,NLOK,QRVO,PNW,WRB,HAS,LNC,NI,AVY,GL,URI,WU,REG,TXT,MYL,TAP,AAL,APA,LKQ,VNO,CHRW,DISH,PKI,HII,EMN,AAP,FBHS,NRG,LYV,WRK,HSIC,IRM,ALB,PKG,IPG,NCLH,DISCK,JBHT,FRT,SNA,WHR,CMA,CF,AIZ,NOV,AIV,CPB,PRGO,JNPR,NBL,KIM,FFIV,ALK,MHK,FLIR,MRO,DVA,SLG,NLSN,ZION,DVN,ABMD,DXC,PNR,PBCT,TPR,NWL,KSS,BEN,MOS,FTI,RHI,XRX,BWA,IVZ,COG,HFC,PVH,AOS,UNM,PWR,ROL,LEG,FLS,FOX,RL,HOG,LB,SEE,HBI,NWSA,M,IPGP,HP,HRB,DISCA,JWN,ADS,CPRI,XEC,GPS,COTY,UAA,UA,NWS'
        f_505 = "%s," *505
        cursor.executemany('insert into sp500_s ({0}) values ({1})'.format(sp500,f_505[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    url = 'https://www.slickcharts.com/sp500'
    html = call_page(url)
    content = parse_html(html)
    insertDB(content)





# create table sp500_s(id int not null primary key auto_increment,MSFT  float,AAPL  float,AMZN  float,FB  float,BRK_B  float,GOOGL  float,GOOG  float,JPM  float,JNJ  float,V  float,PG  float,MA  float,T  float,INTC  float,BAC  float,UNH  float,HD  float,VZ  float,DIS  float,XOM  float,KO  float,MRK  float,CMCSA  float,PEP  float,CVX  float,PFE  float,CSCO  float,WFC  float,ADBE  float,BA  float,NVDA  float,CRM  float,WMT  float,NFLX  float,MCD  float,C  float,BMY  float,ABT  float,MDT  float,COST  float,ABBV  float,PYPL  float,NEE  float,PM  float,ACN  float,IBM  float,TMO  float,AMGN  float,HON  float,UNP  float,NKE  float,UTX  float,LLY  float,AVGO  float,ORCL  float,TXN  float,LIN  float,AMT  float,LMT  float,GE  float,DHR  float,SBUX  float,QCOM  float,LOW  float,FIS  float,GILD  float,CVS  float,MMM  float,AXP  float,MDLZ  float,CHTR  float,MO  float,ADP  float,USB  float,BKNG  float,CME  float,TJX  float,CI  float,DUK  float,INTU  float,D  float,CAT  float,CB  float,TFC  float,GS  float,SPGI  float,SO  float,PLD  float,ANTM  float,SYK  float,UPS  float,CCI  float,BDX  float,ISRG  float,FISV  float,ZTS  float,PNC  float,AGN  float,CL  float,NOW  float,BLK  float,COP  float,MS  float,VRTX  float,MU  float,CSX  float,GPN  float,RTN  float,BIIB  float,TGT  float,AMD  float,MMC  float,BSX  float,NOC  float,AMAT  float,EQIX  float,APD  float,DE  float,ITW  float,NSC  float,AON  float,ICE  float,ECL  float,SCHW  float,AEP  float,LHX  float,WM  float,KMB  float,ATVI  float,PGR  float,EXC  float,EW  float,SHW  float,HUM  float,COF  float,BAX  float,EL  float,ROST  float,SRE  float,LRCX  float,ADI  float,MCO  float,SPG  float,GD  float,SLB  float,ADSK  float,EMR  float,KMI  float,ETN  float,DG  float,GM  float,ILMN  float,NEM  float,EOG  float,AIG  float,ALL_  float,ROP  float,SYY  float,MET  float,PSX  float,DD  float,HCA  float,FDX  float,CTSH  float,XEL  float,WBA  float,MAR  float,MPC  float,BK  float,AFL  float,PRU  float,OXY  float,WELL  float,TRV  float,CNC  float,DOW  float,IR  float,REGN  float,PSA  float,STZ  float,SBAC  float,HPQ  float,GIS  float,JCI  float,VLO  float,WEC  float,ZBH  float,AVB  float,DAL  float,EA  float,MSI  float,INFO  float,TROW  float,OKE  float,ES  float,YUM  float,TMUS  float,EQR  float,MCK  float,TDG  float,PEG  float,TEL  float,F  float,ED  float,HLT  float,ORLY  float,APH  float,IQV  float,EBAY  float,DLR  float,PAYX  float,TWTR  float,FE  float,EIX  float,VRSK  float,PPG  float,STT  float,VFC  float,O  float,WLTW  float,MNST  float,PH  float,ETR  float,LUV  float,FLT  float,DTE  float,MSCI  float,PPL  float,AZO  float,PCAR  float,BLL  float,CMI  float,A  float,AWK  float,WMB  float,KLAC  float,RMD  float,KR  float,MCHP  float,CTAS  float,ADM  float,ANSS  float,HSY  float,ROK  float,VTR  float,IDXX  float,CERN  float,DFS  float,CTVA  float,SWK  float,CMG  float,PXD  float,TSN  float,ALXN  float,WY  float,SNPS  float,MTB  float,AME  float,XLNX  float,DLTR  float,APTV  float,FAST  float,FTV  float,ESS  float,LVS  float,CLX  float,VRSN  float,RSG  float,AMP  float,GLW  float,BXP  float,AEE  float,LYB  float,NTRS  float,HIG  float,DHI  float,CBRE  float,FITB  float,CDNS  float,MKC  float,AJG  float,BBY  float,LEN  float,CMS  float,FRC  float,SYF  float,ARE  float,CPRT  float,SWKS  float,CDW  float,EFX  float,KEY_  float,WDC  float,CHD  float,LH  float,PEAK  float,HPE  float,MTD  float,HAL  float,ALGN  float,VMC  float,CAH  float,COO  float,KEYS_  float,KSU  float,DOV  float,TFX  float,OMC  float,MAA  float,RCL  float,KHC  float,UAL  float,EVRG  float,ULTA  float,CINF  float,FCX  float,IP  float,KMX  float,AMCR  float,MXIM  float,K  float,AKAM  float,CFG  float,HES  float,MLM  float,EXPE  float,MGM  float,XYL  float,FTNT  float,LDOS  float,RF  float,CCL  float,DGX  float,CXO  float,UDR  float,PAYC  float,VIAC  float,ABC  float,NUE  float,DRI  float,TIF  float,STE  float,CAG  float,HBAN  float,INCY  float,GPC  float,LW  float,ATO  float,DRE  float,NVR  float,LNT  float,J  float,EXR  float,GRMN  float,CTXS  float,ODFL  float,HOLX  float,IFF  float,L  float,CBOE  float,WAT  float,WAB  float,FMC  float,PFG  float,AES  float,BR  float,NDAQ  float,IT  float,GWW  float,MAS  float,MKTX  float,ARNC  float,JKHY  float,IEX  float,BKR  float,TTWO  float,CE  float,SIVB  float,CNP  float,CTL  float,EXPD  float,SJM  float,BF_B  float,VAR  float,ZBRA  float,XRAY  float,FOXA  float,HRL  float,STX  float,HST  float,ALLE  float,ANET  float,PHM  float,FANG  float,RJF  float,WYNN  float,TSCO  float,UHS  float,NTAP  float,ETFC  float,RE  float,NLOK  float,QRVO  float,PNW  float,WRB  float,HAS  float,LNC  float,NI  float,AVY  float,GL  float,URI  float,WU  float,REG  float,TXT  float,MYL  float,TAP  float,AAL  float,APA  float,LKQ  float,VNO  float,CHRW  float,DISH  float,PKI  float,HII  float,EMN  float,AAP  float,FBHS  float,NRG  float,LYV  float,WRK  float,HSIC  float,IRM  float,ALB  float,PKG  float,IPG  float,NCLH  float,DISCK  float,JBHT  float,FRT  float,SNA  float,WHR  float,CMA  float,CF  float,AIZ  float,NOV  float,AIV  float,CPB  float,PRGO  float,JNPR  float,NBL  float,KIM  float,FFIV  float,ALK  float,MHK  float,FLIR  float,MRO  float,DVA  float,SLG  float,NLSN  float,ZION  float,DVN  float,ABMD  float,DXC  float,PNR  float,PBCT  float,TPR  float,NWL  float,KSS  float,BEN  float,MOS  float,FTI  float,RHI  float,XRX  float,BWA  float,IVZ  float,COG  float,HFC  float,PVH  float,AOS  float,UNM  float,PWR  float,ROL  float,LEG  float,FLS  float,FOX  float,RL  float,HOG  float,LB  float,SEE  float,HBI  float,NWSA  float,M  float,IPGP  float,HP  float,HRB  float,DISCA  float,JWN  float,ADS  float,CPRI  float,XEC  float,GPS  float,COTY  float,UAA  float,UA  float,NWS  float) engine=InnoDB  charset=utf8;


# drop table sp500_s;



# mei
#*/3 * * * * /usr/local/bin/python3.6 /root/SP500_Nasdap100/SP500.py