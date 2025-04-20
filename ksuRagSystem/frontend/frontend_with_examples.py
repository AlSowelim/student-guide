import gradio as gr
from ksuRagSystem.backend.core_with_ollama_switch import run_llm

class ChatSession:
    def __init__(self):
        self.history = []

    def get_response(self, prompt):
        response = run_llm(query=prompt, chat_history=self.history)
        self.history.append(("human", prompt))
        self.history.append(("ai", response["result"]))
        return self.get_chat_display(), ""

    def get_chat_display(self):
        return "\n".join([f"👤: {m}" if r == "human" else f"🤖: {m}" for r, m in self.history])

chat_sessions = [ChatSession()]
current_index = 0

def select_chat(label):
    global current_index
    current_index = int(label.split()[-1]) - 1
    return chat_sessions[current_index].get_chat_display(), ""

def add_chat():
    global chat_sessions, current_index
    chat_sessions.append(ChatSession())
    current_index = len(chat_sessions) - 1
    labels = [f"استشارة {i+1}" for i in range(len(chat_sessions))]
    return gr.update(choices=labels, value=labels[current_index]), "", ""

def delete_chat():
    global chat_sessions, current_index
    if len(chat_sessions) > 1:
        # حذف الجلسة الحالية
        chat_sessions.pop(current_index)
        current_index = max(0, current_index - 1)  # إذا كانت الجلسة المحذوفة هي الأخيرة، اختر السابقة
        labels = [f"استشارة {i+1}" for i in range(len(chat_sessions))]
        return gr.update(choices=labels, value=labels[current_index]), "", ""
    else:
        # إذا كانت الجلسة الوحيدة في النظام
        chat_sessions = [ChatSession()]  # إعادة تهيئة الجلسات
        labels = [f"استشارة {i+1}" for i in range(len(chat_sessions))]
        return gr.update(choices=labels, value=labels[0]), "", ""

def chat_interface(prompt):
    return chat_sessions[current_index].get_response(prompt)

with gr.Blocks(css="""
body { direction: rtl; text-align: right; }
.gradio-container { direction: rtl; }

#header-row { direction: ltr; }
#ksu-logo { width: 50px !important; height: auto; margin: 10px; float: left; }
#app-title { margin: 20px 20px 0 0; font-size: 26px; font-weight: bold; float: right; }

.clearfix::after {
  content: "";
  display: table;
  clear: both;
}

#example-row {
  direction: rtl;
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
}
#example-btn {
  font-family: 'Amiri', 'Arial', sans-serif;
}
#example-title {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}
""") as demo:
    with gr.Row(elem_id="header-row"):
        with gr.Column(scale=1):
            gr.Image(value="ksu_logo_transparent.png", show_label=False, container=False, show_download_button=False,
                     show_fullscreen_button=False, elem_id="ksu-logo")
        with gr.Column(scale=9):
            gr.HTML('<div id="app-title">🧠 دليل الطالب</div>')

    with gr.Row():
        with gr.Column(scale=1):
            chat_selector = gr.Dropdown(choices=["استشارة 1"], value="استشارة 1", label="اختر الاستشارة")
            add_button = gr.Button("➕ استشارة جديدة")
            delete_button = gr.Button("❌ حذف الجلسة الحالية")
        with gr.Column(scale=4):
            chat_display = gr.Textbox(label="المحادثة", lines=20, interactive=False, rtl=True)
            prompt_input = gr.Textbox(placeholder="اكتب سؤالك هنا...", label="سؤال الطالب", rtl=True)

            gr.Markdown("### ✨ أمثلة على الأسئلة الشائعة", elem_id="example-title")
            with gr.Row(elem_id="example-row"):
                example1 = gr.Button("ما هي خطوات التقديم على التدريب؟", elem_id="example-btn")
                example2 = gr.Button("كيف أطلب إعادة قيد؟", elem_id="example-btn")
                example3 = gr.Button("ما هي خطوات التحويل من كلية إلى أخرى؟", elem_id="example-btn")

            submit_button = gr.Button("📝 أرسل")

    # أحداث التفاعل
    chat_selector.change(select_chat, inputs=chat_selector, outputs=[chat_display, prompt_input])
    add_button.click(add_chat, outputs=[chat_selector, chat_display, prompt_input])
    delete_button.click(delete_chat, outputs=[chat_selector, chat_display, prompt_input])
    submit_button.click(chat_interface, inputs=prompt_input, outputs=[chat_display, prompt_input])

    # تفاعل الأزرار مع الإدخال
    example1.click(fn=lambda: "ما هي خطوات التقديم على التدريب؟", outputs=prompt_input)
    example2.click(fn=lambda: "كيف أطلب إعادة قيد؟", outputs=prompt_input)
    example3.click(fn=lambda: "ما هي خطوات التحويل من كلية إلى أخرى؟", outputs=prompt_input)

demo.launch()
