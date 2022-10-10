import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    """
    Wasted 3 hours here just because I used a variable called 'page' in a for loop.
    Guess what? The iterator in that for loop was called 'page' too which caused a logic error.
    Took me 3 hours to find that error. :(
    """

    number_of_pages = len(corpus[page]) 
    N = len(corpus) 

    transition_dict = {}
    
    # if there are no links in page
    if (number_of_pages == 0):
        for page in corpus:
            transition_dict[page] = 1 / N 
    else:
        for item in corpus:
            transition_dict[item] = (1 - damping_factor) / N
            
        for item in corpus[page]:
            transition_dict[item] += damping_factor / number_of_pages
    
    return transition_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample_dict = {} 

    # initialize variables in dict
    for sample in corpus:
        sample_dict[sample] = 0.0
    
    # get random page and update its value
    page = random.choice(list(corpus))
    sample_dict[page] += 1 / n

    # iterate 'n' times
    for _ in range(1, n):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model), weights=model.values(), k=1)[0]
        sample_dict[page] += 1 / n

    return sample_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterate_dict = {} # dict with estimated PageRank values
    pagerank_dict = {} # dict with temporary PageRank values

    N = len(corpus)

    # initializing page values
    for page in corpus:
        iterate_dict[page] = 1 / N
    
    # Iterate until the value changes by more than 0.001
    iterate = True

    while iterate:
        
        # iterating pages in iterate_dict to calculate PR(p)
        for page in iterate_dict:

            # defaul new PageRank value
            total = 0

            # iterating pages in corpus to calculate PR(i)
            for corpus_page in corpus:

                if page in corpus[corpus_page]:                    
                    # PR(i) / NumLinks(i)
                    total += iterate_dict[corpus_page] / len(corpus[corpus_page])

                # If page(i) has no links, assume that it has links to every page in corpus
                if not corpus[corpus_page]:
                    total += iterate_dict[corpus_page] / len(corpus)
        
            # PR(p) = ((1 - d) / N) + (d * total)
            pagerank_dict[page] = ((1 - damping_factor) / N) + total * damping_factor
    
        # break the loop before checking the PageRank difference
        iterate = False

        # checking the difference for each page in iterate_dict
        for page in iterate_dict:
            # continue iterating loop iff PageRank value of the page did not change by more than 0.001
            if iterate_dict[page] - pagerank_dict[page] > 0.001 or pagerank_dict[page] - iterate_dict[page] > 0.001: 
                iterate = True
        
            # assign PageRank value to the page
            iterate_dict[page] = pagerank_dict[page]
    
    return iterate_dict
            

if __name__ == "__main__":
    main()