import cv2
import easyocr
import llm


def read_image(cv_path):
    """Read the image, preprocess it converting into gray scale and return text."""

    cv_image = cv2.imread(cv_path)

    gray_scaled_cv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("saved CV/gray_scaled_cv.png", gray_scaled_cv)

    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext("saved CV/gray_scaled_cv.png", detail=0)
    recognized_text = " ".join(element for element in result)
    print(result)
    print(recognized_text)

    return llm.classify(recognized_text)
