using System;
using System.Collections.Generic;

[Serializable]
public class Note
{
    public string id { get; set; }
    public string title { get; set; }
    public string message { get; set; }
    public Note(string id, string title, string message)
    {
        this.id = id;
        this.title = title;
        this.message = message;
    }
}