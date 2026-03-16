using System.Diagnostics;

class DoveCommand
{
    public static int Run(string command, string args)
    {
        try
        {
            ProcessStartInfo psi = new ProcessStartInfo(command, args)
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using var proc = Process.Start(psi);
            if (proc == null) return -1;

            string stdout = proc.StandardOutput.ReadToEnd();
            string stderr = proc.StandardError.ReadToEnd();
            proc.WaitForExit();

            if (!string.IsNullOrWhiteSpace(stdout)) Console.WriteLine(stdout.Trim());
            if (!string.IsNullOrWhiteSpace(stderr)) Console.WriteLine("[stderr] " + stderr.Trim());

            return proc.ExitCode;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Command '{command}' failed: {ex.Message}");
            return -1;
        }
    }

    public static bool IsAvailable(string command)
    {
        try
        {
            var psi = new ProcessStartInfo("which", command)
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using var proc = Process.Start(psi);
            proc?.WaitForExit();
            return proc?.ExitCode == 0;
        }
        catch { return false; }
    }
}