import tflite_runtime.interpreter as tflite
import numpy as np

class CoralInference:
    def __init__(self, model_path, labels_path, input_size, use_edgetpu=True):
        self.input_size = input_size
        if use_edgetpu:
            self.interpreter = tflite.Interpreter(model_path=model_path, experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        else:
            self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        with open(labels_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

    def preprocess(self, img):
        if img.shape[0] != self.input_size:
            raise ValueError("Wrong size")
        input_data = np.expand_dims(img, axis=0).astype(np.float32)
        return input_data

    def infer(self, img):
        input_data = self.preprocess(img)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        outputs = [self.interpreter.get_tensor(d['index']) for d in self.output_details]
        return outputs
