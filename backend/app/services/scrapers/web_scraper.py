"""
Basic web scraping service using Crawl4AI
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import aiohttp
from crawl4ai import AsyncWebCrawler

from config.settings import settings

logger = logging.getLogger(__name__)


class WebScrapingService:
    """Web scraping service for monitoring sources"""
    
    def __init__(self):
        self.crawler = None
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def initialize(self):
        """Initialize the crawler"""
        try:
            self.crawler = AsyncWebCrawler(verbose=settings.DEBUG)
            await self.crawler.astart()
            logger.info("Web crawler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize web crawler: {e}")
            raise
            
    async def cleanup(self):
        """Cleanup resources"""
        if self.crawler:
            await self.crawler.aclose()
            
    async def scrape_url(self, url: str, **kwargs) -> Dict[str, Any]:
        """Scrape a single URL"""
        try:
            if not self.crawler:
                await self.initialize()
                
            result = await self.crawler.arun(url=url, **kwargs)
            
            return {
                "url": url,
                "title": result.metadata.get("title", ""),
                "content": result.markdown[:5000] if result.markdown else "",  # Limit content
                "raw_html": result.html[:10000] if result.html else "",  # Limit HTML
                "links": result.links[:50] if result.links else [],  # Limit links
                "media": result.media[:20] if result.media else [],  # Limit media
                "metadata": result.metadata,
                "scraped_at": datetime.utcnow().isoformat(),
                "success": result.success,
                "error": result.error_message if not result.success else None
            }
        except Exception as e:
            logger.error(f"Failed to scrape URL {url}: {e}")
            return {
                "url": url,
                "title": "",
                "content": "",
                "raw_html": "",
                "links": [],
                "media": [],
                "metadata": {},
                "scraped_at": datetime.utcnow().isoformat(),
                "success": False,
                "error": str(e)
            }
            
    async def scrape_multiple_urls(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Scrape multiple URLs concurrently"""
        if not self.crawler:
            await self.initialize()
            
        tasks = [self.scrape_url(url, **kwargs) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Exception scraping URL {urls[i]}: {result}")
                processed_results.append({
                    "url": urls[i],
                    "success": False,
                    "error": str(result),
                    "scraped_at": datetime.utcnow().isoformat()
                })
            else:
                processed_results.append(result)
                
        return processed_results
        
    async def monitor_source(self, source_config: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor a specific source for changes"""
        url = source_config.get("url")
        keywords = source_config.get("keywords", [])
        
        try:
            result = await self.scrape_url(url)
            
            if not result["success"]:
                return {
                    "source_url": url,
                    "status": "error",
                    "error": result["error"],
                    "matches": [],
                    "checked_at": datetime.utcnow().isoformat()
                }
            
            # Check for keyword matches
            content = result["content"].lower()
            matches = []
            
            for keyword in keywords:
                if keyword.lower() in content:
                    matches.append({
                        "keyword": keyword,
                        "context": self._extract_context(content, keyword.lower())
                    })
            
            return {
                "source_url": url,
                "status": "success",
                "title": result["title"],
                "matches": matches,
                "total_matches": len(matches),
                "content_length": len(result["content"]),
                "checked_at": datetime.utcnow().isoformat(),
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            logger.error(f"Failed to monitor source {url}: {e}")
            return {
                "source_url": url,
                "status": "error",
                "error": str(e),
                "matches": [],
                "checked_at": datetime.utcnow().isoformat()
            }
    
    def _extract_context(self, content: str, keyword: str, context_length: int = 200) -> str:
        """Extract context around a keyword match"""
        try:
            index = content.find(keyword)
            if index == -1:
                return ""
            
            start = max(0, index - context_length // 2)
            end = min(len(content), index + len(keyword) + context_length // 2)
            
            context = content[start:end]
            if start > 0:
                context = "..." + context
            if end < len(content):
                context = context + "..."
                
            return context
        except Exception:
            return ""


# Global instance
scraping_service = WebScrapingService()