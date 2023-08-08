import sys
from schema_builder.schema_builder import SchemaBuilder

if __name__ == '__main__':
    if sys.argv[1] == 'extract':
        SchemaBuilder().extract(sys.argv[2])