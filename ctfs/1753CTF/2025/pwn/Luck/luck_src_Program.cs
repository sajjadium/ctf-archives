using System.Security.Cryptography;
using System.Text;

class Program
{
    static async Task Main()
    {
        Console.WriteLine("Joker: Hello, friend-o. Up for a challenge? Let's check your luck. Who get the score of 100 first, wins, okay?");
        Console.WriteLine("Joker: But I only play with real folks, you know what I mean?");
        
        if (!await HumanCheck.VerifyHuman())
        {
            Console.WriteLine("Joker: Ha! I knew it. Come back when you'ree actually human!");
            Console.WriteLine("Press Enter to exit...");
            Console.ReadLine();
            return;
        }
        
        Console.WriteLine("Joker: Good, good! You passed. Let's play!");
        
        var flag = Environment.GetEnvironmentVariable("flag");
        
        Console.Write("Enter a game seed (or press Enter for random): ");
        var seedInput = Console.ReadLine();
        
        var rng = new Random(GetSeed(seedInput));
            
        Console.WriteLine(string.IsNullOrWhiteSpace(seedInput) 
            ? "Using random seed." 
            : $"Using seed: {seedInput}");
        
        var playerScore = 0;
        var jokerScore = 0;
        
        while (playerScore < 100 && jokerScore < 100)
        {
            Console.WriteLine($"\nCurrent scores - You: {playerScore}, Joker: {jokerScore}");
            Console.WriteLine("Press Enter to roll...");
            Console.ReadLine();
            
            var playerRoll = rng.Next(1, 7);
            var jokerRoll = rng.Next(5, 7);
            
            playerScore += playerRoll;
            jokerScore += jokerRoll;
            
            Console.WriteLine($"You rolled: {playerRoll}");
            Console.WriteLine($"Joker rolled: {jokerRoll}");
        }
        
        if (playerScore > jokerScore)
        {
            Console.WriteLine("\nArrhhhh.. You beat me.. how");
            Console.WriteLine($"Here's your flag: {flag}");
        }
        else
        {
            Console.WriteLine("\nJoker wins! Better luck next time!");
        }
        
        Console.WriteLine("Press Enter to exit...");
        Console.ReadLine();
    }
    
    static int GetSeed(string? input)
    {
        if (string.IsNullOrWhiteSpace(input))
            return Environment.TickCount;

        var hash = SHA256.HashData(Encoding.UTF8.GetBytes(input));
        return BitConverter.ToInt32(hash, 0);
    }
}