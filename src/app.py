import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Import fungsi kecocokan dari file matcher.py yang sejajar
from src.matcher import hitung_kecocokan

app = Flask(__name__)

# Konfigurasi folder penyimpanan file unggahan
# Menggunakan path absolut agar aman saat dieksekusi dari root folder project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder static/uploads sudah terbuat otomatis jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Batasi jenis file hanya untuk gambar saja
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routing Halaman Utama
@app.route("/")
def index():
    return render_template("index.html")

# Routing Proses Analisis & Hasil
@app.route("/result", methods=["POST"])
def result():
    # Validasi apakah ada file yang dikirim
    if 'foto_user' not in request.files or 'foto_target' not in request.files:
        return "Error: Form unggahan tidak lengkap!", 400
        
    file_user = request.files['foto_user']
    file_target = request.files['foto_target']
    
    # Validasi jika nama file kosong (user klik submit tanpa pilih foto)
    if file_user.filename == '' or file_target.filename == '':
        return "Error: Kamu harus memilih kedua foto sebelum mengecek!", 400
        
    # Proses penyimpanan file secara aman
    if file_user and allowed_file(file_user.filename) and file_target and allowed_file(file_target.filename):
        # Amankan nama file asli dan tambahkan prefix agar unik
        filename_user = "user_" + secure_filename(file_user.filename)
        filename_target = "target_" + secure_filename(file_target.filename)
        
        path_user = os.path.join(app.config['UPLOAD_FOLDER'], filename_user)
        path_target = os.path.join(app.config['UPLOAD_FOLDER'], filename_target)
        
        file_user.save(path_user)
        file_target.save(path_target)
        
        # Jalankan Otak Computer Vision
        skor_cocok, status_pesan = hitung_kecocokan(path_user, path_target)
        
        # Penanganan jika wajah tidak ditemukan di foto
        if skor_cocok is None:
            # Berikan pesan khusus agar user tahu apa yang salah
            return render_template("result.html", 
                                   skor=0, 
                                   pesan=status_pesan, 
                                   foto_user_name=filename_user, 
                                   foto_target_name=filename_target)
        
        # Theshold kata-kata status (chemistry jodoh) berdasarkan skor persentase
        if skor_cocok >= 85:
            pesan_jodoh = "Wah, garis wajah kalian mirip banget! Fix ini mah tanda-tanda belahan jiwa yang tertukar! ✨"
        elif skor_cocok >= 70:
            pesan_jodoh = "Kemiripan fitur wajah kalian kuat. Ada chemistry alami yang bikin kalian kelihatan serasi pas jalan bareng! 😉"
        elif skor_cocok >= 50:
            pesan_jodoh = "Persentasenya lumayan lah. Ingat, wajah ga harus mirip total, yang penting visi misi hidupnya sefrekuensi! 🙌"
        else:
            pesan_jodoh = "Skornya agak tipis nih, tapi tenang! Banyak kok pasangan yang wajahnya beda jauh tapi langgeng sampai kakek-nenek. Semangat! 🔥"
            
        # 6. Kirim semua data hasil kalkulasi ke template HTML
        return render_template("result.html", 
                               skor=skor_cocok, 
                               pesan=pesan_jodoh, 
                               foto_user_name=filename_user, 
                               foto_target_name=filename_target)
    
    return "Error: Format file tidak didukung! Gunakan format PNG, JPG, atau JPEG.", 400

#  Debug App
if __name__ == "__main__":
    app.run(debug=True)