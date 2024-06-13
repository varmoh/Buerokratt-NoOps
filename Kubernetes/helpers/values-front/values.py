from flask import Flask, render_template, request, redirect, url_for
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString

app = Flask(__name__)

# Paths to your values files
ruuter_values_path = '../../Components/Ruuter/values.yaml'
resql_values_path = '../../Components/Resql/values.yaml'

yaml = YAML()
yaml.preserve_quotes = True  # Preserve quotes when dumping YAML

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file)

def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

@app.route('/')
def index():
    ruuter_values = load_yaml(ruuter_values_path)
    resql_values = load_yaml(resql_values_path)
    return render_template('index.html', ruuter=ruuter_values, resql=resql_values)

@app.route('/update', methods=['POST'])
def update():
    # Extract form data
    ruuter_tag = request.form['ruuter_tag']
    resql_tag = request.form['resql_tag']

    # Load current values
    ruuter_values = load_yaml(ruuter_values_path)
    resql_values = load_yaml(resql_values_path)

    # Update only the image tags
    if 'images' in ruuter_values and 'scope' in ruuter_values['images']:
        ruuter_values['images']['scope']['tag'] = SingleQuotedScalarString(ruuter_tag)

    if 'images' in resql_values and 'scope' in resql_values['images']:
        resql_values['images']['scope']['tag'] = SingleQuotedScalarString(resql_tag)

    # Save updated values
    save_yaml(ruuter_values_path, ruuter_values)
    save_yaml(resql_values_path, resql_values)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
