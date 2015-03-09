<!--
.. title: Printing Right-To-Left PDF Books
.. slug: printing-right-to-left-pdf-books
.. date: 2015-03-09 14:43:50 UTC-04:00
.. tags: pdf,pdfpun,PDFjam,rtl,binders,majeed_amjad,CRL
.. category:
.. link:
.. description:
.. type: text
-->

Today is the first day of Spring Break, and so I am enjoying some nice weather and not teaching.

I am working on a panel abstract about the poet Majeed Amjad for the [Annual Conference on South Asia] held in beautiful Madison, Wisconsin.
I have applied to bring a certain professor from Pakistan to the event, and two amazing Urdu professors
from University of Virginia have also signed on to the panel. I do hope it goes forward.

I found an interesting  [book](http://catalog.crl.edu/record=b2874293~S1) on Majeed Amjad through my library. It is actually available as PDF through the
[Center for Research Libraries] (CRL), of which [my university library] is a member.

It's wonderful to be able to download a PDF of the book. However, I love writing on books.
Actually, I don't like writing on my own books but rather on photocopies of them, especially when doing research. I like to print pages double-sided and then keep the pages in a recycled report cover that I can put it in my file cabinet when I am done. That doesn't take much space, and I can see four pages at a time when reading/skimming.

When printing a PDF, you can print two pages a sheet. For left-to-right documents, that is not a problem.

<a href="http://en.wikipedia.org/wiki/Recto_and_verso"><img alt="Recto and verso.svg" src="http://upload.wikimedia.org/wikipedia/commons/7/7b/Recto_and_verso.svg" height="145" width="218"></a>

However, for [right-to-left](http://en.wikipedia.org/wiki/Right-to-left) books there is a problem as the verso and recto are reversed, meaning one reads the right page then the left page. It's rather disorienting to read them if they are not printed correctly. So I went about looking for a good solution.

<a href="http://en.wikipedia.org/wiki/Recto_and_verso"><img alt="Recto and verso RTL.svg" src="http://upload.wikimedia.org/wikipedia/commons/f/fa/Recto_and_verso_RTL.svg" height="145" width="218"></a>


First, I explored a PDF-manipulation library for the Python language called [PyPDF2]. It is quite neat, but I had some
trouble accomplishing the task of merging the pages.

I then stumbled upon a set of PDF shell scripts called [PDFjam]. I already had them installed on my computer,
perhaps as part of the document preparation system [LaTeX](www.latex-project.org/). (I use [MacTex](https://tug.org/mactex/) which is a distribution of [Tex Live](https://www.tug.org/texlive/) for OS X.)

There is a program in PDFjam called ``pdfnup`` which allows to "n-up the pages of pdf files."
To [n-up](http://en.wikipedia.org/wiki/N-up) apparently means to combine multiple pages into one, so it was very close to what I was looking for. I was delighted to see the package also includes a program called ``pdfpun``—a right-to-left version and exactly what I needed!

For all the other RTL PDF book printers out there, here is the command I used on the original file `dds-85303.pdf` to save it as `gulaab_ke_phuul.pdf`:

```
pdfpun dds-85303.pdf --outfile gulaab_ke_phuul.pdf
```

That was close. However, there was a problem in that the pages were two small. I tried messing around with the
parameters. The CRL puts a cover page on its documents that is a different size then the rest of the pages. So I tried removing that by instead printing the book's cover page twice.  ``pdfpun`` allows an optional page-range parameter. I opened up the original PDF and saw that it was 257 pages, so just plugged in the following to print the first page twice and then the rest of the pages:

```
pdfpun dds-85303.pdf 2,2,3-257 --outfile gulaab_ke_phuul.pdf
```

The pattern is here:

```
pdfpun ORIGFILE PAGERANGE --outfile OUTPUTFILE
```

It worked perfectly. Now I'm off to read the book!

<a href="https://www.flickr.com/photos/129471681@N03/16581802309" title="Gulaab ke phuul by Sean Pue, on Flickr"><img src="https://farm8.staticflickr.com/7610/16581802309_a177566398_n.jpg" width="240" height="320" alt="Gulaab ke phuul"></a><a href="https://www.flickr.com/photos/129471681@N03/16742082536" title="Gulaab ke phuul by Sean Pue, on Flickr"><img src="https://farm9.staticflickr.com/8706/16742082536_b0c7c7ecde_n.jpg" width="240" height="320" alt="Gulaab ke phuul"></a>


[Annual Conference on South Asia]: http://southasiaconference.wisc.edu/
[PyPDF2]: https://github.com/mstamy2/PyPDF2
[Center for Research Libraries]: http://www.crl.edu/
[my university library]: http://lib.msu.edu
[PDFjam]: http://www2.warwick.ac.uk/fac/sci/statistics/staff/academic-research/firth/software/pdfjam/
