import tomlkit
from pathlib import Path

# Create a new TOML document
doc = tomlkit.document()

# Add a table (section)
database_table = tomlkit.table()
database_table.add("host", "localhost")
database_table.add("port", 5432)
database_table.add("username", "admin")
doc.add("database", database_table)

# Add an array within a table
server_table = tomlkit.table()
server_table.add("port", 8080)
server_table.add("debug", False)
server_table.add("allowed_hosts", ["localhost", "127.0.0.1"])
doc.add("server", server_table)

# Define the output file path
output_file = Path("config_template.toml")

# Write the TOML document to a file
with open(output_file, "w") as f:
    f.write(tomlkit.dumps(doc))

print(f"TOML template created at: {output_file}")