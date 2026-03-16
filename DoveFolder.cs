using System.Runtime.InteropServices;

class DoveFolder
{
    public static string? Path { get; private set; }
    public static readonly string FolderName = "★DOVE★";

    public static bool Create()
    {
        try
        {
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            Path = System.IO.Path.Combine(desktop, FolderName);

            Directory.CreateDirectory(Path);
            Console.WriteLine("dove created: " + Path);

            string iconPath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "./Icons/dove.ico");
            Console.WriteLine("Icon path: " + iconPath);
            Console.WriteLine("Icon exists: " + File.Exists(iconPath));

            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                DoveIconSetter.SetWindowsIcon(Path, iconPath);
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                string icnsPath = iconPath.Replace(".ico", ".icns");
                DoveIconSetter.SetMacOSIcon(Path, icnsPath);
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