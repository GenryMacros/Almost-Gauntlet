
(defstruct Num truepart impart)

(defun mul(num1 num2)
  (defvar result (make-Num))
  (setf (Num-truepart result) (- (* (Num-truepart num1) (Num-truepart num2)) (* (Num-impart num1) (Num-impart num2))))
  (setf (Num-impart result) (+ (* (Num-truepart num1) (Num-impart num2)) (* (Num-impart num1) (Num-truepart num2))))
)

(defun add(num1 num2)
  (defvar result (make-Num))
  (setf (Num-truepart result) (+ (Num-truepart num1) (Num-truepart num2)))
  (setf (Num-impart result) (+ (Num-impart num1) (Num-impart num2)))
)
