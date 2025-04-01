from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
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

@app.route('/commits/')
def commits():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': 'Problème avec l\'API GitHub', 'status_code': response.status_code}), 500

        commits_data = response.json()

        
        if not isinstance(commits_data, list):
            return jsonify({'error': 'Format de réponse invalide'}), 500

        
        commit_counts = {}
        for commit in commits_data:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_obj.strftime('%Y-%m-%d %H:%M')

            if minute not in commit_counts:
                commit_counts[minute] = 0
            commit_counts[minute] += 1

        results = [{'minute': minute, 'commit_count': count} for minute, count in commit_counts.items()]

        return jsonify(results=results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
  app.run(debug=True)
