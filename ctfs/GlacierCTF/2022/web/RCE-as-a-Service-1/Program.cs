/*    ___             ___             ___
     /\  \           /\__\           /\__\
    /::\  \         /:/  /          /:/ _/_
   /:/\:\__\       /:/  /          /:/ /\__\
  /:/ /:/  /      /:/  /  ___     /:/ /:/ _/_
 /:/_/:/__/___   /:/__/  /\__\   /:/_/:/ /\__\
 \:\/:::::/  /   \:\  \ /:/  /   \:\/:/ /:/  /
  \::/~~/~~~~     \:\  /:/  /     \::/_/:/  /
   \:\~~\          \:\/:/  /       \:\/:/  /
    \:\__\          \::/  /         \::/  /
     \/__/           \/__/           \/__/    as a Service */

using System.Net.Mime;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Reflection;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.AspNetCore.Diagnostics;

// We gather every assembly that gets referenced from inside *this* assembly, because we
// also want them getting referenced inside our dynamically compiled library.
// There's no need to do it every time the endpoint gets hit, though, so we're doing it on startup.
var systemReference = MetadataReference.CreateFromFile(typeof(object).Assembly.Location);
var references = new List<MetadataReference>
{
    systemReference,
};

Assembly
    .GetEntryAssembly()?
    .GetReferencedAssemblies()
    .ToList()
    .ForEach(a => references.Add(MetadataReference.CreateFromFile(Assembly.Load(a).Location)));

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// We create a custom exception handler, which adds details to the response.
// This is bad practice for production environments, but we want the player
// to have as much feedback as possible.
app.UseExceptionHandler(exceptionHandlerApp =>
{
    exceptionHandlerApp.Run(async context =>
    {
        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        context.Response.ContentType = MediaTypeNames.Application.Json;

        var exceptionHandlerPathFeature = context.Features.Get<IExceptionHandlerPathFeature>();

        var errorResponse = new Dictionary<string, object?>
        {
            {"Endpoint", exceptionHandlerPathFeature?.Endpoint?.DisplayName},
            {"RouteValues", exceptionHandlerPathFeature?.RouteValues},
            {"Message", exceptionHandlerPathFeature?.Error.Message},
            {"FullException", exceptionHandlerPathFeature?.Error.ToString()}
        };
        
        await context.Response.WriteAsync(JsonSerializer.Serialize(errorResponse));
    });
});

// This route is for testing the connectivity.
app.MapGet("/", () => "HACK THE 🌍!");

// The high-level view of this route is the following:
// We take a WorkLoad object containing a string array and a query written as a lambda expression.
// (https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)
//
// The lambda expression (basically a function) gets written into our source code string *as is*!
// Afterwards we compile our code on-the-fly to a DLL and call the user-provided
// lambda expression, passing in the user-provided string array as an argument.
//
// Calling the function happens via Reflection.
// (https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/reflection)
app.MapPost("/rce", (WorkLoad workLoad) =>
{
    var (data, query) = workLoad;

    var src = $@"
        using System;
        using System.Linq;
        using System.Collections.Generic;
        
        namespace RCE
        {{
            public static class Factory
            {{
                public static Func<IEnumerable<string>, IEnumerable<object>> CreateQuery = {query};
            }}
        }}";

    var options = CSharpParseOptions.Default.WithLanguageVersion(LanguageVersion.CSharp10);
    var parsed = SyntaxFactory.ParseSyntaxTree(src, options);

    var compilationOptions = new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary)
                                      .WithUsings("System", "System.Collections.Generic", "System.Linq")
                                      .WithOptimizationLevel(OptimizationLevel.Release);
    
    var compilation = CSharpCompilation
                            .Create("RCE.dll")
                            .AddSyntaxTrees(parsed)
                            .WithOptions(compilationOptions)
                            .WithReferences(references);

    using var peStream= new MemoryStream();
    
    var emitResult = compilation.Emit(peStream);
    if (!emitResult.Success) {
        var errors = string.Join(" && ", emitResult.Diagnostics);
        throw new Exception($"Compiler Error(s): {errors}");
    }
    
    var rawAssembly = peStream.ToArray();
    var assembly = Assembly.Load(rawAssembly);
    var factory = assembly.GetType("RCE.Factory");
    var createQueryField = factory?.GetField("CreateQuery");
    var queryData = (Func<IEnumerable<string>, IEnumerable<object>>) createQueryField?.GetValue(null)!;
    
    var result = queryData(data);
    
    return Results.Ok(result);
});

app.Run();

public record WorkLoad(List<string> Data, string Query );
