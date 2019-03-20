
# coding: utf-8

# In[2]:


import numpy as np

import cv2

def transfer() :
    img = cv2.imread('D://source/tes.jpg')
    h = img.shape[0]
    w = img.shape[1]
    tL = [16,348]
    tR = [293,379]
    bL = [15,483]
    bR = [289,525]
    
    pts = np.float32([tL,tR,bR,bL])
    
    w1 = abs(bR[0]-bL[0])
    w2 = abs(tR[0]-tL[0])
    h1 = abs(tR[1]-bR[1])
    h2 = abs(tL[1]-bL[1])
    
    mW = min([w1,w2])
    mH = min([h1,h2])
    
    npts = np.float32([[0,0], [mW-1,0],[mW-1,mH-1],[0,mH-1]])
    
    M = cv2.getPerspectiveTransform(pts,npts)
    
    result = cv2.warpPerspective(img,M,(int(mW),int(mH)))
    
    cv2.imshow('original',img)
    cv2.imshow('Wrap Transfer',result)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__' :
    transfer()

