using client.views;
using System;
using System.Runtime.InteropServices;
using System.Windows;

namespace client
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            ShowHome();
        }

        private void ShowHome()
        {
            var home = new HomeView();
            home.PromptSelected += OnPromptSelected;
            MainContent.Content = home;
        }

        private void OnPromptSelected(object? sender, PromptSelectedArgs e)
        {
            var chat = new ChatView(e.PromptType, e.CustomInstruction);
            chat.BackRequested += (s, _) => ShowHome();
            MainContent.Content = chat;
        }
    }
}
