using innove.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace innove.services
{
    public static class HistoryService
    {
        private static readonly string HistoryPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "Innove", "history.json");

        public static List<Conversation> Load()
        {
            try
            {
                if (!File.Exists(HistoryPath))
                    return new List<Conversation>();
                string json = File.ReadAllText(HistoryPath);
                return JsonSerializer.Deserialize<List<Conversation>>(json) ?? new List<Conversation>();
            }
            catch
            {
                return new List<Conversation>();
            }
        }

        public static void Save(List<Conversation> conversations)
        {
            try
            {
                if (HistoryPath != null) {
                    Directory.CreateDirectory(HistoryPath);
                    File.WriteAllText(HistoryPath, JsonSerializer.Serialize(conversations));
                }
            }
            catch { }
        }
    }
}
