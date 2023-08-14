<%@ Page Language="C#" AutoEventWireup="true"%>
<%@ Import Namespace="System.Collections.Generic" %>

<script runat="server">
    protected void Page_Load(object sender, EventArgs e)
    {
        if (ViewState["page"] == null)
        {
            DefaultView(sender, e);
        }
        else
        {
            String str = ViewState["page"].ToString();
            if (str.Equals("notes"))
                NotesView(sender, e);
            if (str.Equals("added"))
                AddNewNoteView(sender, e);
        }
    }
    
    protected void DefaultView(object sender, EventArgs e)
    {
        Title1.Text = "Add Your First Note";
        DeleteAllDiv.Visible = false;
        NotesDiv.Visible = false;
        DefaultDiv.Visible = true;
        if (IsPostBack)
        {
            noteName.Visible = false;
            noteText.Visible = false;
            btnText.Visible = false;
            Message1.Visible = true;
            MainPage1.Visible = true;
        }
        else
        {
            Message1.Visible = false;
            MainPage1.Visible = false;
        }
    }
    
    protected void Add_Note(object sender, EventArgs e)
    {
        Guid uuid = Guid.NewGuid();
        string id = uuid.ToString();
        Note newNote = new Note(id, Request.Form["noteName"], Request.Form["noteText"]);
        AddNewNote(id, newNote);
    }

    private void AddNewNote(string id, Note note)
    {
        ViewState.Add(id, note);
        ViewState["page"] = "notes";
    }

    protected void NotesView(object sender, EventArgs e)
    {
        DeleteAllDiv.Visible = false;
        NotesDiv.Visible = true;
        DefaultDiv.Visible = false;
        List<Note> notes = new List<Note>();
        Number1.Text = (ViewState.Count - 1).ToString();
        foreach (String key in ViewState.Keys)
        {
            if (key.Equals("page"))
                continue;
            Note note = (Note)ViewState[key];
            notes.Add(note);
        }
        Repeater1.DataSource = notes;
        Repeater1.DataBind();
    }

    protected void AddNote_Click(object sender, EventArgs e)
    {
        DeleteAllDiv.Visible = false;
        NotesDiv.Visible = false;
        DefaultDiv.Visible = true;
        ViewState["page"] = "addNew";
        AddNewNoteView(sender, e);
    }

    protected void AddNewNoteView(object sender, EventArgs e)
    {
        Title1.Text = "Add New Note";
        String str = ViewState["page"].ToString();
        if (str.Equals("added"))
        {
            Message1.Visible = true;
            MainPage1.Visible = true;
            noteName.Visible = false;
            noteText.Visible = false;
            btnText.Visible = false;
            ViewState["page"] = "notes";
        }
        if (str.Equals("addNew"))
        {
            Message1.Visible = false;
            MainPage1.Visible = false;
            noteName.Visible = true;
            noteText.Visible = true;
            btnText.Visible = true;
            ViewState["page"] = "added";
        }
    }

    protected void DeleteAllView(object sender, EventArgs e)
    {
        NotesDiv.Visible = false;
        DefaultDiv.Visible = false;
        DeleteAllDiv.Visible = true;
    }

    protected void MainPage_Click(object sender, EventArgs e) { }

    protected void DeleteAll_Click(object sender, EventArgs e)
    {
        NotesDiv.Visible = false;
        DefaultDiv.Visible = false;
        DeleteAllDiv.Visible = true;
        ViewState.Clear();
        ViewState.Add("page", "notes");
    }

</script>

<!DOCTYPE html>
<html>
  <head>
    <title>Pageless Notebook</title>    
    <link href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
  </head>
<body>
    <form id="form1" runat="server">
        <div runat="server" id="DefaultDiv">
        <div class="container">
            <h2>
                <asp:Label ID="Title1" runat="server" Text=""></asp:Label>
            </h2>
        </div>
        <div class="container">
            <asp:Label ID="Message1" runat="server" Text="Success! Your new note was added!" Font-Bold="True" Font-Size="Large" ForeColor="Blue"></asp:Label>
        </div>
        <div class="container">
        <asp:TextBox id="noteName" class="form-control input-lg" type="text" placeholder="Set name for your note" required="true" runat="server"/>
            <br>
            <asp:TextBox id="noteText" class="form-control" rows="20" placeholder="Store some secrets here" required="true" TextMode="MultiLine" runat="server"/>
            <br>
            <div class="pull-right navbar fixed-bottom">
                <asp:Button id="btnText" class="btn btn-primary btn-lg" Text="Add note" runat="server" OnClick="Add_Note"/>
            </div>
            <div class="pull-right navbar fixed-bottom">
                <asp:Button ID="MainPage1" class="btn btn-primary btn-lg" Text="Go to Main Page" runat="server" OnClick="MainPage_Click"/>
            </div>
        </div>
        </div>
        <div runat="server" id="NotesDiv">
        <div class="container">
            <h2>Your Notes</h2>
        </div>
            <br>
        <div class="container">
        <div class="panel panel-default">
          <table class="table table-striped">
              <tbody>
                  <tr>
                  <td>Number of notes</td>
            <td><asp:Label ID="Number1" runat="server"></asp:Label></td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <div class="panel-heading">
              <h3>List of notes</h3>
          </div>
          <table class="table table-striped">
            <tbody>
                <tr>
                    <th>Title</th>
                    <th>Text</th>
                </tr>
                <asp:Repeater ID="Repeater1" runat="server">
                    <ItemTemplate>
                        <tr>
                            <td><%# Eval("Title") %></td>
                            <td><%# Eval("Message") %></td>
                        </tr>
                    </ItemTemplate>
                </asp:Repeater>
            </tbody>
          </table>
            <div>
                <asp:Button ID="AddButton" class="btn btn-primary btn-lg" Text="Add New Note" runat="server" OnClick="AddNote_Click"/>
                <asp:Button ID="DeleteAllButton" class="btn btn-primary btn-lg" BackColor="Crimson" Text="Delete All Notes" runat="server" OnClick="DeleteAll_Click"/>
        </div>
        </div>
        </div>
        <div runat="server" id="DeleteAllDiv">
            <div class="container">
                <h3>All your notes were successfully deleted</h3>
            </div>
            <div class="container">
                <asp:Button id="StupidButton1" class="btn btn-primary btn-lg" Text="Go to Main Page" runat="server" OnClick="MainPage_Click"/>
            </div>
        </div>
    </form>
</body>
</html>
