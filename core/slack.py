"""
Slack integration for human-in-the-loop communication.
Allows agents to ask questions and receive answers from users via Slack.
"""
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Callable
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class SlackMessage:
    """Represents a Slack message."""
    channel: str
    text: str
    thread_ts: Optional[str] = None
    user: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class Question:
    """Represents a question waiting for user response."""
    id: str
    text: str
    context: str
    channel: str
    thread_ts: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    answered: bool = False
    answer: Optional[str] = None


class SlackClientInterface(ABC):
    """Abstract interface for Slack operations."""
    
    @abstractmethod
    def send_message(self, channel: str, text: str, thread_ts: str = None) -> Optional[str]:
        """Send a message and return the timestamp."""
        pass
    
    @abstractmethod
    def get_replies(self, channel: str, thread_ts: str, since_ts: str = None) -> list:
        """Get replies in a thread since a given timestamp."""
        pass


class SlackClient(SlackClientInterface):
    """Real Slack client using slack_sdk."""
    
    def __init__(self, token: str):
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        
        self._client = WebClient(token=token)
        self._api_error = SlackApiError
        
    def send_message(self, channel: str, text: str, thread_ts: str = None) -> Optional[str]:
        """Send a message to Slack channel."""
        try:
            response = self._client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts,
            )
            return response.get("ts")
        except self._api_error as e:
            logger.error(f"Failed to send Slack message: {e}")
            return None
    
    def get_replies(self, channel: str, thread_ts: str, since_ts: str = None) -> list:
        """Get replies in a thread."""
        try:
            response = self._client.conversations_replies(
                channel=channel,
                ts=thread_ts,
            )
            messages = response.get("messages", [])
            
            # Filter to only get replies after since_ts (excluding the original message)
            if since_ts:
                messages = [
                    m for m in messages 
                    if m.get("ts") != thread_ts and float(m.get("ts", 0)) > float(since_ts)
                ]
            else:
                messages = [m for m in messages if m.get("ts") != thread_ts]
            
            return messages
        except self._api_error as e:
            logger.error(f"Failed to get Slack replies: {e}")
            return []


class ConsoleSlackClient(SlackClientInterface):
    """Console-based client for testing without Slack."""
    
    def send_message(self, channel: str, text: str, thread_ts: str = None) -> Optional[str]:
        """Print message to console and return fake timestamp."""
        print(f"\n{'='*60}")
        print(f"🤖 AGENT QUESTION")
        print(f"{'='*60}")
        print(f"{text}")
        print(f"{'='*60}\n")
        return str(time.time())
    
    def get_replies(self, channel: str, thread_ts: str, since_ts: str = None) -> list:
        """Get response from console input."""
        response = input("📝 Your answer: ").strip()
        if response:
            return [{"text": response, "ts": str(time.time())}]
        return []


class QuestionTracker:
    """Tracks pending questions and their responses."""
    
    def __init__(self):
        self._questions: dict[str, Question] = {}
    
    def create_question(self, text: str, context: str, channel: str) -> Question:
        """Create and track a new question."""
        question = Question(
            id=str(uuid.uuid4())[:8],
            text=text,
            context=context,
            channel=channel,
        )
        self._questions[question.id] = question
        return question
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """Get a question by ID."""
        return self._questions.get(question_id)
    
    def mark_answered(self, question_id: str, answer: str) -> None:
        """Mark a question as answered."""
        if question_id in self._questions:
            self._questions[question_id].answered = True
            self._questions[question_id].answer = answer
    
    def get_pending_questions(self) -> list[Question]:
        """Get all unanswered questions."""
        return [q for q in self._questions.values() if not q.answered]


class HumanInteractionService:
    """
    Service for managing human-agent interactions via Slack.
    Implements the human-in-the-loop pattern.
    """
    
    def __init__(
        self, 
        client: SlackClientInterface,
        channel: str,
        poll_interval: int = 5,
        timeout: int = 300,
    ):
        self._client = client
        self._channel = channel
        self._poll_interval = poll_interval
        self._timeout = timeout
        self._tracker = QuestionTracker()
        self._current_thread_ts: Optional[str] = None
    
    def start_session(self, card_title: str) -> str:
        """Start a new interaction session for a backlog card."""
        message = (
            f"🚀 *New Development Session Started*\n\n"
            f"📋 *Card:* {card_title}\n\n"
            f"I'll ask questions here as needed during development. "
            f"Please reply in this thread."
        )
        self._current_thread_ts = self._client.send_message(self._channel, message)
        return self._current_thread_ts or ""
    
    def ask_question(self, question: str, context: str = "") -> str:
        """
        Ask a question and wait for the user's response.
        This method blocks until a response is received or timeout.
        """
        # Format the question message
        formatted_question = self._format_question(question, context)
        
        # Send to Slack
        message_ts = self._client.send_message(
            channel=self._channel,
            text=formatted_question,
            thread_ts=self._current_thread_ts,
        )
        
        if not message_ts:
            logger.warning("Failed to send question to Slack")
            return self._fallback_input(question)
        
        # Track the question
        q = self._tracker.create_question(question, context, self._channel)
        q.thread_ts = message_ts
        
        # Wait for response
        response = self._wait_for_response(message_ts)
        
        if response:
            self._tracker.mark_answered(q.id, response)
            return response
        
        return "No response received within timeout."
    
    def send_update(self, message: str) -> None:
        """Send a status update to the Slack thread."""
        self._client.send_message(
            channel=self._channel,
            text=f"📊 *Update:* {message}",
            thread_ts=self._current_thread_ts,
        )
    
    def send_completion(self, summary: str) -> None:
        """Send completion message to Slack."""
        message = (
            f"✅ *Development Complete*\n\n"
            f"{summary}"
        )
        self._client.send_message(
            channel=self._channel,
            text=message,
            thread_ts=self._current_thread_ts,
        )
    
    def _format_question(self, question: str, context: str) -> str:
        """Format a question for Slack."""
        parts = ["❓ *Question from Agent*\n"]
        
        if context:
            parts.append(f"_Context: {context}_\n")
        
        parts.append(f"\n{question}\n")
        parts.append("\n_Please reply to this message with your answer._")
        
        return "".join(parts)
    
    def _wait_for_response(self, question_ts: str) -> Optional[str]:
        """Poll for a response to the question."""
        start_time = time.time()
        last_check_ts = question_ts
        
        logger.info(f"Waiting for user response (timeout: {self._timeout}s)")
        
        while (time.time() - start_time) < self._timeout:
            time.sleep(self._poll_interval)
            
            replies = self._client.get_replies(
                channel=self._channel,
                thread_ts=self._current_thread_ts or question_ts,
                since_ts=last_check_ts,
            )
            
            if replies:
                # Get the first reply text
                response_text = replies[0].get("text", "")
                if response_text:
                    logger.info("Received user response")
                    return response_text
                last_check_ts = replies[-1].get("ts", last_check_ts)
        
        logger.warning("Timeout waiting for user response")
        return None
    
    def _fallback_input(self, question: str) -> str:
        """Fallback to console input if Slack fails."""
        print(f"\n[Slack unavailable] {question}")
        return input("Your answer: ").strip()


def create_slack_service(
    token: Optional[str],
    channel: str,
    use_console: bool = False,
    poll_interval: int = 5,
    timeout: int = 300,
) -> HumanInteractionService:
    """Factory function to create appropriate Slack service."""
    
    if use_console or not token:
        logger.info("Using console-based interaction (no Slack)")
        client = ConsoleSlackClient()
    else:
        logger.info(f"Using Slack channel: {channel}")
        client = SlackClient(token)
    
    return HumanInteractionService(
        client=client,
        channel=channel,
        poll_interval=poll_interval,
        timeout=timeout,
    )
