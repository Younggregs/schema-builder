import json

class SchemaBuilder:
    
    def __init__(self) -> None:
        self.base_schema = 'schema'
    
    def extract(self, file_path: str) -> str:
        """ Extract the schema from the data and save to file """
        data = {}
        with open(file_path, 'r') as f:
            try: 
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f'Error: {file_path} is not a valid JSON file')
                return None
        json_object = self._build(data.get('message', {}))
        json_object = json.dumps(json_object, indent=4)
        file_name = file_path.split('/')[-1].split('.')[0]
        schema_name = f'{self.base_schema}/{file_name}.json'
       
        with open(schema_name, 'w') as f:
            f.write(json_object)
        return schema_name
    
    def _build(self, data: dict) -> dict:
        """ Build the schema from the data """
        schema = {}
        for key, value in data.items():
            schema[key] = {
                "type": self._get_type(value),
                "tag": "",
                "description": "",
                "required": False
            }
            # If the value is an object, then recursively build the schema
            if type(value).__name__ == 'dict':
                schema[key]['properties'] = self._build(value)
            # If the value is a list, and the items are objects then recursively build the schema
            elif type(value).__name__ == 'list' and len(value) != 0 and \
                type(value[0]).__name__ == 'dict':
                schema[key]['items'] = []
                for k, v in enumerate(value):
                    schema[key]['items'].append(self._build(v))
        return schema
    
    def _get_type(self, value) -> str:
        """ Get the type of the value """
        type_name = type(value).__name__
        if type_name == 'str':
            return 'string'
        elif type_name == 'int':
            return 'integer'
        elif type_name == 'bool':
            return 'boolean'
        elif type_name == 'list':
            # If the list is not empty and the first element is a string
            # then it is an enum
            if len(value) != 0 and type(value[0]).__name__ == 'str':
                return 'enum'
            return 'array'
        elif type_name == 'dict':
            return 'object'
        else:
            return type_name