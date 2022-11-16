(ns erd-parser
  (:require ["mermaid/dist/Diagram" :as Diagram])
  )
(def erd-str
  "erDiagram
TEAMS { str department str name int id }
USERS { int id str first_name str last_name str email float GPA str department int team }
TEAMS ||--o{ USERS : \"89% confidence match on USERS.team\""
  )

Diagram
(.-getDiagramFromText Diagram)
;; (.parse (.-mermaidAPI mermaid) erd-str)

;; (js/Object.keys (.-mermaidAPI mermaid))

(defn main [& cli-args]
  (prn "hello world"))
