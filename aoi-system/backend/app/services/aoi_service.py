import cv2, numpy as np
class AOIService:
    @staticmethod
    def detect_defects(path, t_path, threshold=30):
        img=cv2.imread(path,0); tmp=cv2.GaussianBlur(img,(15,15),5); diff=cv2.absdiff(tmp,img)
        _,th=cv2.threshold(diff,threshold,255,0); k=cv2.getStructuringElement(2,(5,5)); cl=cv2.morphologyEx(th,2,k)
        cnt,_=cv2.findContours(cl,1,2); res=cv2.cvtColor(img,8); defs=[]
        for c in cnt:
            a=cv2.contourArea(c)
            if a<50: continue
            x,y,w,h=cv2.boundingRect(c); cv2.drawContours(res,[c],-1,(0,0,255),2); cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
            defs.append({"id":len(defs)+1,"position":{"x":int(x+w//2),"y":int(y+h//2)},"area":float(a),"bbox":{"x":int(x),"y":int(y),"width":int(w),"height":int(h)}})
        return {"defects":defs,"defect_count":len(defs),"annotated_image":res}
    @staticmethod
    def measure_dimensions(path,pmm=0.1):
        img=cv2.imread(path,0); e=cv2.Canny(img,50,150); cnt,_=cv2.findContours(e,1,2); res=cv2.cvtColor(img,8); ms=[]
        for i,c in enumerate(cnt):
            a=cv2.contourArea(c)
            if a<100: continue
            x,y,w,h=cv2.boundingRect(c); cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
            p=cv2.arcLength(c,1); circ=4*np.pi*a/(p*p) if p>0 else 0
            m={"object_id":i+1,"shape":"circle" if circ>0.8 else "rectangle","width_mm":round(w*pmm,2),"height_mm":round(h*pmm,2),"area_mm2":round(a*pmm*pmm,2),"bbox":{"x":int(x),"y":int(y),"width":int(w),"height":int(h)}}
            if circ>0.8: m["diameter_mm"]=round(2*np.sqrt(a/np.pi)*pmm,2)
            ms.append(m)
        return {"measurements":ms,"annotated_image":res}
    @staticmethod
    def detect_fiducial_marks(path,minr=5,maxr=25):
        img=cv2.imread(path,0); b=cv2.GaussianBlur(img,(5,5),1.5); c=cv2.HoughCircles(b,3,1,100,param1=100,param2=30,minRadius=minr,maxRadius=maxr)
        res=cv2.cvtColor(img,8); ms=[]; ang=None
        if c is not None:
            for i,(cx,cy,r) in enumerate(np.uint16(np.around(c))[0]):
                cv2.circle(res,(cx,cy),r,(0,255,0),2); ms.append({"id":i+1,"position":{"x":int(cx),"y":int(cy)},"radius":int(r)})
            if len(ms)>=2:
                p1,p2=ms[0]["position"],ms[1]["position"]; ang=float(np.degrees(np.arctan2(p2["y"]-p1["y"],p2["x"]-p1["x"])))
        return {"marks":ms,"rotation_angle":round(ang,2) if ang else None,"annotated_image":res}
