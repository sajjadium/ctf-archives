(in-package :cl-user)
(defpackage app.web
  (:use :cl
        :caveman2
        :caveman2.exception
        :app.config
        :app.view
        :flexi-streams
        :cl-ppcre)
  (:export :*web*))
(in-package :app.web)

(defparameter *flag* "REDACTED")

;;
;; Exception handling

(define-condition verbose-exception (caveman-exception)
  ((reason :initarg :reason :type string :reader exception-reason))
  (:report
   (lambda (condition stream)
     (format stream "~A~%" (exception-reason condition)))))

(defun throw-status (code format-string &rest args)
  (error 'verbose-exception
         :code code
         :reason (apply #'format nil format-string args)))

(defmacro with-internal-server-error (&body body)
  `(handler-case (progn ,@body)
     ((and error (not caveman-exception)) (condition)
       (throw-code 500))))

; Just an alias
(defmacro w/500 (&rest rest)
  `(with-internal-server-error ,@rest))

;;
;; Utilities

(defun plistp (plist)
  (and (listp plist)
       (evenp (length plist))))

(defun alistp (alist)
  (and (listp alist)
       (every #'consp alist)))

(defun make-keyword (value)
  (intern (string-upcase (string value))
          :keyword))

(defun allowed-sub-key-char-p (c)
  (or (alphanumericp c)
      (char= c #\-)
      (char= c #\_)))

(defun allowed-sub-char-p (c)
  (char/= c #\{ #\}))

(defun request-body (request)
  (let ((decoded-body (make-flexi-stream (request-raw-body request)
                                         :external-format :utf-8)))
    (make-concatenated-stream
      decoded-body
      (make-string-input-stream (string #\Newline)))))

(defun parse-sexp (stream)
  (let ((*read-eval* nil))
    (with-standard-io-syntax
      (read stream))))

;;
;; Business logic

(defun parse-body ()
  (handler-case
      (parse-sexp (request-body *request*))
    (end-of-file (condition)
      (throw-status 400 "Request body does not contain a well-formed s-expression"))))

(defun apply-substitution (template key value)
  (unless (symbolp key)
    (throw-status 422 "Substitution key ~S is not a symbol~@[ (try ~S)~]." key (ignore-errors (make-keyword key))))
  (unless (stringp value)
    (throw-status 422 "Substitution value ~S is not a string." value))
  (let ((key-string (symbol-name key)))
    (unless (every #'allowed-sub-key-char-p key-string)
      (throw-status 422 "Invalid substitution key ~S. Substitution keys can only contain alphanumeric characters, dashes and underscores." key))
    (unless (every #'allowed-sub-char-p value)
      (throw-status 422 "Invalid substitution value for key ~S. Substitution values cannot contain curly braces." key))
    (let ((sub-regex (format nil "(?i){~A}" key-string)))
      (regex-replace-all sub-regex template value))))

;;
;; Application

(defclass <web> (<app>) ())
(defvar *web* (make-instance '<web>))
(clear-routing-rules *web*)

;;
;; Routing rules

(defroute "/" ()
  (with-internal-server-error
    (render #P"index.html" `(:motd ,*flag*))))

(defroute ("/interpolate" :method :post) (&aux (body (w/500 (parse-body))))
  (with-internal-server-error
    (unless (plistp body)
      (throw-status 422 "Request body must be a plist"))
    (destructuring-bind (&key (template nil template-supplied-p)
                              substitutions
                              &allow-other-keys)
        body
      (unless template-supplied-p
        (throw-status 422 "Must specify a template."))
      (unless (stringp template)
        (throw-status 422 "Template must be a string."))
      (unless (alistp substitutions)
        (throw-status 422 "Substitutions must be an association list."))
      (loop for (key . value) in substitutions
            with result = template
            do (setf result (apply-substitution result key value))
            finally (return result)))))

;;
;; Error pages

(defmethod on-exception ((app <web>) (code (eql 404)))
  (declare (ignore app))
  (merge-pathnames #P"_errors/404.html"
                   *template-directory*))
