<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Set" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Simple Memo</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Sticky footer styles
-------------------------------------------------- */
html {
  position: relative;
  min-height: 100%;
}
body {
  margin-bottom: 60px; /* Margin bottom by footer height */
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px; /* Set the fixed height of the footer here */
  line-height: 60px; /* Vertically center the text there */
  background-color: #f5f5f5;
}


/* Custom page CSS
-------------------------------------------------- */
/* Not required for template or sticky footer method. */

.container {
  width: auto;
  max-width: 680px;
  padding: 0 15px;
}
    </style>
  </head>
<body>
      <!-- Begin page content -->
    <main role="main" class="container">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Memo</th>
            </tr>
          </thead>
          <tbody>
            <%
                HashMap<Integer, String> list = (HashMap<Integer, String>)request.getAttribute("list");
                if(list == null) list = new HashMap<Integer, String>();
                Set<Integer> keySet = list.keySet();
            %>
            <% for(Integer key : keySet) { %>
            <tr>
                <th scope="row"><a href="/memo/read?idx=<%=key%>"><%=key%></a></th>
                <td><%=list.get(key)%></td>
            </tr>
          <% } %>
        </tbody>
    </table>
    </main>
</body>
</html>
