// learning: https://www.x5software.com/chunk
// source: https://github.com/tomj74/chunk-templates/releases/tag/release-3.6.1
import com.x5.template.Chunk;
import com.x5.template.Theme;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;

public class ChallengeApp extends HttpServlet {

    // Java 15 has """ strings! (but we're not using that here) :(
    final static String INDEX_HTML =
            "<html>" +
            "    <body>" +
            "        <p>Please tell us a little about yourself:</p>" +
            "        <form action='submit' method='GET'>" +
            "            <label for='name'>Name:</label>" +
            "            <input type='text' id='name' name='name'><br><br>" +
            "            <label for='color'>Favorite Color:</label>" +
            "            <input type='text' id='color' name='color'><br><br>" +
            "            <input type='submit' value='Submit'>" +
            "        </form>" +
            "    </body>" +
            "</html>";

    final static String TEMPLATE_HTML =
            "<html>" +
            "    <body>" +
            "        <p>How are you {$name}?</p>" +
            "        <p>{$color} is also one of our favorites!</p>" +
            "    </body>" +
            "</html>";

    @Override
    protected void doGet(final HttpServletRequest request, final HttpServletResponse response)
            throws IOException {
        route(request, response);
    }

    // nobody routes this way in real apps :)
    private void route(final HttpServletRequest request, final HttpServletResponse response)
            throws IOException {
        String path = request.getServletPath();
        if ("/submit".equals(path)) {
            returnTemplatePage(request, response);
        }
        else {
            returnMainPage(response);
        }
    }

    private void returnMainPage(final HttpServletResponse response) throws IOException {
        response.getWriter().print(INDEX_HTML);
    }

    private void returnTemplatePage(final HttpServletRequest request, final HttpServletResponse response)
            throws IOException {
        Theme theme = new Theme();
        Chunk html = theme.makeChunk();
        html.append(TEMPLATE_HTML);

        Map<String, String[]> params = request.getParameterMap();
        for (String paramName: params.keySet()) {
            String[] paramValues = params.get(paramName);
            String paramValue = String.join("", paramValues);
            html.set(paramName, preventTrickery(paramValue));
        }

        String flag = System.getenv("FLAG");
        html.set("flag", flag);

        response.getWriter().print(html.toString());
    }

    private String preventTrickery(final String input) {
        return preventRecursiveTags(htmlEncode(input));
    }

    private String preventRecursiveTags(final String input) {
        return input.replace("$", "");
    }

    private String htmlEncode(final String input) {
        return input
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }
}