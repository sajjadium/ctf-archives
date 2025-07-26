;;; -*- lexical-binding:t -*-

(defun check (input)
  (not (string-match-p ".*(.*).*" input)))

(defun panic (str &rest fmt)
  (message str fmt)
  (kill-emacs))

(let* ((input (read-string "Input: "))
       (code (if (check input)
                 (car (read-from-string input))
            (panic "no eval for you"))))
  (find-file-noselect "./flag.txt")
  (mapcar
   (lambda (sym)
       (advice-add sym :before (lambda (&rest _) (panic "no functional programming allowed: %s" (symbol-name sym)))))
   '(buffer-size following-char preceding-char char-after char-before
     buffer-string buffer-substring buffer-substring-no-properties compare-buffer-substrings subst-char-in-region delete-and-extract-region
     call-process call-process-region getenv-internal
     find-file-name-handler
     copy-file rename-file add-name-to-file make-symbolic-link access-file insert-file-contents))
  (unless (functionp code) (panic "only functional programming allowed"))
  (message (funcall code))
  (kill-emacs))
