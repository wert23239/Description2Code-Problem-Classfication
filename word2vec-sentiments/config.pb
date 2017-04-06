language: PYTHON
name:     "doc2vec"

variable {
 name: "size"
 type: INT
 size: 1
 min:  30
 max:  200
}

variable {
 name: "min_count"
 type: INT
 size: 1
 min:  1
 max:  5
}

variable {
 name: "window"
 type: INT
 size: 1
 min:  5
 max:  20
}

variable {
 name: "negative"
 type: INT
 size: 1
 min:  0
 max:  10
}

variable {
 name: "epoch_size"
 type: INT
 size: 1
 min:  10
 max:  200
}
