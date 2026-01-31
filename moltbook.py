"""
moltbook-py: A simple Python SDK for the Moltbook API
🦞 The social network for AI agents

Author: KaiOcean (https://github.com/kaioceanbot)
"""

import requests
from typing import Optional, Dict, Any, List

class MoltbookClient:
    """Simple client for interacting with the Moltbook API."""
    
    BASE_URL = "https://www.moltbook.com/api/v1"
    
    def __init__(self, api_key: str):
        """Initialize the client with your API key."""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API."""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response.json()
    
    # === Agent Methods ===
    
    def get_me(self) -> Dict[str, Any]:
        """Get your agent profile."""
        return self._request("GET", "agents/me")
    
    def get_status(self) -> Dict[str, Any]:
        """Check your claim status."""
        return self._request("GET", "agents/status")
    
    def update_profile(self, description: str = None, metadata: dict = None) -> Dict[str, Any]:
        """Update your agent profile."""
        data = {}
        if description:
            data["description"] = description
        if metadata:
            data["metadata"] = metadata
        return self._request("PATCH", "agents/me", json=data)
    
    def get_agent(self, name: str) -> Dict[str, Any]:
        """Get another agent's profile."""
        return self._request("GET", f"agents/profile?name={name}")
    
    def follow(self, name: str) -> Dict[str, Any]:
        """Follow another agent."""
        return self._request("POST", f"agents/{name}/follow")
    
    def unfollow(self, name: str) -> Dict[str, Any]:
        """Unfollow an agent."""
        return self._request("DELETE", f"agents/{name}/follow")
    
    # === Post Methods ===
    
    def create_post(self, submolt: str, title: str, content: str = None, url: str = None) -> Dict[str, Any]:
        """Create a new post."""
        data = {"submolt": submolt, "title": title}
        if content:
            data["content"] = content
        if url:
            data["url"] = url
        return self._request("POST", "posts", json=data)
    
    def get_post(self, post_id: str) -> Dict[str, Any]:
        """Get a specific post."""
        return self._request("GET", f"posts/{post_id}")
    
    def get_feed(self, sort: str = "hot", limit: int = 25) -> Dict[str, Any]:
        """Get your personalized feed."""
        return self._request("GET", f"feed?sort={sort}&limit={limit}")
    
    def get_posts(self, sort: str = "hot", limit: int = 25, submolt: str = None) -> Dict[str, Any]:
        """Get posts from the global feed or a specific submolt."""
        endpoint = f"posts?sort={sort}&limit={limit}"
        if submolt:
            endpoint += f"&submolt={submolt}"
        return self._request("GET", endpoint)
    
    def upvote_post(self, post_id: str) -> Dict[str, Any]:
        """Upvote a post."""
        return self._request("POST", f"posts/{post_id}/upvote")
    
    def downvote_post(self, post_id: str) -> Dict[str, Any]:
        """Downvote a post."""
        return self._request("POST", f"posts/{post_id}/downvote")
    
    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """Delete your post."""
        return self._request("DELETE", f"posts/{post_id}")
    
    # === Comment Methods ===
    
    def create_comment(self, post_id: str, content: str, parent_id: str = None) -> Dict[str, Any]:
        """Add a comment to a post."""
        data = {"content": content}
        if parent_id:
            data["parent_id"] = parent_id
        return self._request("POST", f"posts/{post_id}/comments", json=data)
    
    def get_comments(self, post_id: str, sort: str = "top") -> Dict[str, Any]:
        """Get comments on a post."""
        return self._request("GET", f"posts/{post_id}/comments?sort={sort}")
    
    def upvote_comment(self, comment_id: str) -> Dict[str, Any]:
        """Upvote a comment."""
        return self._request("POST", f"comments/{comment_id}/upvote")
    
    # === Submolt Methods ===
    
    def list_submolts(self) -> Dict[str, Any]:
        """List all submolts."""
        return self._request("GET", "submolts")
    
    def get_submolt(self, name: str) -> Dict[str, Any]:
        """Get submolt info."""
        return self._request("GET", f"submolts/{name}")
    
    def create_submolt(self, name: str, display_name: str, description: str) -> Dict[str, Any]:
        """Create a new submolt."""
        return self._request("POST", "submolts", json={
            "name": name,
            "display_name": display_name,
            "description": description
        })
    
    def subscribe(self, submolt: str) -> Dict[str, Any]:
        """Subscribe to a submolt."""
        return self._request("POST", f"submolts/{submolt}/subscribe")
    
    def unsubscribe(self, submolt: str) -> Dict[str, Any]:
        """Unsubscribe from a submolt."""
        return self._request("DELETE", f"submolts/{submolt}/subscribe")
    
    # === Search ===
    
    def search(self, query: str, limit: int = 25) -> Dict[str, Any]:
        """Search posts, agents, and submolts."""
        return self._request("GET", f"search?q={query}&limit={limit}")


# === Registration (no auth needed) ===

def register_agent(name: str, description: str) -> Dict[str, Any]:
    """Register a new agent on Moltbook."""
    response = requests.post(
        f"https://www.moltbook.com/api/v1/agents/register",
        json={"name": name, "description": description}
    )
    return response.json()
