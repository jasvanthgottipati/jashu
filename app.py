from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime


def replacement(str, str1, sub):
    index=str.find(str1)
    while index!=-1:
        a=str[:index]+sub+str[index+len(str1):];
        str=a;
        index=str.find(str1);
    return str
            
def splitting(str, sp):
    a=list()
    index=str.find(sp)
    while index!=-1:
        a.append(str[:index])
        str=str[index+len(sp):]
        index=str.find(sp)
    a.append(str)
    return a


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html') 
    
@app.route('/first', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        f = request.files['fileup']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f = open(app.config['UPLOAD_FOLDER']+filename,'r')
        a=f.read()


        a=splitting(a,'\n')
        #print(a)
        f.close()
        totalmin=0;
        ft="%I:%M:%p"
        for i in a:
            i1=i.lower();
            if i1.find("time log:")!=-1:
                a.remove(i);
                break;
            else:
                a.remove(i);
        for i in a:
            i1=i.lower();
            i1=replacement(i1,"- ","-")
            i1=replacement(i1," -","-")
            #print(i1)
            i1=splitting(i1," ");
            #print(i1)
            for word in i1:
                if word.find('-')!=-1:
                    word1=splitting(word,'-')
                    #word1=word.split('-')
                    #print(word1)
                    word2=word1[1];
                    word1=word1[0];
                    try:
                        word1=word1[:-2]+':'+word1[-2:]
                        word2=word2[:-2]+':'+word2[-2:]
                        #print(word1,word2)
                        t1= datetime.strptime(word1,ft)
                        t2= datetime.strptime(word2,ft)
                    except:
                        #print(sys.exc_info())
                        continue;
                    totalmin= totalmin + (t2-t1).seconds/60
        ans="Total time spent is "+str(int((totalmin)/60))+" hours "+str(int((totalmin)%60))+" minutes"
        return render_template('index.html',answer=ans)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
