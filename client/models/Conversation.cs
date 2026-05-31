using System;
using System.Collections.Generic;

namespace innove.Models
{
    public class Conversation
    {
        public required string Id { get; set; }
        public required string PromptType { get; set; }
        public required string CustomInstruction { get; set; }
        public DateTime CreatedAt { get; set; }
        public List<ChatMessage> Messages { get; set; } = new List<ChatMessage>();
    }
}
