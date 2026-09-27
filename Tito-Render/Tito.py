import base64
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

# =========================
# Gemini Client & Model Configuration
# =========================

client = genai.Client(api_key="AQ.Ab8RN6IQJSAshu12vtf3PQFBUzeISdvEUUZNlqD6sjsq9zEhIw")
MODEL = "gemini-3.5-flash"

# =========================
# واجهة Tito AI
# =========================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="google-site-verification" content="MmR0XF7E1_-Eci7A0VnABqMkCqNd0zpf5c-5JlR1rx0">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="description" content="Tito AI - مساعد ذكاء اصطناعي عربي">
<title>Tito AI</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #101010;
    color: white;
    overflow: hidden;
}

/* ========================= القائمة الجانبية ========================= */
.sidebar {
    position: fixed;
    right: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: #181818;
    border-left: 1px solid #303030;
    padding: 18px;
    transition: transform 0.25s ease;
    z-index: 100;
}

.sidebar.hidden {
    transform: translateX(100%);
}

.logo {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 25px;
}

.new-chat {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 12px;
    background: #303030;
    color: white;
    cursor: pointer;
    font-size: 15px;
    margin-bottom: 20px;
}

.new-chat:hover {
    background: #3a3a3a;
}

.history-title {
    color: #999;
    font-size: 13px;
    margin-bottom: 10px;
}

.history {
    overflow-y: auto;
    height: calc(100vh - 160px);
}

.topic {
    padding: 11px;
    border-radius: 10px;
    cursor: pointer;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.topic:hover {
    background: #292929;
}

.topic.active {
    background: #303030;
}

.overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.5);
    z-index: 90;
}

.overlay.show {
    display: block;
}

/* ========================= الصفحة الرئيسية ========================= */
.main {
    height: 100vh;
    margin-right: 280px;
    display: flex;
    flex-direction: column;
    transition: margin-right 0.25s ease;
}

.main.full {
    margin-right: 0;
}

.header {
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    border-bottom: 1px solid #292929;
}

.menu {
    background: transparent;
    color: white;
    border: none;
    font-size: 24px;
    cursor: pointer;
}

.header-title {
    font-size: 20px;
    font-weight: bold;
}

/* ========================= المحادثة ========================= */
.chat {
    flex: 1;
    overflow-y: auto;
    padding: 35px;
    max-width: 950px;
    width: 100%;
    margin: auto;
}

.welcome {
    text-align: center;
    margin-top: 120px;
}

.welcome h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.welcome p {
    color: #999;
    font-size: 17px;
}

.message {
    display: flex;
    margin: 22px 0;
    flex-direction: column;
}

.message.user {
    align-items: flex-start;
}

.message.tito {
    align-items: flex-end;
}

.bubble {
    max-width: 75%;
    padding: 15px 18px;
    border-radius: 18px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}

.user .bubble {
    background: #303030;
}

.tito .bubble {
    background: #202020;
}

.chat-media {
    max-width: 300px;
    max-height: 250px;
    border-radius: 12px;
    margin-bottom: 8px;
}

/* ========================= منطقة الكتابة والقائمة ========================= */
.input-area {
    width: 100%;
    padding: 18px;
    background: #101010;
    position: relative;
}

.input-container {
    max-width: 850px;
    margin: auto;
    position: relative;
}

.attachment-preview {
    display: none;
    align-items: center;
    background: #252525;
    padding: 8px 12px;
    border-radius: 12px 12px 0 0;
    border: 1px solid #353535;
    border-bottom: none;
}

.attachment-preview img, .attachment-preview video {
    height: 50px;
    border-radius: 6px;
    margin-left: 10px;
}

.remove-attach {
    background: #ff4d4d;
    color: white;
    border: none;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    cursor: pointer;
    margin-right: auto;
    font-weight: bold;
}

.input-box {
    background: #202020;
    border: 1px solid #353535;
    border-radius: 22px;
    display: flex;
    align-items: center;
    padding: 5px 10px;
}

.plus-btn {
    background: transparent;
    border: none;
    color: #ccc;
    font-size: 26px;
    cursor: pointer;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}

.plus-btn:hover {
    background: #303030;
    color: white;
}

textarea {
    flex: 1;
    resize: none;
    border: none;
    outline: none;
    background: transparent;
    color: white;
    font-size: 16px;
    padding: 10px;
    max-height: 150px;
    font-family: Arial;
}

.send {
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 50%;
    background: white;
    color: black;
    cursor: pointer;
    font-size: 18px;
    flex-shrink: 0;
}

.send:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* القائمة المنسدلة عند إتاحة الضغط على + */
.upload-menu {
    display: none;
    position: absolute;
    bottom: 60px;
    right: 0;
    background: #252525;
    border: 1px solid #383838;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    width: 200px;
    z-index: 500;
    overflow: hidden;
}

.upload-menu.show {
    display: block;
}

.menu-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    cursor: pointer;
    color: white;
    font-size: 15px;
    gap: 12px;
    transition: background 0.2s;
}

.menu-item:hover {
    background: #333333;
}

@media (max-width: 768px) {
    .sidebar { width: 260px; transform: translateX(100%); }
    .sidebar.show-mobile { transform: translateX(0); }
    .main { margin-right: 0 !important; }
    .chat { padding: 15px; }
    .bubble { max-width: 88%; font-size: 15px; padding: 12px 15px; }
    .welcome { margin-top: 60px; }
    .welcome h1 { font-size: 28px; }
    .welcome p { font-size: 15px; }
    .input-area { padding: 10px; }
    .header { height: 55px; padding: 0 15px; }
    .header-title { font-size: 17px; }
}
</style>
</head>

<body>

<div id="overlay" class="overlay" onclick="toggleSidebar()"></div>

<!-- القائمة الجانبية -->
<div id="sidebar" class="sidebar hidden">
    <div class="logo">🤖 Tito AI</div>
    <button class="new-chat" onclick="newChat()">＋ محادثة جديدة</button>
    <div class="history-title">المواضيع السابقة</div>
    <div id="history" class="history"></div>
</div>

<!-- الواجهة الرئيسية -->
<div id="main" class="main full">
    <div class="header">
        <button class="menu" onclick="toggleSidebar()">☰</button>
        <div id="headerTitle" class="header-title">Tito AI</div>
        <div></div>
    </div>

    <div id="chat" class="chat">
        <div id="welcome" class="welcome">
            <h1>مرحبًا، أنا Tito 🤖</h1>
            <p>كيف أقدر أساعدك اليوم؟</p>
        </div>
    </div>

    <div class="input-area">
        <div class="input-container">
            
            <!-- قائمة الخيارات عند الضغط على + -->
            <div id="uploadMenu" class="upload-menu">
                <div class="menu-item" onclick="triggerFileSelect('image/*')">
                    📷 إضافة صورة
                </div>
                <div class="menu-item" onclick="triggerFileSelect('video/*')">
                    🎥 إضافة مقطع فيديو
                </div>
            </div>

            <!-- المعاينة الخاصة بالمرفق قبل الإرسال -->
            <div id="attachmentPreview" class="attachment-preview">
                <span id="previewContainer"></span>
                <span id="fileName" style="font-size: 14px; color: #ccc;"></span>
                <button class="remove-attach" onclick="clearAttachment()">✕</button>
            </div>

            <!-- مربع إدخال النص والأزرار -->
            <div class="input-box">
                <button class="plus-btn" onclick="toggleUploadMenu(event)">＋</button>
                <textarea id="message" rows="1" placeholder="اكتب رسالتك إلى Tito..." onkeydown="handleKey(event)"></textarea>
                <button id="sendButton" class="send" onclick="sendMessage()">↑</button>
            </div>

            <!-- مدخل الملفات المخفي -->
            <input type="file" id="fileInput" style="display: none;" onchange="handleFileSelected(event)">

        </div>
    </div>
</div>

<script>
let conversations = JSON.parse(localStorage.getItem("tito_conversations") || "[]");
let currentId = null;
let currentAttachment = null; // { data: base64, mimeType: string, url: string, type: 'image'|'video' }

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    const overlay = document.getElementById("overlay");

    if (window.innerWidth <= 768) {
        sidebar.classList.toggle("show-mobile");
        overlay.classList.toggle("show");
    } else {
        sidebar.classList.toggle("hidden");
        main.classList.toggle("full");
    }
}

function newChat() {
    currentId = null;
    clearAttachment();
    document.getElementById("chat").innerHTML = `
        <div id="welcome" class="welcome">
            <h1>مرحبًا، أنا Tito 🤖</h1>
            <p>كيف أقدر أساعدك اليوم؟</p>
        </div>
    `;
    document.getElementById("headerTitle").textContent = "Tito AI";
    document.getElementById("message").focus();
    if (window.innerWidth <= 768) toggleSidebar();
    renderHistory();
}

function createConversation(firstMessage) {
    const id = Date.now().toString();
    const conversation = {
        id: id,
        title: firstMessage.substring(0, 35) || "محادثة جديدة",
        messages: []
    };
    conversations.unshift(conversation);
    currentId = id;
    saveConversations();
    return conversation;
}

function saveConversations() {
    localStorage.setItem("tito_conversations", JSON.stringify(conversations));
}

function renderHistory() {
    const history = document.getElementById("history");
    history.innerHTML = "";
    conversations.forEach(function(conversation) {
        const div = document.createElement("div");
        div.className = "topic";
        if (conversation.id === currentId) div.classList.add("active");
        div.textContent = "💬 " + conversation.title;
        div.onclick = function() {
            loadConversation(conversation.id);
            if (window.innerWidth <= 768) toggleSidebar();
        };
        history.appendChild(div);
    });
}

function loadConversation(id) {
    const conversation = conversations.find(c => c.id === id);
    if (!conversation) return;
    currentId = id;
    const chat = document.getElementById("chat");
    chat.innerHTML = "";
    document.getElementById("headerTitle").textContent = conversation.title;
    conversation.messages.forEach(function(message) {
        addMessage(message.text, message.type, false, message.media);
    });
    renderHistory();
}

function toggleUploadMenu(e) {
    e.stopPropagation();
    const menu = document.getElementById("uploadMenu");
    menu.classList.toggle("show");
}

document.addEventListener("click", function() {
    document.getElementById("uploadMenu").classList.remove("show");
});

function triggerFileSelect(acceptType) {
    const input = document.getElementById("fileInput");
    input.accept = acceptType;
    input.click();
    document.getElementById("uploadMenu").classList.remove("show");
}

function handleFileSelected(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        const base64Data = event.target.result.split(',')[1];
        const isImage = file.type.startsWith("image/");
        const isVideo = file.type.startsWith("video/");

        currentAttachment = {
            data: base64Data,
            mimeType: file.type,
            url: URL.createObjectURL(file),
            type: isImage ? "image" : (isVideo ? "video" : "file")
        };

        // إظهار المعاينة
        const previewContainer = document.getElementById("previewContainer");
        if (isImage) {
            previewContainer.innerHTML = `<img src="${currentAttachment.url}">`;
        } else if (isVideo) {
            previewContainer.innerHTML = `<video src="${currentAttachment.url}" muted></video>`;
        }

        document.getElementById("fileName").textContent = file.name;
        document.getElementById("attachmentPreview").style.display = "flex";
    };
    reader.readAsDataURL(file);
}

function clearAttachment() {
    currentAttachment = null;
    document.getElementById("attachmentPreview").style.display = "none";
    document.getElementById("previewContainer").innerHTML = "";
    document.getElementById("fileName").textContent = "";
    document.getElementById("fileInput").value = "";
}

function addMessage(text, type, save = true, media = null) {
    const chat = document.getElementById("chat");
    const welcome = document.getElementById("welcome");
    if (welcome) welcome.remove();

    const message = document.createElement("div");
    message.className = "message " + type;

    // إضافة الوسائط إذا وجد صوره أو فيديو
    if (media) {
        if (media.type === "image") {
            const img = document.createElement("img");
            img.src = media.url || `data:${media.mimeType};base64,${media.data}`;
            img.className = "chat-media";
            message.appendChild(img);
        } else if (media.type === "video") {
            const video = document.createElement("video");
            video.src = media.url || `data:${media.mimeType};base64,${media.data}`;
            video.controls = true;
            video.className = "chat-media";
            message.appendChild(video);
        }
    }

    if (text) {
        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = text;
        message.appendChild(bubble);
    }

    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;

    if (save && currentId) {
        const conversation = conversations.find(c => c.id === currentId);
        if (conversation) {
            conversation.messages.push({
                text: text,
                type: type,
                media: media
            });
            saveConversations();
        }
    }

    return message;
}

async function sendMessage() {
    const input = document.getElementById("message");
    const button = document.getElementById("sendButton");
    const text = input.value.trim();

    if (!text && !currentAttachment) return;

    if (!currentId) {
        createConversation(text || "ملف مرفق");
        document.getElementById("headerTitle").textContent = (text || "ملف مرفق").substring(0, 35);
    }

    const mediaToSend = currentAttachment;
    
    // إضافة رسالة المستخدم للمحادثة
    addMessage(text, "user", true, mediaToSend);

    // مسح الحقول
    input.value = "";
    clearAttachment();
    button.disabled = true;

    const conversation = conversations.find(c => c.id === currentId);

    // إضافة مؤشر "Tito يكتب..."
    const loadingMessage = addMessage("Tito يكتب... 🤔", "tito", false);
    const loadingBubble = loadingMessage.querySelector(".bubble");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                attachment: mediaToSend ? {
                    data: mediaToSend.data,
                    mimeType: mediaToSend.mimeType
                } : null,
                history: conversation.messages
            })
        });

        const data = await response.json();
        loadingBubble.textContent = data.reply;

        // حفظ رد Tito
        conversation.messages.push({
            text: data.reply,
            type: "tito"
        });

        saveConversations();
        renderHistory();

    } catch (error) {
        loadingBubble.textContent = "❌ حصل خطأ في الاتصال بـ Tito";
    }

    button.disabled = false;
    input.focus();
}

function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

renderHistory();
</script>

</body>
</html>
"""

# =========================
# الرئيسية
# =========================

@app.route("/")
def home():
    return render_template_string(HTML)

# =========================
# مسار المحادثة مع Gemini
# =========================

@app.route("/chat", methods=["POST"])
def chat_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "❌ لم يتم إرسال بيانات"})

        message = data.get("message", "").strip()
        attachment = data.get("attachment")
        history = data.get("history", [])

        if not message and not attachment:
            return jsonify({"reply": "❌ اكتب رسالة أو أرفق ملفًا أولًا"})

        # تجهيز أجزاء طلب المعالجة
        contents = []

        # إدراج المرفق الحالي (صورة أو فيديو) مع الطلب
        if attachment and "data" in attachment and "mimeType" in attachment:
            raw_bytes = base64.b64decode(attachment["data"])
            part = types.Part.from_bytes(data=raw_bytes, mime_type=attachment["mimeType"])
            contents.append(part)

        # بناء نص الحوار والتعليمات
        prompt_text = "أنت Tito AI، مساعد ذكاء اصطناعي عربي ودود ومفيد جداً.\n\n"
        if history:
            prompt_text += "سجل المحادثة السابقة:\n"
            for item in history[:-1]:  # التجاوز عن آخر رسالة أضيفت توًا
                msg_type = item.get("type", "")
                txt = item.get("text", "")
                if txt:
                    prompt_text += f"{'المستخدم' if msg_type == 'user' else 'Tito'}: {txt}\n"

        prompt_text += f"\nالمستخدم الآن: {message if message else '[قام المرفق بإرساله]'}\nTito:"
        contents.append(prompt_text)

        # إرسال إلى نموذج Gemini 2.5 Flash المتوافق مع الوسائط
        response = client.models.generate_content(
            model=MODEL,
            contents=contents
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("Gemini Error:", repr(e))
        return jsonify({"reply": f"❌ حصل خطأ أثناء الاتصال بـ Gemini: {str(e)}"})

# =========================
# التشغيل
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
