import streamlit as st
import json
import requests
from datetime import datetime
import time
import re

# Set page config
st.set_page_config(
    page_title="SkinCare AI Assistant", 
    page_icon="🌸",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Skincare Knowledge Base (Replace with your NotebookLM Q&A data)
SKINCARE_KB = {
    "acne": {
        "keywords": ["acne", "pimples", "breakouts", "blackheads", "whiteheads", "oily skin"],
        "answer": "For acne-prone skin, I recommend using gentle, non-comedogenic products. Start with a mild cleanser, use salicylic acid or benzoyl peroxide treatments, and always moisturize. Our Facebook page features effective acne-fighting products that many customers love!",
        "products": ["Gentle Foam Cleanser", "Salicylic Acid Treatment", "Oil-Free Moisturizer"]
    },
    "dry_skin": {
        "keywords": ["dry skin", "flaky", "tight", "dehydrated", "moisturizer"],
        "answer": "Dry skin needs intensive hydration. Use a cream-based cleanser, apply hydrating serums with hyaluronic acid, and use rich moisturizers. Don't forget SPF during the day!",
        "products": ["Hydrating Cream Cleanser", "Hyaluronic Acid Serum", "Rich Night Cream"]
    },
    "anti_aging": {
        "keywords": ["wrinkles", "fine lines", "anti-aging", "aging", "mature skin", "retinol"],
        "answer": "For anti-aging, focus on retinoids, vitamin C, and SPF protection. Start slowly with retinol and always use sunscreen. Our anti-aging collection has proven results!",
        "products": ["Vitamin C Serum", "Retinol Cream", "Anti-Aging Moisturizer"]
    },
    "sensitive_skin": {
        "keywords": ["sensitive", "irritated", "redness", "burning", "stinging"],
        "answer": "Sensitive skin needs gentle, fragrance-free products. Look for ingredients like ceramides, niacinamide, and avoid harsh actives. Patch test everything!",
        "products": ["Gentle Cleanser", "Calming Serum", "Barrier Repair Cream"]
    }
}

# Free AI API function (using Hugging Face Inference API)
def get_ai_response(user_input, context=""):
    """
    Use Hugging Face's free inference API for natural language responses
    You can replace this with other free APIs like Cohere, etc.
    """
    try:
        # Simple keyword matching first (no API cost)
        user_input_lower = user_input.lower()
        
        for category, data in SKINCARE_KB.items():
            if any(keyword in user_input_lower for keyword in data["keywords"]):
                return {
                    "response": data["answer"],
                    "products": data["products"],
                    "category": category
                }
        
        # If no direct match, create a general response
        return {
            "response": "I'd love to help you with your skincare concerns! Could you tell me more about your skin type or specific issues? I can recommend products from our collection.",
            "products": [],
            "category": "general"
        }
        
    except Exception as e:
        return {
            "response": "I'm here to help with your skincare questions! What would you like to know about skincare routines, products, or ingredients?",
            "products": [],
            "category": "general"
        }

def add_to_chat(role, message, products=None):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "message": message,
        "products": products or [],
        "timestamp": datetime.now().strftime("%H:%M")
    })

def display_chat():
    """Display chat messages"""
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**You** ({chat['timestamp']})")
                st.write(chat["message"])
        else:
            with st.chat_message("assistant"):
                st.write(f"**SkinCare AI** ({chat['timestamp']})")
                st.write(chat["message"])
                
                if chat["products"]:
                    st.write("**Recommended Products:**")
                    for product in chat["products"]:
                        st.write(f"• {product}")
                    
                    st.info("💫 Visit our Facebook page to see these products and more!")

def skin_analysis_form():
    """Skin analysis questionnaire"""
    st.subheader("🔍 Skin Analysis")
    st.write("Help me understand your skin better!")
    
    with st.form("skin_analysis"):
        skin_type = st.selectbox(
            "What's your skin type?",
            ["Not sure", "Oily", "Dry", "Combination", "Sensitive", "Normal"]
        )
        
        concerns = st.multiselect(
            "What are your main skin concerns?",
            ["Acne/Breakouts", "Dryness", "Fine lines/Wrinkles", "Dark spots", "Sensitivity", "Large pores", "Dullness"]
        )
        
        current_routine = st.text_area("Describe your current skincare routine (optional)")
        
        age_range = st.selectbox(
            "Age range",
            ["Under 20", "20-30", "30-40", "40-50", "50+"]
        )
        
        submitted = st.form_submit_button("Get Personalized Recommendations")
        
        if submitted:
            # Store user profile
            st.session_state.user_profile = {
                "skin_type": skin_type,
                "concerns": concerns,
                "routine": current_routine,
                "age_range": age_range
            }
            
            # Generate personalized response
            analysis_text = f"Based on your {skin_type.lower()} skin type and concerns about {', '.join(concerns).lower()}, here are my recommendations:"
            
            ai_response = get_ai_response(f"skin type {skin_type} concerns {' '.join(concerns)}")
            
            add_to_chat("assistant", f"{analysis_text}\n\n{ai_response['response']}", ai_response['products'])
            st.rerun()

# Main App Layout
st.title("🌸 SkinCare AI Assistant")
st.subheader("Your Personal Skincare Expert & Product Consultant")

# Sidebar
with st.sidebar:
    st.header("📱 About")
    st.write("I'm your AI skincare assistant! I can help you with:")
    st.write("• Skincare routines")
    st.write("• Product recommendations") 
    st.write("• Ingredient questions")
    st.write("• Skin concerns")
    
    st.markdown("---")
    
    st.header("🛍️ Our Products")
    st.write("Visit our Facebook page for:")
    st.write("• Latest skincare products")
    st.write("• Customer reviews")
    st.write("• Special offers")
    st.write("• Skincare tips")
    
    if st.button("📋 Take Skin Analysis"):
        st.session_state.show_analysis = True
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with AI Assistant")
    
    # Show skin analysis form if requested
    if st.session_state.get('show_analysis', False):
        skin_analysis_form()
        if st.button("Back to Chat"):
            st.session_state.show_analysis = False
            st.rerun()
    else:
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            # Display existing chat
            if st.session_state.chat_history:
                display_chat()
            else:
                st.info("👋 Hi! I'm your skincare AI assistant. Ask me anything about skincare, routines, or our products!")
        
        # Chat input
        user_input = st.chat_input("Ask me about skincare...")
        
        if user_input:
            # Add user message
            add_to_chat("user", user_input)
            
            # Get AI response
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(user_input)
            
            # Add AI response
            add_to_chat("assistant", ai_response['response'], ai_response['products'])
            
            st.rerun()

with col2:
    st.header("🎯 Quick Actions")
    
    # Quick question buttons
    if st.button("What's my skin type?"):
        add_to_chat("user", "What's my skin type?")
        response = get_ai_response("skin type help")
        add_to_chat("assistant", "To determine your skin type, consider: How does your skin feel after cleansing? Oily skin feels greasy, dry skin feels tight, combination has both, and sensitive skin gets irritated easily. Try our skin analysis for personalized recommendations!")
        st.rerun()
    
    if st.button("Morning routine help"):
        add_to_chat("user", "What should my morning routine be?")
        add_to_chat("assistant", "A basic morning routine: 1) Gentle cleanser 2) Toner (optional) 3) Serum (vitamin C is great) 4) Moisturizer 5) SPF (most important!). Adjust based on your skin type and concerns.")
        st.rerun()
    
    if st.button("Product recommendations"):
        add_to_chat("user", "Can you recommend products?")
        add_to_chat("assistant", "I'd love to help! What's your skin type and main concerns? Check our Facebook page for our complete product range with customer reviews and detailed descriptions.")
        st.rerun()
    
    st.markdown("---")
    
    st.header("🌟 User Profile")
    if st.session_state.user_profile:
        profile = st.session_state.user_profile
        st.write(f"**Skin Type:** {profile.get('skin_type', 'Not set')}")
        st.write(f"**Age Range:** {profile.get('age_range', 'Not set')}")
        if profile.get('concerns'):
            st.write(f"**Concerns:** {', '.join(profile['concerns'])}")
    else:
        st.info("Take the skin analysis to get personalized recommendations!")
    
    st.markdown("---")
    
    st.header("📞 Connect With Us")
    st.write("🔗 Facebook Page: [Visit our store](#)")
    st.write("📱 WhatsApp: [Chat with us](#)")
    st.write("📧 Email: skincare@example.com")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>🌸 Your Brand Name AI - Your trusted beauty companion</p>
    <p>For product purchases and detailed consultations, visit our Facebook page!</p>
    </div>
    """, 
    unsafe_allow_html=True
)
