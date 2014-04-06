.. title: Word clouds and topic modeling in Hindi and Urdu
.. slug: word-clouds-in-hindi-and-urdu
.. date: 2014/03/28 16:18:20
.. tags: draft,word clouds, topic modeling, d3, 
.. link: 
.. description: 
.. type: text

A few weeks ago Matthew Jockers came to MSU to give a lecture and run two workshops on using the programming language R. I assigned his first book, `Macroanalysis: Digital Methods and Literary History <http://www.press.uillinois.edu/books/catalog/88wba3wn9780252037528.html>`, to my undergraduate Digital Humanities Seminar class and wound up coordinating his visit.

Jockers earlier worked at Stanford University and now is an assistant professor in the English department at University of Nebraska-Lincoln.  I have actually been to Lincoln twice, once for a CIC (Center for Institutional Cooperation) digital humanities summit and once to attend the Digital Humanities conference but had not met him before. 

Jockers's book **Macroanalysis** addresses how to analyze lots and lots of books computationally. He originally titled his talk “Macroanalysis: Tracking Valence and Plot in 40,000 Narratives,” but he wound up talking about 50,000 English novels. Valence, I learned, means something like affect in the cognitive science realm.

Jockers ran two workshops, one on text analysis with R and the other on topic modeling in R. Jockers loves R. R is a computer language that is great for doing statistical analysis and visualizations of data analysis. In preparation for his visit, I read the draft version of his forthcoming book, `Text Analysis with R for Students of Literature <http://www.springer.com/statistics/computational+statistics/book/978-3-319-03163-7>`, which he had released online but later took down. I had not done any substantial work in the R language before, so I was grateful to have an excuse to use it. Among my computational biologist friends, there is a bit of a rift between Python and R users. I once saw two bioinformaticians nearly resort to fisticuff at a two-year-old's birthday to determine which is best, though they conceded it is important to know how to use both. I have more experience  with Python, but I definitely see the advantages of R for many tasks, and it has some great data structures. Because the languages I work on require a ton of preprocessing, meaning manipulation of data into an analyzable format, Python's better readability may be an advantage, though I am not ideological on that point.

In any case, I had hoped to blog about my experiments with topic modeling Urdu poetry, but I immediately ran into some problems with the R package used for word clouds, as the Urdu text did not connect properly. I did some looking around and stumbled upon a nice Javascript library for rendering word clouds that actually worked for Urdu's Nastaleeq script as well as Hindi's devanagari. The question then became how to get that to work with the topic modeling packages. 

What is topic modeling? I’m still figuring that out, but the basic idea is that if you imagine a text document–say a poem—as drawing from words associating with different topics—in the case of Urdu poetry say love, desire, mortality, ostricization, and censure—then it is should be possible to reconstruct those topics from a given text by looking at words that frequently occur together. Jockers has a number of what he calls "themes" on his website. 

Here is a sample from Frances Pritchett's translation of Ghalib's poetry below (generated using R). It’s fairly easy to guess the topic. 

Where it gets interesting is that you can then get a measurement when comparing that topic against a text. That's the work Jockers is doing, except based on a number of themes at the same time.

I am still working on topic modeling Ghalib’s poetry. In the meantime, here is a word cloud based on 250 most common words. These were generated using R. They are sized according to frequency. I will post to source

