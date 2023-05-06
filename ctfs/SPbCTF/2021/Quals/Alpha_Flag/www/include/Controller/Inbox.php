<?php
class Controller_Inbox extends Proven_Controller {
    function Process($parameters) {
        $inbox = new Mail_Inbox((new Misc_Session())->User());

        if (!isset($parameters[0]) || ! $inbox->GetMail($parameters[0])) {
            $title = "Inbox";
            $head = "";
            $body = new Template_Inbox_List();
            $body->AssignVariable('inbox_list', $inbox);
        } else {
            $mail = $inbox->GetMail($parameters[0]);
            $title = $mail->GetSubject();
            $head = "";
            $body = new Template_Inbox_Mail();
            $body->AssignVariable('id', $mail->GetId());
            $body->AssignVariable('mail_meta', $mail);
            $body->AssignVariable('mail_body', nl2br(htmlspecialchars($mail->GetBody())));
        }

        return [$title, $head, $body];
    }
}
