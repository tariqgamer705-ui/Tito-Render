from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)

# =========================
# Gemini
# =========================

client = genai.Client(api_key="AQ.Ab8RN6IQJSAshu12vtf3PQFBUzeISdvEUUZNlqD6sjsq9zEhIw")

MODEL = "gemini-3.6-flash"


# =========================
# واجهة Tito AI
# =========================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="google-site-verification"
content="MmR0XF7E1_-Eci7A0VnABqMkCqNd0zpf5c-5JlR1rx0">

<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<meta name="description"
content="Tito AI - مساعد ذكاء اصطناعي عربي">

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

/* =========================
   القائمة الجانبية
   ========================= */

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

/* طبقة تعتيم للجوال عند فتح القائمة */
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

/* =========================
   الصفحة
   ========================= */

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

/* =========================
   الهيدر
   ========================= */

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

/* =========================
   المحادثة
   ========================= */

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

/* =========================
   الرسائل
   ========================= */

.message {
    display: flex;
    margin: 22px 0;
}

.message.user {
    justify-content: flex-start;
}

.message.tito {
    justify-content: flex-end;
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

/* =========================
   منطقة الكتابة
   ========================= */

.input-area {
    width: 100%;
    padding: 18px;
    background: #101010;
}

.input-box {
    max-width: 850px;
    margin: auto;
    background: #202020;
    border: 1px solid #353535;
    border-radius: 22px;
    display: flex;
    align-items: flex-end;
    padding: 10px;
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
    width: 45px;
    height: 45px;
    border: none;
    border-radius: 50%;
    background: white;
    color: black;
    cursor: pointer;
    font-size: 19px;
    flex-shrink: 0;
}

.send:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* =========================
   التجاوب مع الشاشات الصغيرة (الجوال)
   ========================= */

@media (max-width: 768px) {

    .sidebar {
        width: 260px;
        transform: translateX(100%);
    }

    .sidebar.show-mobile {
        transform: translateX(0);
    }

    .main {
        margin-right: 0 !important;
    }

    .chat {
        padding: 15px;
    }

    .bubble {
        max-width: 88%;
        font-size: 15px;
        padding: 12px 15px;
    }

    .welcome {
        margin-top: 60px;
    }

    .welcome h1 {
        font-size: 28px;
    }

    .welcome p {
        font-size: 15px;
    }

    .input-area {
        padding: 10px;
    }

    .header {
        height: 55px;
        padding: 0 15px;
    }

    .header-title {
        font-size: 17px;
    }
}

</style>

</head>


<body>

<div id="overlay" class="overlay" onclick="toggleSidebar()"></div>

<!-- القائمة -->

<div id="sidebar" class="sidebar hidden">

    <div class="logo">
        🤖 Tito AI
    </div>

    <button class="new-chat" onclick="newChat()">
        ＋ محادثة جديدة
    </button>

    <div class="history-title">
        المواضيع السابقة
    </div>

    <div id="history" class="history"></div>

</div>


<!-- الموقع -->

<div id="main" class="main full">

    <div class="header">

        <button class="menu" onclick="toggleSidebar()">
            ☰
        </button>

        <div id="headerTitle" class="header-title">
            Tito AI
        </div>

        <div></div>

    </div>


    <div id="chat" class="chat">

        <div id="welcome" class="welcome">

            <h1>
                مرحبًا، أنا Tito 🤖
            </h1>

            <p>
                كيف أقدر أساعدك اليوم؟
            </p>

        </div>

    </div>


    <div class="input-area">

        <div class="input-box">

            <textarea
                id="message"
                rows="1"
                placeholder="اكتب رسالتك إلى Tito..."
                onkeydown="handleKey(event)"
            ></textarea>

            <button
                id="sendButton"
                class="send"
                onclick="sendMessage()"
            >
                ↑
            </button>

        </div>

    </div>

</div>


<script>

/* =========================
   حفظ المحادثات
   ========================= */

let conversations =
    JSON.parse(localStorage.getItem("tito_conversations") || "[]");

let currentId = null;


/* =========================
   القائمة
   ========================= */

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


/* =========================
   محادثة جديدة
   ========================= */

function newChat() {

    currentId = null;

    document.getElementById("chat").innerHTML = `

        <div id="welcome" class="welcome">

            <h1>
                مرحبًا، أنا Tito 🤖
            </h1>

            <p>
                كيف أقدر أساعدك اليوم؟
            </p>

        </div>
    `;

    document.getElementById("headerTitle").textContent =
        "Tito AI";

    document.getElementById("message").focus();

    if (window.innerWidth <= 768) {
        toggleSidebar();
    }

    renderHistory();
}


/* =========================
   إنشاء محادثة
   ========================= */

function createConversation(firstMessage) {

    const id = Date.now().toString();

    const conversation = {

        id: id,

        title:
            firstMessage.substring(0, 35) ||
            "محادثة جديدة",

        messages: []

    };

    conversations.unshift(conversation);

    currentId = id;

    saveConversations();

    return conversation;
}


/* =========================
   حفظ
   ========================= */

function saveConversations() {

    localStorage.setItem(
        "tito_conversations",
        JSON.stringify(conversations)
    );

}


/* =========================
   عرض المواضيع
   ========================= */

function renderHistory() {

    const history =
        document.getElementById("history");

    history.innerHTML = "";

    conversations.forEach(function(conversation) {

        const div =
            document.createElement("div");

        div.className = "topic";

        if (conversation.id === currentId) {
            div.classList.add("active");
        }

        div.textContent = "💬 " + conversation.title;

        div.onclick = function() {

            loadConversation(conversation.id);
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }

        };

        history.appendChild(div);

    });

}


/* =========================
   فتح محادثة
   ========================= */

function loadConversation(id) {

    const conversation =
        conversations.find(c => c.id === id);

    if (!conversation) return;

    currentId = id;

    const chat =
        document.getElementById("chat");

    chat.innerHTML = "";

    document.getElementById("headerTitle").textContent =
        conversation.title;

    conversation.messages.forEach(function(message) {

        addMessage(
            message.text,
            message.type,
            false
        );

    });

    renderHistory();

}


/* =========================
   إضافة رسالة
   ========================= */

function addMessage(text, type, save = true) {

    const chat =
        document.getElementById("chat");

    const welcome =
        document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }

    const message =
        document.createElement("div");

    message.className =
        "message " + type;

    const bubble =
        document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = text;

    message.appendChild(bubble);

    chat.appendChild(message);

    chat.scrollTop =
        chat.scrollHeight;

    if (save && currentId) {

        const conversation =
            conversations.find(
                c => c.id === currentId
            );

        if (conversation) {

            conversation.messages.push({
                text: text,
                type: type
            });

            saveConversations();

        }

    }

    return bubble;
}


/* =========================
   إرسال
   ========================= */

async function sendMessage() {

    const input =
        document.getElementById("message");

    const button =
        document.getElementById("sendButton");

    const text =
        input.value.trim();

    if (!text) return;


    /* إنشاء محادثة */

    if (!currentId) {

        createConversation(text);

        document.getElementById("headerTitle")
            .textContent =
            text.substring(0, 35);

    }


    /* رسالة المستخدم */

    addMessage(
        text,
        "user"
    );

    input.value = "";

    button.disabled = true;


    /* تجهيز سجل المحادثة */

    const conversation =
        conversations.find(
            c => c.id === currentId
        );


    const loading =
        addMessage(
            "Tito يكتب... 🤔",
            "tito",
            false
        );


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    message: text,

                    history:
                        conversation.messages

                })

            });


        const data =
            await response.json();


        loading.textContent =
            data.reply;


        /* حفظ رد Tito */

        conversation.messages.push({

            text: data.reply,

            type: "tito"

        });


        saveConversations();

        renderHistory();


    } catch (error) {

        loading.textContent =
            "❌ حصل خطأ في الاتصال بـ Tito";

    }


    button.disabled = false;

    input.focus();

}


/* =========================
   Enter
   ========================= */

function handleKey(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


/* =========================
   تحميل المواضيع
   ========================= */

renderHistory();

</script>

</body>

</html>
"""


# =========================
# الصفحة الرئيسية
# =========================

@app.route("/")
def home():
    return render_template_string(HTML)


# =========================
# الذكاء الاصطناعي
# =========================

@app.route("/chat", methods=["POST"])
def chat_message():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "reply": "❌ لم يتم إرسال رسالة"
            })

        message = data.get(
            "message",
            ""
        ).strip()

        history = data.get(
            "history",
            []
        )


        if not message:

            return jsonify({
                "reply": "❌ اكتب رسالة أولًا"
            })


        # بناء سياق المحادثة
        prompt = """
أنت Tito AI، مساعد ذكاء اصطناعي مفيد وودود.
أجب باللغة العربية إذا كان المستخدم يتحدث بالعربية.
كن واضحًا ومفيدًا ولا تكرر نفسك.

سجل المحادثة السابقة:
"""


        for item in history:

            msg_type = item.get(
                "type",
                ""
            )

            text = item.get(
                "text",
                ""
            )

            if msg_type == "user":

                prompt += (
                    "\nالمستخدم: "
                    + text
                )

            elif msg_type == "tito":

                prompt += (
                    "\nTito: "
                    + text
                )


        prompt += (
            "\n\nالمستخدم الآن: "
            + message
            + "\n\nTito:"
        )


        response = client.models.generate_content(

            model=MODEL,

            contents=prompt

        )


        return jsonify({

            "reply":
                response.text

        })


    except Exception as e:

        print(
            "Gemini Error:",
            repr(e)
        )

        return jsonify({

            "reply":
                "❌ حصل خطأ أثناء الاتصال بـ Gemini"

        })


# =========================
# تشغيل
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
