import org.jfree.chart.ChartFactory
import org.jfree.chart.ChartUtils
import org.jfree.data.category.DefaultCategoryDataset
import java.io.File

object DataVisualization {
  def main(args: Array[String]): Unit = {
    val dataset = new DefaultCategoryDataset()
    dataset.addValue(1.0, "Series1", "Category1")
    dataset.addValue(4.0, "Series1", "Category2")
    dataset.addValue(3.0, "Series1", "Category3")
    dataset.addValue(5.0, "Series1", "Category4")

    val chart = ChartFactory.createBarChart(
      "Sample Chart",
      "Category",
      "Value",
      dataset
    )

    ChartUtils.saveChartAsPNG(new File("chart.png"), chart, 800, 600)
    println("Chart saved as chart.png")
  }
}
