from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

HF_TOKEN = "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"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

qa_data = {
    "thong_tin": {
        "keywords": ["thông tin", "địa chỉ", "tên trường", "chỉ tiêu", "neu ở đâu"],
        "answer": """Đại học Kinh tế Quốc dân (NEU)
Địa chỉ: 207 Giải Phóng, Phường Bạch Mai, Hai Bà Trưng, Hà Nội
Tổng chỉ tiêu 2026: 9.000 (8780 chính quy, 220 liên thông)"""
    },

    "phuong_thuc": {
        "keywords": ["phương thức", "xét tuyển", "tuyển sinh"],
        "answer": """2 nhóm:
- Nhóm 1 (3%): Tuyển thẳng
- Nhóm 2 (97%): Xét kết hợp (PTXT 1→4) + điểm thi THPT 2026"""
    },

    "dieu_kien": {
        "keywords": ["điều kiện", "sat", "act", "hsa", "tsa"],
        "answer": """PTXT:
- SAT ≥1200 hoặc ACT ≥26
- HSA ≥85 / V-ACT ≥700 / TSA ≥60
- IELTS ≥5.5 kết hợp điểm khác"""
    },

    "hoc_phi": {
        "keywords": ["học phí", "tiền học"],
        "answer": """- Tiêu chuẩn: 22–25 triệu/năm
- CLC: 50–55 triệu
- POHE: 45–50 triệu
- Tiếng Anh: 55–68 triệu"""
    },

    "nganh": {
        "keywords": ["ngành", "ngành mới"],
        "answer": """104 ngành + 15 ngành mới:
Fintech, Kinh tế số, Marketing công nghệ, Logistics công nghệ..."""
    }
}

@app.route("/")
def home():
    return render_template("chatbot.html")

def check_static_answer(user_input):
    user_input = user_input.lower()

    for item in qa_data.values():
        for keyword in item["keywords"]:
            if keyword in user_input:
                return item["answer"]

    return None

def call_glm(user_input):
    try:
        completion = client.chat.completions.create(
            model="zai-org/GLM-5.1:fireworks-ai",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là chatbot tư vấn tuyển sinh NEU. Trả lời ngắn gọn, đúng trọng tâm."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return "❌ Lỗi AI"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")

        if not user_input:
            return jsonify({"response": "❌ Bạn chưa nhập câu hỏi"})

        static_answer = check_static_answer(user_input)
        if static_answer:
            return jsonify({"response": static_answer})

        ai_response = call_glm(user_input)
        return jsonify({"response": ai_response})

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"response": "❌ Server lỗi"})

if __name__ == "__main__":
    app.run(debug=True)