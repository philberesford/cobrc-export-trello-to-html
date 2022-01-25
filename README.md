# Transforms a Trello board into HTML snippets

Takes a standard data export in JSON format from Trello, parses the output to produce HTML tables that can be used
for generating agendas and meeting notes.

Redirection of standard output should be used to direct the HTML to a specific file.

[How to specify redirection of standard output](https://stackoverflow.com/questions/6674327/redirect-all-output-to-file-in-bash)

## Example script usage
To take a data export located in `./export.json` and to transform the contents into a file located at `./output.html`, 
execute the command below from the root of this repository:

```bash
python trello_to_html_table\src\trello_to_html_table.py --sourcePath export.json > output.html
```
### Input parameters
`--sourcePath` is used to specify the source path for the export from Trello

