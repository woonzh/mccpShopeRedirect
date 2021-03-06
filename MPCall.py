# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:40:15 2018

@author: woon.zhenhao
"""

import requests
import json
import pandas as pd
import TMSCall as tc

header=None

mainurl='https://www.urbanfox.store/rest/all/V1/'

def getHeader():
    global header
    if (header==None):
        url=mainurl+'integration/admin/token'
        
        body={
                "username": "ims",
                "password": "urbanfox2018"
                }
        
        response = requests.post(url, params = body)
        
        key = json.loads(response.content)
        
        header2={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer "+key
                }
        
        header=header2

def updateOrder(refNum, trNum, width, height, length, weight):
    global header
    url=mainurl+'order/readytoship'
    body={
        "referenceNumber": refNum,
        "trackingNumber": trNum,
        "width": width,
        "height": height,
        "length": length,
        "weight": weight
            }
    response=requests.post(url, headers = header, params = body)
    
    df=json.loads(response.content)
    
    print(df)
    
def updateInven(sku, qty, sellerid):
    getHeader()
    global header
    url=mainurl+'inventory/update'
    body={
        "sku": sku,
        "qty": qty,
        "seller": sellerid,
        }
    response=requests.post(url, headers=header, params=body)
    df=json.loads(response.content)
    return df
    
def getMCCPInventory(sku):
    global header
    url=mainurl+('stockItems/%s' %(sku))
    response=requests.get(url, headers=header)
    df=json.loads(response.content)
    return df["qty"]

def getUncompletedDeliveries():
    getHeader()
    result=pd.DataFrame(columns=['shipmend increment id','Tracking number', 'status'])
    global header
    url=mainurl+'shipments?searchCriteria[filterGroups][0][filters][0][field]=seller_id&searchCriteria[filterGroups][0][filters][0][value]=1'
#    url=mainurl+'shipments?searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=new order'
    
    response=requests.get(url,headers=header)
    df=json.loads(response.content)['items']
    
    for ship in df:
        shipId=ship['increment_id']
        try:
            tracking=ship['shipping_label']
        except:
            tracking="N.A"
        status='new order'
        ls=[shipId, tracking, status]
        result.loc[len(result)]=ls
    
    return result 
    
def updateOrders(df):
    getHeader()
    for i in list(range(len(df))):
        line=df.iloc[i]
        trnum=line["tracking number"]
        refnum=line["reference number"]
        width=line["width"]
        length=line["length"]
        height=line["height"]
        weight=line["weight"]
        updateOrder(header, refnum, trnum, width, height, length, weight)
        print(refnum + " updated")
        
def getMCCPProductList(sellerid):
    global header
    getHeader()
    url=mainurl+('products?searchCriteria[filter_groups][0][filters][0][field]=seller_id&searchCriteria[filter_groups][0][filters][0][value]='+str(sellerid))
    response=requests.get(url, headers=header)
    df=json.loads(response.content)
    items=df['items']
    ls=[]
    
    #remove seller id suffic and only for simple products
    for i in list(range(len(items))):
        itm=items[i]
        if itm['type_id']=='simple':
            sku=itm['sku']
            sku=sku[:-(len(str(sellerid))+1)]
            ls.append(sku)
    
    
    return ls

def getTimeNeeded(sellerid):
    multiplier=1.3
    items=getMCCPProductList(sellerid)
    itemCount=len(items)
    timeNeeded=itemCount*multiplier
    
    return timeNeeded
    
def getMCCPInventories(sellerid):
    result=pd.DataFrame(columns=['mccp sku','mccp qty', 'ims sku'])
    items=getMCCPProductList(sellerid)
    for imssku in items:
        mccpsku=imssku+"-"+str(sellerid)
        qty=getMCCPInventory(mccpsku)
        ls=[mccpsku,qty, imssku]
        result.loc[len(result)]=ls
            
    return result
        
def reconInven(sellerid, invenlist):
    result=[]
    for i in list(range(len(invenlist))):
        mccpqty=invenlist.iloc[i,1]
        imsqty=invenlist.iloc[i,3]
        if (int(mccpqty)!=int(imsqty)):
            imssku=invenlist.iloc[i,2]
            res=updateInven(imssku, imsqty, sellerid)
            result.append(res)
        else:
            result.append("N.A")
            
    invenlist['recon result']=result
    
    return invenlist

def getOrders(increment_id):
    getHeader()
    global header
    
    if len(increment_id)<9:
        increment_id=('0'*(9-len(increment_id)))+increment_id
    
    url=mainurl+'orders?searchCriteria[filter_groups][0][filters][0][field]=increment_id&searchCriteria[filter_groups][0][filters][0][value]='+increment_id
#    url=mainurl+'orders?searchCriteria[pageSize]=100&searchCriteria[currentPage]=4'
    response=requests.get(url, headers = header)
    
    df=json.loads(response.content)
    
    return df

def parseShipments(df, skuLst, nameLst):
    shipments=df['items']
    
    store={}
    shipStore={}
    count=0
    
    for ship in shipments:
        try:
            tn=ship['shipping_label']
            if tn[0:2]=='OL' or tn[0:2]=='ML':
                shipType='UF deliver'
                info=tc.getStatus(tn)
            else:
                shipType='self deliver'
                info={}
        except:
            tn="Nil"
            shipType='self deliver'
            info={}
        
        items=ship['items']
        itmLst=''
        for item in items:
            name=item['name']
            try:
                itId=skuLst.index(name)
                skuLst=skuLst.pop(itId)
                nameLst=nameLst.pop(itId)
            except:
                t=1
            itmLst+=" / "+name
        
        shipStore[count]={
            "tracking":tn,
            "shipType":shipType,
            "items":itmLst,
            "info":info
                }
    
        count+=1
        
    if count==0:
        summary= "no shipment has been found for this order."
    else:
        summary= str(count) + " shipments have been found for this order."
        
    store["summary"]=summary
    store["outstanding items"]=str(nameLst)
    store["count"]=count
    store["shipments"]=shipStore
         
    return store

def getOrderSKUs(orderNo):
    df=getOrders(orderNo)['items'][0]['items']
    skuLst=[]
    nameLst=[]
    for i in df:
        sku=i['sku']
        skuLst.append(sku)
        name=i['name']
        nameLst.append(name)
        
    return skuLst, nameLst

def parseIncrementId(incId):
    try:
        orderId=int(incId)
    except:
        incId=incId[5:]
        orderId=int(incId)
    
#    return orderId
    return str(orderId)

def getShipments(increment_id):
    getHeader()
    global header
    
    if len(increment_id)<9:
        increment_id=('0'*(9-len(increment_id)))+increment_id
                     
    skuLst, nameLst=getOrderSKUs(increment_id)
    
    order_id=parseIncrementId(increment_id)
    print(order_id)
    
#    url=mainurl+'shipments?searchCriteria[filter_groups][0][filters][0][field]=order_id&searchCriteria[filter_groups][0][filters][0][value]='+order_id
#    url=mainurl+'shipments?searchCriteria[pageSize]=10&searchCriteria[currentPage]=10'
#    response=requests.get(url, headers = header)
    
    url=mainurl+'shipments'
    body={
        "searchCriteria[filter_groups][0][filters][0][field]":"increment_id",
        "searchCriteria[filter_groups][0][filters][0][value]":"000000474"
            }
#    
    response=requests.get(url,headers=header, params=body)
#    
    df=json.loads(response.content)
    
    return df
    
    store=parseShipments(df, skuLst, nameLst)
        
    return store

#df=getShipments('730')
df=getOrders('000000730')
#sku=getOrderSKUs('835')