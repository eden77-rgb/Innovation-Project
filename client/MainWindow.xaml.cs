using client.views;
using System;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;

namespace client
{
    public partial class MainWindow : Window
    {
        // --- Importation des fonctions natives de Windows (Win32) ---
        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        // https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-hotkey
        private const int HOTKEY_ID = 9000;         // Un ID du raccourci
        private const uint K_ALT = 0x0001;          // ALT
        private const uint K_CTRL = 0x0002;         // CTRL
        private const uint K_A = 0x41;              // A
        private const int WM_HOTKEY = 0x0312;

        private IntPtr _windowHandle;
        private HwndSource? _hwndSource;

        public MainWindow()
        {
            InitializeComponent();
            ShowHome();
            
            Loaded += MainWindow_Loaded;
            Closed += MainWindow_Closed;
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

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            _windowHandle = new WindowInteropHelper(this).Handle;

            _hwndSource = HwndSource.FromHwnd(_windowHandle);
            _hwndSource?.AddHook(HwndHook);

            bool success = RegisterHotKey(_windowHandle, HOTKEY_ID, K_CTRL | K_ALT, K_A);   // CTRL + ALT + A
        }

        private IntPtr HwndHook(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
        {
            if (msg == WM_HOTKEY && wParam.ToInt32() == HOTKEY_ID)
            {
                OpenClosedApp();
                handled = true; // event gérer
            }
            return IntPtr.Zero;
        }

        private void OpenClosedApp()
        {
            if (this.WindowState == WindowState.Minimized || this.Visibility != Visibility.Visible)
            {
                this.Show();
                this.WindowState = WindowState.Normal;
                this.Activate(); 
            }
            else
            {
                this.WindowState = WindowState.Minimized;
            }
        }

        private void MainWindow_Closed(object? sender, EventArgs e)
        { // free
            _hwndSource?.RemoveHook(HwndHook);
            UnregisterHotKey(_windowHandle, HOTKEY_ID);
        }
    }
}
