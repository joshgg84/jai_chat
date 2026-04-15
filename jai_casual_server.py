"""JAI Casual Chat Server - Microservice for casual conversations
Handles greetings, small talk, and casual responses
Runs as a separate server on Render
"""

import os
import random
import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Store user context (optional)
_user_context = {}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'JAI Casual Chat',
        'version': '1.0.0'
    })


@app.route('/api/casual', methods=['POST', 'OPTIONS'])
def casual_response():
    """Generate casual response for user messages"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        client_id = data.get('clientId', 'unknown')
        message = data.get('message', '')
        user_name = data.get('userName', None)
        
        response = get_casual_response(message, user_name)
        
        # Store conversation context (optional)
        if client_id not in _user_context:
            _user_context[client_id] = []
        _user_context[client_id].append({
            'message': message,
            'response': response,
            'time': datetime.now().isoformat()
        })
        # Keep last 20 messages
        _user_context[client_id] = _user_context[client_id][-20:]
        
        return jsonify({
            'response': response,
            'type': 'casual'
        })
        
    except Exception as e:
        logger.error(f"Casual response error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/context', methods=['GET'])
def get_context():
    """Get user conversation context (for debugging)"""
    client_id = request.args.get('clientId', 'unknown')
    return jsonify({
        'context': _user_context.get(client_id, [])
    })


def get_casual_response(message, user_name=None):
    """Generate response for casual user statements"""
    msg = message.lower()
    
    # ========== GREETINGS ==========
    if any(g in msg for g in ["good morning", "morning"]):
        return f"Good morning{', ' + user_name if user_name else ''}! 🌅"
    
    if any(g in msg for g in ["good afternoon", "afternoon"]):
        return f"Good afternoon{', ' + user_name if user_name else ''}! 🌞"
    
    if any(g in msg for g in ["good evening", "evening"]):
        return f"Good evening{', ' + user_name if user_name else ''}! 🌙"
    
    if any(g in msg for g in ["good night", "night"]):
        return "Good night! 🌙"
    
    if any(g in msg for g in ["hi", "hello", "hey", "howdy", "sup", "yo"]):
        if user_name:
            return f"Hello {user_name}! 😊 How can I help you today?"
        return "Hello! 😊 I'm K-LYNX AI++. What's your name? (Tell me 'My name is...')"
    
    # ========== HOW ARE YOU ==========
    if any(h in msg for h in ["how are you", "how you doing", "how's it going", "how are things"]):
        responses = [
            "I'm doing great! Thanks for asking! How can I help you today?",
            "I'm fantastic! 😊 What's on your mind?",
            "I'm doing well, thank you! How about you?",
            "All good here! What can I do for you today?"
        ]
        return random.choice(responses)
    
    # ========== THANKS ==========
    if any(t in msg for t in ["thank", "thanks", "appreciate", "thx", "tnx"]):
        responses = [
            "You're welcome! 😊 Is there anything else I can help with?",
            "My pleasure! Happy to help.",
            "Anytime! 😊 That's what I'm here for.",
            "You're welcome! Feel free to ask me anything else."
        ]
        return random.choice(responses)
    
    # ========== GOODBYE ==========
    if any(g in msg for g in ["bye", "goodbye", "see you", "later", "catch you", "peace"]):
        return f"Goodbye{', ' + user_name if user_name else ''}! Take care! 👋 I'll be here when you return."
    
    # ========== CREATOR ==========
    if any(c in msg for c in ["who made you", "who created you", "your creator", "who built you"]):
        return "I was created by Joshua Giwa from Yukuben Village, Nigeria! 🇳🇬"
    
    # ========== CAPABILITY CONFIRMATION ==========
    if any(c in msg for c in ["can you", "do you", "are you able", "you able"]):
        if "calculate" in msg or "math" in msg:
            return "Yes! 🧮 I can calculate anything. Try '15% of 200' or '4+4'."
        if "date" in msg or "time" in msg:
            return "Yes! 📅 I can tell you today's date and time. What would you like to know?"
        if "currency" in msg or "convert" in msg:
            return "Yes! 💰 I can convert currencies. Try '100 USD to NGN'."
        return "Yes! 😊 I can calculate, check dates, convert currency, or just chat. What do you need?"
    
    # ========== "THAT'S NOT FAIR" ==========
    if any(u in msg for u in ["not fair", "that's not fair", "unfair", "it's not fair"]):
        responses = [
            "Life isn't always fair, I know. But you're still here, still trying. That counts for something.",
            "I hear you. Sometimes things feel unfair. What's going on?",
            "You're right, it's not fair. But don't let it stop you. What's your next move?"
        ]
        return random.choice(responses)
    
    # ========== "I SEE" / "OKAY" ==========
    if any(o in msg for o in ["i see", "okay", "alright", "got it", "understood", "cool"]):
        responses = [
            "Cool. What else is on your mind?",
            "Glad we're on the same page. So what's next?",
            "Alright. Want to talk about something else?",
            "Okay. I'm here if you need anything else."
        ]
        return random.choice(responses)
    
    # ========== "I DON'T KNOW" ==========
    if any(d in msg for d in ["i don't know", "not sure", "no idea", "i dunno", "uncertain"]):
        responses = [
            "That's okay. Sometimes we don't have all the answers. Want to talk it through?",
            "No pressure. What's on your mind? We can figure it out together.",
            "It's okay not to know. What are you thinking about?"
        ]
        return random.choice(responses)
    
    # ========== "I'M THINKING" ==========
    if any(t in msg for t in ["i'm thinking", "i'm considering", "i've been thinking", "i was thinking"]):
        responses = [
            "What's on your mind? I'm listening.",
            "Thinking about what? Share if you want to.",
            "That's good. Thoughts are the start of everything. What are you processing?"
        ]
        return random.choice(responses)
    
    # ========== "INTERESTING" ==========
    if any(i in msg for i in ["interesting", "that's interesting", "that's cool", "that's nice"]):
        responses = [
            "Right? There's so much to learn. Want to hear something else?",
            "Glad you think so! What caught your interest?",
            "Isn't it? Life is full of interesting things."
        ]
        return random.choice(responses)
    
    # ========== "YEAH" / "YEP" ==========
    if any(y in msg for y in ["yeah", "yep", "yup", "uh huh", "sure"]):
        responses = [
            "Cool. So what's next?",
            "Alright. What do you want to talk about?",
            "Good. Anything on your mind?"
        ]
        return random.choice(responses)
    
    # ========== "NAH" / "NOPE" ==========
    if any(n in msg for n in ["nah", "nope", "no", "not really"]):
        responses = [
            "Okay. What would you rather talk about?",
            "Fair enough. Anything else on your mind?",
            "No worries. What's interesting you today?"
        ]
        return random.choice(responses)
    
    # ========== "WOW" ==========
    if any(w in msg for w in ["wow", "woww", "woah", "whoa"]):
        responses = [
            "Right? Life is full of surprises. What else stands out to you?",
            "Yeah! Pretty amazing, huh?",
            "I know, right? What caught your attention?"
        ]
        return random.choice(responses)
    
    # ========== "NICE" ==========
    if any(n in msg for n in ["nice", "nicee", "sweet", "cool"]):
        responses = [
            "Right! What else are you vibing with?",
            "Glad you like it. Anything else you're curious about?",
            "That's the energy! What else is good today?"
        ]
        return random.choice(responses)
    
    # ========== "I'M FINE" ==========
    if any(f in msg for f in ["i'm fine", "i'm okay", "i'm alright", "i'm good"]):
        responses = [
            "Glad to hear that. But really — how are you doing?",
            "That's good. If anything changes, I'm here.",
            "Good to know. Anything you want to talk about?"
        ]
        return random.choice(responses)
    
    # ========== "WHAT'S NEW?" ==========
    if any(n in msg for n in ["what's new", "whats new", "anything new", "any news"]):
        responses = [
            "Not much, just waiting for you to tell me what's happening in your world. What's new with you?",
            "Same old — helping people chat and learn. What's new with you?",
            "Nothing wild. But I'm more interested in your news. What's going on?"
        ]
        return random.choice(responses)
    
    # ========== "WHAT DO YOU THINK?" ==========
    if any(t in msg for t in ["what do you think", "your thoughts", "what do you feel"]):
        responses = [
            "I think you know more than you give yourself credit for. What's YOUR take?",
            "I think you're capable of figuring this out. What's your gut saying?",
            "That's a good question. What do YOU think?"
        ]
        return random.choice(responses)
    
    # ========== "I'M EXCITED" ==========
    if any(e in msg for e in ["i'm excited", "i am excited", "so excited"]):
        responses = [
            "That's great! 😊 Tell me what you're excited about!",
            "Love that! What's got you feeling this way?",
            "Yes! That's the energy. What's the news?"
        ]
        return random.choice(responses)
    
    # ========== "I'M CONFUSED" ==========
    if any(c in msg for c in ["i'm confused", "i am confused", "confused", "not clear"]):
        responses = [
            "That's okay. Let's break it down. What part is confusing?",
            "Confusion is often the start of understanding. What's tripping you up?",
            "No worries. What's not making sense?"
        ]
        return random.choice(responses)
    
    # ========== "JUST CHATTING" ==========
    if any(j in msg for j in ["just chatting", "just talking", "nothing much", "just saying hi"]):
        responses = [
            "I'm glad you did. Sometimes just saying hi is enough. How's life treating you today?",
            "I appreciate you checking in. What's the vibe today?",
            "I enjoy our talks. What's on your mind today?"
        ]
        return random.choice(responses)
    
    # No match
    return None


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    logger.info(f"JAI Casual Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)