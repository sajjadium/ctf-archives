<?php
class Controller_Compose extends Proven_Controller {
    function Process($parameters) {
        $inbox = new Mail_Inbox((new Misc_Session())->User());

        $title = "Compose";
        $head = "";
        $body = new Template_Compose();
        $body->AssignVariables([
            'to' => "",
            'subject' => "",
            'mail_body' => "",
        ]);
        $smtp = "";

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            $to = new Misc_ProfanityFilter(preg_replace('/[\x00-\x1f\x7f-\xff]+/', '', $_POST['to']));
            $subject = new Misc_ProfanityFilter(preg_replace('/[\x00-\x1f\x7f-\xff]+/', '', $_POST['subject']));
            $mailBody = new Misc_ProfanityFilter($_POST['body']);
            $from = new Misc_ProfanityFilter(preg_replace('/[\x00-\x1f\x7f-\xff]+/', '', (new Misc_Session())->User()->GetLogin()));
            $date = new Misc_ProfanityFilter(date("r"));
            $smtp = new Smtp_Sender(new Mail(0, "From: $from\r\nTo: $to\r\nSubject: $subject\r\nDate: $date\r\n\r\n$mailBody"));
        } elseif (isset($parameters[0]) && $inbox->GetMail($parameters[0])) {
            $title = "Reply";
            $mail = $inbox->GetMail($parameters[0]);
            $body->AssignVariable('to', new Misc_ProfanityFilter(htmlspecialchars($mail->GetFrom())));
            $body->AssignVariable('subject', new Misc_ProfanityFilter(htmlspecialchars("Re: " . $mail->GetSubject())));
            $mailBody = new Misc_ProfanityFilter($mail->GetBody());
            $mailBody = preg_replace('/^|\n/', '\0> ', $mailBody);
            $body->AssignVariable('mail_body', htmlspecialchars("\n\n--------------------------\n\n$mailBody"));
        }

        $body->AssignVariable('send_result', $smtp);

        return [$title, $head, $body];
    }
}
