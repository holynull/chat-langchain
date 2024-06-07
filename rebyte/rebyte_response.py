class RebyteResponse:
    def __init__(self, data, headers, stream=False):
        self._headers = headers
        self.data = data
        self.stream = stream

    def get_error(self):
        if self.stream:
            return self.get_stream_error()
        result = self.data["run"]["results"][0][0]
        if result['error'] is not None:
            return result['error']
        if result['value'] is None:
            raise "No value found"
        return
    
    def get_stream_type(self):
        return self.data['type']
    
    def get_stream_chunk(self):
        res_type = self.get_stream_type()
        if res_type != "block_execution":
            return None
        elif self.data['content']['block_type']!= "output":
            return None
        return self.data['content']['execution'][0][0]['value']['content']
    
    def get_stream_error(self):
        res_type = self.get_stream_type()
        if res_type == "run_status":
            if self.data['content']['status'] == "errored":
              return "internal error. trace id: " + self.data['content']['run_id']
        elif res_type == "block_execution":
            err = self.data["content"]["execution"][0][0]
            if err["error"]:
                return err["error"]
        elif res_type == "final":
            return None

    