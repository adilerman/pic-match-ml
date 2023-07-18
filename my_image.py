import cv2


class MyImage:
    def __init__(self, path):
        self.sift = cv2.SIFT_create(nfeatures=3000, edgeThreshold=2000)
        self.path = path
        self.img = cv2.imread(path)
        self.img_grey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.keypoints, self.descriptors = self.sift.detectAndCompute(self.img, None)
        self.matches = []

    def show_img(self):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)

    def add_match(self, img):
        self.matches.append(img)
