using System;

namespace innove.Models
{
    public class ChatMessage
    {
        public required string Role { get; set; }       // "user" or "assistant"
        public required string Content { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
