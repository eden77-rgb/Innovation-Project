using System;
using System.Windows;
using System.Windows.Controls;

namespace client.views
{
    public class PromptSelectedArgs : EventArgs
    {
        public string PromptType { get; }
        public string? CustomInstruction { get; }

        public PromptSelectedArgs(string promptType, string? customInstruction = null)
        {
            PromptType = promptType;
            CustomInstruction = customInstruction;
        }
    }

    public partial class HomeView : UserControl
    {
        public event EventHandler<PromptSelectedArgs>? PromptSelected;

        public HomeView()
        {
            InitializeComponent();
        }

        private void TranslateButton_Click(object sender, RoutedEventArgs e) =>
            PromptSelected?.Invoke(this, new PromptSelectedArgs("translate"));

        private void SummaryButton_Click(object sender, RoutedEventArgs e) =>
            PromptSelected?.Invoke(this, new PromptSelectedArgs("summary"));

        private void RewriteButton_Click(object sender, RoutedEventArgs e) =>
            PromptSelected?.Invoke(this, new PromptSelectedArgs("rewrite"));

        private void AnswerButton_Click(object sender, RoutedEventArgs e) =>
            PromptSelected?.Invoke(this, new PromptSelectedArgs("response"));

        private void CustomSendButton_Click(object sender, RoutedEventArgs e)
        {
            string custom = CustomPromptTextBox.Text.Trim();
            if (string.IsNullOrEmpty(custom))
            {
                MessageBox.Show("Veuillez entrer un prompt personnalisé.", "G.E.R.A.R.D");
                return;
            }
            PromptSelected?.Invoke(this, new PromptSelectedArgs("custom", custom));
        }
    }
}
