object DataProcessor {
  def main(args: Array[String]): Unit = {
    val data = List(1, 2, 3, 4, 5)
    val squared = data.map(x => x * x)
    println("Original: " + data)
    println("Squared: " + squared)
  }
}
