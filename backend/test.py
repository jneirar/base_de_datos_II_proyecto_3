from Comparator import Comparator

#Total = 13174
comparator = Comparator(12800)
res = comparator.KNNSearchInd("steve_jobs.jpeg", 8)
print()
res = comparator.KNNSearch("steve_jobs.jpeg", 8)
print()

res = comparator.rangeSearchInd("steve_jobs.jpeg", 0.65)
print()
res = comparator.rangeSearch("steve_jobs.jpeg", 0.65)
print()
