from flask import Flask, render_template, request, jsonify
import re
import unicodedata

app = Flask(__name__)

def normalize_text(text):
    text = text.lower().strip()

    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')

    text = re.sub(r'[^a-z0-9\s]', '', text)

    return text

abbreviations = {
    "neu": "dai hoc kinh te quoc dan",
    "ktqd": "dai hoc kinh te quoc dan",
    "dh": "dai hoc",

    "xt": "xet tuyen",
    "pt": "phuong thuc",
    "ptxt": "phuong thuc xet tuyen",

    "cntt": "cong nghe thong tin",
    "it": "cong nghe thong tin",

    "clc": "chat luong cao",
    "tt": "tien tien",

    "ts": "tuyen sinh",
    "nv": "nguyen vong",

    "hp": "hoc phi",
    "hb": "hoc bong",

    "hsa": "hsa",
    "tsa": "tsa",
    "sat": "sat",
    "act": "act",

    "ko": "khong",
    "k": "khong",
    "dc": "duoc",
    "bn": "bao nhieu"
}

qa_data = {

# ===== THÔNG TIN CHUNG =====
"thong tin truong": "ĐH Kinh tế Quốc dân (NEU), địa chỉ 207 Giải Phóng, Hà Nội. Tổng chỉ tiêu ~9000 (8780 chính quy, 220 liên thông).",
"neu o dau": "Địa chỉ: 207 Giải Phóng, Hai Bà Trưng, Hà Nội.",
"chi tieu 2026": "Khoảng 9000 chỉ tiêu (8780 chính quy, 220 liên thông).",
"tong chi tieu": "NEU tuyển khoảng 9000 sinh viên năm 2026.",

# ===== PHƯƠNG THỨC =====
"phuong thuc xet tuyen": "2 nhóm: 3% tuyển thẳng, 97% gồm xét kết hợp + điểm thi THPT.",
"neu xet tuyen the nao": "NEU xét tuyển theo tuyển thẳng, xét kết hợp và điểm thi THPT.",
"ptxt neu": "Có 5 phương thức: SAT/ACT, HSA/TSA, kết hợp IELTS + năng lực, IELTS + THPT, hoặc THPT thuần.",

# ===== ĐIỀU KIỆN =====
"dieu kien xet tuyen": "SAT ≥1200, ACT ≥26, HSA ≥85, TSA ≥60 hoặc kết hợp IELTS.",
"sat bao nhieu": "SAT cần từ 1200 trở lên.",
"hsa bao nhieu": "HSA từ 85 điểm trở lên.",
"tsa bao nhieu": "TSA từ 60 điểm trở lên.",
"ielts bao nhieu": "IELTS từ 5.5 trở lên.",

# ===== IELTS QUY ĐỔI =====
"quy doi ielts": "IELTS 5.5→8.0, 6.0→8.5, 6.5→9.0, 7.0→9.5, 7.5+→10.",
"ielts sang diem": "IELTS được quy đổi tối đa 10 điểm theo bảng chuẩn.",
"toefl toeic quy doi": "TOEFL, TOEIC cũng được quy đổi tương đương IELTS.",

# ===== ĐIỂM ƯU TIÊN =====
"diem uu tien": "Nếu ≥22.5 điểm, ưu tiên = [(30 - điểm)/7.5] × mức ưu tiên.",
"cong thuc diem": "Công thức tính ưu tiên áp dụng cho thí sinh điểm cao để đảm bảo công bằng.",

# ===== CHƯƠNG TRÌNH =====
"chuong trinh hoc": "Có chương trình chuẩn, tiên tiến (TT), chất lượng cao (CLC), POHE.",
"pohe la gi": "POHE là chương trình định hướng thực hành, học gắn với doanh nghiệp.",
"tt clc": "TT là chương trình tiên tiến, CLC là chất lượng cao.",

# ===== HỌC PHÍ =====
"hoc phi": "Tiêu chuẩn ~22-25tr/năm; CLC ~50-55tr; POHE ~45-50tr; Tiếng Anh ~55-68tr.",
"hp neu": "Học phí NEU từ ~22 triệu đến ~68 triệu tùy chương trình.",

# ===== HỌC BỔNG =====
"hoc bong": "Tổng quỹ học bổng ~30 tỷ (25 tỷ học tập + 5 tỷ tài trợ).",
"hb neu": "NEU có nhiều học bổng và hỗ trợ tài chính.",

# ===== TRAO ĐỔI =====
"trao doi sinh vien": "Có thể đi Nhật, Hàn, Pháp, Mỹ, Canada, Singapore từ 3 tuần đến 1 năm.",
"du hoc trao doi": "NEU có chương trình trao đổi quốc tế.",

# ===== NGUYỆN VỌNG =====
"nguyen vong": "Được đăng ký tối đa 15 nguyện vọng.",
"nv toi da": "Tối đa 15 nguyện vọng.",

# ===== NGOẠI NGỮ =====
"chuan dau ra": "Yêu cầu tiếng Anh IELTS 5.5–6.5 tùy chương trình.",
"tot nghiep ielts": "Cần đạt IELTS tối thiểu ~5.5.",

# ===== QUY ĐỊNH =====
"bao luu diem": "Không dùng điểm bảo lưu THPT.",
"mien thi anh": "Không sử dụng miễn thi ngoại ngữ.",

# ===== NGÀNH =====
"nganh neu": "Khoảng 104 ngành/chương trình đào tạo.",
"nganh moi": "Thêm ~15 ngành mới như Fintech, Kinh tế số, Marketing công nghệ...",
"fintech": "Công nghệ tài chính (Fintech) là ngành mới tại NEU.",
"kinh te so": "Kinh tế số là ngành xu hướng gắn với dữ liệu và công nghệ.",

# ===== CHUNG =====
"neu 2026": "NEU tuyển ~9000 chỉ tiêu với nhiều phương thức linh hoạt.",
"tu van": "Bạn có thể hỏi về ngành, điểm, học phí hoặc xét tuyển."
}

@app.route("/")
def home():
    return render_template("chatbot.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    user_input = normalize_text(user_input)

    user_input = expand_abbreviations(user_input)

    for key in qa_data:
        if key in user_input:
            return jsonify({"response": qa_data[key]})

    return jsonify({"response": "❌ Mình chưa có thông tin cho câu hỏi này."})


def expand_abbreviations(text):
    words = text.split()
    new_words = []

    for word in words:
        if word in abbreviations:
            new_words.append(abbreviations[word])
        else:
            new_words.append(word)

    return " ".join(new_words)


if __name__ == "__main__":
    app.run(debug=True)