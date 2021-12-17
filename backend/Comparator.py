from typing import Collection
import face_recognition
import numpy
import matplotlib.pyplot as plt
import random
import json
import linecache
import io
from rtree import index
import os
from os.path import join, dirname, realpath
from queue import PriorityQueue
from timeit import default_timer as timer

path_data = "data.json"

UPLOAD_PATH = os.getcwd() + '/instance/Uploads/'


class Comparator():
    n = 0
    dict128VectorPhotos = {}
    vectors = []

    def __init__(self, N):
        line = linecache.getline(path_data, 1).rstrip()
        item_json = json.load(io.StringIO(line))

        self.dict128VectorPhotos = dict(item_json)
        cont = 0
        for key in self.dict128VectorPhotos:
            np = numpy.array(list(map(float, key.strip("()").split(', '))))
            self.vectors.append(np)
            cont = cont + 1
            if cont == N:
                break

        self.n = len(self.vectors)

        # Configuration for RTree
        if os.path.isfile("128d_index.data"):
            os.remove("128d_index.data")
        if os.path.isfile("128d_index.index"):
            os.remove("128d_index.index")
        p = index.Property()
        p.dimension = 128  # D
        p.buffering_capacity = 4  # M
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.idx = index.Index('128d_index', properties=p)

        # insertar puntos
        for i in range(self.n):
            self.idx.insert(i, tuple(self.vectors[i]))

    def rangeSearchInd(self, file, r):
        if not os.path.isfile(UPLOAD_PATH + file):
            print("Archivo no encontrado")
            return []
        os.chdir(UPLOAD_PATH)
        img = face_recognition.load_image_file(file)
        imgEncoding = face_recognition.face_encodings(img)
        if len(imgEncoding) == 0:
            print("No se pudo procesar la imagen")
            return []
        vector0 = tuple(imgEncoding[0])
        qmin = []
        qmax = []
        for d in vector0:
            qmin.append(d - r)
            qmax.append(d + r)
        q = qmin + qmax
        print("Imagen:", file)
        print("Radius:", r)
        print("\nResult RangeSearchInd")
        start = timer()
        rangeValues = [n for n in self.idx.intersection(q)]
        end = timer()
        result = []
        for rangeValue in rangeValues:
            dist = numpy.linalg.norm(numpy.asarray(
                vector0)-numpy.asarray(self.vectors[rangeValue]))
            if dist < r:
                route = self.dict128VectorPhotos[str(
                    tuple(self.vectors[rangeValue]))]
                name = route.split('/')[1]
                result.append((route, name, dist))
        result = sorted(result, key=lambda item: item[2])
        for par in result:
            print(par[0], "\tname:", par[1], "\tdist:", par[2])
        print("Time in ms:", (end-start)*1000)
        return result

    def rangeSearch(self, file, r):
        if not os.path.isfile(UPLOAD_PATH + file):
            print("Archivo no encontrado")
            return []
        os.chdir(UPLOAD_PATH)
        img = face_recognition.load_image_file(file)
        imgEncoding = face_recognition.face_encodings(img)
        if len(imgEncoding) == 0:
            print("No se pudo procesar la imagen")
            return []
        vector0 = tuple(imgEncoding[0])
        print("Imagen:", file)
        print("Radius:", r)
        print("\nResult RangeSearch")
        start = timer()
        partialResult = []
        for i in range(self.n):
            dist = numpy.linalg.norm(numpy.asarray(
                self.vectors[i])-numpy.asarray(vector0))
            if dist < r:
                partialResult.append((i, dist))
        partialResult = sorted(partialResult, key=lambda item: item[1])
        end = timer()
        result = []
        for rangeValue in partialResult:
            if numpy.linalg.norm(numpy.asarray(vector0)-numpy.asarray(self.vectors[rangeValue[0]])) < r:
                route = self.dict128VectorPhotos[str(
                    tuple(self.vectors[rangeValue[0]]))]
                name = route.split('/')[1]
                dist = rangeValue[1]
                print(route, "\tname:", name, "\tdist:", dist)
                result.append((route, name, dist))
        print("Time in ms:", (end-start)*1000)
        return result

    def KNNSearchInd(self, file, K):
        if not os.path.isfile(UPLOAD_PATH + file):
            print("Archivo no encontrado")
            return []
        os.chdir(UPLOAD_PATH)
        img = face_recognition.load_image_file(file)
        imgEncoding = face_recognition.face_encodings(img)
        if len(imgEncoding) == 0:
            print("No se pudo procesar la imagen")
            return []
        vector0 = tuple(imgEncoding[0])

        print("Imagen:", file)
        print("K:", K)
        print("\nResult KNNind")
        start = timer()
        KNNvalues = list(self.idx.nearest(coordinates=vector0, num_results=K))
        end = timer()
        result = []
        for KNNvalue in KNNvalues:
            route = self.dict128VectorPhotos[str(
                tuple(self.vectors[KNNvalue]))]
            name = route.split('/')[1]
            dist = numpy.linalg.norm(numpy.asarray(
                self.vectors[KNNvalue])-numpy.asarray(vector0))
            print(route, "\tname:", name, "\tdist:", dist)
            result.append((route, name, dist))
        print("Time in ms:", (end-start)*1000)
        return result

    def KNNSearch(self, file, K):
        if not os.path.isfile(UPLOAD_PATH + file):
            print("Archivo no encontrado")
            return []
        os.chdir(UPLOAD_PATH)
        img = face_recognition.load_image_file(file)
        imgEncoding = face_recognition.face_encodings(img)
        print("K: ", K)
        print("Nombre archivo: ", file)
        if len(imgEncoding) == 0:
            print("No se pudo procesar la imagen")
            return 0
        vector0 = tuple(imgEncoding[0])
        print("Imagen:", file)
        print("K:", K)
        print("\nResult KNN")
        start = timer()

        partialResult = []
        pq = PriorityQueue(False)
        for i in range(self.n):
            dist = numpy.linalg.norm(numpy.asarray(
                self.vectors[i])-numpy.asarray(vector0))
            if pq.qsize() == K:
                cur = pq.get()
                if dist < -cur[0]:
                    pq.put((-dist, i))
                else:
                    pq.put(cur)
            else:
                pq.put((-dist, i))
        while not pq.empty():
            cur = pq.get()
            partialResult.append((cur[1], -cur[0]))
        partialResult = sorted(partialResult, key=lambda item: item[1])
        end = timer()

        result = []
        for KNNvalue in partialResult:
            route = self.dict128VectorPhotos[str(
                tuple(self.vectors[KNNvalue[0]]))]
            name = route.split('/')[1]
            dist = KNNvalue[1]
            print(route, "\tname:", name, "\tdist:", dist)
            result.append((route, name, dist))
        print("Time in ms:", (end-start)*1000)
        return result
