# ADR #1: Preprocessor

-   We need to take data from a set, and put it in a format that works well with our analysis tools.
    
-   Get a dictionary of (name : tier) for each pokemon where tier is the highest allowed competetive bracket for that pokemon.
    
-   Create one-hot encodings for all categorical variables (any str variables w/ finite # of options, such as abilities or color)

-   