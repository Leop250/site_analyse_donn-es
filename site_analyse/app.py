from flask import Flask, request, render_template, send_file, redirect, url_for, abort
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        separator = request.form.get('separator', ',')  # Default separator is comma
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('operations', filename=file.filename, separator=separator))
    return render_template('index.html')

@app.route('/path', methods=['POST'])
def handle_path():
    file_path = request.form['filepath']
    separator = request.form.get('separator', ',')  # Default separator is comma
    if os.path.exists(file_path) and os.path.isfile(file_path):
        filename = os.path.basename(file_path)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.system(f"cp '{file_path}' '{saved_path}'")
        return redirect(url_for('operations', filename=filename, separator=separator))
    else:
        return "The provided file path does not exist or is not a file. Please go back and try again.", 400

@app.route('/operations/<filename>', methods=['GET', 'POST'])
def operations(filename):
    separator = request.args.get('separator', ',')  # Retrieve the separator from the query string
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path, sep=separator)
    if request.method == 'POST':
        operation = request.form.get('operation')
        column = request.form.get('column')
        
        if operation == 'read':
            result = df.to_html(classes='table table-striped', border=0)
        elif operation == 'mean':
            numeric_df = df.select_dtypes(include=[np.number])
            result = numeric_df.mean().to_frame('Mean').to_html(classes='table table-striped', border=0)
        elif operation == 'median':
            numeric_df = df.select_dtypes(include=[np.number])
            result = numeric_df.median().to_frame('Median').to_html(classes='table table-striped', border=0)
        elif operation == 'std_dev':
            numeric_df = df.select_dtypes(include=[np.number])
            result = numeric_df.std().to_frame('Standard Deviation').to_html(classes='table table-striped', border=0)
        elif operation == 'plot_histogram':
            if column and column in df.columns:
                plt.figure()
                df[column].dropna().hist()
                img = io.BytesIO()
                plt.savefig(img, format='png')
                plt.close()
                img.seek(0)
                return send_file(img, mimetype='image/png')
            else:
                result = "Colonne spécifiée non trouvée."
        elif operation == 'plot_bar':
            if column and column in df.columns:
                plt.figure()
                df[column].value_counts().plot(kind='bar')
                img = io.BytesIO()
                plt.savefig(img, format='png')
                plt.close()
                img.seek(0)
                return send_file(img, mimetype='image/png')
        elif operation == 'plot_box':
            numeric_df = df.select_dtypes(include=[np.number])
            plt.figure()
            numeric_df.plot(kind='box')
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            return send_file(img, mimetype='image/png')
        elif operation == 'clean_data':
            df_clean = df.dropna()
            result = df_clean.to_html(classes='table table-striped', border=0)
        elif operation == 'sort_data':
            if column and column in df.columns:
                df_sorted = df.sort_values(by=column)
                result = df_sorted.to_html(classes='table table-striped', border=0)
            else:
                result = "Colonne spécifiée non trouvée."
        elif operation == 'save_data':
            df.to_csv(file_path, index=False)
            result = f"Fichier sauvegardé avec succès à {file_path}"
        else:
            result = 'Operation not supported'
        return render_template('operations.html', result=result, filename=filename)
    return render_template('operations.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
