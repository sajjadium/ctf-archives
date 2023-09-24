var rng = new Random();
byte[] Encrypt(byte[] x) => x.Select(a=>(byte)(a^rng.Next(256))).ToArray();
Console.WriteLine(Convert.ToHexString(Encrypt(File.ReadAllBytes("flag.txt"))));
Console.WriteLine(Convert.ToHexString(Encrypt(new byte[2000])));
