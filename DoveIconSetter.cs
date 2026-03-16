using System.Runtime.InteropServices;

class DoveIconSetter
{
    // Windows 
    [DllImport("shell32.dll")]
    static extern void SHChangeNotify(uint wEventId, uint uFlags, IntPtr dwItem1, IntPtr dwItem2);

    public static void SetWindowsIcon(string folderPath, string iconPath)
    {
        string desktopIni = Path.Combine(folderPath, "desktop.ini");

        if (File.Exists(desktopIni))
        {
            File.SetAttributes(desktopIni, FileAttributes.Normal);
            File.Delete(desktopIni);
        }

        File.WriteAllText(desktopIni,
$@"[.ShellClassInfo]
IconResource={iconPath},0
");
        DirectoryInfo dirInfo = new DirectoryInfo(folderPath);
        dirInfo.Attributes |= FileAttributes.System | FileAttributes.ReadOnly;
        File.SetAttributes(desktopIni, FileAttributes.Hidden | FileAttributes.System);
        SHChangeNotify(0x08000000, 0x0000, IntPtr.Zero, IntPtr.Zero);

        Console.WriteLine("Windows icon set.");
    }

    // macOS
    public static void SetMacOSIcon(string folderPath, string icnsPath)
    {
        // Quarantine attribute remove
        DoveCommand.Run("xattr", $"-r -d com.apple.quarantine \"{icnsPath}\"");

        // fileicon
        if (DoveCommand.IsAvailable("fileicon"))
        {
            if (DoveCommand.Run("fileicon", $"set \"{folderPath}\" \"{icnsPath}\"") == 0)
            {
                Console.WriteLine("macOS icon set via fileicon.");
                return;
            }
            Console.WriteLine("fileicon failed, trying Swift fallback...");
        }
        else
        {
            Console.WriteLine("fileicon not found, trying Swift fallback...");
        }

        // Swift
        if (SetMacOSViaSwift(folderPath, icnsPath))
        {
            Console.WriteLine("macOS icon set via Swift.");
            return;
        }

        Console.WriteLine("All icon methods failed. Icon skipped.");
    }

    // macOS command
    static bool SetMacOSViaSwift(string folderPath, string icnsPath)
    {
        string swiftCode = $@"
import AppKit
let img = NSImage(contentsOfFile: ""{icnsPath}"")!
NSWorkspace.shared.setIcon(img, forFile: ""{folderPath}"", options: [])
";
        string scriptPath = Path.Combine(Path.GetTempPath(), "dove_set_icon.swift");
        File.WriteAllText(scriptPath, swiftCode);

        return DoveCommand.Run("swift", $"\"{scriptPath}\"") == 0;
    }
}