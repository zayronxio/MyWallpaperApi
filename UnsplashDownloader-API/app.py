from flask import Flask, jsonify, request, send_from_directory
import os
from unsplash_downloader import download_images

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

@app.route('/api/download', methods=['GET'])
def download():
    try:
        query = request.args.get('query')
        count = int(request.args.get('count', 10))

        if count > 30:
            return jsonify({"error": "El límite máximo es 30 imágenes"}), 400

        downloaded_files = download_images(query, count, DOWNLOAD_FOLDER)
        return jsonify({
            "status": "success",
            "query": query,
            "images": [f"/api/images/{file}" for file in downloaded_files]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/images/<filename>')
def get_image(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run()
