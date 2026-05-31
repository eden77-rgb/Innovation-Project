using client.models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace client.services
{
    public static class HistoryService
    {
        private static readonly string HistoryPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "G.E.R.A.R.D", "history.json");

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
                if (HistoryPath != null) 
                {
                    string? directoryPath = Path.GetDirectoryName(HistoryPath);
                    
                    if (directoryPath != null)
                    {
                        Directory.CreateDirectory(directoryPath);
                    }

                    string json = JsonSerializer.Serialize(conversations);
                    File.WriteAllText(HistoryPath, json);
                }
            }
        }
    }
}
