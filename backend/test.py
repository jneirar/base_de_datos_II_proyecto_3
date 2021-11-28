from Comparator import Comparator

comparator = Comparator(13174)
print()
res = comparator.KNNSearchInd("steve_jobs.jpeg", 10)
print()
res = comparator.KNNSearch("steve_jobs.jpeg", 10)
print()
res = comparator.rangeSearchInd("steve_jobs.jpeg", 0.58)
print()
res = comparator.rangeSearch("steve_jobs.jpeg", 0.58)
