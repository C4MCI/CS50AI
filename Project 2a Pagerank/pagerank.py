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
    
    all_pages = list(corpus.keys())
    probabilities = {page_name : 0 for page_name in corpus}
    
    if len(corpus[page]) < 1:
        for key in corpus.keys():
            probabilities[key] = 1.0 / len(all_pages)
        return probabilities
    
    # Probability of picking any page at random:
    random_prob = (1 - damping_factor) / len(corpus)

    # Probability of picking a link from the page:
    link_prob = damping_factor / len(corpus[page])

    # Add probabilities to the distribution:
    for page_name in all_pages:
        probabilities[page_name] += random_prob

        if page_name in corpus[page]:
            probabilities[page_name] += link_prob
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    all_pages = list(corpus.keys())
    visit_counts = dict()
    for page in corpus.keys():
        visit_counts[page] = 0
        
    sample = None
        
    for iter in range(n):
        if sample:
            probs = transition_model(corpus, sample, damping_factor)
            sample = random.choices(list(probs.keys()), weights=probs.values(), k=1)[0]
        else:
            sample = random.choice(all_pages)
        visit_counts[sample] += 1
    
    for page in visit_counts.keys():
        visit_counts[page] /= n
        

        
    return visit_counts


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pagerank = dict()
    num_pages = len(corpus.keys())
    for page in corpus.keys():
        pagerank[page] = 1 / num_pages
        
    difference = 1
    while difference > 0.001:
        old_pagerank = dict()
        for page in pagerank.keys():
            old_pagerank[page] = pagerank[page]
            
        for page_p in corpus.keys():
            prob = 0
            for page_i in corpus.keys():
                if len(corpus[page_i]) == 0:
                    prob += pagerank[page_i] / len(corpus)
                elif page_p in corpus[page_i]:
                    prob += (pagerank[page_i] / len(corpus[page_i]))
            
            pagerank[page_p] = (((1 - damping_factor) / num_pages) + (damping_factor * prob))
            
    
        # Normalise the new page ranks:
        norm_factor = sum(pagerank.values())
        pagerank = {page: (rank / norm_factor) for page, rank in pagerank.items()}
        
        # Find max change in page rank:
        for page_name in corpus:
            difference = abs(old_pagerank[page_name] - pagerank[page_name])

    return pagerank


if __name__ == "__main__":
    main()
