GRPC_OPTIONS = [('grpc.max_send_message_length', 500 * 1024 * 1024),
                ('grpc.max_receive_message_length', 500 * 1024 * 1024)]


def encode_matrix(matrix):
    return ";".join([",".join([str(item) for item in inner_array]) for inner_array in matrix])


def decode_matrix(matrix):
    return [[int(item) for item in array.split(",")] for array in matrix.split(";")]
