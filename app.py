from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    if not file:
        message = "File not found"
        return render_template('index.html', message=message)
    df = pd.read_csv(file)
    columns = ['product']  # Specify the column names you want to modify

    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        message = f"Columns not found in CSV: {', '.join(missing_columns)}"
        return render_template('index.html', message=message)

    column_data = {col: df[col].tolist() for col in columns}
    # Modify the specified values in column_data
    for col in column_data:
        if col in columns:
            for i in range(len(column_data[col])):
                value = column_data[col][i]
                if isinstance(value, str) and ' ' in value:
                    modified_value = re.sub(r'(\d+)\s(\d+)', r'\1/\2', value)

                    column_data[col][i] = modified_value


    df['product'] = column_data['product']

    material_totals = df.groupby('product')['tons'].sum().to_dict()


    items = df.values.tolist()

    return render_template('list.html', items=items, material_totals=material_totals)

if __name__ == '__main__':
    app.run(debug=True)
