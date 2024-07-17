import io


class MultiIO(io.StringIO):
    def __init__(self, outputs=None):
        super().__init__()
        if outputs is None:
            outputs = []
        self.outputs = outputs

    def write(self, __s):
        for output in self.outputs:
            try:
                output.write(__s)
            except:
                continue


