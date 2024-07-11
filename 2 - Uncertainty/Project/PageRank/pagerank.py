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
    # initialize probability distribution 
    probability = {page_name : 0 for page_name in corpus} 

    # if page has no links, return equal probability for next page 
    if len(corpus[page]) == 0: 
        for page_name in probability: 
            probability[page_name] = 1/len(corpus) 
        return probability
    
    # probability of random page 
    random_prob = (1 - damping_factor) / len(corpus) 

    # probability of picking link 
    link_prob = damping_factor / len(corpus[page]) 

    # add probabilities 
    for page_name in probability: 
        probability[page_name] = probability[page_name] + random_prob

        if page_name in corpus[page]: 
            probability[page_name] = probability[page_name] + link_prob 

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # tally of visits 
    visits = {page_name: 0 for page_name in corpus}

    # choose first page at random 
    current_page = random.choice(list(visits))
    visits[current_page] = visits[current_page] + 1 

    # for remaining samples, pick next page depending on transition model 
    for i in range(0, n-1): 
        # initialize 
        trans_model = transition_model(corpus, current_page, damping_factor) 

        # select 
        rand_num = random.random() 
        ans = 0 

        for page_name, prob in trans_model.items(): 
            ans = ans + prob 
            if rand_num <= ans: 
                current_page = page_name 
                break 
        
        visits[current_page] = visits[current_page] + 1 

    # normalize using sample number 
    page_ranks = {page_name: (visit_count/n) for page_name, visit_count in visits.items()} 

    print("Sum", round(sum(page_ranks.values()), 4))
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # calculate constants form corpus 
    page_num = len(corpus) 
    initial_rank = 1 / page_num 
    random_choice = (1 - damping_factor) / len(corpus) 
    iterations = 0 

    # initial page rank split 
    page_ranks = {page_name: initial_rank for page_name in corpus} 
    updated_ranks = {page_name: None for page_name in corpus} 
    max_rank_change = initial_rank 

    # calculate page rank until no change greater than 0.001 
    while max_rank_change > 0.001: 
        iterations = iterations + 1 
        max_rank_change = 0 

        for page_name in corpus: 
            surfer_choice = 0 
            for other_page in corpus: 
                # if other page has no links, pick random 
                if len(corpus[other_page]) == 0: 
                    surfer_choice = surfer_choice + page_ranks[other_page] * initial_rank
                # if other_page has link to page_name, randomly pcisk from all links there 
                elif page_name in corpus[other_page]: 
                    surfer_choice = surfer_choice + page_ranks[other_page] / len(corpus[other_page]) 
            # calculate new page rank 
            updated_rank = random_choice + (damping_factor * surfer_choice) 
            updated_ranks[page_name] = updated_rank

        # normalize new page ranks 
        norm_factor = sum(updated_ranks.values()) 
        updated_ranks = {page: (rank/norm_factor) for page, rank in updated_ranks.items()} 

        # find max change 
        for page_name in corpus: 
            rank_change = abs(page_ranks[page_name] - updated_ranks[page_name]) 
            if rank_change > max_rank_change: 
                max_rank_change = rank_change

        # update page ranks 
        page_ranks = updated_ranks.copy() 

    print("Took ", iterations, "iterations")
    print("Sum", round(sum(page_ranks.values()))) 

    return page_ranks


if __name__ == "__main__":
    main()
