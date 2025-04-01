from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

# 🔹 Page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# 🔹 Page contact
@app.route('/contact/')
def contact():
    return render_template('contact.html')

# 🔹 Météo de Tawarano (exemple API)
@app.route('/tawarano/')
def meteo():
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin ➝ Celsius
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        
        return jsonify(results=results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🔹 Graphique d'évolution des températures
@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme.html')

# 🔹 Page du rapport
@app.route('/rapport/')
def mongraphique():
    return render_template('graphique.html')

# 🔹 Extraction des minutes depuis une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    
    except ValueError:
        return jsonify({'error': 'Format de date invalide'}), 400

# 🔹 Récupération des commits GitHub minute par minute
@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # 🔹 Ajout d'un User-Agent pour éviter le blocage
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': 'Problème avec l\'API GitHub', 'status_code': response.status_code}), 500

        commits_data = response.json()
        commit_counts = {}

        for commit in commits_data:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_obj.strftime('%Y-%m-%d %H:%M')  # 🔹 Format : YYYY-MM-DD HH:MM
            
            if minute not in commit_counts:
                commit_counts[minute] = 0
            commit_counts[minute] += 1

        results = [{'minute': minute, 'commit_count': count} for minute, count in commit_counts.items()]
        return jsonify(results=results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🔹 Affichage du graphique des commits
@app.route('/commits_graph/')
def commits_graph():
    return render_template('commits.html')

# 🔹 Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
