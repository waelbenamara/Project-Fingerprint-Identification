from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
from Fingerprint import FingerPrint 
import pickle
from comparator import identify_fingerprint
from new_person import new_per
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# default access page
@app.route("/")
def main():
    return render_template('index.html')


# upload selected image and forward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')
    for file in os.listdir('static/images/'):
        os.remove("static/images/"+file)
    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp") or (ext == ".JPG") or (ext == ".JPG"):
        print("File accepted")
    else:
        return render_template("error.html", message="The selected file is not supported"), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)

    # forward to processing page
    return render_template("processing.html", image_name=filename)


z=-1
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

@app.route("/binarize", methods=["POST","GET"])
def binarize():
    
    fp=FingerPrint("./static/images/")
    loaded_model=pickle.load(open("detection_model.sav", 'rb')) 
    fp.dataload()
    x=fp.getres()
    result=str(loaded_model.predict([x[0]]))
    if "0" in result:
        s="It is not a fingerprint"
        z=0
    else:
        s="It is a fingerprint"  
        z=1 
    print(result)
    print(s)  

    if z==1 :
        template = "result1.html"
    else:
        template="result2.html"   
    return render_template(template,message=s)
     #return result


@app.route("/identify",methods=["POST","GET"]) 
def identify():
    y=identify_fingerprint()
    return render_template("resultc.html",message=y)   



@app.route("/newp",methods=["POST","GET"])
def newp():
    result=  request.form["newname"]
    newname=str(result)
    global tmp 
    tmp=newname
    new_per(newname)

    return render_template("uploading.html")

@app.route("/upload_new",methods=["POST","GET"])
def upload_new():
    target = os.path.join(APP_ROOT, 'people/'+tmp)
   
    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp") or (ext == ".JPG") or (ext == ".JPG"):
        print("File accepted")
    else:
        return render_template("error.html", message="The selected file is not supported"), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)
    return render_template("uploading.html")

if __name__ == "__main__":
    app.run(debug=True)
    

