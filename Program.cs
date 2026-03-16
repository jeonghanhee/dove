using System.Threading;

class Program
{
    static void Main()
    {
        Console.WriteLine("dove running...");

        if (!DoveFolder.Create())
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
}