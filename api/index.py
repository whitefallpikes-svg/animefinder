from flask import Flask, request, jsonify, send_from_directory
import urllib.request, urllib.parse, json

app = Flask(__name__, static_folder='..', static_url_path='')

SERPAPI='https://serpapi.com/search.json'
GEMINI='https://generativelanguage.googleapis.com/v1beta/models'
MODELS=['gemini-3.5-flash-lite','gemini-3.8-flash','gemini-flash-latest']

@app.get('/')
def home():
    return send_from_directory('..','index.html')

@app.get('/api/search')
def search():
    key=request.args.get('key','')
    q=request.args.get('q','')
    page=request.args.get('ijn','0')
    tbs=request.args.get('tbs','')
    if not key or not q:
        return jsonify({'error':'SerpApi anahtarı veya arama eksik'}),400
    params={'engine':'google_images','q':q,'safe':'active','api_key':key,'ijn':page}
    if tbs:
        params['tbs']=tbs
    url=SERPAPI+'?'+urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url,timeout=20) as r:
            data=json.loads(r.read())
        return jsonify(data)
    except Exception as e:
        return jsonify({'error':str(e)}),502

@app.post('/api/gemini')
def gemini():
    key=request.headers.get('x-goog-api-key','')
    if not key:
        return jsonify({'error':'Gemini anahtarı yok'}),400
    body=request.get_data()
    last=''
    for model in MODELS:
        url=f'{GEMINI}/{model}:generateContent'
        req=urllib.request.Request(url,data=body,headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=15) as r:
                data=json.loads(r.read())
            return jsonify(data)
        except Exception as e:
            last=str(e)
            continue
    return jsonify({'error':'Gemini modelleri denendi: '+last}),502
