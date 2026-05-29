using innove.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Web.Script.Serialization;

namespace innove.Services
{
    public static class HistoryService
    {
        private static readonly string HistoryPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "Innove", "history.json");

        private static readonly JavaScriptSerializer Serializer = new JavaScriptSerializer();

        public static List<Conversation> Load()
        {
            try
            {
                if (!File.Exists(HistoryPath))
                    return new List<Conversation>();
                string json = File.ReadAllText(HistoryPath);
                return Serializer.Deserialize<List<Conversation>>(json) ?? new List<Conversation>();
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
                Directory.CreateDirectory(Path.GetDirectoryName(HistoryPath));
                File.WriteAllText(HistoryPath, Serializer.Serialize(conversations));
            }
            catch { }
        }
    }
}
