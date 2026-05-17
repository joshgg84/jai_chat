from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

class ChatEngine:
    def generate_response(self, message: str, memory_context: dict) -> str:
        """Generate response using memory context"""
        message_lower = message.lower()
        
        # Use memory to personalize responses
        recent_topics = [m['interaction'].get('input', '') 
                        for m in memory_context.get('memories', [])[:3]]
        
        if any('name' in topic for topic in recent_topics):
            return "I remember you asked about my capabilities earlier!"
        
        # Basic responses
        if "remember" in message_lower:
            if memory_context.get('memories'):
                return f"I remember our previous conversations! You've spoken about {len(memory_context['memories'])} topics."
            else:
                return "This is our first conversation! I don't have any memories yet."
        
        # Default responses
        responses = {
            'hello': "Hello! Good to see you again!" if memory_context.get('memories') else "Hello! Nice to meet you!",
            'help': "I can remember our conversations and help with document processing. What do you need?",
            'bye': "Goodbye! I'll remember our conversation for next time."
        }
        
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return f"I understand: '{message}'. I'll remember this interaction."
    
    def get_conversation_summary(self, memory_context: dict) -> str:
        """Summarize past conversations from memory"""
        memories = memory_context.get('memories', [])
        if not memories:
            return "No previous conversations"
        
        topics = [m['interaction'].get('input', '')[:30] for m in memories[:5]]
        return f"Previously discussed: {', '.join(topics)}"

chat_engine = ChatEngine()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    response = chat_engine.generate_response(
        message=data.get('message', ''),
        memory_context=data.get('memory_context', {})
    )
    
    return jsonify({
        'reply': response,
        'context_id': data.get('context_id'),
        'used_memory': bool(data.get('memory_context', {}).get('memories'))
    })

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    summary = chat_engine.get_conversation_summary(
        data.get('memory_context', {})
    )
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)