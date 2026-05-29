using System;
using System.Collections.Generic;

namespace innove.Models
{
    public class Conversation
    {
        public string Id { get; set; }
        public string PromptType { get; set; }
        public string CustomInstruction { get; set; }
        public DateTime CreatedAt { get; set; }
        public List<ChatMessage> Messages { get; set; } = new List<ChatMessage>();
    }
}
