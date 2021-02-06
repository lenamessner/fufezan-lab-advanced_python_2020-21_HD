import exercice4.protein as ep
import pandas as pd


def test_get_data():
    testprotein = ep.Protein("P32249", lookup={})
    sequence = testprotein.get_data()
    assert sequence == "MDIQMANNFTPPSATPQGNDCDLYAHHSTARIVMPLHYSLVFIIGLVGNLLALVVIVQNRKKINSTTLYSTNLVISDILFTTALPTRIAYYAMGFDWRIGDALCRITALVFYINTYAGVNFMTCLSIDRFIAVVHPLRYNKIKRIEHAKGVCIFVWILVFAQTLPLLINPMSKQEAERITCMEYPNFEETKSLPWILLGACFIGYVLPLIIILICYSQICCKLFRTAKQNPLTEKSGVNKKALNTIILIIVVFVLCFTPYHVAIIQHMIKKLRFSNFLECSQRHSFQISLHFTVCLMNFNCCMDPFIYFFACKGYKRKVMRMLKRQVSVSISSAVKSAPEENSREMTETQMMIHSKSSNGK"


def test_get_lookup_dict():
    test_df = pd.DataFrame({
        "1-letter code": ["A", "C", "D", "E", "G"],
        "country": ["Brazil", "Russia", "India", "China", "South Africa"],
        "capital": ["Brasilia", "Moscow", "New Delhi", "Beijing", "Pretoria"],
        "area": [8.516, 17.10, 3.286, 9.597, 1.221],
        "population": [200.4, 143.5, 1252, 1357, 52.98]})
    lookup_dict = ep.get_lookup_dict(test_df)
    assert lookup_dict == {"1-letter code": {"A": "A", "C": "C", "D": "D", "E": "E", "G": "G"},
                           "country": {"A": "Brazil", "C": "Russia", "D": "India", "E": "China", "G": "South Africa"},
                           "capital": {"A": "Brasilia", "C": "Moscow", "D": "New Delhi", "E": "Beijing",
                                       "G": "Pretoria"},
                           "area": {"A": 8.516, "C": 17.10, "D": 3.286, "E": 9.597, "G": 1.221},
                           "population": {"A": 200.4, "C": 143.5, "D": 1252.0, "E": 1357.0, "G": 52.98}}


def test_map():
    lookup_dict = {"1-letter code": {"A": "A", "C": "C", "D": "D", "E": "E", "G": "G"},
                   "country": {"A": "Brazil", "C": "Russia", "D": "India", "E": "China", "G": "South Africa"},
                   "capital": {"A": "Brasilia", "C": "Moscow", "D": "New Delhi", "E": "Beijing",
                               "G": "Pretoria"},
                   "area": {"A": 8.516, "C": 17.10, "D": 3.286, "E": 9.597, "G": 1.221},
                   "population": {"A": 200.4, "C": 143.5, "D": 1252.0, "E": 1357.0, "G": 52.98}}

    testprotein = ep.Protein("P32249", lookup=lookup_dict)
    testprotein.sequence = "ACEGCEE"
    population = testprotein.map("population", 1)
    assert population == [200.4, 143.5, 1357.0, 52.98, 143.5, 1357.0, 1357.0]


def test_map_2():
    lookup_dict = {"1-letter code": {"A": "A", "C": "C", "D": "D", "E": "E", "G": "G"},
                   "country": {"A": "Brazil", "C": "Russia", "D": "India", "E": "China", "G": "South Africa"},
                   "capital": {"A": "Brasilia", "C": "Moscow", "D": "New Delhi", "E": "Beijing",
                               "G": "Pretoria"},
                   "area": {"A": 8.516, "C": 17.10, "D": 3.286, "E": 9.597, "G": 1.221},
                   "population": {"A": 200.4, "C": 143.5, "D": 1252.0, "E": 1357.0, "G": 52.98}}

    testprotein = ep.Protein("P32249", lookup=lookup_dict)
    testprotein.sequence = "ACEGCEE"
    population = testprotein.map("population", 2)
    assert population == [(200.4+143.5)/2, (143.5+1357.0)/2, (1357.0+52.98)/2, (52.98+143.5)/2, (143.5+1357.0)/2, (1357.0+1357.0)/2]
