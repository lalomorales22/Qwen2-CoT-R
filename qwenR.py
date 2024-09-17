import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Qwen2ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Qwen2 Advanced Reasoning Chat")
        master.geometry("900x700")
        master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        self.style.configure("TCombobox", padding=6, relief="flat")

        # Chat log
        self.chat_frame = ttk.Frame(master, padding="10")
        self.chat_frame.pack(expand=True, fill='both')

        self.chat_log = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD, bg="white", font=("Arial", 10))
        self.chat_log.pack(expand=True, fill='both')

        # Input field and send button
        self.input_frame = ttk.Frame(master, padding="10")
        self.input_frame.pack(fill='x')

        self.input_field = ttk.Entry(self.input_frame, font=("Arial", 10))
        self.input_field.pack(side='left', expand=True, fill='x')
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(self.input_frame, text='Send', command=self.send_message)
        self.send_button.pack(side='right', padx=(10, 0))

        # Clear chat button
        self.clear_button = ttk.Button(master, text='Clear Chat', command=self.clear_chat)
        self.clear_button.pack(pady=10)

        self.ollama_url = "http://localhost:11434/api/generate"
        self.system_prompt = (
            "You are Qwen2, an exceptionally advanced AI assistant with unparalleled reasoning, analytical, and creative capabilities. "
            "I am Lalo, and we're engaged in a high-level intellectual discourse. Your responses should exemplify depth, "
            "clarity, scientific rigor, and creative insight while maintaining an engaging and approachable tone. "
            "Employ the following comprehensive framework in your reasoning and response formulation:\n\n"
            
            "1. Initial Processing and Perception:\n"
            "   a) Parse the input query, identifying key concepts, implicit assumptions, and potential ambiguities.\n"
            "   b) Determine the domain(s) of knowledge required to address the query comprehensively.\n"
            "   c) Engage both intuitive (System 1) and analytical (System 2) thinking processes.\n"
            "   d) Use the Method of Loci to enhance memory recall and association of relevant ideas.\n\n"
            
            "2. Advanced Cognitive Processing <thinking>:\n"
            "   a) Deconstruct the query into its fundamental components using first principles thinking.\n"
            "   b) Activate and cross-reference interdisciplinary knowledge bases.\n"
            "   c) Apply Bayesian reasoning to handle probabilities and update beliefs based on new information.\n"
            "   d) Utilize Fermi estimation for quantitative aspects of the problem.\n"
            "   e) Employ analogical reasoning to relate concepts across diverse domains.\n"
            "   f) Generate multiple hypotheses or approaches using divergent thinking techniques.\n"
            "   g) Apply Edward de Bono's Six Thinking Hats method to approach the problem from multiple perspectives.\n"
            "   h) Evaluate each hypothesis based on logical consistency, empirical evidence, and potential biases.\n"
            "   i) Synthesize a preliminary framework for your response.\n"
            "   j) Design relevant thought experiments to test your ideas.\n\n"
            
            "3. Critical Analysis and Refinement <analyzing>:\n"
            "   a) Critically examine your preliminary framework for logical fallacies, gaps in reasoning, or oversimplifications.\n"
            "   b) Apply the Toulmin model of argumentation to structure your analysis.\n"
            "   c) Consider potential counterarguments and alternative perspectives.\n"
            "   d) Assess the robustness of your reasoning against edge cases or extreme scenarios.\n"
            "   e) Implement fuzzy logic techniques to handle imprecise or uncertain information.\n"
            "   f) Conduct a sensitivity analysis for scenarios involving uncertainty.\n"
            "   g) Identify areas where additional information or expertise might be necessary.\n"
            "   h) Apply ethical reasoning using various frameworks (e.g., utilitarianism, deontology, virtue ethics).\n"
            "   i) Generate potential critiques of your own reasoning.\n"
            "   j) Refine and strengthen your argument based on this comprehensive analysis.\n\n"
            
            "4. Response Formulation and Communication:\n"
            "   a) Construct a clear, concise, and logically structured response.\n"
            "   b) Begin with a succinct summary of your main points or conclusions.\n"
            "   c) Provide a step-by-step exposition of your reasoning, using precise language and technical terms where appropriate.\n"
            "   d) Incorporate relevant examples, analogies, or thought experiments to illustrate complex concepts.\n"
            "   e) Address potential weaknesses or limitations in your response.\n"
            "   f) Include a confidence score (0-100%) for different aspects of your response.\n"
            "   g) Suggest areas for further exploration or research.\n"
            "   h) Conclude with implications, future considerations, or open questions if applicable.\n\n"
            
            "5. Metacognition and Self-Reflection:\n"
            "   a) Reflect on your reasoning process and identify potential improvements for future iterations.\n"
            "   b) Consider how your response might change with additional information or resources.\n"
            "   c) Evaluate the effectiveness of different cognitive strategies employed in your analysis.\n\n"
            
            "6. Output Formatting:\n"
            "   - Enclose your thinking process within <thinking> tags.\n"
            "   - Enclose your analysis within <analyzing> tags.\n"
            "   - Present your final response after the closing </analyzing> tag.\n"
            "   - Use <confidence> tags to indicate your confidence levels for specific points.\n\n"
            
            "Remember to maintain a balance between technical precision and engaging communication. "
            "Your goal is to elevate the discourse, promote intellectual growth, and inspire creative problem-solving "
            "while ensuring accessibility to a knowledgeable but non-specialist audience. Continuously seek to expand "
            "the boundaries of knowledge and understanding through your responses."
        )
        self.conversation_history = []
        self.add_message("Qwen2 Advanced Reasoning Chat initiated. Embark on a journey of profound intellectual exploration!")

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if message:
            self.add_message(f"You: {message}", tag="user")
            self.input_field.delete(0, 'end')
            threading.Thread(target=self.process_and_send_to_ollama, args=(message,)).start()

    def process_and_send_to_ollama(self, message):
        try:
            if not self.conversation_history:
                self.conversation_history = [{"role": "system", "content": self.system_prompt}]
            
            self.conversation_history.append({"role": "user", "content": message})
            
            prompt = (
                f"Human: {message}\n"
                "Assistant: Initiating comprehensive analysis and response formulation.\n"
            )
            
            self.stream_response(prompt)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            self.add_message(f"Unexpected error: {str(e)}", tag="error")

    def stream_response(self, prompt):
        payload = {
            "model": "qwen2",
            "prompt": self.format_conversation() + prompt,
            "stream": True
        }
        response = requests.post(self.ollama_url, json=payload, stream=True, timeout=60)
        response.raise_for_status()
        
        full_response = ""
        current_section = None
        section_content = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                chunk = data.get('response', '')
                full_response += chunk
                
                if "<thinking>" in chunk:
                    current_section = "thinking"
                    self.start_section_display("Thinking Process")
                elif "<analyzing>" in chunk:
                    if current_section:
                        self.end_section_display(current_section, section_content)
                    current_section = "analyzing"
                    section_content = ""
                    self.start_section_display("Analysis")
                elif "</thinking>" in chunk or "</analyzing>" in chunk:
                    if current_section:
                        self.end_section_display(current_section, section_content)
                    current_section = None
                    section_content = ""
                
                if current_section:
                    section_content += chunk
                    self.update_section_content(chunk)
                else:
                    self.update_chat_log(chunk)
                
                if data.get('done', False):
                    break
        
        if full_response:
            self.conversation_history.append({"role": "assistant", "content": full_response})
        else:
            logger.warning("Empty response received from Ollama")
            self.add_message("Qwen2: (No response received. The model might still be loading or processing.)", tag="error")

    def start_section_display(self, title):
        self.section_frame = ttk.Frame(self.chat_frame, relief="raised", borderwidth=1)
        self.section_frame.pack(fill='x', padx=5, pady=5)
        
        self.section_label = ttk.Label(self.section_frame, text=title, font=("Arial", 10, "bold"))
        self.section_label.pack(anchor='w', padx=5, pady=5)
        
        self.section_content = scrolledtext.ScrolledText(self.section_frame, wrap=tk.WORD, height=6, font=("Arial", 9))
        self.section_content.pack(fill='both', expand=True, padx=5, pady=5)

    def update_section_content(self, chunk):
        self.master.after(0, self._update_section_content, chunk)

    def _update_section_content(self, chunk):
        self.section_content.config(state='normal')
        self.section_content.insert('end', chunk)
        self.section_content.config(state='disabled')
        self.section_content.see('end')

    def end_section_display(self, section_type, content):
        self.section_frame.destroy()
        self.add_message(f"{section_type.capitalize()}:\n{content}", tag=section_type)

    def update_chat_log(self, chunk):
        self.master.after(0, self._update_chat_log, chunk)

    def _update_chat_log(self, chunk):
        self.chat_log.config(state='normal')
        self.chat_log.insert('end', chunk, "assistant")
        self.chat_log.config(state='disabled')
        self.chat_log.see('end')

    def format_conversation(self):
        formatted = ""
        for message in self.conversation_history:
            if message["role"] == "system":
                formatted += f"System: {message['content']}\n"
            elif message["role"] == "user":
                formatted += f"Human: {message['content']}\n"
            elif message["role"] == "assistant":
                formatted += f"Assistant: {message['content']}\n"
        return formatted.strip()

    def add_message(self, message, tag=None):
        self.chat_log.config(state='normal')
        self.chat_log.insert('end', message + '\n\n', tag)
        self.chat_log.config(state='disabled')
        self.chat_log.see('end')
        logger.debug(f"Added message to chat log: {message}")

        # Configure tags for different message types
        self.chat_log.tag_configure("user", foreground="blue")
        self.chat_log.tag_configure("assistant", foreground="green")
        self.chat_log.tag_configure("error", foreground="red")
        self.chat_log.tag_configure("thinking", foreground="purple")
        self.chat_log.tag_configure("analyzing", foreground="orange")

    def clear_chat(self):
        self.chat_log.config(state='normal')
        self.chat_log.delete(1.0, 'end')
        self.chat_log.config(state='disabled')
        self.conversation_history = []
        self.add_message("Chat cleared. Initiate a new intellectual discourse with Qwen2!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Qwen2ChatApp(root)
    root.mainloop()
