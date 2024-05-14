# Lexer

`lib.lexer.LexerRe`

Lexer based on trie structure of tokens.
Tokens are defined in `TokenType` Enum, as strings (stored in trie) or regex patterns.
Lexer automatically skips space symbols (defined via `is_separator`),
then by-symbol trie is searched till the longest existing match with terminal node from TokenType.
For anything that is not found in the trie, regex matching is done over strings between separators.
Lexer could be extended to override actions on each token detection.

# Parser

`lib.parser.combinator.*Comb`

For parsing there is a parser-combinator library with number of combinators available.

AST is build immediately when parsing as each combinator returns structured tree `PNode`.

# Transformer

For transforming AST there is class `lib.parser.Transformer`.
It allows to define handlers for `PNode` types just with names of methods, see docs for more.

# BNF parser

For automated parser building, there is small BNF parser. It compiles BNF definitions to parse-combinators code.

Limitations:

- recursion is not detected automatically
- order of definitions is copied in order of BNF file

## Forth parser

As example in `src/forth` lexer and parser for Forth language are implemented.


