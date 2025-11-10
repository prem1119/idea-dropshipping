"""AI customer service agent for handling customer messages."""
import logging
from typing import List, Optional, Dict
from datetime import datetime
import httpx

from backend.models.schemas import CustomerMessage
from backend.config.settings import get_settings
import shopify

logger = logging.getLogger(__name__)
settings = get_settings()


class CustomerServiceAgent:
    """AI agent for handling customer service messages."""
    
    def __init__(self):
        self.huggingface_token = settings.huggingface_api_token
        self.huggingface_model = settings.huggingface_model
        self.openai_key = settings.openai_api_key
        self.auto_service_enabled = settings.auto_customer_service_enabled
        self.shopify_store_name = settings.shopify_store_name
        self.shopify_access_token = settings.shopify_access_token
        self.use_huggingface = bool(self.huggingface_token)
        
        if not self.huggingface_token and not self.openai_key:
            logger.warning("No AI API key configured (Hugging Face or OpenAI), using mock responses")
        
        # Initialize Shopify session
        if self.shopify_store_name and self.shopify_access_token:
            shopify.ShopifyResource.set_site(
                f"https://{self.shopify_store_name}.myshopify.com/admin/api/2024-01"
            )
            self.session = shopify.Session(
                f"{self.shopify_store_name}.myshopify.com",
                "2024-01",
                self.shopify_access_token
            )
        else:
            self.session = None
    
    async def get_messages(self, answered: bool = False) -> List[CustomerMessage]:
        """Get customer service messages from Shopify."""
        if not self.session:
            logger.warning("Shopify not configured, returning mock messages")
            return self._get_mock_messages()
        
        try:
            # Get customer messages/emails from Shopify
            # Note: Shopify doesn't have a direct messages API
            # In production, you'd integrate with:
            # - Shopify Chat/Inbox
            # - Email service (Gmail API, etc.)
            # - Third-party chat platforms
            
            # For now, we'll simulate getting messages
            messages = []
            
            # In production, fetch actual messages
            # messages = await self._fetch_shopify_messages()
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []
    
    async def handle_message(self, message_id: str) -> Dict:
        """
        Automatically handle a customer service message.
        Generates AI response and sends it.
        """
        if not self.auto_service_enabled:
            return {"status": "disabled", "message": "Auto customer service is disabled"}
        
        logger.info(f"Handling message: {message_id}")
        
        try:
            # Get message (would fetch from DB/API in production)
            message = await self._get_message(message_id)
            if not message:
                return {"status": "error", "message": "Message not found"}
            
            # Check if message needs response
            if message.answered:
                return {"status": "already_answered", "message": "Message already handled"}
            
            # Generate AI response
            response_text = await self._generate_response(message)
            
            # Send response
            sent = await self._send_response(message, response_text)
            
            if sent:
                logger.info(f"Response sent for message {message_id}")
                return {
                    "status": "success",
                    "message_id": message_id,
                    "response": response_text
                }
            else:
                return {"status": "error", "message": "Failed to send response"}
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _generate_response(self, message: CustomerMessage) -> str:
        """Generate AI-powered response to customer message."""
        if not self.huggingface_token and not self.openai_key:
            return self._get_mock_response(message)
        
        try:
            # Get order context if available
            order_context = ""
            if message.order_id:
                order_context = await self._get_order_context(message.order_id)
            
            system_prompt = "You are a professional customer service agent for an e-commerce store. Always be helpful, polite, and solution-oriented."
            
            prompt = f"""You are a helpful customer service representative for an e-commerce dropshipping store.

Customer Message:
Subject: {message.subject}
Message: {message.message}

Order Context: {order_context if order_context else "No order reference"}

Requirements:
- Be friendly, professional, and empathetic
- Address the customer's concern directly
- If it's about shipping, provide tracking info if available
- If it's about a product issue, offer solutions (refund, replacement, etc.)
- Keep response concise (2-3 sentences) but helpful
- Always end with asking if there's anything else you can help with

Generate an appropriate response:"""
            
            # Use Hugging Face or OpenAI
            if self.use_huggingface:
                response_text = await self._call_huggingface(prompt, system_prompt, max_tokens=200)
            else:
                response_text = await self._call_openai(prompt, system_prompt, max_tokens=200)
            
            if response_text:
                return response_text.strip()
            else:
                return self._get_mock_response(message)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_mock_response(message)
    
    async def _call_huggingface(self, prompt: str, system_prompt: str = "", max_tokens: int = 200) -> str:
        """Call Hugging Face Inference API."""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.huggingface_token}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "inputs": full_prompt,
                    "parameters": {
                        "max_new_tokens": max_tokens,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "return_full_text": False
                    }
                }
                
                api_url = f"https://api-inference.huggingface.co/models/{self.huggingface_model}"
                response = await client.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    if "generated_text" in data[0]:
                        return data[0]["generated_text"].strip()
                    elif "text" in data[0]:
                        return data[0]["text"].strip()
                
                if isinstance(data, dict) and "generated_text" in data:
                    return data["generated_text"].strip()
                
                return str(data).strip()
                
        except Exception as e:
            logger.error(f"Error calling Hugging Face API: {e}")
            return ""
    
    async def _call_openai(self, prompt: str, system_prompt: str = "", max_tokens: int = 200) -> str:
        """Call OpenAI API (fallback)."""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.openai_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return ""
    
    async def _get_order_context(self, order_id: str) -> str:
        """Get order context for customer service response."""
        if not self.session:
            return ""
        
        try:
            order = shopify.Order.find(order_id)
            return f"Order #{order.order_number} - Total: ${order.total_price} - Status: {order.fulfillment_status}"
        except:
            return ""
    
    async def _get_message(self, message_id: str) -> Optional[CustomerMessage]:
        """Get message by ID."""
        # Would fetch from database/API in production
        messages = await self.get_messages()
        for msg in messages:
            if msg.id == message_id:
                return msg
        return None
    
    async def _send_response(
        self,
        message: CustomerMessage,
        response_text: str
    ) -> bool:
        """Send response to customer."""
        try:
            # In production, send via:
            # - Shopify Chat API
            # - Email API
            # - Third-party chat platform API
            
            logger.info(f"Sending response to {message.customer_email}")
            
            # Mock sending
            # In production, actually send the message
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending response: {e}")
            return False
    
    def _get_mock_response(self, message: CustomerMessage) -> str:
        """Get mock response when AI is not available."""
        if "shipping" in message.message.lower() or "tracking" in message.message.lower():
            return "Thank you for contacting us! Your order is being processed and you'll receive a tracking number via email once it ships. Please allow 7-15 business days for delivery. Is there anything else I can help you with?"
        elif "refund" in message.message.lower() or "return" in message.message.lower():
            return "I understand you'd like to return your item. We offer a 30-day money-back guarantee. Please reply with your order number and I'll process your return request. Is there anything else I can assist you with?"
        else:
            return "Thank you for reaching out! I'd be happy to help you with that. Could you provide a bit more information so I can assist you better? Is there anything else I can help with?"
    
    def _get_mock_messages(self) -> List[CustomerMessage]:
        """Get mock messages for testing."""
        return [
            CustomerMessage(
                id="msg-001",
                customer_name="Jane Smith",
                customer_email="jane@example.com",
                subject="Order Shipping Question",
                message="Hi, when will my order ship? I placed it 3 days ago.",
                order_id="order-001",
                answered=False,
                created_at=datetime.utcnow()
            ),
            CustomerMessage(
                id="msg-002",
                customer_name="Bob Johnson",
                customer_email="bob@example.com",
                subject="Product Issue",
                message="The product I received is different from what was advertised. Can I get a refund?",
                order_id="order-002",
                answered=False,
                created_at=datetime.utcnow()
            )
        ]

