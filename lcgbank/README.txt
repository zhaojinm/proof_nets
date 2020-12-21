Tim Fowler (tfowler@cs) translated CCGbank to LCG.

Below is a description of the files in this directory, based on what I (Aditya)
have ascertained from looking through them and reading the relevant parts of
Tim's dissertation. Any changes I've made are documented here as well.

================================================================================
LCGbank.xml
================================================================================
This is the primary LCGbank corpus file that includes my fixes. It can be
regenerated from the original files using my clean_fix.py script.
(Note that fixes are ongoing and I'll be adding them as I go.)

* Included the left-out sentences (see below)
* Reordered the sentences so that they are sorted by numerical (not string
  lexicographic) sentence ID
* Separated the sentences into different <section> elements
* Fix sentence 0290.16 (see clean_fix.py for details)
* Fix sentence 0142.4
  * The word "1/2" was (erroneously, somehow) moved over two spots to be *after*
    "point".
* Comment out a number of sentences that either didn't produce derivable
  sequents (commented out with note "noparse") or have incomplete matchings
  (commented out with note "badmatch").
* See below for full notes about the LCGbank corpus file

================================================================================
included_in_ccgbank.lcgbank.lcg,included_in_ccgbank.lcgbank.auto
================================================================================
The first file is Tim's original primary file for the LCGbank corpus. It
provides the words and categories for 48,934 sentences, along with the LCG
dependencies as defined by linkages in the corresponding LCG proof net. It does
*NOT* include my fixes (see above), nor the translation of the sentences that
were originaly excluded from CCGbank.

The second file (.auto) is the same thing, but in the CCGbank .auto file format,
giving the full phrase-structure tree.

* Categories are written left-associatively, so in comparison to CCGbank (etc.),
  reading the categories requires a bit of adjustment. Unlike the LCG
  literature, though, the categories here are written in Steedman notation, the
  convention followed in the CCG literature.
* The sentences originally omitted from CCGbank are not included here (see
  below).
* Features were stripped from categories.
* Derivations requiring crossing rules were adjusted to use lexicalized
  versions.
* I got the sentence count via:
  $ grep sentential included_in_ccgbank.lcgbank.lcg

================================================================================
left_out_from_ccgbank.lcgbank.lcg,left_out_from_ccgbank.lcgbank.auto
================================================================================
The files are as the included_in_ccgbank files above, but are the 274 sentences
that were in the original PTB but omitted from CCGbank. They were parsed with
the Petrov parser first, verified, and converted to LCG. 223 of them required
Tim to make some manual fixes.

* Features were stripped from categories.
* The original output on these sentences of the Petrov parser is in the
  left_out_from_ccgbank.petrov.auto file.

================================================================================
included_in_ccgbank.crossing.auto
================================================================================
This file provides the original CCG sentences translated according to Tim's LCG
procedure, but keep the features on the categories and do *NOT* translate the
crossing rules. This keeps things as compatible as possible with CCG and CCGbank
while still lexicalizing.

* The categories are written fully-parenthesized, as with CCGbank.
