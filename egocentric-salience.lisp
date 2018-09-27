;; Simple model to show blending in action.
;; Load the model and call run to see the 
;; trace of two blended retrievals.  The
;; second one will usually fail because
;; it will be below the retrieval threshold.
;;
;; This is a simple case without partial
;; matching enabled and demonstrating both
;; a numeric value blending and a chunk based 
;; blending.


(clear-all)
(require-extra "blending")

(define-model test-blending
    (sgp :sim-hook "similarity_function"
         ;:blending-request-hook "new_blend_request"
         :tmp 1.0
         ;:seed (1 1) :bll nil :blc 5 :mp 1 :v t :blt t :esc t :ans .25 :rt -5)
         :seed (1 1) :bll nil :blc 5 :mp 1 :v t :blt t :esc t :ans nil :rt -5 :value->mag second)

  ;(chunk-type observation needsRadio needsFood needsFA needsWater actual)
  (chunk-type observation current_altitude heading view_left view_diagonal_left view_center view_diagonal_right view_right)
  ;(chunk-type decision needsRadio needsFood needsFA needsWater radio food firstaid water)
  (chunk-type decision current_altitude heading view_left view_diagonal_left view_center view_diagonal_right view_right
              action)
  
  

  
  (p p1
     =imaginal>
       current_altitude =CA
       heading =HD
       view_left =VL
       view_diagonal_left =VDL
       view_center =VC
       view_diagonal_right =VDR
       view_right =VR
     ?blending>
       state free
       buffer empty
       error nil
     ==>
     @imaginal>
     +blending>
       isa decision
       current_altitude =CA
       heading =HD
       view_left =VL
       view_diagonal_left =VDL
       view_center =VC
       view_diagonal_right =VDR
       view_right =VR)

  
  (p p2
     =blending>
       isa decision
       action =action
     ?blending>
       state free
     ==>
     ;!output! (blended value is =val)
     
     ; Overwrite the blended chunk to erase it and keep it 
     ; from being added to dm.  Not necessary, but keeps the 
     ; examples simpler.
     
     @blending>    
     
     ;;+blending>
     ;;  isa target
     ;;  key key-2)
     )
  )

