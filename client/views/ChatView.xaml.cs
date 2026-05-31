using innove.Models;
using innove.services;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Text.Json;

namespace innove.Views
{
    public partial class ChatView : UserControl
    {
        public event EventHandler? BackRequested;

        private static readonly HttpClient _httpClient = new HttpClient { Timeout = System.Threading.Timeout.InfiniteTimeSpan };
        private const string ApiBaseUrl = "http://localhost:8000/api";

        private readonly string _promptType;
        private readonly string? _customInstruction;
        private readonly Conversation _conversation;
        private readonly List<Conversation> _allConversations;

        public ChatView(string promptType, string? customInstruction = null)
        {
            InitializeComponent();
            _promptType = promptType;
            _customInstruction = customInstruction;

            _allConversations = HistoryService.Load();
            _conversation = new Conversation
            {
                Id = Guid.NewGuid().ToString(),
                PromptType = promptType,
                CustomInstruction = customInstruction ?? string.Empty,
                CreatedAt = DateTime.Now,
                Messages = new List<ChatMessage>()
            };
            _allConversations.Add(_conversation);

            ModeLabel.Text = "Mode : " + GetModeLabel();

            LoadHistory();
            Loaded += (_, __) => HistoryScroll.ScrollToBottom();
        }

        private void LoadHistory()
        {
            foreach (var conv in _allConversations)
            {
                if (conv.Id == _conversation.Id) continue;
                if (conv.PromptType != _promptType) continue;
                if (conv.Messages == null || conv.Messages.Count == 0) continue;

                AppendSeparator(conv.CreatedAt.ToString("dd/MM/yyyy HH:mm"));
                foreach (var msg in conv.Messages)
                {
                    bool isUser = msg.Role == "user";
                    AppendMessage(isUser ? "Vous" : "IA", msg.Content, isUser ? "#003366" : "#006600");
                }
            }

            if (MessagesPanel.Children.Count > 0)
                AppendSeparator("— Nouvelle conversation —");
        }

        private void AppendSeparator(string label)
        {
            MessagesPanel.Children.Add(new TextBlock
            {
                Text = label,
                TextWrapping = TextWrapping.Wrap,
                Margin = new Thickness(0, 8, 0, 8),
                FontStyle = System.Windows.FontStyles.Italic,
                Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#888888"))
            });
        }

        private string GetModeLabel()
        {
            switch (_promptType)
            {
                case "translate": return "Traduire";
                case "summary":   return "Résumer";
                case "rewrite":   return "Réécrire";
                case "response":    return "Répondre";
                case "custom":    return "Personnalisé — " + _customInstruction;
                default:          return _promptType;
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            BackRequested?.Invoke(this, EventArgs.Empty);
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            string inputText = InputTextBox.Text.Trim();
            if (string.IsNullOrEmpty(inputText))
                return;

            InputTextBox.Text = "";
            SendButton.IsEnabled = false;
            BackButton.IsEnabled = false;
            StreamToggle.IsEnabled = false;
            LoadingPanel.Visibility = Visibility.Visible;

            AppendMessage("Vous", inputText, "#003366");
            _conversation.Messages.Add(new ChatMessage
            {
                Role = "user",
                Content = inputText,
                Timestamp = DateTime.Now
            });

            string content = _promptType == "custom"
                ? _customInstruction + "\n\n---\n\n" + inputText
                : inputText;

            string json = JsonSerializer.Serialize(new Dictionary<string, string>
            {
                { "prompt_type", _promptType },
                { "content", content }
            });

            try
            {
                string? reply = StreamToggle.IsChecked == true
                    ? await SendStreamRequest(json)
                    : await SendGenerateRequest(json);

                if (reply != null)
                    _conversation.Messages.Add(new ChatMessage
                    {
                        Role = "assistant",
                        Content = reply,
                        Timestamp = DateTime.Now
                    });
            }
            catch (HttpRequestException)
            {
                AppendMessage("Système", "Impossible de contacter le serveur.", "#CC0000");
            }
            catch (Exception ex)
            {
                AppendMessage("Système", "Erreur inattendue : " + ex.Message, "#CC0000");
            }
            finally
            {
                LoadingPanel.Visibility = Visibility.Collapsed;
                SendButton.IsEnabled = true;
                BackButton.IsEnabled = true;
                StreamToggle.IsEnabled = true;
                HistoryService.Save(_allConversations);
                HistoryScroll.ScrollToBottom();
            }
        }

        private async Task<string?> SendGenerateRequest(string json)
        {
            var httpContent = new StringContent(json, Encoding.UTF8, "application/json");
            using (HttpResponseMessage response = await _httpClient.PostAsync(ApiBaseUrl + "/generate", httpContent))
            {
                if (!response.IsSuccessStatusCode)
                {
                    AppendMessage("Système", "Erreur serveur : " + (int)response.StatusCode, "#CC0000");
                    return null;
                }

                string responseBody = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<Dictionary<string, string>>(responseBody);
                string reply = StripQuotes(result != null && result.ContainsKey("data") && result["data"] != null
                    ? result["data"]
                    : "Réponse inattendue du serveur.");

                AppendAiMessage(reply);
                return reply;
            }
        }

        private async Task<string?> SendStreamRequest(string json)
        {
            var request = new HttpRequestMessage(HttpMethod.Post, ApiBaseUrl + "/stream");
            request.Content = new StringContent(json, Encoding.UTF8, "application/json");

            using (HttpResponseMessage response = await _httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
            {
                if (!response.IsSuccessStatusCode)
                {
                    AppendMessage("Système", "Erreur serveur : " + (int)response.StatusCode, "#CC0000");
                    return null;
                }

                LoadingPanel.Visibility = Visibility.Collapsed;
                var iaBlock = AppendAiMessage();

                var sb = new StringBuilder();
                using (Stream stream = await response.Content.ReadAsStreamAsync())
                using (var reader = new StreamReader(stream, Encoding.UTF8))
                {
                    var buffer = new char[64];
                    int read;
                    while ((read = await reader.ReadAsync(buffer, 0, buffer.Length)) > 0)
                    {
                        sb.Append(buffer, 0, read);
                        iaBlock.Text = "IA : " + StripQuotes(sb.ToString());
                        HistoryScroll.ScrollToBottom();
                    }
                }

                string reply = StripQuotes(sb.ToString());
                iaBlock.Text = "IA : " + reply;
                return reply;
            }
        }

        private TextBlock AppendAiMessage(string? text = null)
        {
            const string prefix = "IA : ";

            var panel = new DockPanel { Margin = new Thickness(0, 4, 0, 4) };

            var copyButton = new Button
            {
                Content = "Copier",
                Width = 55,
                Height = 20,
                FontSize = 11,
                VerticalAlignment = VerticalAlignment.Top,
                Margin = new Thickness(6, 0, 0, 0)
            };
            DockPanel.SetDock(copyButton, Dock.Right);

            var textBlock = new TextBlock
            {
                Text = text != null ? prefix + text : prefix,
                TextWrapping = TextWrapping.Wrap,
                Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#006600"))
            };

            copyButton.Click += (s, e) =>
            {
                string toCopy = textBlock.Text.StartsWith(prefix)
                    ? textBlock.Text.Substring(prefix.Length)
                    : textBlock.Text;
                Clipboard.SetText(toCopy);
            };

            panel.Children.Add(copyButton);
            panel.Children.Add(textBlock);
            MessagesPanel.Children.Add(panel);
            return textBlock;
        }

        private static string StripQuotes(string text)
        {
            return text.TrimStart('"').TrimEnd('"').Trim();
        }

        private void AppendMessage(string sender, string text, string hexColor)
        {
            var block = new TextBlock
            {
                Text = sender + " : " + text,
                TextWrapping = TextWrapping.Wrap,
                Margin = new Thickness(0, 4, 0, 4),
                Foreground = new SolidColorBrush(
                    (Color)ColorConverter.ConvertFromString(hexColor))
            };
            MessagesPanel.Children.Add(block);
        }
    }
}
