namespace test
{
    class Program
    {
        public readonly System.Collections.Generic.List<int> a = new System.Collections.Generic.List<int>();
        public Program(){
            a.Add(1);
            a.Add(2);
        }
        public void Run(){
            System.Action<int>  b = x=>{
$user_input
            };
            try {
                a.ForEach(b);
                if(a.Count!=2||(a.Count>0&&a[0]!=1)){
                    System.Console.WriteLine("$password");
                }
            } catch (System.Exception e) {
                System.Console.WriteLine("failed");
            }
        }
        static void Main(string[] args)
        {
            var p = new Program();
            p.Run();
        }
    }
}
