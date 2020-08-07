'''
 * @author Waileinsamkeit
 * @email Zenglz_pro@163.com
 * @create date 2020-08-07 15:51:58
 * @modify date 2020-08-07 15:51:58
'''



from sklearn.metrics import confusion_matrix
import numpy as np

class Eval_unit(object):
    def __init__(self,tp,fp,fn,tn,label):
        super(Eval_unit,self).__init__()
        self.id=label
        self.d={'tp':tp,'fp':fp,'fn':fn,'tn':tn}
        self.accuracy=self.cal_accuracy(tp,fp,fn,tn)
        self.precision=self.cal_precision(tp,fp,fn,tn)
        self.recall=self.cal_recall(tp,fp,fn,tn)
        self.f1_score=self.cal_f1_score(tp,fp,fn,tn)
    
    def __getattr__(self,name):
        return self[name] if name in self.__dict__ else self.d[name]

    def show(self):
        pass

    @classmethod
    def cal_accuracy(cls,tp:int,fp:int,fn:int,tn:int)->float:
        return float(tp+tn)/(tp+tn+fp+fn)
    
    @classmethod
    def cal_precision(cls,tp:int,fp:int,fn:int,tn:int)->float:
        return float(tp)/(tp+fp)
    
    @classmethod
    def cal_recall(cls,tp:int,fp:int,fn:int,tn:int)->float:
        return float(tp)/(tp+fn)
    
    @classmethod
    def cal_f1_score(cls,tp:int,fp:int,fn:int,tn:int)->float:
        p=cls.cal_precision(tp,fp,fn,tn)
        r=cls.cal_recall(tp,fp,fn,tn)
        return 2*p*r/(r+p)


def evaluate_single_label(pred,label,classes):
    matrix=confusion_matrix(pred,label,classes)
    TP=np.diag(matrix)
    FP=matrix.sum(axis=1)-TP
    FN=matrix.sum(axis=0)-TP
    TN=matrix.sum()-TP-FN-FP
    unit_list=[]
    for i in range(classes):
        cla=classes[i]
        unit=Eval_unit(TP[i],FP[i],FN[i],TN[i],cla)
        unit_list.append(unit)
    return unit_list

"""
B-LOC
I-LOC

B-ORG
I-ORG

B-PER
I-PER

O
"""
def evaluate_entity_label(pred,label,classes):
    assert len(pred)==len(label)
    cla=[i.split('-')[-1] for i in classes if i!='O']
    cla=list(set(cla))
    cla2ind={}
    cla2ind=dict((c,ind) for ind,c in enumerate(cla))
    index=0;
    pred_entities=np.zeros(len(cla),dtype=int) #TP+FP
    label_entities=np.zeros(len(cla),dtype=int) #TP+FN
    acc=np.zeros(len(cla),dtype=int) #TP
    while index<len(pred):
        label_tag=label[index]
        if label_tag=='O':
            index+=1
        else:
            c=label_tag.split('-')[-1]
            c=cla2ind[c]
            next_tag='I'+label_tag[1:]
            j=index+1
            while label[j]==next_tag:
                j+=1
            label_entities[c]+=1
            label_entity= ''.join(label[index:j])
            pred_entity=''.join(pred[index:j])
            if label_entity==pred_entity:
                acc[c]+=1
            index=j
    index=0
    while index<len(pred):
        pred_tag=pred[index]
        if pred_tag=='0':
            index+=1
        elif pred_tag.split('-')[0]=='B':
            c=label_tag.split('-')[-1]
            c=cla2ind[c]
            next_tag='I'+label_tag[1:]
            j=index+1
            while pred[j]==next_tag:
                j+=1
            pred_entities[c]+=1
            index=j
    units=[]
    TP=acc
    FP=pred_entities-acc
    FN=label_entities-acc
    TN=acc.sum()-acc
    for c,ind in cla2ind.items():
        units.append(Eval_unit(TP[ind],FP[ind],FN[ind],TN[ind],c))
    return units


def evaluate_multiclass(units:list,type:str):
    assert type in ['macro','micro']
    if type=='macro':
        P=float(sum([unit.precision for unit in units]))/len(units)
        R=float(sum([unit.recall for unit in units]))/len(units)

    else:
        tp=float(sum([unit.tp for unit in units]))/len(units)
        fp=float(sum([unit.fp for unit in units]))/len(units)
        fn=float(sum([unit.fn for unit in units]))/len(units)
        P=tp/(tp+fp)
        R=tp/(tp+fn)
    f1=2*P*R/(P+R)
    return P,R,f1


if __name__=='__main__':
    k=Eval_unit(1,2,3,4,'test')
    print(k.__dict__)
    setattr(k,"id","name")
    print(k.__dict__)
    print(k.precision)
    print(k.tp)
         
