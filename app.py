from flask import Flask, render_template, request, redirect, send_file, url_for
import csv
import json
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jsonGenerator', methods=['POST'])
def jsonGenerator():
    if request.method == 'POST':
        return render_template('jsonGen.html')

@app.route('/menuParser', methods=['POST'])
def menuParser():
    if request.method == 'POST':
        return render_template('menuParse.html')

@app.route('/generateJSON', methods=['POST'])
def generateJSON():
    if request.method == 'POST':
        hostel = request.form['hostel']
        mess = request.form['mess']
        file = request.files['menu']
        if not os.path.isdir('static'):
            os.mkdir('static')
        if os.path.isfile("static/menu.csv"):
            os.remove("static/menu.csv")
        filepath = os.path.join('static', file.filename)
        menu = "static/menu.csv"
        file.save(filepath)
        os.rename(filepath, menu)

        hostel_dict={"MH":1, "LH":2}
        mess_dict={"Special":1, "Veg":2, "NonVeg":3}
        json_menu={"hostel":hostel_dict[hostel],"mess":mess_dict[mess],"menu":[]}

        with open(menu) as file_obj:
            reader_obj=csv.reader(file_obj)
            for row in reader_obj:
                menu_json={}
                menu_json["date"]=row[0]
                menu_json["menu"]=[]
                for i in range(1,len(row)):
                    menu_json["menu"].append({"type":i,"menu":row[i].replace('\n',', ')})
                json_menu["menu"].append(menu_json)

        jsonFileName='menu-'+hostel+'-'+mess+'.json'
        if os.path.isfile("static/"+jsonFileName):
            os.remove("static/"+jsonFileName)
        with open("static/"+jsonFileName,'w') as file_obj:
            json.dump(json_menu,file_obj)

        return send_file('static/'+jsonFileName, as_attachment=True)

@app.route('/parseMenu', methods=['POST'])
def parseMenu():
    if request.method == 'POST':
        file = request.files['menu']
        extension=file.filename.split('.')[-1]
        menu = "static/menu"+"."+extension
        if not os.path.isdir('static'):
            os.mkdir('static')
        if os.path.isfile(menu):
            os.remove(menu)
        filepath = os.path.join('static', file.filename)
        file.save(filepath)
        os.rename(filepath, menu)

        url = 'https://app.nanonets.com/api/v2/OCR/Model/c6ae1aa4-0006-4a65-8001-f8492d3e20bf/LabelFile/?async=false'
        data = {'file': open(menu, 'rb')}
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('VMKD_k5J8_RNlzO9chHTYbnAjvuHbn63', ''), files=data)
        pred=json.loads(response.text)

        if os.path.isfile("static/prediction.txt"):
            os.remove("static/prediction.txt")
        f=open('static/prediction.txt','w')

        for content in pred['result'][0]['prediction'][0]['cells']:
            f.write(content['text']+'\n')

        return redirect(url_for('downloadTxt'))

@app.route('/downloadTxt', methods=['POST','GET'])
def downloadTxt():
    return send_file('static/prediction.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)