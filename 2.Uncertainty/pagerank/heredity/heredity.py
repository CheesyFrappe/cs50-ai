import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
    
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            # print(f"ONE {one_gene}")
            for two_genes in powerset(names - one_gene):
                # print(f"TWO {two_genes}")

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # joint probability of the family
    joint_prob = 1

    for person in people:

        # personal probability
        person_prob = 1

        # check number of genes that person have 
        if person in one_gene:
            gene_num = 1
        elif person in two_genes:
            gene_num = 2
        else:
            gene_num = 0
        
        # check that wheter the person have the trait or not
        if person in have_trait:
            trait_align = True
        else:
            trait_align = False
        
        # check that if the person is a parent
        if people[person]["mother"] == None and people[person]["father"] == None:
            person_prob *= PROBS["gene"][gene_num]
            # print(f"{person} => {gene_probability * trait_probability}")
        
        # person is a child
        else:
            """
            There are two ways that child can get the gene. 
            Either he gets the gene from his mother and not his father, 
            or he gets the gene from his father and not his mother. 

            mother_yes stands for the probability of that the child gets the gene from mother. And vice-versa for mother_no
            Same thing goes for father.
            """
            mother = people[person]["mother"]
            father = people[person]["father"]
            
            # mother, father probabilities
            mother_prob = get_parent_prob(mother, one_gene, two_genes)
            father_prob = get_parent_prob(father, one_gene, two_genes)

            # if there are two genes that comes from parents
            # there is only one scenario that child gets the gene
            if gene_num == 2:
                person_prob *= mother_prob * father_prob
            # if there is one gene comes from parents
            # there are two scenarios, either child gets the gene from his mother or from his father
            elif gene_num == 1:
                person_prob *= (1 - mother_prob) * father_prob + mother_prob * (1 - father_prob)
            # if there is no gene
            # probability of that is => (not from mother) * (not from father)
            else:
                person_prob *= (1 - mother_prob) * (1 - father_prob)
        
        person_prob *= PROBS["trait"][gene_num][trait_align]
        joint_prob *= person_prob
    
    return joint_prob   


def get_parent_prob(parent, one_gene, two_genes):
    """
    Returns parent probabilities for children
    """
    # checks how many genes parent have
    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1 - PROBS["mutation"]
    else:
        return PROBS["mutation"]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # updating each person's value in probabilities
    for person in probabilities:
        
        # updating person's gene value
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        
        # updating person's trait value
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        person_gene, person_trait, j, k = 0, 0, 0, 0

        for prob in probabilities[person]["gene"]:
            person_gene += probabilities[person]["gene"][prob]
        for prob in probabilities[person]["trait"]:
            person_trait += probabilities[person]["trait"][prob]
        
        j = 1 / person_gene
        k = 1 / person_trait

        for prob in probabilities[person]["gene"]:
            probabilities[person]["gene"][prob] *= j 
        
        for prob in probabilities[person]["trait"]:
            probabilities[person]["trait"][prob] *= k
            
            
if __name__ == "__main__":
    main()