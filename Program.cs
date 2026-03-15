using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    static string? dovePath;
    static string doveFileName = "★DOVE★";

    [DllImport("shell32.dll")]
    static extern void SHChangeNotify(uint wEventId, uint uFlags, IntPtr dwItem1, IntPtr dwItem2);

    static void Main()
    {
        Console.WriteLine("dove running...");

        if (!CreateDoveFolder())
        {
            Console.WriteLine("Failed to create dove.");
            return;
        }

        while (true)
        {
            CheckNotifications();
            Thread.Sleep(10000);
        }
    }

    static void CheckNotifications()
    {
        Console.WriteLine("checking notifications...");
    }

    static bool CreateDoveFolder()
    {
        try
        {
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            dovePath = Path.Combine(desktop, doveFileName);

            Directory.CreateDirectory(dovePath);
            Console.WriteLine("dove created: " + dovePath);

            string iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "favicon.ico");
            Console.WriteLine("Icon path: " + iconPath);
            Console.WriteLine("Icon exists: " + File.Exists(iconPath));

            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                string desktopIni = Path.Combine(dovePath, "desktop.ini");

                if (File.Exists(desktopIni))
                {
                    File.SetAttributes(desktopIni, FileAttributes.Normal);
                    File.Delete(desktopIni);
                }

                File.WriteAllText(desktopIni,
$@"[.ShellClassInfo]
IconResource={iconPath},0
");

                DirectoryInfo dirInfo = new DirectoryInfo(dovePath);
                dirInfo.Attributes |= FileAttributes.System | FileAttributes.ReadOnly;
                File.SetAttributes(desktopIni, FileAttributes.Hidden | FileAttributes.System);
                SHChangeNotify(0x08000000, 0x0000, IntPtr.Zero, IntPtr.Zero);
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                string script = $@"
tell application ""Finder""
    set folderRef to POSIX file ""{dovePath}"" as alias
    set iconFile to POSIX file ""{iconPath}"" as alias
    set icon of folderRef to iconFile
end tell";
                string tempScriptPath = Path.Combine(Path.GetTempPath(), "setIcon.scpt");
                File.WriteAllText(tempScriptPath, script);

                System.Diagnostics.Process.Start("osascript", tempScriptPath);
            }

            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine("Failed to create dove: " + ex.Message);
            return false;
        }
    }

}