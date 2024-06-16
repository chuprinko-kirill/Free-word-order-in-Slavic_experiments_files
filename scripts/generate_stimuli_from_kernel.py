def permutate(kernel: 'str') -> 'pandas.DataFrame':
  """
  Take a string and return a DataFrame with a single column containing all possible permutations
  """
  from itertools import permutations
  from pandas import DataFrame
  if type(kernel) is str:
    kernel = kernel.split(" ")

  kernel = [x for x in kernel if x !="" and x != "."]
  kernel = [x.removesuffix(".") for x in kernel]
  kernel = [x.lower() for x in kernel]


  p = permutations(kernel)
  dic = {"sentence":[]}
  for variant in p:
    dic["sentence"].append(" ".join(variant))
  return DataFrame(dic)

def annotate_order_5words(sentences: 'pandas.DataFrame', n_words=5) -> 'pandas.DataFrame':
  """
  Give annotation of movement types with respect to the indexes of words in a sentence
  Add annotations as columns to the DataFrame with a list of possible permutations
  """

  from pandas import DataFrame
  if not isinstance(sentences, DataFrame):
    raise Exception("it works only with the pandas.DataFrame object")
  kernel = sentences.iloc[0,0]
  if len(kernel.split(" ")) != n_words:
    raise Exception("This works only with " + str(n_words) + " words in kernel")

  words_kernel = kernel.split(" ")
  # dictionary of kernel positions
  kernel_words_gram_func_dict = {"subj":words_kernel[0],"clitic":words_kernel[1],"verb":words_kernel[2],"adj":words_kernel[3],"obj":words_kernel[4]}

  NotClitic2 = [] # clitic_index != 1
  LBE = [] # adj_index < verb_index
  NotSV = [] # subj_index > verb_index
  NounScram = [] # obj_index != len(sentence)-1


  for sentence in sentences.iloc[:,0]:
    gram_func_index_map = {}
    for word in sentence.split(" "):
      word_func = list(kernel_words_gram_func_dict.keys())[list(kernel_words_gram_func_dict.values()).index(word)] # identify word's gram function
      gram_func_index_map[word_func] = sentence.split(" ").index(word)

    if gram_func_index_map["clitic"] != 1:
      NotClitic2.append(1)
    else:
      NotClitic2.append(0)

    if gram_func_index_map["adj"] < gram_func_index_map["verb"]:
      LBE.append(1)
    else:
      LBE.append(0)

    if gram_func_index_map["subj"] > gram_func_index_map["verb"]:
      NotSV.append(1)
    else:
      NotSV.append(0)

    if gram_func_index_map["obj"] != n_words-1:
      NounScram.append(1)
    else:
      NounScram.append(0)


  sentences["NotClitic2"] = NotClitic2
  sentences["LBE"] = LBE
  sentences["NotSV"] = NotSV
  sentences["NounScram"] = NounScram

  # add dots at the end of each sentence and make the first letter capital
  sentences.sentence = sentences.sentence.str.capitalize()
  sentences.sentence = sentences.sentence.astype("str") + "."


  return sentences


def permutate_and_annotate(kernel: 'str') -> 'pandas.DataFrame':
  """Unites permutation and annotation functions under the hood of one function
  Returns DataFrame"""
  sentences = permutate(kernel)
  return annotate_order_5words(sentences)