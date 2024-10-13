<?php

namespace App\Controllers;

use CodeIgniter\API\ResponseTrait;
use DOMDocument;
use Knp\Snappy\Pdf;
use Template;

helper("render");

class PDFMaker extends BaseController
{
    use ResponseTrait;

    public function create()
    {
        if (!session()->get("username")) {
            return $this->response->redirect("/login");
        }
        $validation = \Config\Services::validation();
        $post = $this->request->getPost(['body', 'option']);
        if (!$validation->run($post, 'upload_pdf')) {
            $errors = $validation->getErrors();
            return $this->failValidationErrors($errors);
        }
        $snappy = new Pdf('/usr/bin/wkhtmltopdf');
        $snappy->setTimeout(5);
        switch ($post['option']) {
            case 'getOutputFromHtml':
                $pdf_out = $snappy->getOutputFromHtml($post['body']);
                $b64_pdf = base64_encode($pdf_out);
                return $this->respond([
                    'pdf' => $b64_pdf
                ]);
            case 'generateFromHtml':
                // only admin can use this functionality
                if (
                    session()->get("role") === "admin" &&
                    $_SERVER['REMOTE_ADDR'] === "127.0.0.1"
                ){
                    $filename = "/tmp/" . uniqid("generated_pdf");
                    $dom = new DOMDocument();
                    $dom->loadHTML($post['body']);
                    $h1Element = $dom->getElementsByTagName('h1')->item(0);
                    if ($h1Element) {
                        $filename = $h1Element->nodeValue;
                    }
                    $pdf_out = $snappy->generateFromHtml($post['body'], $filename);
                    return $this->setResponseFormat('json')->respond([
                        'filename' => $filename
                    ]);
                } else {
                    echo $_SERVER['REMOTE_ADDR'];
                    return $this->failForbidden("forbidden");
                }

            default:
                return $this->failNotFound("command not found");
        }
    }
    public function view()
    {
        if (!session()->get("username")) {
            return $this->response->redirect("/login");
        }
        return (new Template('pages/pdf-maker'))
            ->setData('title', 'PDF Maker')
            ->render();
    }
}
