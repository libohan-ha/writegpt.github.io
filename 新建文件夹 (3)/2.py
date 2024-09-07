from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    os.makedirs(folder_name, exist_ok=True)
    return jsonify({'message': f'Folder "{folder_name}" created successfully'})

@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form['folder_name']
    try:
        os.rmdir(folder_name)
        return jsonify({'message': f'Folder "{folder_name}" deleted successfully'})
    except OSError as e:
        return jsonify({'message': str(e)})

@app.route('/save_note', methods=['POST'])
def save_note():
    folder_name = request.form['folder_name']
    note_content = request.form['note_content']
    with open(os.path.join(folder_name, 'note.txt'), 'w') as file:
        file.write(note_content)
    return jsonify({'message': 'Note saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
