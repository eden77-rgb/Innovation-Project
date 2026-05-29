using System;

namespace innove.Models
{
    public class ChatMessage
    {
        public string Role { get; set; }       // "user" or "assistant"
        public string Content { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
