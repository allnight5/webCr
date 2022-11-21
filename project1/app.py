
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)

db = client.dbsparta
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    today = datetime.now()
    my_time = today.strftime('%Y.%m.%d')
    diarys = list(db.diary.find({}, {'_id':False}))
    return jsonify({'all_diary': diarys,'time_now':my_time})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    today = datetime.now()

    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    #파일 저장하기
    #
    file = request.files["file_give"]

    #확장자를 가져오는것(jpg.BDP.PNG 등)
    extension = file.filename.split('.')[-1]
    
    save_to = f'static/{filename}.{extension}'
    time = today.strftime('%Y.%m.%d')
    file.save(save_to)

    doc = {
        'title' : title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'time': time
    }
    db.diary.insert_one(doc)

    print(title_receive)

    return jsonify({'msg': '저장완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
