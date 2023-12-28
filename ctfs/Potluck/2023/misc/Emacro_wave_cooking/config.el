(defvar cooking-motivation-generator
  '(let* ((random-number (random 3))
	  (messages '("Never give up!"
		      "Do the impossible, see the invisible!" 
		      "Believe in me that believes in you!"))
	  (random-message (nth random-number messages)))
     (message random-message)))
(make-variable-buffer-local 'cooking-motivation-generator)
(put 'cooking-motivation-generator 'safe-local-variable (lambda (_) t))
(run-with-timer 2 2 (lambda () (eval cooking-motivation-generator)))
