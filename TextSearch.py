from Levenshtein import distance as levenshtein_distance

class TS:
    def __init__(self):
        pass

    def search(self, text, text_list, id_list=None):
        m = len(text)
        id = None
        if id_list is None:
            for i in text_list:
                l = levenshtein_distance(text, i)
                if l <= m:
                    m = l
                    result = i
            doubtfulness = m / len(text)
            return result, None, doubtfulness
        
        ind = 0
        for i in text_list:
            l = levenshtein_distance(text, i)
            if l <= m:
                m = l
                result = i
                id = id_list[ind]
            ind += 1
        doubtfulness = m / len(text)
        return result, id, doubtfulness


if __name__ == '__main__':
    text1 = "kitten"
    text_list = ["kittens", "sitting", "sittin", "kiten"]
    ts = TS()
    result, _, doubtfulness = ts.search(text1, text_list)
    print(result, doubtfulness)