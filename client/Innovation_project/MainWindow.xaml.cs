using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Web.Script.Serialization;

namespace innove
{
    public partial class MainWindow : Window
    {
        private static readonly HttpClient _httpClient = new HttpClient();
        private const string ApiBaseUrl = "http://localhost:8000/api";
        private readonly JavaScriptSerializer _serializer = new JavaScriptSerializer();

        public MainWindow()
        {
            InitializeComponent();
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            string inputText = InputTextBox.Text.Trim();

            if (string.IsNullOrEmpty(inputText))
            {
                ResponseTextBox.Text = "Veuillez entrer un texte.";
                return;
            }

            if (PromptTypeComboBox.SelectedItem == null)
            {
                ResponseTextBox.Text = "Veuillez sélectionner un type de prompt.";
                return;
            }
            string promptType = ((ComboBoxItem)PromptTypeComboBox.SelectedItem).Content.ToString();

            SendButton.IsEnabled = false;
            SendButton.Content = "Chargement...";
            ResponseTextBox.Text = "";

            try
            {
                var requestBody = new Dictionary<string, string>
                {
                    { "prompt_type", promptType },
                    { "content", inputText }
                };

                string json = _serializer.Serialize(requestBody);
                var httpContent = new StringContent(json, Encoding.UTF8, "application/json");

                HttpResponseMessage response = await _httpClient.PostAsync(ApiBaseUrl + "/generate", httpContent);

                if (!response.IsSuccessStatusCode)
                {
                    ResponseTextBox.Text = "Erreur serveur : " + (int)response.StatusCode;
                    return;
                }

                string responseBody = await response.Content.ReadAsStringAsync();
                var result = _serializer.Deserialize<Dictionary<string, string>>(responseBody);
                if (result.ContainsKey("data"))
                    ResponseTextBox.Text = result["data"];
                else
                    ResponseTextBox.Text = "Réponse inattendue du serveur.";
            }
            catch (HttpRequestException)
            {
                ResponseTextBox.Text = "Impossible de contacter le serveur.";
            }
            catch (Exception ex)
            {
                ResponseTextBox.Text = "Erreur inattendue : " + ex.Message;
            }
            finally
            {
                SendButton.IsEnabled = true;
                SendButton.Content = "Envoyer";
            }
        }
    }
}
