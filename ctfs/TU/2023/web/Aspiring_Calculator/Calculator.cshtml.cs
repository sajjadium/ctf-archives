using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorEngine;
using RazorEngine.Templating;

using System.Threading;
using System.Threading.Tasks;

namespace challenge.Pages;

public class CalculatorModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;

    public CalculatorModel(ILogger<IndexModel> logger)
    {
        _logger = logger;
    }

    public void OnGet()
    {
    }


    public void OnPost()
    {
        var calculation = Request.Form["calculation"];

        if (!calculation.Contains("@"))
        {
            calculation = $"@({calculation})";
        }

        ViewData["result"] = "Result: " + calculation;

        var templateKey = Guid.NewGuid().ToString();
        var tpl = $"{calculation}";

        var cancellationTokenSource = new CancellationTokenSource(TimeSpan.FromSeconds(10));
        var cancellationToken = cancellationTokenSource.Token;

        var compileTask = Task.Run(() =>
        {
            return Engine.Razor.RunCompile(tpl, templateKey, null, new { result = calculation });
        }, cancellationToken);

        var completedTask = Task.WhenAny(compileTask, Task.Delay(TimeSpan.FromSeconds(10), cancellationToken)).Result;

        if (completedTask == compileTask)
        {
            ViewData["result"] = compileTask.Result;
        }
        else
        {
            ViewData["result"] = "Timeout occurred";
        }
    }
}
