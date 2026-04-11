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
    "cntt": "cong nghe thong tin",
    "it": "cong nghe thong tin",
    "xt": "xet tuyen",
    "pt": "phuong thuc",
    "nv": "nguyen vong",
    "clc": "chat luong cao",
    "tt": "tien tien",
    "dh": "dai hoc",
    "ts": "tuyen sinh",
    "ielts": "ielts",
    "hsa": "hsa",
    "ko": "khong",
    "k": "khong",
    "dc": "duoc",
    "bn": "bao nhieu"
}

# ===== DATA CHATBOT =====
qa_data = {
    # TUYỂN SINH
    "xet tuyen 2026": "NEU 2026 có 3 phương thức: tuyển thẳng, thi THPT (A00, A01, D01, D07), xét tuyển kết hợp.",
    "neu xet tuyen the nao": "NEU có 3 phương thức: tuyển thẳng, THPT, xét tuyển kết hợp.",
    "phuong thuc xet tuyen": "Gồm tuyển thẳng, thi THPT và xét tuyển kết hợp.",

    # KẾT HỢP
    "xet ket hop": "Cần SAT 1200+ hoặc IELTS 5.5+ hoặc HSA/ACT + kết hợp điểm khác.",
    "sat ielts hsa": "SAT 1200+, IELTS 5.5+, HSA 85+ hoặc kết hợp THPT.",

    # NGÀNH
    "nganh moi 2026": "Có Kinh tế số, Fintech, Marketing công nghệ, Logistics công nghệ.",
    "kinh te so": "Ngành kinh tế số học về dữ liệu + công nghệ + kinh tế.",
    "fintech": "Fintech là tài chính + công nghệ + dữ liệu.",

    # CNTT
    "cong nghe thong tin": "CNTT NEU thiên về ứng dụng kinh tế + lập trình.",
    "cong nghe thong tin neu": "CNTT NEU kết hợp công nghệ + kinh tế.",

    # CHƯƠNG TRÌNH
    "chuong trinh hoc": "Có tiếng Việt, POHE, tiếng Anh, tiên tiến, chất lượng cao.",
    "pohe": "POHE là chương trình định hướng thực hành, đi thực tế từ năm 1.",

    # CHỌN NGÀNH
    "chon nganh": "Chọn ngành theo sở thích + năng lực + cơ hội việc làm.",
    "nganh hot": "Nên chia nguyện vọng: cao – phù hợp – an toàn.",

    # THÔNG TIN
    "thong tin": "Xem tại website NEU hoặc app tuyển sinh.",
    "lien he": "Hotline 0888.128.558 | tuvantuyensinh@neu.edu.vn",

    # CHUNG
    "dai hoc kinh te quoc dan": "NEU là trường top về kinh tế, quản trị và công nghệ.",
    "tuyen sinh": "Bạn có thể hỏi về ngành, phương thức hoặc điểm chuẩn."
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