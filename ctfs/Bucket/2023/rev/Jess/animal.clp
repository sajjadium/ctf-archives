/*
* 10/4/22
* Think of an Animal
*/
(reset)
(run)

(batch "utilities_v4.clp")

(deftemplate attribute (slot id) (slot value))  ; 0 is false; 1 is true

(do-backward-chaining attribute)

(assert (attribute (id -1) (value 0)))          ; Finished attribute

/*
* Property ID Guide
* 0 - Animal stays in the water
* 1 - Animal flies
* 2 - Animal eats meat
* 3 - Animal is massive
* 4 - Animal is a mammal
* 5 - Animal is an insect
* 6 - Animal bites
* 7 - Animal has claws
* 8 - Animal lives in africa
* 9 - Animal has tentacles
* 10 - Animal has smooth skin
* 11 - Animal has striped skin
* 12 - Animal is domesticated
* 13 - Animal has black skin/fur
*/

/*
* Rule to finish the game
* Only place where halt is used
*/
(defrule finished
   (attribute (id -1) (value 1))
   =>
   (halt)
)

/****************PROPERTY RULES******************/

(defrule getWater
   "gets whether the animal stays in the water or not; Requires water unset"
   (not (attribute (id 0)))
   =>
   (printout t "Does your animal stay in the water? (Must stay in the water, not just temporarily go there)  ")
   (setboolproperty 0)
)

(defrule getFly
   "gets whether the animal flys or not; Requires fly unset"
   (not (attribute (id 1)))
   =>
   (printout t "Does your animal fly?  ")
   (setboolproperty 1)
)

(defrule getCarninvore
   "gets whether the animal eats meat or not; Requires carnivore unset"        ; Iguanas can rarely eat meat but they are not supposed to so they are considered herbivores
   (not (attribute (id 2)))
   =>
   (printout t "Does it eat meat?  ")
   (setboolproperty 2)
)

(defrule getMassive
   "gets whether the animal is massive; Requires massive unset"
   (not (attribute (id 3)))
   =>
   (printout t "Is the animal massive?  ")
   (setboolproperty 3)
)

(defrule getmammal
   "gets whether the animal is a mammal; Requires mammal unset"
   (not (attribute (id 4)))
   =>
   (printout t "Is the animal a mammal?  ")
   (setboolproperty 4)
)

(defrule getInsect
   "gets whether the animal is an insect; Requires insect unset"
   (not (attribute (id 5)))
   =>
   (printout t "Is the animal an insect?  ")
   (setboolproperty 5)
)

(defrule getbite
   "gets whether the animal bites; Requires bite unset"
   (not (attribute (id 6)))
   =>
   (printout t "Does the animal bite?  ")
   (setboolproperty 6)
)

(defrule getClaws
   "gets whether the animal has claws; Requires claws unset"
   (not (attribute (id 7)))
   =>
   (printout t "Does the animal have claws?  ")
   (setboolproperty 7)
)

(defrule getAfrica
   "gets whether the animal is in Africa; Requires africa unset"
   (not (attribute (id 8)))
   =>
   (printout t "Does the animal live in Africa?  ")
   (setboolproperty 8)
)

(defrule getTentacles
   "gets whether the animal has tentacles; Requires tentacles unset"           ; The antenna looking parts on some snails and snakes are also called tentacles
   (not (attribute (id 9)))
   =>
   (printout t "Does the animal have tentacles?  ")
   (setboolproperty 9)
)

(defrule getSmoothSkin
   "gets whether the animal has smooth skin; Requires smooth skin unset"
   (not (attribute (id 10)))
   =>
   (printout t "Does the animal have smooth skin?  ")
   (setboolproperty 10)
)

(defrule getStripedSkin
   "gets whether the animal has striped skin; Requires striped skin unset"
   (not (attribute (id 11)))
   =>
   (printout t "Does the animal have striped skin?  ")
   (setboolproperty 11)
)

(defrule getDomesticated
   "gets whether the animal is domesticated; Requires domesticated unset"
   (not (attribute (id 12)))
   =>
   (printout t "Is the animal domesticated?  ")
   (setboolproperty 12)
)

(defrule getBlack
   "gets whether the animal has black skin/fur; Requires black skin/fur unset"
   (not (attribute (id 13)))
   =>
   (printout t "Does the animal have black skin/fur?  ")
   (setboolproperty 13)
)

(defrule getOrange
   "gets whether the animal has orange skin/fur; Requires orange skin/fur unset"
   (not (attribute (id 14)))
   =>
   (printout t "Does the animal have orange skin/fur?  ")
   (setboolproperty 14)
)

/*************ANIMAL RULES***************/

/*
* Index of the first comma
* ?string: the string to check
*/
(deffunction ci (?string)
   (return (str-index "," ?string))
)

/*
* Gets the next comma or the length of the string
* ?string: The string to check
*/
(deffunction nextCommaOrLength (?string)
   (if (> (str-length ?string) 1) then                                        ; Ensure the string is over 1 char
      (bind ?currComma (+ (ci ?string) 1))                                    ; Get the location of the first comma
      (bind ?newString (sub-string ?currComma (str-length ?string) ?string))  ; Make a new string without it
      (bind ?ci (ci ?newString))                                              ; Get the location of it
      (if (integerp ?ci) then                                                 ; Check if the comma even exists, this will be a boolean if there is no other comma
         (return ?ci)                                                         ; Return the location
      else
         (return (str-length ?string))                                        ; Return the length of the string
      )
   else
      (return 1)
   ) ; if (> (str-length ?string) 1)
) ; deffunction nextCommaOrLength (?string)

/*
* loads all animal rules
* ?filename: The name of the file
*/
(deffunction loadRules (?filename)
   (open ?filename r)
   (bind ?reading TRUE)
   (bind ?line (readline r))
   (while ?reading
      (loadAnimal ?line)
      (bind ?line (readline r))
      (if (numberp (str-index "EOF" ?line)) then  ; If at end of file, set reading to false
         (bind ?reading FALSE)
      )
   )
   (return)
) ; deffunction loadRules (?filename)

/*
* Load the rule for an animal from a csv
* This method uses helper functions ci and nextCommaOrLength
* ?line: The line of the rule
* Example generated rule:
(defrule isfrog
   (attribute (id 0) (value 1))
   (attribute (id 2) (value 1))
   (attribute (id 3) (value 0))
   (attribute (id 4) (value 0))
   (attribute (id 7) (value 0))
   => 
   (verify "frog")
)
*/
(deffunction loadAnimal (?line)
   (bind ?animal (sub-string 1 (- (ci ?line) 1) ?line))                                     ; The name of the animal being loaded
   (bind ?rule (str-cat "(defrule is" ?animal " "))                                         ; The rule being created
   (bind ?line (sub-string (ci ?line) (str-length ?line) ?line))                            ; The current line

   (for (bind ?i 0) (numberp (ci ?line)) (++ ?i)                                            ; Reads through the line while there is a comma in it and increments a ticker for attribute id
      (if (= (ci ?line) 1) then                                                             ; If the comma is in the first char as it should be
         (bind ?stringWithoutComma (nextCommaOrLength ?line))                               ; Gets the location of the next comma, if there is no other comma it gets the string length

         (if (and (> (str-length ?line) 1) (not (= (ci ?line) ?stringWithoutComma))) then   ; If the string is long enough and if this is not the only comma in the string
            (bind ?value (sub-string (+ (ci ?line) 1) 2 ?line))                             ; Bind the value which will be a 1 or 0
         else                                                                               ; If there is no value
            (bind ?value "")                                                                ; Bind the value to an empty string
         )

         (if (= (str-length ?value) 1) then                                                 ; Only check for the attribute if it is set
            (bind ?rule (str-cat ?rule "(attribute (id " ?i ") (value " ?value ")) "))      ; Sets the attribute
         )
      ) ; if (= (ci ?line) 1)

      (if (> (str-length ?line) 2) then                                                     ; If there are more attributes to parse
         (bind ?locInString (ci (sub-string (+ (ci ?line) 1) (str-length ?line) ?line)))    ; Checks the location of the next comma
         (bind ?nextComma (+ ?locInString (ci ?line)))                                      ; Binds the location of the next comma in the current line
         (bind ?line (sub-string ?nextComma (str-length ?line) ?line))                      ; Remove the current attribute from the string
      else
         (bind ?line "")                                                                    ; If there are no more attributes set the line to nothing
      ) ; if (> (str-length ?line) 2)
   ) ; for (bind ?i 0) (numberp (ci ?line)) (++ ?i)
   (bind ?rule (str-cat ?rule " => (verify \"" ?animal "\"))"))                             ; Add the right hand side of the rule with the animal name

   (build ?rule)                                                                            ; Loads the rule
) ; deffunction loadAnimal (?line)

(loadRules "animal.csv")

/*******************HELPER FUNCTIONS*********************/

/*
* Checks if the system guessed the animal correctly
* ?name: the name of the animal
*/
(deffunction verify (?name)
   (bind ?response (sub-string 1 1 (lowcase (ask (str-cat "Is your animal a " ?name "? ")))))
   (if (eq ?response "y") then
      (printout t ":)" crlf)
   else
      (printout t ":(" crlf)
   )
   (assert (attribute (id -1) (value 1)))     ; Special attribute finished
   (return)
) ; deffunction verify (?name)

/*
* Checks for the user input and sets the attribute to the proper result
* Uses the first letter ascii code so "Yes" returns true
* ?response: the ascii of the first letter of the user's response
*/
(deffunction setboolproperty (?attribute)
   (bind ?res (sub-string 1 1 (lowcase (read))))                     ; Set res to the first letter of the lowercase of the user response
   (if (or (eq ?res "y") (eq ?res "n")) then
      (if (eq ?res "y") then
         (assert (attribute (id ?attribute) (value 1)))
      else 
         (assert (attribute (id ?attribute) (value 0)))
      )
   else
      (if (not (eq ?res "u")) then                                   ; If the response is not Y N or U tell the user the correct inputs
         (printout t "Only use Y N and U!" crlf)
      )
   ) ; if (or (eq ?res "y") (eq ?res "n"))
   (return)
) ; deffunction setboolproperty (?attribute)

(run)