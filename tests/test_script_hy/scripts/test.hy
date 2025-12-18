(require hyrule [-> ->>])

(defn is-odd? [n] (!= (% n 2) 0))

(setv result
      (->> (get ismk.input 0)
           open
           .readlines
           (map int)
           (filter is-odd?)
           sum))

(print result
       :file
       (-> (get ismk.output 0)
           (open "w")))
