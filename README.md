# XD_Parser

The parser is functional and stable, however it still needs an interface in order to be easily used. The refined interface will likely be built around Jan 2017.

# Demo
To get a quick feel for the project, clone the repo, and run the parser file. It parses some demo code and prints the code as a syntax tree. 

# How it works
The parser works by importing Scout objects. Those Scout objects are the definition of different things: phone numbers, emails, if statements, assignments, functions, infix operators, etc. Scouts can find other scouts recursively. For example the phone-number Scout could call the number Scout. They can also search by scout attributes. For example the assignment scout can search for all scouts with a value attribute. The XD_Parser is very flexible so it allows the scouts to record whatever kind of information they want on the syntax tree. 

For now there are only a few demo Scout objects, and some demo input. However, in the distant future their will be a standard library of scouts that can be used to quickly parse programming languages.
