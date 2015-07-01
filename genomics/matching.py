def matchScore(seqA, seqB):

  score = 0

  for i in range(len(seqA)):

    if seqA[i] == seqB[i]:
      score += 1
    elif seqA[i] == '-' or seqB[i] == '-':
      score += 0
    elif seqA[i] != seqB[i]:
      score -= 1

  return score