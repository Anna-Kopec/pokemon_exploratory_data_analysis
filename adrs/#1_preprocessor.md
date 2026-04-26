# ADR #1: Preprocessor

-   We need to take data from a set, and put it in a format that works well with our analysis tools.
    
-   Get a dictionary of (name : tier) for each pokemon where tier is the highest allowed competetive bracket for that pokemon.
    
-   Use label encoding for categorical variables (as opposed to one-hot) as trees can work w/ label encoded data which allows for an entirely integer dataset while avoiding the sparsity of one-hot encoding

- needed to account for encoding in multiple different scenarios: some properties had multiple different possibilities (e.g. 3 possible abilities), so we had to split all possibilities up into 3 columns
