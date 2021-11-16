package com.l3hsec;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@WebServlet("/UploadServlet")
public class UploadServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    // 上传文件存储目录
    private static final String UPLOAD_DIRECTORY = "upload";

    // 上传配置
    private static final int MEMORY_THRESHOLD = 1024 * 1024 * 3;
    private static final int MAX_FILE_SIZE = 1024 * 1024 * 1;
    private static final int MAX_REQUEST_SIZE = 1024 * 1024 * 1;

    /**
     * 上传数据及保存文件
     */
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response) throws ServletException, IOException {

        response.setCharacterEncoding("UTF-8");
        response.setContentType("text/html;charset=UTF-8");


        DiskFileItemFactory factory = new DiskFileItemFactory();
        factory.setSizeThreshold(MEMORY_THRESHOLD);
        factory.setRepository(new File(System.getProperty("java.io.tmpdir")));

        ServletFileUpload upload = new ServletFileUpload(factory);

        upload.setFileSizeMax(MAX_FILE_SIZE);

        upload.setSizeMax(MAX_REQUEST_SIZE);

        upload.setHeaderEncoding("UTF-8");


        String userDir = md5(request.getRemoteAddr());
        String uploadPath = request.getServletContext().getRealPath("./") + File.separator + UPLOAD_DIRECTORY + File.separator + userDir;


        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdir();
        }

        try {
            List<FileItem> formItems = upload.parseRequest(request);

            if (formItems != null && formItems.size() > 0) {
                for (FileItem item : formItems) {
                    if (!item.isFormField()) {
                        String fileName = new File(item.getName()).getName();
                        if (fileName.lastIndexOf('.') == -1) {
                            PrintWriter writer = response.getWriter();
                            writer.println("Error: 缺少文件后缀！");
                            writer.flush();
                            return;
                        }


                        String ext = fileName.substring(fileName.lastIndexOf('.'));
                        ext = checkExt(ext);

                        String filePath = uploadPath + File.separator + randName() + ext;
                        File storeFile = new File(filePath);

                        String content = item.getString();
                        boolean check = checkValidChars(content);

                        if (check){
                            response.getWriter().write("上传失败：检测到可见字符");
                            return;
                        }

                        //居然被绕过了，得再加一层过滤
                        BlackWordsDetect blackWordsDetect = new BlackWordsDetect(item);
                        boolean detectResult = blackWordsDetect.detect();
                        if (detectResult) {
                            response.getWriter().write("上传失败：检测到黑名单关键字！ " + blackWordsDetect.getBlackWord());
                            return;
                        } else {
                            item.write(storeFile);
                            response.getWriter().write("文件上传成功! 文件路径: " + filePath);
                        }
                    }
                }
            }
        } catch (Exception ex) {
            response.getWriter().write(
                    "上传失败：错误原因: " + ex.getMessage());
        }
    }

    public static String md5(String s) {
        String ret = null;
        try {
            java.security.MessageDigest m;
            m = java.security.MessageDigest.getInstance("MD5");
            m.update(s.getBytes(), 0, s.length());
            ret = new java.math.BigInteger(1, m.digest()).toString(16).toLowerCase();
        } catch (Exception e) {
        }
        return ret;
    }

    public static String randName() {

        return UUID.randomUUID().toString();
    }

    public static boolean checkValidChars(String content) {
        Pattern pattern = Pattern.compile("[a-zA-Z0-9]{2,}");
        Matcher matcher = pattern.matcher(content);
        return matcher.find();
    }

    public static String checkExt(String ext) {
        ext = ext.toLowerCase();

        String[] blackExtList = {
                "jsp", "jspx"
        };
        for (String blackExt : blackExtList) {
            if (ext.contains(blackExt)) {
                ext = ext.replace(blackExt, "");
            }
        }

        return ext;
    }
}