# ADR #1: Preprocessor

-   We need to take data from a set, and put it in a format that works well with our analysis tools.
    
-   Get a dictionary of (name : tier) for each pokemon where tier is the highest allowed competetive bracket for that pokemon.
    
-   do one-hot encoding, models will be able to work (no ordinal bias, easy splits)

-   multi-hot encoding for categories like type
