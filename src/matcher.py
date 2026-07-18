import os
import cv2
import numpy as np

# Kita coba import face_recognition. 
# Jika user belum install/gagal install dlib, server ga bakal langsung mati.
try:
    import face_recognition
    HAS_FACE_REC = True
except ImportError:
    HAS_FACE_REC = False

def hitung_kecocokan(img_path1, img_path2):
    """
    Fungsi untuk mendeteksi dua wajah dan menghitung persentase kemiripannya.
    Menggunakan algoritma Euclidean Distance pada 128-fitur wajah (Facial Encodings).
    """
    
    # --- JALUR UTAMA: MENGGUNAKAN FACE_RECOGNITION (DEEP LEARNING) ---
    if HAS_FACE_REC:
        try:
            # Load gambar ke format numpy array
            img1 = face_recognition.load_image_file(img_path1) # Gamabar 1 
            img2 = face_recognition.load_image_file(img_path2) # Gambar 2
            
            # Ekstrak koordinat fitur wajah (128 dimensi)
            encoding1 = face_recognition.face_encodings(img1) # Encoding Gambar 1
            encoding2 = face_recognition.face_encodings(img2) # Encoding Gambar 2
            
            # Validasi jika ada landmark wajahnya gak ketemu (karna pake basis dlib)
            if len(encoding1) == 0:
                return None, "Wajah kamu tidak terdeteksi di dalam foto. Coba foto lain yang lebih jelas, ya!"
            if len(encoding2) == 0:
                return None, "Wajah doi tidak terdeteksi di dalam foto. Pastikan mukanya menghadap ke kamera!"
                
            # Hitung Jarak Wajah (Euclidean Distance)
            # Nilai berkisar dari 0.0 (kembar identik) sampai 1.0+ (sangat tidak mirip)
            face_dist = face_recognition.face_distance([encoding1[0]], encoding2[0])[0]
            
            # Threshold Pemetaan Distance ke Persentase Jodoh (0% - 100%)
            # Standar kecocokan dlib biasanya di batas angka 0.6
            if face_dist > 0.6:
                # Jika jaraknya jauh (tidak mirip), kasih skor di kisaran 10% - 59%
                match_percentage = max(10, int((1.2 - face_dist) * 80))
            else:
                # Jika jaraknya dekat (mirip), dongkrak skor ke 60% - 100%
                match_percentage = int((1 - (face_dist / 0.6)) * 40 + 60)
                
            return min(match_percentage, 100), "Sukses"
            
        except Exception as e:
            # Jika ada error internal saat processing deep learning, lempar ke fallback
            print(f"[System Notice] Face_recognition error, switching to fallback: {e}")

    # --- JALUR ALTERNATIF (FALLBACK): OPENCV BASIC TEMPLATE MATCHING ---
    # Dipakai jika library face_recognition tidak terinstall atau error.
    try:
        # Baca gambar lewat OpenCV standar (Grayscale)
        im1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)
        
        if im1 is None or im2 is None:
            return None, "Gagal membaca file foto. Pastikan formatnya benar!"
            
        # Resize kedua gambar ke ukuran yang sama biar bisa dibandingin secara matriks
        im1_res = cv2.resize(im1, (200, 200))
        im2_res = cv2.resize(im2, (200, 200))
        
        # Hitung korelasi kecocokan piksel (Template Matching)
        res = cv2.matchTemplate(im1_res, im2_res, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        
        # Pemetaan nilai korelasi (-1 sampai 1) menjadi persentase (0% sampai 100%)
        match_percentage = int((max_val + 1) * 50)
        
        # Sedikit bumbu variasi matematika biar nilainya ga terlalu kaku
        match_percentage = max(15, min(match_percentage, 98))
        
        return match_percentage, "Sukses (Menggunakan basic mode)"
        
    except Exception as e:
        return None, f"Terjadi kesalahan sistem saat memproses gambar: {str(e)}"