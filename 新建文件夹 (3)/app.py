from flask import Flask, render_template, request, jsonify
import os
import datetime
from openai import OpenAI


app = Flask(__name__)

#
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

#
@app.route('/')
def index():
    return render_template('index.html')

#
@app.route('/process', methods=['POST'])
def process():
    selected_text = request.form['selected_text']

    # Call the OpenAI API to get chat completion
    completion = client.chat.completions.create(
        model="meta/llama-3.1-405b-instruct",
        messages=[{"role": "user", "content": selected_text}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Collect the response in chunks
    output = []
    for chunk in completion:
        if chunk.choices[0].delta.content:
            output.append(chunk.choices[0].delta.content)

    gpt_response = ''.join(output)

    return jsonify({'gpt_response': gpt_response})

#
@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join('notes', folder_name)

    try:
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'文件夹 {folder_name} 已创建'})
    except Exception as e:
        return jsonify({'message': f'创建文件夹时出错: {str(e)}'}), 500

#
@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join('notes', folder_name)

    try:
        if os.path.exists(folder_path):
            os.rmdir(folder_path)
            return jsonify({'message': f'文件夹 {folder_name} 已删除'})
        else:
            return jsonify({'message': '文件夹不存在'}), 404
    except Exception as e:
        return jsonify({'message': f'删除文件夹时出错: {str(e)}'}), 500

#
@app.route('/save_note', methods=['POST'])
def save_note():
    folder_name = request.form['folder_name']
    note_content = request.form['note_content']

    folder_path = os.path.join('notes', folder_name)
    os.makedirs(folder_path, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'note_{timestamp}.txt'
    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as note_file:
            note_file.write(note_content)
        return jsonify({'message': f'笔记已保存到 {file_path}'})
    except Exception as e:
        return jsonify({'message': f'保存笔记时出错: {str(e)}'}), 500


@app.route('/list_folders', methods=['GET'])
def list_folders():
    try:
        folders = os.listdir('notes')
        return jsonify({'folders': folders})
    except Exception as e:
        return jsonify({'message': f'列出文件夹时出错: {str(e)}'}), 500


@app.route('/list_notes', methods=['POST'])
def list_notes():
    folder_name = request.form['folder_name']
    folder_path = os.path.join('notes', folder_name)

    try:
        if os.path.exists(folder_path):
            notes = os.listdir(folder_path)
            return jsonify({'notes': notes})
        else:
            return jsonify({'message': '文件夹不存在'}), 404
    except Exception as e:
        return jsonify({'message': f'列出笔记时出错: {str(e)}'}), 500


@app.route('/get_note', methods=['POST'])
def get_note():
    folder_name = request.form['folder_name']
    note_name = request.form['note_name']
    note_path = os.path.join('notes', folder_name, note_name)

    try:
        if os.path.exists(note_path):
            with open(note_path, 'r', encoding='utf-8') as note_file:
                content = note_file.read()
            return jsonify({'content': content})
        else:
            return jsonify({'message': '笔记不存在'}), 404
    except Exception as e:
        return jsonify({'message': f'读取笔记时出错: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)