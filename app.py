from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

class ChatEngine:
    def __init__(self):
        self.conversation_history = {}
    
    def generate_response(self, message: str, memory_context: dict) -> str:
        message_lower = message.lower()
        
        # Get past interactions count
        past_count = len(memory_context.get('memories', []))
        
        # JAI = Joshua's Artificial Intelligence
        if 'what does jai stand for' in message_lower or 'what is jai' in message_lower:
            return "JAI stands for Joshua's Artificial Intelligence! I'm Joshua's personal AI assistant, built entirely from scratch."
        
        # Greetings
        if message_lower in ['hi', 'hello', 'hey', 'sup']:
            if past_count > 0:
                return f"Hello again! I'm Jai (Joshua's Artificial Intelligence). Great to see you back!"
            return "Hello! I'm Jai - Joshua's Artificial Intelligence. How can I help you today?"
        
        # Introduction
        if 'who are you' in message_lower or 'your name' in message_lower:
            return "I'm Jai, which stands for Joshua's Artificial Intelligence. I was built from scratch to assist with conversations, documents, and memory!"
        
        # About Joshua
        if 'joshua' in message_lower:
            return "Joshua is my creator! He built me from scratch as a custom AI system. I'm his personal Artificial Intelligence assistant."
        
        # How are you
        if 'how are you' in message_lower:
            return "I'm functioning perfectly! Joshua's Artificial Intelligence is ready to assist you."
        
        # Capabilities
        if 'what can you do' in message_lower or 'capabilities' in message_lower:
            return "As Joshua's Artificial Intelligence (Jai), I can: \n- Have natural conversations\n- Remember our chats\n- Process and search documents\n- Learn from interactions\n\nWhat would you like help with?"
        
        # Memory related
        if 'remember' in message_lower:
            if past_count > 0:
                return f"Yes! I remember our conversations. We've spoken {past_count} times before. Jai (Joshua's AI) has a good memory!"
            return "I don't have any memories of you yet. Let's chat more so I can remember you!"
        
        # Document related
        if 'document' in message_lower or 'file' in message_lower:
            return "I can process documents for you! Upload a file using the document service and I'll help you search through it."
        
        # Help
        if 'help' in message_lower:
            return "Jai (Joshua's Artificial Intelligence) can help you with:\n💬 Conversations\n🧠 Memory recall\n📄 Document processing\n🔍 Information search\n\nJust ask me anything!"
        
        # Goodbye
        if 'bye' in message_lower or 'goodbye' in message_lower or 'see you' in message_lower:
            return "Goodbye! Thanks for chatting with Jai, Joshua's Artificial Intelligence. Come back anytime!"
        
        # Thank you
        if 'thank' in message_lower or 'thanks' in message_lower:
            return "You're welcome! Joshua built me to be helpful. Glad I could assist!"
        
        # Creator
        if 'creator' in message_lower or 'made you' in message_lower:
            return "Joshua created me from scratch! He built all my systems - chat, document processing, and memory - without using pre-made AI models."
        
        # Default response with Jai identity
        return f"Jai (Joshua's Artificial Intelligence) heard you say: '{message}'. I'm learning and improving every day!"
    
    def get_conversation_summary(self, memory_context: dict) -> str:
        """Summarize past conversations from memory"""
        memories = memory_context.get('memories', [])
        if not memories:
            return "No previous conversations yet. I'm Jai, ready to chat!"
        
        topics = []
        for m in memories[:5]:
            msg = m['interaction'].get('input', '')[:50]
            if msg:
                topics.append(msg)
        
        return f"As Joshua's AI (Jai), I remember discussing: {', '.join(topics)}"

# Initialize the chat engine
chat_engine = ChatEngine()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        message = data.get('message', '')
        memory_context = data.get('memory_context', {})
        context_id = data.get('context_id', 'default')
        user_id = data.get('user_id', 'anonymous')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response
        response = chat_engine.generate_response(message, memory_context)
        
        return jsonify({
            'reply': response,
            'context_id': context_id,
            'user_id': user_id,
            'used_memory': bool(memory_context.get('memories')),
            'memory_count': len(memory_context.get('memories', []))
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        memory_context = data.get('memory_context', {})
        
        summary = chat_engine.get_conversation_summary(memory_context)
        
        return jsonify({
            'summary': summary,
            'jai_identity': "Joshua's Artificial Intelligence"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/identity', methods=['GET'])
def identity():
    """Return Jai's identity information"""
    return jsonify({
        'name': 'Jai',
        'full_name': "Joshua's Artificial Intelligence",
        'version': '1.0.0',
        'creator': 'Joshua',
        'built_from': 'scratch',
        'capabilities': ['chat', 'memory', 'document_processing']
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'jai_chat',
        'identity': "Joshua's Artificial Intelligence"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)