from flask import Flask, request, jsonify, render_template_string
import urllib.request
import json

app = Flask(__name__)

# =========================
# Google Gemini Configuration
# =========================
API_KEY = "AQ.Ab8RN6L-fNW_4imyzYHoiRBhKxJZiuUJ11v2pQJyfzxntay0dQ"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"

def call_gemini(messages):
    contents = []
    
    # 1. إعطاء تعليمات أساسية للنظام (System Instruction) ليعرف من هو مالك المشروع
    system_instruction = (
        "أنت مساعد ذكاء اصطناعي اسمه Tito AI. "
        "تم تطويرك وبرمجتك بواسطة المطور طارق عبدالله الوائلي، وهو المالك الحصري وصاحب الملكية الفكرية للمشروع. "
        "إذا سألك أي شخص عن من صممك أو برمجك أو من يمتلكك، يجب أن تجيب بكل فخر أن مطورك ومالكك هو طارق عبدالله الوائلي."
    )
    
    # إدراج التعليمات في بداية المحادثة كإرشادات نظام
    contents.append({
        "role": "user",
        "parts": [{"text": system_instruction}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": "أهلاً بك! أنا Tito AI، مساعد ذكاء اصطناعي فخور بأنني تم تطويري وبرمجتي بواسطة المطور طارق عبدالله الوائلي."}]
    })

    # إضافة رسائل المستخدم والتاريخ السابق
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": contents}
    
    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ خطأ من Gemini: {str(e)}"

# =========================
# واجهة Tito AI
# =========================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Tito AI</title>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: Arial, sans-serif; background: #101010; color: white; overflow: hidden; }
.sidebar { position: fixed; right: 0; top: 0; width: 280px; height: 100vh; background: #181818; border-left: 1px solid #303030; padding: 18px; transition: transform 0.25s ease; z-index: 100; display: flex; flex-direction: column; }
.sidebar.hidden { transform: translateX(100%); }
.logo { font-size: 24px; font-weight: bold; margin-bottom: 25px; }
.new-chat { width: 100%; padding: 13px; border: none; border-radius: 12px; background: #303030; color: white; cursor: pointer; font-size: 15px; margin-bottom: 20px; }
.new-chat:hover { background: #3a3a3a; }
.history-title { color: #999; font-size: 13px; margin-bottom: 10px; }
.history { overflow-y: auto; flex: 1; }
.copyright-footer { font-size: 11px; color: #777; text-align: center; padding-top: 15px; border-top: 1px solid #282828; margin-top: 10px; line-height: 1.5; }
.topic { position: relative; display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border-radius: 10px; cursor: pointer; margin-bottom: 5px; transition: background 0.2s; }
.topic:hover { background: #292929; }
.topic.active { background: #303030; }
.topic-title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; font-size: 14px; }
.topic-menu-btn { background: transparent; border: none; color: #aaa; cursor: pointer; font-size: 16px; padding: 2px 6px; border-radius: 4px; display: none; }
.topic:hover .topic-menu-btn, .topic-menu-btn.show { display: block; }
.topic-dropdown { display: none; position: absolute; left: 10px; top: 40px; background: #252525; border: 1px solid #383838; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 150px; z-index: 200; overflow: hidden; }
.topic-dropdown.show { display: block; }
.dropdown-item { padding: 10px 14px; font-size: 13px; color: white; cursor: pointer; display: flex; align-items: center; gap: 8px; }
.dropdown-item:hover { background: #333333; }
.dropdown-item.delete { color: #ff4d4d; }
.overlay { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); z-index: 90; }
.overlay.show { display: block; }
.main { height: 100vh; margin-right: 280px; display: flex; flex-direction: column; transition: margin-right 0.25s ease; }
.main.full { margin-right: 0; }
.header { height: 65px; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #292929; }
.menu { background: transparent; color: white; border: none; font-size: 24px; cursor: pointer; }
.header-title { font-size: 20px; font-weight: bold; }
.chat { flex: 1; overflow-y: auto; padding: 35px; max-width: 950px; width: 100%; margin: auto; }
.welcome { text-align: center; margin-top: 120px; }
.welcome h1 { font-size: 42px; margin-bottom: 10px; }
.welcome p { color: #999; font-size: 17px; }
.message { display: flex; margin: 22px 0; flex-direction: column; }
.message.user { align-items: flex-start; }
.message.tito { align-items: flex-end; }
.bubble { max-width: 75%; padding: 15px 18px; border-radius: 18px; line-height: 1.7; white-space: pre-wrap; word-break: break-word; }
.user .bubble { background: #303030; }
.tito .bubble { background: #202020; }
.chat-media { max-width: 300px; max-height: 250px; border-radius: 12px; margin-bottom: 8px; }
.input-area { width: 100%; padding: 18px; background: #101010; position: relative; }
.input-container { max-width: 850px; margin: auto; position: relative; }
.attachment-preview { display: none; align-items: center; background: #252525; padding: 8px 12px; border-radius: 12px 12px 0 0; border: 1px solid #353535; border-bottom: none; }
.attachment-preview img, .attachment-preview video { height: 50px; border-radius: 6px; margin-left: 10px; }
.remove-attach { background: #ff4d4d; color: white; border: none; border-radius: 50%; width: 22px; height: 22px; cursor: pointer; margin-right: auto; font-weight: bold; }
.input-box { background: #202020; border: 1px solid #353535; border-radius: 22px; display: flex; align-items: center; padding: 5px 10px; }
.plus-btn { background: transparent; border: none; color: #ccc; font-size: 26px; cursor: pointer; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
textarea { flex: 1; resize: none; border: none; outline: none; background: transparent; color: white; font-size: 16px; padding: 10px; max-height: 150px; font-family: Arial; }
.action-btn { width: 40px; height: 40px; border: none; border-radius: 50%; background: white; color: black; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.action-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.action-btn.listening { background: #ff4d4d; color: white; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
.upload-menu { display: none; position: absolute; bottom: 60px; right: 0; background: #252525; border: 1px solid #383838; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 200px; z-index: 500; overflow: hidden; }
.upload-menu.show { display: block; }
.menu-item { display: flex; align-items: center; padding: 12px 16px; cursor: pointer; color: white; font-size: 15px; gap: 12px; }
.menu-item:hover { background: #333333; }
@media (max-width: 768px) {
    .sidebar { width: 260px; transform: translateX(100%); }
    .sidebar.show-mobile { transform: translateX(0); }
    .main { margin-right: 0 !important; }
    .chat { padding: 15px; }
    .bubble { max-width: 88%; font-size: 15px; padding: 12px 15px; }
}
</style>
</head>

<body>
<div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar" class="sidebar hidden">
    <div>
        <div class="logo">🤖 Tito AI</div>
        <button class="new-chat" onclick="newChat()">＋ محادثة جديدة</button>
        <div class="history-title">المواضيع السابقة</div>
    </div>
    <div id="history" class="history"></div>
    <div class="copyright-footer">
        © 2026 Tito AI<br>
        جميع الحقوق محفوظة<br>
        <b>طارق عبدالله الوائلي</b>
    </div>
</div>

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
            <div id="uploadMenu" class="upload-menu">
                <div class="menu-item" onclick="triggerFileSelect('image/*')">📷 إضافة صورة</div>
                <div class="menu-item" onclick="triggerFileSelect('video/*')">🎥 إضافة مقطع فيديو</div>
            </div>
            <div id="attachmentPreview" class="attachment-preview">
                <span id="previewContainer"></span>
                <span id="fileName" style="font-size: 14px; color: #ccc;"></span>
                <button class="remove-attach" onclick="clearAttachment()">✕</button>
            </div>
            <div class="input-box">
                <button class="plus-btn" onclick="toggleUploadMenu(event)">＋</button>
                <textarea id="message" rows="1" placeholder="اكتب رسالتك إلى Tito..." oninput="handleInput()" onkeydown="handleKey(event)"></textarea>
                <button id="actionButton" class="action-btn" onclick="handleActionClick()" title="تسجيل صوتي أو إرسال">🎤</button>
            </div>
            <input type="file" id="fileInput" style="display: none;" onchange="handleFileSelected(event)">
        </div>
    </div>
</div>

<script>
let conversations = JSON.parse(localStorage.getItem("tito_conversations") || "[]");
let currentId = null;
let currentAttachment = null;
let recognition = null;
let isListening = false;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("message");
        input.value += (input.value ? " " : "") + transcript;
        handleInput();
    };
    recognition.onerror = function() { stopListening(); };
    recognition.onend = function() { stopListening(); };
}

function startListening() {
    if (!recognition) { alert("متصفحك لا يدعم خاصية التعرف الصوتي."); return; }
    try { recognition.start(); isListening = true; document.getElementById("actionButton").classList.add("listening"); } catch(e) { stopListening(); }
}

function stopListening() {
    if (recognition && isListening) { try { recognition.stop(); } catch(e){} }
    isListening = false;
    document.getElementById("actionButton").classList.remove("listening");
}

function handleInput() {
    const input = document.getElementById("message");
    const btn = document.getElementById("actionButton");
    if (input.value.trim().length > 0 || currentAttachment) {
        if (isListening) stopListening();
        btn.textContent = "↑";
    } else {
        btn.textContent = "🎤";
    }
}

function handleActionClick() {
    const input = document.getElementById("message");
    if (input.value.trim().length > 0 || currentAttachment) { sendMessage(); }
    else { if (isListening) stopListening(); else startListening(); }
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    const overlay = document.getElementById("overlay");
    if (window.innerWidth <= 768) { sidebar.classList.toggle("show-mobile"); overlay.classList.toggle("show"); }
    else { sidebar.classList.toggle("hidden"); main.classList.toggle("full"); }
}

function newChat() {
    currentId = null;
    clearAttachment();
    document.getElementById("chat").innerHTML = `<div id="welcome" class="welcome"><h1>مرحبًا، أنا Tito 🤖</h1><p>كيف أقدر أساعدك اليوم؟</p></div>`;
    document.getElementById("headerTitle").textContent = "Tito AI";
    document.getElementById("message").focus();
    if (window.innerWidth <= 768) toggleSidebar();
    renderHistory();
}

function createConversation(firstMessage) {
    const id = Date.now().toString();
    const conversation = { id: id, title: firstMessage.substring(0, 35) || "محادثة جديدة", pinned: false, messages: [] };
    conversations.unshift(conversation);
    currentId = id;
    saveConversations();
    return conversation;
}

function saveConversations() { localStorage.setItem("tito_conversations", JSON.stringify(conversations)); }

function renderHistory() {
    const history = document.getElementById("history");
    history.innerHTML = "";
    [...conversations].sort((a, b) => (a.pinned === b.pinned ? 0 : (a.pinned ? -1 : 1))).forEach(function(conversation) {
        const div = document.createElement("div");
        div.className = "topic" + (conversation.id === currentId ? " active" : "");
        div.innerHTML = `<span class="topic-title">${conversation.pinned ? "📌 " : "💬 "}${conversation.title}</span><button class="topic-menu-btn" onclick="toggleTopicMenu('${conversation.id}', event)">⋮</button><div id="dropdown-${conversation.id}" class="topic-dropdown"><div class="dropdown-item" onclick="togglePin('${conversation.id}', event)">${conversation.pinned ? '📍 إلغاء التثبيت' : '📌 تثبيت'}</div><div class="dropdown-item" onclick="renameConversation('${conversation.id}', event)">✏️ إعادة تسمية</div><div class="dropdown-item delete" onclick="deleteConversation('${conversation.id}', event)">🗑️ حذف</div></div>`;
        div.onclick = function() { loadConversation(conversation.id); if (window.innerWidth <= 768) toggleSidebar(); };
        history.appendChild(div);
    });
}

function toggleTopicMenu(id, e) {
    e.stopPropagation();
    document.querySelectorAll('.topic-dropdown').forEach(m => { if (m.id !== `dropdown-${id}`) m.classList.remove('show'); });
    document.getElementById(`dropdown-${id}`).classList.toggle("show");
}

document.addEventListener("click", function() {
    document.querySelectorAll('.topic-dropdown').forEach(m => m.classList.remove('show'));
    document.getElementById("uploadMenu").classList.remove("show");
});

function togglePin(id, e) {
    e.stopPropagation();
    const c = conversations.find(x => x.id === id);
    if (c) { c.pinned = !c.pinned; saveConversations(); renderHistory(); }
}

function renameConversation(id, e) {
    e.stopPropagation();
    const c = conversations.find(x => x.id === id);
    if (c) {
        const nt = prompt("أدخل العنوان الجديد للمحادثة:", c.title);
        if (nt && nt.trim()) { c.title = nt.trim(); saveConversations(); renderHistory(); if (currentId === id) document.getElementById("headerTitle").textContent = c.title; }
    }
}

function deleteConversation(id, e) {
    e.stopPropagation();
    if (confirm("هل أنت متأكد من رغبتك في حذف هذه المحادثة؟")) {
        conversations = conversations.filter(x => x.id !== id);
        saveConversations();
        if (currentId === id) newChat(); else renderHistory();
    }
}

function loadConversation(id) {
    const c = conversations.find(x => x.id === id);
    if (!c) return;
    currentId = id;
    document.getElementById("chat").innerHTML = "";
    document.getElementById("headerTitle").textContent = c.title;
    c.messages.forEach(m => addMessage(m.text, m.type, false, m.media));
    renderHistory();
}

function toggleUploadMenu(e) { e.stopPropagation(); document.getElementById("uploadMenu").classList.toggle("show"); }
function triggerFileSelect(type) { document.getElementById("fileInput").accept = type; document.getElementById("fileInput").click(); document.getElementById("uploadMenu").classList.remove("show"); }

function handleFileSelected(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(event) {
        currentAttachment = { data: event.target.result.split(',')[1], mimeType: file.type, url: URL.createObjectURL(file), type: file.type.startsWith("image/") ? "image" : "video" };
        document.getElementById("previewContainer").innerHTML = currentAttachment.type === "image" ? `<img src="${currentAttachment.url}">` : `<video src="${currentAttachment.url}" muted></video>`;
        document.getElementById("fileName").textContent = file.name;
        document.getElementById("attachmentPreview").style.display = "flex";
        handleInput();
    };
    reader.readAsDataURL(file);
}

function clearAttachment() {
    currentAttachment = null;
    document.getElementById("attachmentPreview").style.display = "none";
    document.getElementById("previewContainer").innerHTML = "";
    document.getElementById("fileName").textContent = "";
    document.getElementById("fileInput").value = "";
    handleInput();
}

function addMessage(text, type, save = true, media = null) {
    const chat = document.getElementById("chat");
    const welcome = document.getElementById("welcome");
    if (welcome) welcome.remove();
    const msg = document.createElement("div");
    msg.className = "message " + type;
    if (media) {
        const el = document.createElement(media.type === "image" ? "img" : "video");
        el.src = media.url || `data:${media.mimeType};base64,${media.data}`;
        if (media.type === "video") el.controls = true;
        el.className = "chat-media";
        msg.appendChild(el);
    }
    if (text) {
        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = text;
        msg.appendChild(bubble);
    }
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
    if (save && currentId) {
        conversations.find(x => x.id === currentId).messages.push({ text: text, type: type, media: media });
        saveConversations();
    }
    return msg;
}

async function sendMessage() {
    const input = document.getElementById("message");
    const text = input.value.trim();
    if (!text && !currentAttachment) return;
    if (isListening) stopListening();
    if (!currentId) { createConversation(text || "ملف مرفق"); document.getElementById("headerTitle").textContent = (text || "ملف مرفق").substring(0, 35); }
    const mediaToSend = currentAttachment;
    addMessage(text, "user", true, mediaToSend);
    input.value = "";
    clearAttachment();
    const c = conversations.find(x => x.id === currentId);
    const loading = addMessage("Tito يكتب... 🤔", "tito", false);
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, history: c.messages })
        });
        const data = await res.json();
        loading.querySelector(".bubble").textContent = data.reply;
        c.messages.push({ text: data.reply, type: "tito" });
        saveConversations();
        renderHistory();
    } catch(e) {
        loading.querySelector(".bubble").textContent = "❌ حصل خطأ في الاتصال";
    }
    input.focus();
    handleInput();
}

function handleKey(e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); } }
renderHistory();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat_message():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        history = data.get("history", [])

        formatted_messages = []
        for item in history:
            if item.get("text"):
                formatted_messages.append({
                    "role": "user" if item.get("type") == "user" else "model",
                    "content": item.get("text")
                })
        
        if not formatted_messages or formatted_messages[-1]["content"] != message:
            formatted_messages.append({"role": "user", "content": message})

        reply_text = call_gemini(formatted_messages)
        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"reply": f"❌ خطأ: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
