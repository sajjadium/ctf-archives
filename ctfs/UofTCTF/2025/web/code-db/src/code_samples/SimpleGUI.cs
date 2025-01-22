using System;
using System.Windows.Forms;

public class SimpleGUI : Form
{
    private Button button;
    private Label label;

    public SimpleGUI()
    {
        button = new Button();
        button.Text = "Click Me";
        button.Location = new System.Drawing.Point(50, 50);
        button.Click += Button_Click;

        label = new Label();
        label.Text = "Hello!";
        label.Location = new System.Drawing.Point(50, 100);
        label.AutoSize = true;

        Controls.Add(button);
        Controls.Add(label);
    }

    private void Button_Click(object sender, EventArgs e)
    {
        label.Text = "Button Clicked!";
    }

    [STAThread]
    public static void Main()
    {
        Application.Run(new SimpleGUI());
    }
}
