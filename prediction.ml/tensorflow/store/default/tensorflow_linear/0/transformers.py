
    # TODO:  don't hard code this!
    inputs_np = np.asarray([1.0])
    #print(inputs_np)
    inputs_tensor_proto = tf.contrib.util.make_tensor_proto(inputs_np,
                                                            dtype=tf.float32)
    request.inputs['x_observed'].CopyFrom(inputs_tensor_proto)

      # Send request
      output = stub.Predict(transformed_input, self.request_timeout)
      print(output)

    result_np = tf.contrib.util.make_ndarray(result.outputs['y_pred'])
    #print(result_np)
