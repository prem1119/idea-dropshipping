"""AI content generation service for product descriptions, ads, etc."""
import logging
from typing import List
import httpx

from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AIContentGenerator:
    """Service for generating AI-powered content."""
    
    def __init__(self):
        self.huggingface_token = settings.huggingface_api_token
        self.huggingface_model = settings.huggingface_model
        self.openai_key = settings.openai_api_key
        self.use_huggingface = bool(self.huggingface_token)
        
        if not self.huggingface_token and not self.openai_key:
            logger.warning("No AI API key configured (Hugging Face or OpenAI), using mock responses")
        
        if self.use_huggingface:
            logger.info(f"Using Hugging Face model: {self.huggingface_model}")
    
    async def _call_ai_api(self, prompt: str, system_prompt: str = "", max_tokens: int = 500) -> str:
        """Call AI API (Hugging Face or OpenAI)."""
        if self.use_huggingface:
            return await self._call_huggingface(prompt, system_prompt, max_tokens)
        elif self.openai_key:
            return await self._call_openai(prompt, system_prompt, max_tokens)
        else:
            return ""
    
    async def _call_huggingface(self, prompt: str, system_prompt: str = "", max_tokens: int = 500) -> str:
        """Call Hugging Face Inference API."""
        try:
            # Format prompt with system message
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
                
                # Use Hugging Face Inference API
                api_url = f"https://api-inference.huggingface.co/models/{self.huggingface_model}"
                
                response = await client.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Handle different response formats
                if isinstance(data, list) and len(data) > 0:
                    if "generated_text" in data[0]:
                        return data[0]["generated_text"].strip()
                    elif "text" in data[0]:
                        return data[0]["text"].strip()
                
                # Fallback: try direct text response
                if isinstance(data, dict) and "generated_text" in data:
                    return data["generated_text"].strip()
                
                return str(data).strip()
                
        except Exception as e:
            logger.error(f"Error calling Hugging Face API: {e}")
            return ""
    
    async def _call_openai(self, prompt: str, system_prompt: str = "", max_tokens: int = 500) -> str:
        """Call OpenAI API (fallback)."""
        try:
            import openai
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
    
    async def generate_product_description(
        self,
        product_title: str,
        base_description: str,
        category: str
    ) -> str:
        """Generate enhanced product description using AI."""
        if not self.huggingface_token and not self.openai_key:
            return self._mock_product_description(product_title, base_description)
        
        try:
            system_prompt = "You are an expert e-commerce copywriter who writes compelling product descriptions that drive sales."
            
            prompt = f"""Create a compelling, sales-focused product description for an e-commerce store.

Product Title: {product_title}
Category: {category}
Base Information: {base_description}

Requirements:
- Write in a persuasive, benefit-focused tone
- Include key features and benefits
- Use bullet points for easy scanning
- Include a call-to-action
- Optimize for SEO without keyword stuffing
- Length: 200-300 words

Format the response as HTML with proper tags."""
            
            description = await self._call_ai_api(prompt, system_prompt, max_tokens=500)
            
            if description:
                logger.info(f"Generated product description for: {product_title}")
                return description
            else:
                return self._mock_product_description(product_title, base_description)
            
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            return self._mock_product_description(product_title, base_description)
    
    async def generate_seo_title(self, product_title: str) -> str:
        """Generate SEO-optimized product title."""
        if not self.huggingface_token and not self.openai_key:
            return product_title
        
        try:
            system_prompt = "You are an SEO expert specializing in e-commerce product titles."
            
            prompt = f"""Optimize this product title for SEO and conversions while keeping it natural:

Original: {product_title}

Requirements:
- Include relevant keywords
- Keep it under 60 characters
- Make it compelling
- Maintain readability

Return only the optimized title, nothing else."""
            
            result = await self._call_ai_api(prompt, system_prompt, max_tokens=50)
            
            if result:
                # Clean up the response (remove quotes, extra text)
                result = result.strip().strip('"').strip("'")
                # Take first line if multiple lines
                result = result.split('\n')[0].strip()
                return result if result else product_title
            else:
                return product_title
            
        except Exception as e:
            logger.error(f"Error generating SEO title: {e}")
            return product_title
    
    async def generate_product_tags(self, product_title: str, category: str) -> List[str]:
        """Generate relevant product tags."""
        if not self.huggingface_token and not self.openai_key:
            return [category.lower(), product_title.split()[0].lower()]
        
        try:
            prompt = f"""Generate 5-8 relevant tags for this product:

Title: {product_title}
Category: {category}

Return only a comma-separated list of tags, no explanations."""
            
            result = await self._call_ai_api(prompt, max_tokens=50)
            
            if result:
                # Extract tags from response
                tags = [tag.strip() for tag in result.split(",")]
                # Clean up tags (remove extra text, quotes)
                tags = [tag.strip('"').strip("'").strip() for tag in tags if tag.strip()]
                return tags[:8] if tags else [category.lower(), product_title.split()[0].lower()]
            else:
                return [category.lower(), product_title.split()[0].lower()]
            
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            return [category.lower(), product_title.split()[0].lower()]
    
    async def generate_ad_caption(
        self,
        product_title: str,
        product_description: str,
        platform: str = "tiktok"
    ) -> str:
        """Generate ad caption for TikTok/Facebook ads."""
        if not self.huggingface_token and not self.openai_key:
            return self._mock_ad_caption(product_title, platform)
        
        try:
            tone = "casual, trendy, Gen-Z friendly" if platform == "tiktok" else "engaging, professional"
            
            system_prompt = f"You are a social media marketing expert specializing in {platform} ads."
            
            prompt = f"""Create a compelling ad caption for {platform}:

Product: {product_title}
Description: {product_description}

Requirements:
- Tone: {tone}
- Include relevant hashtags (5-8 for TikTok, 3-5 for Facebook)
- Create urgency or FOMO
- Include a clear call-to-action
- Length: 150-200 characters for TikTok, 200-300 for Facebook

Return only the caption, nothing else."""
            
            result = await self._call_ai_api(prompt, system_prompt, max_tokens=200)
            
            if result:
                return result.strip()
            else:
                return self._mock_ad_caption(product_title, platform)
            
        except Exception as e:
            logger.error(f"Error generating ad caption: {e}")
            return self._mock_ad_caption(product_title, platform)
    
    async def generate_video_script(
        self,
        product_title: str,
        product_description: str,
        duration_seconds: int = 15
    ) -> str:
        """Generate video script for product ad."""
        if not self.huggingface_token and not self.openai_key:
            return self._mock_video_script(product_title)
        
        try:
            system_prompt = "You are a video script writer specializing in short-form social media ads."
            
            prompt = f"""Create a short, engaging video script for a product ad:

Product: {product_title}
Description: {product_description}
Duration: {duration_seconds} seconds

Format:
- Hook (0-3s): Attention-grabbing opening
- Problem (3-6s): Show the pain point
- Solution (6-12s): Present the product benefits
- CTA (12-15s): Call to action

Return a structured script with timestamps."""
            
            result = await self._call_ai_api(prompt, system_prompt, max_tokens=300)
            
            if result:
                return result.strip()
            else:
                return self._mock_video_script(product_title)
            
        except Exception as e:
            logger.error(f"Error generating video script: {e}")
            return self._mock_video_script(product_title)
    
    def _mock_product_description(self, title: str, base: str) -> str:
        """Mock product description."""
        return f"""<h2>{title}</h2>
        <p>{base}</p>
        <ul>
            <li>High quality materials</li>
            <li>Fast shipping</li>
            <li>30-day money-back guarantee</li>
        </ul>
        <p><strong>Order now and transform your daily routine!</strong></p>"""
    
    def _mock_ad_caption(self, title: str, platform: str) -> str:
        """Mock ad caption."""
        if platform == "tiktok":
            return f"🔥 This {title} is EVERYTHING! 😱 #viral #fyp #trending #musthave"
        return f"Discover the {title}. Perfect for your needs. Shop now!"
    
    def _mock_video_script(self, title: str) -> str:
        """Mock video script."""
        return f"""0-3s: [Hook] "You won't believe this!"
3-6s: [Problem] Show frustration with current solution
6-12s: [Solution] Demonstrate {title}
12-15s: [CTA] "Link in bio! 🔗" """

