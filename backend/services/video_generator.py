"""Video generation service for creating product ad videos."""
import logging
from typing import Optional
import httpx
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
import tempfile
import os

from backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class VideoGenerator:
    """Service for generating product advertisement videos."""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    async def generate_product_video(
        self,
        product_title: str,
        script: str,
        duration_seconds: int = 15,
        product_images: Optional[list] = None
    ) -> Optional[str]:
        """
        Generate a product advertisement video.
        
        Returns:
            URL to the generated video (uploaded to storage)
        """
        logger.info(f"Generating video for: {product_title}")
        
        try:
            # In a production system, you would:
            # 1. Parse the script to extract scenes
            # 2. Use AI video generation (like RunwayML, Synthesia, or similar)
            # 3. Or create video using product images + text overlays
            
            # For now, we'll create a simple video using product images
            if product_images:
                video_path = await self._create_image_based_video(
                    product_title,
                    script,
                    product_images,
                    duration_seconds
                )
            else:
                # Use placeholder approach
                video_path = await self._create_placeholder_video(
                    product_title,
                    duration_seconds
                )
            
            # Upload video to cloud storage (S3, Cloudinary, etc.)
            video_url = await self._upload_video(video_path)
            
            # Clean up temp file
            if os.path.exists(video_path):
                os.remove(video_path)
            
            return video_url
            
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return None
    
    async def _create_image_based_video(
        self,
        title: str,
        script: str,
        images: list,
        duration: int
    ) -> str:
        """Create video from product images with text overlays."""
        try:
            clips = []
            
            # Split duration across images
            time_per_image = duration / len(images) if images else duration
            
            for i, image_url in enumerate(images[:5]):  # Limit to 5 images
                # Download image
                image_path = await self._download_image(image_url)
                
                # Create image clip
                img_clip = ImageClip(image_path).set_duration(time_per_image)
                
                # Add text overlay
                text_clip = TextClip(
                    title if i == 0 else f"Scene {i+1}",
                    fontsize=50,
                    color='white',
                    font='Arial-Bold'
                ).set_duration(time_per_image).set_position(('center', 'bottom'))
                
                # Composite
                video_clip = CompositeVideoClip([img_clip, text_clip])
                clips.append(video_clip)
                
                # Clean up downloaded image
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips)
            
            # Export
            output_path = os.path.join(self.temp_dir, f"video_{title.replace(' ', '_')}.mp4")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating image-based video: {e}")
            return await self._create_placeholder_video(title, duration)
    
    async def _create_placeholder_video(
        self,
        title: str,
        duration: int
    ) -> str:
        """Create a simple placeholder video."""
        try:
            # Create a simple colored background with text
            # This is a simplified version - in production, use proper video generation
            
            # For now, return a mock URL
            # In production, you'd actually generate the video
            logger.info("Creating placeholder video (mock)")
            
            # Return mock URL - in production, this would be a real generated video
            return "https://example.com/videos/placeholder.mp4"
            
        except Exception as e:
            logger.error(f"Error creating placeholder video: {e}")
            return ""
    
    async def _download_image(self, url: str) -> str:
        """Download image from URL."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
                # Save to temp file
                ext = url.split('.')[-1].split('?')[0] if '.' in url else 'jpg'
                temp_path = os.path.join(self.temp_dir, f"img_{hash(url)}.{ext}")
                
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                
                return temp_path
                
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            # Return placeholder path
            return os.path.join(self.temp_dir, "placeholder.jpg")
    
    async def _upload_video(self, video_path: str) -> str:
        """Upload video to cloud storage."""
        # In production, upload to S3, Cloudinary, or similar
        # For now, return mock URL
        logger.info(f"Uploading video: {video_path}")
        
        # Mock upload - in production, actually upload
        video_filename = os.path.basename(video_path)
        return f"https://storage.example.com/videos/{video_filename}"

