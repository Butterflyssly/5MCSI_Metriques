from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__) #commit                                                                                                                 
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

import requests
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Response


@app.route('/commits/')
def commits():
   
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

  
    commit_minutes = []
    for commit in commits_data:
        commit_time = commit['commit']['author']['date']
        commit_datetime = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(commit_datetime.minute)

   
    minute_counts = [commit_minutes.count(minute) for minute in range(60)]

    
    plt.figure(figsize=(10, 5))
    plt.bar(range(60), minute_counts, color='blue')
    plt.xlabel('Minute')
    plt.ylabel('Nombre de commits')
    plt.title('Nombre de commits par minute')

   
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return Response(img, mimetype='image/png')

if __name__ == "__main__":
  app.run(debug=True)
