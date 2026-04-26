# ADR #3: Smogon

-   Not all pokemon have a smogon build for gen9nationaldex because not all are competitively relevant enough to have been meticulously given a perfect build.
-   However, we are able to parse through more formats going backwards. Checking just normal gn9 data afterwards means that if a pokemon like bulbasaur isn't smogonned in gen9natdex, but was relevant enough to get a smogon in gen9, while it may be missing the opportunity for a natdex move that might've changed it slightly, it's still a perfectly viable iteration of bulbasaur, and for our purposes more than acceptable.
-   If it didn't have one there, we keep going back through gen8, gen7, etc. until eventually we either have some version of the mon that's viable, or we truly don't have one, at which point we can just ignore it.
-   Because gen9natdex is a superset of all these other formats, it should go without saying that any prior gen smogon build will consist of gen9natdex legal moves (barring possibly very few exceptions, and for those the other preprocessor will just eliminate them from the dataset later).

- add megas and gmax to learnsets