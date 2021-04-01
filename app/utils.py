def encode_matrix(matrix):
    return ";".join([",".join([str(item) for item in inner_array]) for inner_array in matrix])


def decode_matrix(matrix):
    return [[int(item) for item in array.split(",")] for array in matrix.split(";")]
