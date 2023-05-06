using System.Globalization;
using System.Linq;
using System.Net.Http.Headers;

namespace MichaelBank
{
    class Program
    {
        static Dictionary<string, float> curConv = new();

        static HashSet<string> users = new();
        static Dictionary<string, string> userPasswords = new(StringComparer.InvariantCultureIgnoreCase);
        static Dictionary<string, float> userBalances = new(StringComparer.InvariantCultureIgnoreCase);

        static string loggedInUser = "anon";

        static void SetupUsers()
        {
            users.Add("michael");
            userPasswords["michael"] = File.ReadAllText("michael_password.txt");
            userBalances["michael"] = 999966.85f;

            users.Add("bob");
            userPasswords["bob"] = "bob";
            userBalances["bob"] = 25.35f;
        }

        static void SetupCurrencyConversion()
        {
            CultureInfo.CurrentCulture = new CultureInfo("en-US");
            
            var ccLines = File.ReadAllLines("currency_conversion.txt");
            for (var i = 1; i < ccLines.Length; i++)
            {
                var line = ccLines[i];
                var firstSpace = line.IndexOf(' ');
                var firstParens = line.LastIndexOf('(');
                var lastParens = line.LastIndexOf(')');
                var value = float.Parse(line.Substring(0, firstSpace));
                var curName = line.Substring(firstParens + 1, lastParens - firstParens - 1);
                curConv[curName] = value;
            }
        }

        static string GetCurrencySymbol()
        {
            var curCulture = CultureInfo.CurrentCulture;
            var regionName = curCulture.Name.Substring(curCulture.Name.IndexOf('_') + 1);
            var ri = new RegionInfo(regionName);
            return ri.ISOCurrencySymbol;
        }

        static void CreateAccount()
        {
            Console.Write("Type username: ");
            var username = Console.ReadLine()!;
            Console.Write("Type password: ");
            var password = Console.ReadLine()!;

            foreach (var user in users)
            {
                if (user.ToLower() == username.ToLower())
                {
                    Console.WriteLine("User already exists in database!");
                    return;
                }
            }

            if (users.Count > 10000)
            {
                Console.WriteLine("Database has too many users! Check back later.");
                return;
            }

            users.Add(username.ToLower());
            userPasswords[username] = password;
        }

        static void LogIn()
        {
            Console.Write("Type username: ");
            var username = Console.ReadLine()!;
            Console.Write("Type password: ");
            var password = Console.ReadLine()!;

            var success = false;
            foreach (var user in users)
            {
                if (user == username.ToLower())
                {
                    if (userPasswords[user] == password)
                    {
                        Console.WriteLine("Success");
                        success = true;
                        loggedInUser = user;
                    }
                }
            }

            if (!success)
            {
                Console.WriteLine("No login matched.");
            }
        }

        static string GetMoneyInConvertedCurrency(float usd)
        {
            var curSymbol = GetCurrencySymbol();
            var convertedStr = $"{usd * curConv[curSymbol]} {curSymbol}";
            return convertedStr;
        }

        static void CheckBalance()
        {
            if (loggedInUser == "anon")
            {
                Console.WriteLine("Not logged in.");
                return;
            }

            if (!userBalances.ContainsKey(loggedInUser))
            {
                userBalances[loggedInUser] = 5.0f;
            }
            else if (userBalances[loggedInUser] > 1000000)
            {
                Console.WriteLine("Wow, you have a million dollars! Here's the flag!");
                Console.WriteLine(File.ReadAllText("flag.txt"));
                return;
            }

            var balance = userBalances[loggedInUser];
            var convertedStr = GetMoneyInConvertedCurrency(balance);
            Console.WriteLine("Current balance: " + convertedStr);
        }

        static void CheckMoneyLeaderboard()
        {
            var balances = userBalances.AsEnumerable().OrderBy(p => -p.Value);
            foreach (var balancePair in balances)
            {
                var convertedStr = GetMoneyInConvertedCurrency(balancePair.Value);
                Console.WriteLine($"{balancePair.Key}: {convertedStr}");
            }
        }

        static void ChangeCurrency()
        {
            while (true)
            {
                Console.Write("Type language code to use its currency: ");
                var localeStr = Console.ReadLine()!;
                try
                {
                    var cultureInf = new CultureInfo(localeStr);
                    CultureInfo.CurrentCulture = cultureInf;
                    var curSymbol = GetCurrencySymbol();
                    if (!curConv.ContainsKey(curSymbol))
                    {
                        Console.WriteLine("Currency not in database.");
                        continue;
                    }
                    Console.WriteLine("New currency: " + curSymbol);
                    return;
                }
                catch
                {
                    Console.WriteLine("Not a valid code.");
                }
            }
        }

        static void SendMoney()
        {
            if (loggedInUser == "anon")
            {
                Console.WriteLine("Not logged in.");
                return;
            }

            if (!userBalances.ContainsKey(loggedInUser))
            {
                userBalances[loggedInUser] = 5.0f;
            }

            Console.WriteLine("Amount in USD: ");
            var amountStr = Console.ReadLine()!;

            if (!float.TryParse(amountStr, out float amount))
            {
                Console.WriteLine("Invalid amount.");
                return;
            }
            else if (amount < 0.0f)
            {
                Console.WriteLine("You cannot send negative money.");
                return;
            }
            else if (amount > userBalances[loggedInUser])
            {
                Console.WriteLine("You don't have enough money for that.");
                return;
            }

            Console.WriteLine("Who to send to: ");
            var sendToUser = Console.ReadLine()!;
            foreach (var user in users)
            {
                if (user == sendToUser.ToLower())
                {
                    userBalances[loggedInUser] -= amount;
                    userBalances[user] += amount;
                    Console.WriteLine("Done.");
                    return;
                }
            }

            Console.WriteLine("User not in database.");
        }

        static void Main(string[] args)
        {
            SetupUsers();
            SetupCurrencyConversion();
            Console.WriteLine("Welcome to Michael Bank! What would you like to do?");
            while (true)
            {
                Console.WriteLine("1. Create an account");
                Console.WriteLine("2. Log in");
                Console.WriteLine("3. Check balance");
                Console.WriteLine("4. Check leaderboard");
                Console.WriteLine("5. Change currency");
                Console.WriteLine("6. Send money");
                Console.WriteLine("7. Exit");
                var choice = Console.ReadLine();
                Console.WriteLine();
                try
                {
                    switch (choice)
                    {
                        case "1": CreateAccount(); break;
                        case "2": LogIn(); break;
                        case "3": CheckBalance(); break;
                        case "4": CheckMoneyLeaderboard(); break;
                        case "5": ChangeCurrency(); break;
                        case "6": SendMoney(); break;
                        case "7": return;
                        default: Console.WriteLine("Not a valid choice."); break;
                    }
                } catch { }
                Console.WriteLine();
                Console.WriteLine("What would you like to do?");
            }
        }
    }
}