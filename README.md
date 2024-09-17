# Qwen2-CoT-R

Qwen2-CoT-R (Qwen2 Chain-of-Thought Reasoning) is an advanced AI chat application that leverages the power of the Qwen2 language model to provide in-depth, analytical responses. This application offers a unique interface for engaging in high-level intellectual discourse with an AI assistant capable of complex reasoning and analysis.

## Features

- Interactive GUI built with tkinter
- Real-time streaming of AI responses
- Visualization of the AI's thinking and analysis process
- Clear chat functionality
- Error handling and logging
- Custom styling for an enhanced user experience

## Requirements

- Python 3.6+
- tkinter
- requests
- Ollama with the Qwen2 model

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lalomorales22/Qwen2-CoT-R.git
   cd Qwen2-CoT-R
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have Ollama installed and the Qwen2 model pulled:
   ```
   ollama pull qwen2
   ```

## Usage

1. Start the Ollama server with the Qwen2 model.

2. Run the application:
   ```
   python qwen2_chat_app.py
   ```

3. Use the GUI to interact with the Qwen2 AI:
   - Type your message in the input field and press Enter or click 'Send'
   - View the AI's thinking process and analysis in separate sections
   - Clear the chat history using the 'Clear Chat' button

## Configuration

The application is pre-configured to use `http://localhost:11434/api/generate` as the Ollama API endpoint. If your Ollama server is running on a different address or port, modify the `ollama_url` variable in the `Qwen2ChatApp` class.

## Contributing

Contributions to Qwen2-CoT-R are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License

[MIT License](LICENSE)

## Acknowledgements

- Qwen2 model by Alibaba Cloud
- Ollama for providing local API access to large language models

